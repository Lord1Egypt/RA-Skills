"""Bilibili subtitle downloading and processing module."""

import json
import os
from typing import Optional, Dict, Any, List

import httpx

from .auth import BilibiliAuth
from .utils import (
    API_VIDEO_INFO,
    API_SUBTITLE,
    DEFAULT_HEADERS,
    extract_bvid,
    ensure_dir,
    sanitize_filename,
)


class SubtitleDownloader:
    """Download and process subtitles from Bilibili videos.

    Supports multiple subtitle formats (SRT, ASS, VTT, TXT, JSON) and languages.
    """

    def __init__(self, auth: Optional[BilibiliAuth] = None, output_dir: str = "./subtitles"):
        """Initialize SubtitleDownloader.

        Args:
            auth: Optional BilibiliAuth instance for authenticated requests.
            output_dir: Default output directory for subtitle files.
        """
        self.auth = auth
        self.output_dir = output_dir

    def _get_client(self) -> httpx.AsyncClient:
        """Get an HTTP client, using auth if available."""
        if self.auth:
            return self.auth.get_client()
        return httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=30.0,
            follow_redirects=True,
        )

    async def list_subtitles(self, url: str) -> Dict[str, Any]:
        """List available subtitles for a video.

        Args:
            url: Bilibili video URL or BV number.

        Returns:
            List of available subtitles with language info.
        """
        bvid = extract_bvid(url)
        if not bvid:
            return {"success": False, "message": f"Invalid URL or BV number: {url}"}

        # Get video info to get cid
        async with self._get_client() as client:
            resp = await client.get(API_VIDEO_INFO, params={"bvid": bvid})
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "API error")}

        video = data["data"]
        cid = video["pages"][0]["cid"]
        title = video.get("title", bvid)

        # Get subtitle info
        async with self._get_client() as client:
            resp = await client.get(
                API_SUBTITLE,
                params={"bvid": bvid, "cid": cid},
            )
            sub_data = resp.json()

        if sub_data.get("code") != 0:
            return {"success": False, "message": sub_data.get("message", "API error")}

        subtitles_info = sub_data.get("data", {}).get("subtitle", {})
        subtitles = []
        for sub in subtitles_info.get("subtitles", []):
            subtitles.append({
                "id": sub.get("id"),
                "language": sub.get("lan"),
                "language_name": sub.get("lan_doc"),
                "url": sub.get("subtitle_url"),
                "ai_type": sub.get("ai_type", 0),
                "ai_status": sub.get("ai_status", 0),
            })

        return {
            "success": True,
            "bvid": bvid,
            "title": title,
            "cid": cid,
            "subtitles": subtitles,
            "count": len(subtitles),
        }

    async def download(
        self,
        url: str,
        language: str = "zh-CN",
        format: str = "srt",
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Download subtitles for a video.

        Args:
            url: Bilibili video URL or BV number.
            language: Subtitle language code (e.g., 'zh-CN', 'en', 'ja').
            format: Output format ('srt', 'ass', 'vtt', 'txt', 'json').
            output_dir: Output directory.

        Returns:
            Download result with file path.
        """
        out_dir = ensure_dir(output_dir or self.output_dir)

        # List available subtitles
        sub_list = await self.list_subtitles(url)
        if not sub_list.get("success"):
            return sub_list

        # Find matching subtitle
        target_sub = None
        for sub in sub_list.get("subtitles", []):
            if sub["language"] == language or sub["language"].startswith(language.split("-")[0]):
                target_sub = sub
                break

        if not target_sub:
            available = [s["language"] for s in sub_list.get("subtitles", [])]
            return {
                "success": False,
                "message": f"Subtitle for language '{language}' not found. Available: {available}",
            }

        # Download subtitle JSON
        sub_url = target_sub["url"]
        if sub_url.startswith("//"):
            sub_url = "https:" + sub_url

        async with self._get_client() as client:
            resp = await client.get(sub_url)
            sub_data = resp.json()

        # Convert and save
        title = sanitize_filename(sub_list.get("title", "subtitle"))
        filename = f"{title}_{language}.{format}"
        filepath = os.path.join(out_dir, filename)

        body = sub_data.get("body", [])

        converters = {
            "srt": self._to_srt,
            "ass": self._to_ass,
            "vtt": self._to_vtt,
            "txt": self._to_txt,
            "json": self._to_json,
        }

        converter = converters.get(format, self._to_srt)
        content = converter(body, title)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "bvid": sub_list.get("bvid"),
            "title": sub_list.get("title"),
            "language": language,
            "format": format,
            "filepath": filepath,
            "entries": len(body),
        }

    async def convert(
        self,
        input_path: str,
        output_format: str,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convert a subtitle file to a different format.

        Args:
            input_path: Path to the input subtitle file.
            output_format: Target format ('srt', 'ass', 'vtt', 'txt').
            output_dir: Output directory (defaults to same as input).

        Returns:
            Conversion result.
        """
        if not os.path.exists(input_path):
            return {"success": False, "message": f"File not found: {input_path}"}

        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to detect input format and parse
        body = self._parse_subtitle(content, input_path)
        if body is None:
            return {"success": False, "message": "Cannot parse input subtitle file"}

        out_dir = output_dir or os.path.dirname(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(out_dir, f"{base_name}.{output_format}")

        converters = {
            "srt": self._to_srt,
            "ass": self._to_ass,
            "vtt": self._to_vtt,
            "txt": self._to_txt,
            "json": self._to_json,
        }

        converter = converters.get(output_format, self._to_srt)
        output_content = converter(body, base_name)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)

        return {
            "success": True,
            "input": input_path,
            "output": output_path,
            "format": output_format,
            "entries": len(body),
        }

    async def merge(
        self,
        input_paths: List[str],
        output_path: str,
        output_format: str = "srt",
    ) -> Dict[str, Any]:
        """Merge multiple subtitle files into one.

        Args:
            input_paths: List of input subtitle file paths.
            output_path: Output file path.
            output_format: Output format.

        Returns:
            Merge result.
        """
        all_body = []
        time_offset = 0.0

        for path in input_paths:
            if not os.path.exists(path):
                return {"success": False, "message": f"File not found: {path}"}

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            body = self._parse_subtitle(content, path)
            if body is None:
                return {"success": False, "message": f"Cannot parse: {path}"}

            # Offset timestamps
            for entry in body:
                entry["from"] = entry.get("from", 0) + time_offset
                entry["to"] = entry.get("to", 0) + time_offset

            if body:
                time_offset = body[-1].get("to", 0) + 0.5

            all_body.extend(body)

        converters = {
            "srt": self._to_srt,
            "ass": self._to_ass,
            "vtt": self._to_vtt,
            "txt": self._to_txt,
            "json": self._to_json,
        }

        converter = converters.get(output_format, self._to_srt)
        output_content = converter(all_body, "merged")

        ensure_dir(os.path.dirname(output_path) or ".")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)

        return {
            "success": True,
            "output": output_path,
            "format": output_format,
            "total_entries": len(all_body),
            "merged_files": len(input_paths),
        }

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a subtitle action.

        Args:
            action: Action name ('download', 'list', 'convert', 'merge').
            **kwargs: Additional parameters for the action.

        Returns:
            Action result dict.
        """
        actions = {
            "download": self.download,
            "list": self.list_subtitles,
            "convert": self.convert,
            "merge": self.merge,
        }

        handler = actions.get(action)
        if not handler:
            return {"success": False, "message": f"Unknown action: {action}"}

        import inspect
        sig = inspect.signature(handler)
        valid_params = {k: v for k, v in kwargs.items() if k in sig.parameters}

        return await handler(**valid_params)

    # --- Format converters ---

    @staticmethod
    def _format_time_srt(seconds: float) -> str:
        """Format seconds to SRT timestamp (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def _format_time_vtt(seconds: float) -> str:
        """Format seconds to VTT timestamp (HH:MM:SS.mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    @staticmethod
    def _format_time_ass(seconds: float) -> str:
        """Format seconds to ASS timestamp (H:MM:SS.cc)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centis = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"

    @classmethod
    def _to_srt(cls, body: List[Dict], title: str = "") -> str:
        """Convert subtitle body to SRT format."""
        lines = []
        for i, entry in enumerate(body, 1):
            start = cls._format_time_srt(entry.get("from", 0))
            end = cls._format_time_srt(entry.get("to", 0))
            content = entry.get("content", "")
            lines.append(f"{i}\n{start} --> {end}\n{content}\n")
        return "\n".join(lines)

    @classmethod
    def _to_vtt(cls, body: List[Dict], title: str = "") -> str:
        """Convert subtitle body to WebVTT format."""
        lines = ["WEBVTT", ""]
        for i, entry in enumerate(body, 1):
            start = cls._format_time_vtt(entry.get("from", 0))
            end = cls._format_time_vtt(entry.get("to", 0))
            content = entry.get("content", "")
            lines.append(f"{i}\n{start} --> {end}\n{content}\n")
        return "\n".join(lines)

    @classmethod
    def _to_ass(cls, body: List[Dict], title: str = "") -> str:
        """Convert subtitle body to ASS format."""
        header = f"""[Script Info]
Title: {title}
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        lines = [header]
        for entry in body:
            start = cls._format_time_ass(entry.get("from", 0))
            end = cls._format_time_ass(entry.get("to", 0))
            content = entry.get("content", "").replace("\n", "\\N")
            lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{content}")

        return "\n".join(lines)

    @staticmethod
    def _to_txt(body: List[Dict], title: str = "") -> str:
        """Convert subtitle body to plain text."""
        lines = []
        for entry in body:
            content = entry.get("content", "")
            if content.strip():
                lines.append(content)
        return "\n".join(lines)

    @staticmethod
    def _to_json(body: List[Dict], title: str = "") -> str:
        """Convert subtitle body to JSON format."""
        return json.dumps(
            {"title": title, "body": body},
            ensure_ascii=False,
            indent=2,
        )

    @staticmethod
    def _parse_subtitle(content: str, filepath: str) -> Optional[List[Dict]]:
        """Parse a subtitle file into internal body format.

        Args:
            content: File content.
            filepath: File path (used to detect format).

        Returns:
            List of subtitle entries or None.
        """
        ext = os.path.splitext(filepath)[1].lower()

        if ext == ".json":
            try:
                data = json.loads(content)
                if isinstance(data, dict) and "body" in data:
                    return data["body"]
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                return None

        if ext == ".srt":
            return SubtitleDownloader._parse_srt(content)

        if ext == ".vtt":
            # Remove WEBVTT header
            content = content.replace("WEBVTT", "").strip()
            return SubtitleDownloader._parse_srt(content)

        if ext == ".txt":
            lines = content.strip().split("\n")
            body = []
            for i, line in enumerate(lines):
                if line.strip():
                    body.append({
                        "from": i * 3.0,
                        "to": (i + 1) * 3.0,
                        "content": line.strip(),
                    })
            return body

        return None

    @staticmethod
    def _parse_srt(content: str) -> List[Dict]:
        """Parse SRT format content."""
        import re

        body = []
        blocks = re.split(r"\n\s*\n", content.strip())

        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) < 3:
                continue

            time_match = re.match(
                r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})",
                lines[1],
            )
            if not time_match:
                continue

            start_str = time_match.group(1).replace(",", ".")
            end_str = time_match.group(2).replace(",", ".")

            def parse_ts(ts: str) -> float:
                parts = ts.split(":")
                return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])

            body.append({
                "from": parse_ts(start_str),
                "to": parse_ts(end_str),
                "content": "\n".join(lines[2:]),
            })

        return body
