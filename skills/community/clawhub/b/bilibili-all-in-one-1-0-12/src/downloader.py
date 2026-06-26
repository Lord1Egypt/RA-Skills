"""Bilibili video downloading module."""

import os
import asyncio
from typing import Optional, Dict, Any, List

import httpx

from .auth import BilibiliAuth
from .utils import (
    API_VIDEO_INFO,
    API_PLAY_URL,
    QUALITY_MAP,
    DEFAULT_HEADERS,
    extract_bvid,
    format_duration,
    format_number,
    ensure_dir,
    sanitize_filename,
)


class BilibiliDownloader:
    """Download videos from Bilibili.

    Supports multiple quality options, format selection, and batch downloading.
    """

    def __init__(self, auth: Optional[BilibiliAuth] = None, output_dir: str = "./downloads"):
        """Initialize BilibiliDownloader.

        Args:
            auth: Optional BilibiliAuth instance for authenticated requests.
            output_dir: Default output directory for downloaded files.
        """
        self.auth = auth
        self.output_dir = output_dir

    def _get_client(self) -> httpx.AsyncClient:
        """Get an HTTP client, using auth if available."""
        if self.auth:
            return self.auth.get_client()
        return httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=60.0,
            follow_redirects=True,
        )

    async def get_info(self, url: str) -> Dict[str, Any]:
        """Get video information.

        Args:
            url: Bilibili video URL or BV number.

        Returns:
            Video information dict.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        video = data["data"]
        stat = video.get("stat", {})
        owner = video.get("owner", {})

        pages = []
        for p in video.get("pages", []):
            pages.append({
                "page": p.get("page"),
                "cid": p.get("cid"),
                "title": p.get("part"),
                "duration": format_duration(p.get("duration", 0)),
            })

        return {
            "success": True,
            "bvid": video.get("bvid"),
            "aid": video.get("aid"),
            "title": video.get("title"),
            "description": video.get("desc"),
            "cover": video.get("pic"),
            "duration": format_duration(video.get("duration", 0)),
            "author": {
                "mid": owner.get("mid"),
                "name": owner.get("name"),
            },
            "stats": {
                "views": format_number(stat.get("view", 0)),
                "likes": format_number(stat.get("like", 0)),
                "coins": format_number(stat.get("coin", 0)),
                "favorites": format_number(stat.get("favorite", 0)),
                "danmaku": stat.get("danmaku", 0),
            },
            "pages": pages,
            "url": f"https://www.bilibili.com/video/{video.get('bvid')}",
        }

    async def get_formats(self, url: str) -> Dict[str, Any]:
        """Get available download formats and qualities for a video.

        Args:
            url: Bilibili video URL or BV number.

        Returns:
            Available formats and qualities.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        # First get video info to get cid
        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        cid = data["data"]["pages"][0]["cid"]

        # Get play URL to see available qualities
        async with self._get_client() as client:
            resp = await client.get(
                API_PLAY_URL,
                params={
                    "bvid": bvid,
                    "cid": cid,
                    "fnval": 4048,
                    "fourk": 1,
                },
            )
            play_data = resp.json()

        if play_data.get("code") != 0:
            return {"success": False, "message": play_data.get("message", "API error")}

        dash = play_data.get("data", {})
        quality_names = {v: k for k, v in QUALITY_MAP.items()}

        available_qualities = []
        for qn in dash.get("accept_quality", []):
            name = quality_names.get(qn, f"qn_{qn}")
            available_qualities.append({
                "quality": name,
                "qn": qn,
            })

        return {
            "success": True,
            "bvid": bvid,
            "available_qualities": available_qualities,
            "formats": ["mp4", "flv", "mp3"],
        }

    async def download(
        self,
        url: str,
        quality: str = "1080p",
        output_dir: Optional[str] = None,
        format: str = "mp4",
        page: int = 1,
    ) -> Dict[str, Any]:
        """Download a single video.

        Args:
            url: Bilibili video URL or BV number.
            quality: Desired quality ('360p', '480p', '720p', '1080p', '1080p+', '4k').
            output_dir: Output directory (uses default if not specified).
            format: Output format ('mp4', 'flv', 'mp3').
            page: Page/episode number for multi-part videos.

        Returns:
            Download result dict with file path.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        out_dir = ensure_dir(output_dir or self.output_dir)
        qn = QUALITY_MAP.get(quality, 80)

        # Get video info
        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        video = data["data"]
        title = sanitize_filename(video.get("title", bvid))

        pages = video.get("pages", [])
        if page > len(pages):
            return {"success": False, "message": f"Page {page} not found, video has {len(pages)} pages"}

        cid = pages[page - 1]["cid"]
        page_title = pages[page - 1].get("part", "")

        if len(pages) > 1 and page_title:
            filename = f"{title}_P{page}_{sanitize_filename(page_title)}.{format}"
        else:
            filename = f"{title}.{format}"

        filepath = os.path.join(out_dir, filename)

        # Get download URL
        async with self._get_client() as client:
            resp = await client.get(
                API_PLAY_URL,
                params={
                    "bvid": bvid,
                    "cid": cid,
                    "qn": qn,
                    "fnval": 4048 if format != "flv" else 0,
                    "fourk": 1,
                },
            )
            play_data = resp.json()

        if play_data.get("code") != 0:
            return {"success": False, "message": play_data.get("message", "API error")}

        # Extract download URLs from DASH or legacy format
        dash_data = play_data.get("data", {}).get("dash")
        if dash_data and format != "flv":
            video_url = self._select_dash_stream(dash_data.get("video", []), qn)
            audio_url = self._select_dash_audio(dash_data.get("audio", []))

            if not video_url:
                return {"success": False, "message": "No suitable video stream found"}

            if format == "mp3":
                # Audio only
                if not audio_url:
                    return {"success": False, "message": "No audio stream found"}
                filepath = filepath.replace(f".{format}", ".mp3")
                await self._download_stream(audio_url, filepath)
            else:
                # Download video and audio separately, then combine
                video_tmp = filepath + ".video.tmp"
                audio_tmp = filepath + ".audio.tmp"

                await asyncio.gather(
                    self._download_stream(video_url, video_tmp),
                    self._download_stream(audio_url, audio_tmp) if audio_url else asyncio.sleep(0),
                )

                if audio_url and os.path.exists(audio_tmp):
                    # Merge video and audio (requires ffmpeg)
                    merge_result = await self._merge_streams(video_tmp, audio_tmp, filepath)
                    # Clean up temp files
                    for tmp in [video_tmp, audio_tmp]:
                        if os.path.exists(tmp):
                            os.remove(tmp)
                    if not merge_result:
                        # Fallback: rename video file
                        os.rename(video_tmp, filepath)
                else:
                    os.rename(video_tmp, filepath)
        else:
            # Legacy FLV format
            durl = play_data.get("data", {}).get("durl", [])
            if not durl:
                return {"success": False, "message": "No download URL found"}
            await self._download_stream(durl[0]["url"], filepath)

        file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
        return {
            "success": True,
            "bvid": bvid,
            "title": video.get("title"),
            "quality": quality,
            "format": format,
            "filepath": filepath,
            "file_size": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
        }

    async def batch_download(
        self,
        urls: List[str],
        quality: str = "1080p",
        output_dir: Optional[str] = None,
        format: str = "mp4",
    ) -> Dict[str, Any]:
        """Download multiple videos.

        Args:
            urls: List of Bilibili video URLs or BV numbers.
            quality: Desired quality.
            output_dir: Output directory.
            format: Output format.

        Returns:
            Batch download results.
        """
        results = []
        for url in urls:
            result = await self.download(
                url=url,
                quality=quality,
                output_dir=output_dir,
                format=format,
            )
            results.append(result)

        succeeded = sum(1 for r in results if r.get("success"))
        return {
            "success": True,
            "total": len(urls),
            "succeeded": succeeded,
            "failed": len(urls) - succeeded,
            "results": results,
        }

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a downloader action.

        Args:
            action: Action name ('download', 'get_info', 'get_formats', 'batch_download').
            **kwargs: Additional parameters for the action.

        Returns:
            Action result dict.
        """
        actions = {
            "download": self.download,
            "get_info": self.get_info,
            "get_formats": self.get_formats,
            "batch_download": self.batch_download,
        }

        handler = actions.get(action)
        if not handler:
            return {"success": False, "message": f"Unknown action: {action}"}

        import inspect
        sig = inspect.signature(handler)
        valid_params = {k: v for k, v in kwargs.items() if k in sig.parameters}

        return await handler(**valid_params)

    async def _download_stream(self, url: str, filepath: str) -> None:
        """Download a stream URL to a file.

        Args:
            url: Stream URL to download.
            filepath: Destination file path.
        """
        headers = DEFAULT_HEADERS.copy()
        headers["Referer"] = "https://www.bilibili.com"

        async with httpx.AsyncClient(
            headers=headers,
            timeout=300.0,
            follow_redirects=True,
        ) as client:
            async with client.stream("GET", url) as resp:
                with open(filepath, "wb") as f:
                    async for chunk in resp.aiter_bytes(chunk_size=1024 * 1024):
                        f.write(chunk)

    @staticmethod
    async def _merge_streams(video_path: str, audio_path: str, output_path: str) -> bool:
        """Merge video and audio streams using ffmpeg.

        Args:
            video_path: Path to the video file.
            audio_path: Path to the audio file.
            output_path: Path for the merged output file.

        Returns:
            True if merge succeeded, False otherwise.
        """
        try:
            proc = await asyncio.create_subprocess_exec(
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c", "copy",
                output_path,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.wait()
            return proc.returncode == 0
        except FileNotFoundError:
            return False

    @staticmethod
    def _select_dash_stream(streams: List[Dict], target_qn: int) -> Optional[str]:
        """Select the best matching DASH video stream.

        Args:
            streams: List of available video streams.
            target_qn: Target quality number.

        Returns:
            Stream URL or None.
        """
        if not streams:
            return None

        # Sort by quality (descending) and find best match
        sorted_streams = sorted(streams, key=lambda s: s.get("id", 0), reverse=True)

        # Try exact match first
        for s in sorted_streams:
            if s.get("id") == target_qn:
                return s.get("baseUrl") or s.get("base_url")

        # Fall back to the best available that doesn't exceed target
        for s in sorted_streams:
            if s.get("id", 0) <= target_qn:
                return s.get("baseUrl") or s.get("base_url")

        # If nothing below target, return lowest available
        return sorted_streams[-1].get("baseUrl") or sorted_streams[-1].get("base_url")

    @staticmethod
    def _select_dash_audio(streams: List[Dict]) -> Optional[str]:
        """Select the best DASH audio stream.

        Args:
            streams: List of available audio streams.

        Returns:
            Stream URL or None.
        """
        if not streams:
            return None

        # Sort by bandwidth (descending) and pick the best
        sorted_streams = sorted(streams, key=lambda s: s.get("bandwidth", 0), reverse=True)
        return sorted_streams[0].get("baseUrl") or sorted_streams[0].get("base_url")
