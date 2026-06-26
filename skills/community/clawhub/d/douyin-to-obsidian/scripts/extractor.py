#!/usr/bin/env python3
"""
抖音视频文案提取 - 可直接使用的简化版
只保留最稳定的方案：Playwright 抓取 + 本地 Whisper
支持长视频自动分段
"""

import asyncio
import json
import re
import os
import shutil
import tempfile
import gc
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List

import aiohttp


@dataclass
class VideoInfo:
    """视频信息"""
    video_id: str
    title: str
    author: str
    duration: int  # 秒
    audio_url: Optional[str]
    has_subtitle: bool
    subtitle_content: Optional[str]


class DouyinExtractor:
    """
    抖音文案提取器 - 可直接使用版本

    使用步骤：
    1. pip install -r requirements.txt
    2. playwright install chromium
    3. python extractor.py
    """

    def __init__(self, whisper_model: str = "base", segment_minutes: int = 10):
        self.whisper_model = whisper_model
        self.segment_seconds = segment_minutes * 60
        self.temp_dir = Path(tempfile.gettempdir()) / "douyin_extract"
        self.temp_dir.mkdir(exist_ok=True)
        
        # 确保 ffmpeg 可用（自动下载）
        self._ensure_ffmpeg()

        # 注册自动清理
        import atexit
        atexit.register(self.cleanup)
    
    def _ensure_ffmpeg(self):
        """确保 ffmpeg 可用，如不可用则自动下载"""
        # 检查是否已有 ffmpeg
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            print(f"✅ 已找到 ffmpeg: {ffmpeg_path}")
            return
        
        # 检查用户目录下的缓存
        cache_dir = Path.home() / ".douyin_skill" / "ffmpeg"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        if os.name == 'nt':  # Windows
            ffmpeg_exe = cache_dir / "ffmpeg.exe"
            if ffmpeg_exe.exists():
                print(f"✅ 使用缓存的 ffmpeg: {ffmpeg_exe}")
                os.environ["PATH"] = str(cache_dir) + os.pathsep + os.environ.get("PATH", "")
                return
            
            # 下载 ffmpeg
            print("⏳ 正在下载 FFmpeg...")
            self._download_ffmpeg(cache_dir)
        else:
            # macOS/Linux 尝试使用系统包管理器
            print("⚠️ 未找到 ffmpeg，请手动安装：")
            print("  macOS: brew install ffmpeg")
            print("  Linux: sudo apt-get install ffmpeg")
            raise RuntimeError("FFmpeg not found")
    
    def _download_ffmpeg(self, cache_dir: Path):
        """下载 FFmpeg (Windows)"""
        import zipfile
        import requests
        
        # FFmpeg Windows 构建版 URL
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = cache_dir / "ffmpeg.zip"
        
        try:
            # 下载
            print(f"  下载地址：{ffmpeg_url}")
            with requests.get(ffmpeg_url, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                downloaded = 0
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            print(f"  进度：{downloaded/1024/1024:.1f}/{total/1024/1024:.1f} MB", end='\r')
            
            print(f"\n  ✅ 下载完成：{zip_path.stat().st_size/1024/1024:.1f} MB")
            
            # 解压
            print("  解压中...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # 找到包含 ffmpeg.exe 的目录
                for name in zip_ref.namelist():
                    if 'bin/ffmpeg.exe' in name:
                        extract_path = zip_ref.extract(name, cache_dir)
                        # 将 ffmpeg.exe 复制到根目录
                        bin_dir = Path(extract_path).parent
                        for file in bin_dir.iterdir():
                            if file.suffix == '.exe':
                                shutil.copy2(file, cache_dir / file.name)
                        break
            
            # 清理 zip
            zip_path.unlink()
            
            # 添加到 PATH
            os.environ["PATH"] = str(cache_dir) + os.pathsep + os.environ.get("PATH", "")
            print(f"  ✅ FFmpeg 已安装到：{cache_dir}")
            
        except Exception as e:
            print(f"\n❌ FFmpeg 下载失败：{e}")
            print("请手动下载 ffmpeg.exe 并放到以下目录：")
            print(f"  {cache_dir}")
            raise

    async def extract(self, video_url: str) -> tuple[str, VideoInfo]:
        """
        提取视频文案并返回元数据

        流程：
        1. 抓取视频信息（Playwright）
        2. 如果有字幕，直接返回字幕文本和元数据
        3. 否则下载音频，使用 Whisper 识别并返回
        """
        print(f"开始处理：{video_url}")

        # 1. 获取视频信息
        info = await self._fetch_video_info(video_url)
        print(f"\n视频信息:")
        print(f"  标题：{info.title[:60] if info.title else 'N/A'}")
        print(f"  作者：{info.author}")
        print(f"  时长：{info.duration // 60}分{info.duration % 60}秒")
        print(f"  有字幕：{info.has_subtitle}")

        # 2. 优先使用字幕（最快最准）
        if info.has_subtitle and info.subtitle_content:
            print("\n使用字幕提取...")
            return info.subtitle_content, info

        # 3. 使用 Whisper 识别音频
        if not info.audio_url:
            raise RuntimeError("无法获取音频 URL")

        print(f"\n使用 Whisper 识别音频 ({self.whisper_model}模型)...")
        text = await self._transcribe_audio(info.audio_url, info.duration)
        return text, info

    async def _fetch_video_info(self, video_url: str) -> VideoInfo:
        """使用 Playwright 抓取视频信息"""
        import requests
        from playwright.async_api import async_playwright
        from urllib.parse import parse_qs, urlparse

        # 解析短链与转化模态以绕过风控
        try:
            if "v.douyin.com" in video_url:
                print(f"检测到短链，正在解析真实地址：{video_url}")
                resp = requests.get(video_url, allow_redirects=True, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                video_url = resp.url
                print(f"短链已解析为真实链接：{video_url}")
            
            # 抖音直接访问 /video/ 会触发验证码或空页面，使用 jingxuan 的 modal_id 绕过
            if "/video/" in video_url:
                parsed = urlparse(video_url)
                parts = parsed.path.split("/video/")
                if len(parts) > 1:
                    vid = parts[1].split("/")[0]
                    if vid.isdigit():
                        video_url = f"https://www.douyin.com/jingxuan?modal_id={vid}"
                        print(f"为绕过风控，已转化为精选模态链接：{video_url}")

        except Exception as e:
            print(f"链接解析警告：{e}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                ]
            )

            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0.36',
                locale='zh-CN',
                timezone_id='Asia/Shanghai'
            )

            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            """)

            page = await context.new_page()

            try:
                print("正在加载页面...")
                await page.goto(video_url, wait_until='domcontentloaded', timeout=60000)
                await asyncio.sleep(3)

                # 检查是否是 modal 页面（jingxuan 页面）
                parsed = urlparse(video_url)
                if 'jingxuan' in parsed.path or 'modal_id' in parsed.query:
                    print("检测到精选页 modal，等待视频加载...")
                    # 等待 modal 中的视频加载
                    await asyncio.sleep(2)
                    # 获取当前页面的真实 URL
                    current_url = page.url
                    print(f"页面重定向到：{current_url}")

                # 从 SSR 数据中提取
                ssr_data = await page.evaluate("""() => {
                    return window._SSR_HYDRATED_DATA || window.__INITIAL_STATE__;
                }""")

                if not ssr_data:
                    # 尝试从页面脚本中提取
                    print("尝试从页面脚本提取数据...")
                    page_content = await page.content()
                    ssr_data = self._extract_from_html(page_content)

                if not ssr_data:
                    raise RuntimeError("无法获取页面数据，可能遇到反爬")

                video_data = self._parse_video_data(ssr_data)

                await browser.close()
                return video_data

            except Exception as e:
                try:
                    _page_html = await page.content()
                    with open("failed_page.html", "w", encoding="utf-8") as _f:
                        _f.write(_page_html)
                except:
                    pass
                await browser.close()
                raise RuntimeError(f"抓取失败：{e}")

    def _extract_from_html(self, html: str) -> dict:
        """从 HTML 内容中提取 SSR 数据"""
        import urllib.parse

        # 尝试提取 RENDER_DATA
        match = re.search(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', html, re.DOTALL)
        if match:
            try:
                data_str = urllib.parse.unquote(match.group(1))
                return json.loads(data_str)
            except Exception as e:
                print(f"RENDER_DATA 解析失败：{e}")
        
        # 尝试提取 routerData
        match = re.search(r'<script id="douyin_web_SSR_ROUTER_DATA" type="application/json">(.*?)</script>', html, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        # 尝试多种可能的脚本数据格式
        patterns = [
            r'<script[^>]*>window\._SSR_HYDRATED_DATA\s*=\s*({.+?})</script>',
            r'<script[^>]*>window\.__INITIAL_STATE__\s*=\s*({.+?})</script>',
            r'<script[^>]*>window\.__INITIAL_DATA__\s*=\s*({.+?})</script>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue

        return {}

    def _parse_video_data(self, ssr_data: dict) -> VideoInfo:
        """解析 SSR 数据结构（支持多种页面类型）"""
        try:
            video_detail = None

            # 尝试多种可能的数据路径
            if 'app' in ssr_data:
                if 'videoDetail' in ssr_data['app']:
                    video_detail = ssr_data['app']['videoDetail']
                elif 'videoInfo' in ssr_data['app']:
                    video_detail = ssr_data['app']['videoInfo']

            if 'videoInfo' in ssr_data:
                video_detail = ssr_data['videoInfo']

            if 'data' in ssr_data and isinstance(ssr_data['data'], list) and len(ssr_data['data']) > 0:
                # jingxuan 页面的数据结构
                for item in ssr_data['data']:
                    if 'aweme_info' in item:
                        video_detail = item['aweme_info']
                        break

            if not video_detail:
                app_keys = list(ssr_data['app'].keys()) if 'app' in ssr_data and isinstance(ssr_data['app'], dict) else []
                import json
                with open("failed_ssr_data.json", "w", encoding="utf-8") as _f:
                    json.dump(ssr_data, _f, ensure_ascii=False)
                
                raise ValueError("无法找到视频详情，数据结构：" + str(list(ssr_data.keys())) + "，已保存至 failed_ssr_data.json")

            # 标准化字段名
            video = video_detail.get('video', {})
            author = video_detail.get('author', {})
            music = video_detail.get('music', {})

            # 提取音频 URL
            audio_url = None
            if music:
                play_url = music.get('playUrl') or music.get('play_url', {})
                if isinstance(play_url, dict):
                    url_list = play_url.get('urlList') or play_url.get('url_list', [])
                    audio_url = url_list[0] if url_list else None

            # 尝试从 video 中提取音频
            if not audio_url and video:
                play_addr = video.get('playAddr') or video.get('play_addr', {})
                if isinstance(play_addr, dict):
                    url_list = play_addr.get('urlList') or play_addr.get('url_list', [])
                    audio_url = url_list[0] if url_list else None

            # 提取字幕
            has_subtitle = False
            subtitle_content = None
            subtitles = video_detail.get('subtitleInfos') or video_detail.get('subtitle_info', [])
            if subtitles and len(subtitles) > 0:
                has_subtitle = True
                subtitle_url = subtitles[0].get('url')
                if subtitle_url:
                    try:
                        import requests
                        resp = requests.get(subtitle_url, timeout=10)
                        subtitle_content = self._parse_subtitle(resp.text)
                    except:
                        pass

            # 获取时长（可能是毫秒或秒）
            duration = video.get('duration', 0)
            if duration > 10000:  # 如果是毫秒（大于 10 秒*1000）
                duration = duration // 1000

            return VideoInfo(
                video_id=str(video_detail.get('awemeId') or video_detail.get('aweme_id', '')),
                title=video_detail.get('desc', ''),
                author=author.get('nickname', ''),
                duration=duration,
                audio_url=audio_url,
                has_subtitle=has_subtitle,
                subtitle_content=subtitle_content
            )

        except Exception as e:
            raise RuntimeError(f"解析视频数据失败：{e}")

    def _parse_subtitle(self, content: str) -> str:
        """解析字幕文件为纯文本"""
        lines = []
        for line in content.split('\n'):
            line = line.strip()
            # 跳过时间戳和序号
            if line and not line.isdigit() and '-->' not in line and not line.startswith('WEBVTT'):
                lines.append(line)
        return ' '.join(lines)

    async def _transcribe_audio(self, audio_url: str, duration: int) -> str:
        """转录音频（支持长视频分段）"""
        import whisper

        print(f"加载 Whisper 模型：{self.whisper_model}")
        model = whisper.load_model(self.whisper_model)

        # 判断是否需要分段
        if duration <= 1800:  # <30 分钟，直接处理
            return await self._transcribe_single(model, audio_url)
        else:
            # 长视频分段处理
            return await self._transcribe_segments(model, audio_url, duration)

    async def _transcribe_single(self, model, audio_url: str) -> str:
        """处理短视频（直接下载识别）"""
        print("下载音频...")

        # 下载音频
        audio_path = self.temp_dir / "audio.mp3"
        async with aiohttp.ClientSession() as session:
            async with session.get(audio_url, timeout=aiohttp.ClientTimeout(total=300)) as resp:
                audio_data = await resp.read()
                audio_path.write_bytes(audio_data)

        try:
            print("识别中...")
            result = model.transcribe(
                str(audio_path),
                language="zh",
                initial_prompt="以下是普通话的句子。"
            )
            return result["text"]
        finally:
            audio_path.unlink()

    async def _transcribe_segments(self, model, audio_url: str, duration: int) -> str:
        """处理长视频（分段识别）"""
        import ffmpeg

        num_segments = (duration // self.segment_seconds) + 1
        print(f"长视频分段处理：共{num_segments}段，每段{self.segment_seconds // 60}分钟")

        # 先下载完整音频（因为大部分 URL 不支持 Range 请求）
        full_audio = self.temp_dir / "full_audio.mp3"

        if not full_audio.exists():
            print("下载完整音频...")
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url, timeout=aiohttp.ClientTimeout(total=600)) as resp:
                    audio_data = await resp.read()
                    full_audio.write_bytes(audio_data)
                    print(f"下载完成：{len(audio_data) / 1024 / 1024:.1f} MB")

        all_texts = []

        try:
            for i in range(num_segments):
                start_sec = i * self.segment_seconds
                end_sec = min(start_sec + self.segment_seconds, duration)

                print(f"\n处理第{i+1}/{num_segments}段 ({start_sec}-{end_sec}秒)...")

                # 使用 ffmpeg 裁剪音频段
                segment_path = self.temp_dir / f"segment_{i:03d}.mp3"

                (
                    ffmpeg
                    .input(str(full_audio), ss=start_sec, t=end_sec - start_sec)
                    .output(str(segment_path), acodec='libmp3lame', ar=16000, ac=1)
                    .run(overwrite_output=True, quiet=True)
                )

                # 识别
                result = model.transcribe(
                    str(segment_path),
                    language="zh",
                    initial_prompt="以下是普通话的句子。"
                )

                all_texts.append(result["text"])

                # 删除分段文件
                segment_path.unlink()

                # 强制垃圾回收
                gc.collect()

            return "\n".join(all_texts)

        finally:
            # 清理完整音频文件
            if full_audio.exists():
                full_audio.unlink()

    def cleanup(self):
        """清理所有临时文件"""
        if self.temp_dir and self.temp_dir.exists():
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
            except:
                pass

if __name__ == "__main__":
    print("💡 请运行 scripts/run_extract.py 来开始提取文案。")
