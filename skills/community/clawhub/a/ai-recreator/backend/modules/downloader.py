"""视频下载模块 - 基于 yt-dlp + 多重降级策略"""
import asyncio
import logging
import re
import json
from pathlib import Path
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)

DOUYIN_PATTERN = re.compile(
    r"(https?://)?(www\.)?(douyin\.com|iesdouyin\.com|"
    r"v\.douyin\.com|t\.douyin\.com|"
    r"www\.iesdouyin\.com)/\S+"
)

TIKTOK_PATTERN = re.compile(
    r"(https?://)?(www\.)?(tiktok\.com|vm\.tiktok\.com|"
    r"m\.tiktok\.com)/\S+"
)

KUAISHOU_PATTERN = re.compile(
    r"(https?://)?(www\.)?(kuaishou\.com|v\.kuaishou\.com)/\S+"
)


def detect_platform(url: str) -> str:
    """检测短视频平台"""
    if DOUYIN_PATTERN.match(url):
        return "douyin"
    if TIKTOK_PATTERN.match(url):
        return "tiktok"
    if KUAISHOU_PATTERN.match(url):
        return "kuaishou"
    return "generic"


def resolve_short_url(url: str) -> str:
    """解析短链接为真实 URL"""
    import requests
    try:
        resp = requests.get(url, allow_redirects=True, timeout=10,
                            headers={"User-Agent": "Mozilla/5.0"})
        return resp.url
    except Exception:
        return url


class Downloader:
    """视频/音频下载（多重降级策略）"""

    def __init__(self):
        self._cookies_path = None
        cookies_file = settings.DATA_DIR.parent / "cookies.txt"
        if cookies_file.exists():
            self._cookies_path = str(cookies_file)
            logger.info(f"Found cookies file: {cookies_file}")

    async def download_audio(self, url: str, task_id: str) -> Path:
        """多策略下载音频"""
        output_dir = settings.DOWNLOAD_DIR / task_id
        output_dir.mkdir(parents=True, exist_ok=True)

        # 策略1: yt-dlp 尝试
        try:
            return await self._ytdlp_download(url, output_dir)
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"yt-dlp failed: {error_msg[:100]}")

            # 抖音专有：尝试直接网页提取
            if "douyin" in url.lower() or "iesdouyin" in url.lower():
                try:
                    resolved = resolve_short_url(url)
                    logger.info(f"Resolved URL: {resolved}")
                    return await self._douyin_direct(resolved, output_dir)
                except Exception as e2:
                    logger.warning(f"Direct douyin extraction failed: {e2}")
                    raise RuntimeError(
                        f"抖音视频下载失败：服务器IP被限制。\n"
                        f"解决方案：\n"
                        f"  1. 在 ai-recreator/ 目录下放 cookies.txt\n"
                        f"     （从浏览器导出抖音 cookies，Netscape格式）\n"
                        f"  2. 或直接私信发给智能助手，让助手代为处理\n"
                        f"  3. 或在本地（有浏览器登录态）运行 yt-dlp 下载后上传"
                    )
            raise

    async def _ytdlp_download(self, url: str, output_dir: Path) -> Path:
        """策略1: yt-dlp 标准下载"""
        audio_path = output_dir / "audio.mp3"
        platform = detect_platform(url)

        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", str(audio_path),
            "--no-playlist",
            "--socket-timeout", "30",
            "--retries", "3",
        ]

        # 全局：指定 JS 运行时（新版 yt-dlp 需要）
        cmd += ["--js-runtimes", "node"]

        # 抖音专用参数
        if platform == "douyin":
            cmd += [
                "--extractor-args", "douyin:app_version=30.9.0;manifest_app_version=30.9.0",
                "--add-header", "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                "--add-header", "Referer:https://www.douyin.com/",
            ]

        # 代理（绕过云服务器 IP 封锁）
        if settings.DOWNLOAD_PROXY:
            cmd += ["--proxy", settings.DOWNLOAD_PROXY]

        # 如果用户提供了 cookies.txt
        if self._cookies_path:
            cmd += ["--cookies", self._cookies_path]

        process = await asyncio.create_subprocess_exec(
            *cmd + [url],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=settings.DOWNLOAD_TIMEOUT,
            )
        except asyncio.TimeoutError:
            process.kill()
            raise RuntimeError(f"视频下载超时（{settings.DOWNLOAD_TIMEOUT}s）")

        if process.returncode != 0:
            error_msg = stderr.decode()[:500]
            raise RuntimeError(f"下载失败: {error_msg}")

        actual_files = list(output_dir.glob("*"))
        if not actual_files:
            raise RuntimeError("下载完成但找不到音频文件")

        logger.info(f"yt-dlp OK: {actual_files[0]} ({actual_files[0].stat().st_size / 1024:.0f} KB)")
        return actual_files[0]

    async def _douyin_direct(self, url: str, output_dir: Path) -> Path:
        """策略2: 通过 iesdouyin 移动端页面提取视频直链"""
        import requests

        # 配置代理
        proxies = {}
        if settings.DOWNLOAD_PROXY:
            proxies = {"http": settings.DOWNLOAD_PROXY, "https": settings.DOWNLOAD_PROXY}

        video_id_match = re.search(r'/video/(\d+)', url)
        if not video_id_match:
            raise RuntimeError("无法提取抖音视频ID")
        video_id = video_id_match.group(1)

        mobile_headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S9080) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Referer": "https://www.douyin.com/",
        }

        # 1. 从 iesdouyin 移动端页面提取 play_addr
        share_url = f"https://www.iesdouyin.com/share/video/{video_id}/"
        resp = requests.get(share_url, headers=mobile_headers, proxies=proxies, timeout=15)
        if resp.status_code != 200:
            raise RuntimeError(f"无法访问抖音页面（{resp.status_code}）")

        # 2. 正则提取 play_addr URL
        play_addrs = re.findall(r'play_addr[^}]+url_list[^}]+\[(.*?)\]', resp.text, re.DOTALL)
        play_urls = re.findall(r'"([^"]+)"', play_addrs[0]) if play_addrs else []
        
        if not play_urls:
            raise RuntimeError("未能提取到视频播放地址")

        # 3. 尝试无水印版本 (playwm → play)
        raw_url = play_urls[0].replace('\\u002F', '/').replace('\\/', '/').replace('\\', '')
        no_wm_url = raw_url.replace('/playwm/', '/play/').replace('playwm?', 'play?')

        video_resp = requests.get(no_wm_url, headers=mobile_headers, proxies=proxies, timeout=120)
        if video_resp.status_code not in (200, 206):
            # 回退到有水印版本
            video_resp = requests.get(raw_url, headers=mobile_headers, proxies=proxies, timeout=120)

        if video_resp.status_code not in (200, 206):
            raise RuntimeError(f"视频下载失败（HTTP {video_resp.status_code}）")

        # 4. 保存并提取音频
        audio_path = output_dir / "audio.mp3"
        tmp_video = output_dir / "source.mp4"
        tmp_video.write_bytes(video_resp.content)
        logger.info(f"Downloaded {len(video_resp.content)/1024:.0f}KB video")

        proc = await asyncio.create_subprocess_exec(
            "ffmpeg", "-y", "-i", str(tmp_video),
            "-vn", "-acodec", "libmp3lame",
            "-q:a", "2", str(audio_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()

        if not audio_path.exists():
            raise RuntimeError("FFmpeg 音频提取失败")

        logger.info(f"Douyin direct OK: {audio_path}")
        return audio_path

    async def download_video(self, url: str, task_id: str) -> Path:
        """下载视频文件"""
        output_dir = settings.DOWNLOAD_DIR / task_id
        output_dir.mkdir(parents=True, exist_ok=True)
        video_path = output_dir / "video.mp4"

        platform = detect_platform(url)
        extra_args = []
        if platform == "douyin":
            extra_args = [
                "--extractor-args", "douyin:app_version=30.9.0;manifest_app_version=30.9.0",
                "--add-header", "User-Agent:Mozilla/5.0...Chrome/120.0.0.0",
                "--add-header", "Referer:https://www.douyin.com/",
            ]

        cmd = [
            "yt-dlp",
            "--js-runtimes", "node",
            "-f", "best[height<=720]",
            "-o", str(video_path),
            "--no-playlist",
            "--socket-timeout", "30",
            "--retries", "3",
        ] + extra_args
        if settings.DOWNLOAD_PROXY:
            cmd += ["--proxy", settings.DOWNLOAD_PROXY]
        if self._cookies_path:
            cmd += ["--cookies", self._cookies_path]

        process = await asyncio.create_subprocess_exec(
            *cmd + [url],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=settings.DOWNLOAD_TIMEOUT,
            )
        except asyncio.TimeoutError:
            process.kill()
            raise RuntimeError(f"视频下载超时（{settings.DOWNLOAD_TIMEOUT}s）")

        if process.returncode != 0:
            error_msg = stderr.decode()[:500]
            raise RuntimeError(f"视频下载失败: {error_msg}")

        actual_files = list(output_dir.glob("*.mp4"))
        if not actual_files:
            raise RuntimeError("下载完成但找不到视频文件")

        logger.info(f"Video OK: {actual_files[0]}")
        return actual_files[0]
