#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音文案提取工具
从抖音分享链接提取无水印视频并 AI 识别语音文案
支持硅基流动 API，新用户引导注册并使用邀请码 84kySW0S
自动检测并安装 FFmpeg
"""

import os
import re
import json
import time
import sys
import requests
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime


def check_ffmpeg():
    """检查 FFmpeg 是否可用"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, result.stdout.split('\n')[0]
    except Exception:
        pass
    
    return False, None


def auto_install_ffmpeg():
    """自动安装 FFmpeg"""
    print("\n⚠️  检测到未安装 FFmpeg")
    print("\n💡 FFmpeg 是音视频处理工具，提取文案需要它。")
    print("\n选择安装方式:")
    print("  1. 自动下载 FFmpeg（推荐，约 100MB）")
    print("  2. 使用系统包管理器安装")
    print("  3. 跳过，仅使用获取信息功能")
    
    choice = input("\n请选择 [1-3]，默认 1: ").strip() or "1"
    
    if choice == "1":
        # 运行自动安装脚本
        script_dir = Path(__file__).parent.parent / "scripts"
        install_script = script_dir / "install_ffmpeg.py"
        
        if install_script.exists():
            print("\n🚀 启动 FFmpeg 自动安装...")
            subprocess.run([sys.executable, str(install_script)])
            
            # 验证安装
            installed, version = check_ffmpeg()
            if installed:
                print(f"\n✅ FFmpeg 安装成功：{version}")
                return True
            else:
                print("\n⚠️  安装完成但未检测到 FFmpeg，请重启终端或手动添加 PATH")
                return False
        else:
            print(f"\n❌ 未找到安装脚本：{install_script}")
            return False
    
    elif choice == "2":
        print("\n📦 使用系统包管理器安装:")
        print("\n  macOS: brew install ffmpeg")
        print("  Ubuntu/Debian: apt install ffmpeg")
        print("  CentOS/RHEL: yum install ffmpeg")
        print("  Windows: https://ffmpeg.org/download.html")
        print("\n安装完成后重新运行此命令。")
        return False
    
    else:
        print("\n💡 已跳过 FFmpeg 安装")
        print("   您仍可以使用获取视频信息和下载链接功能")
        return False


class DouyinExtractor:
    """抖音文案提取器"""
    
    # 硅基流动 API 配置
    SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
    SILICONFLOW_MODEL = "FunAudioLLM/SenseVoiceSmall"
    
    # 邀请码信息
    INVITE_CODE = "84kySW0S"
    REGISTER_URL = f"https://cloud.siliconflow.cn/i/{INVITE_CODE}"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化提取器
        
        Args:
            api_key: 硅基流动 API Key，可从环境变量获取
        """
        self.api_key = api_key or os.getenv("API_KEY", "")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        })
    
    def get_video_info(self, share_url: str) -> Dict:
        """
        获取抖音视频信息
        
        Args:
            share_url: 抖音分享链接
            
        Returns:
            包含视频 ID、标题、下载链接的字典
        """
        # 处理短链接重定向
        url = self._resolve_short_url(share_url)
        
        # 获取视频页面数据
        video_data = self._fetch_video_data(url)
        
        # 解析视频信息
        video_id = video_data.get("aweme_id", "")
        title = video_data.get("desc", "未命名视频")
        
        # 获取无水印下载链接
        download_url = self._get_download_url(video_data)
        
        return {
            "video_id": video_id,
            "title": title,
            "download_url": download_url,
            "share_url": share_url
        }
    
    def download_video(self, share_url: str, output_dir: str = "./videos") -> str:
        """
        下载无水印视频
        
        Args:
            share_url: 抖音分享链接
            output_dir: 输出目录
            
        Returns:
            下载的视频文件路径
        """
        video_info = self.get_video_info(share_url)
        video_id = video_info["video_id"]
        download_url = video_info["download_url"]
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 下载视频
        video_file = output_path / f"{video_id}.mp4"
        print(f"正在下载视频：{video_info['title']}")
        
        response = self.session.get(download_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        
        with open(video_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f"\r下载进度：{progress:.1f}%", end="", flush=True)
        
        print(f"\n视频已保存到：{video_file}")
        return str(video_file)
    
    def extract_text(self, share_url: str, output_dir: str = "./output", 
                     save_video: bool = False) -> Dict:
        """
        提取视频文案
        
        Args:
            share_url: 抖音分享链接
            output_dir: 输出目录
            save_video: 是否同时保存视频
            
        Returns:
            包含文案内容和输出路径的字典
        """
        if not self.api_key:
            print("\n❌ 未检测到 API Key")
            print("\n📝 首次使用需要先获取硅基流动 API Key：")
            print(f"1. 访问注册页面：{self.REGISTER_URL}")
            print(f"2. 使用邀请码注册：{self.INVITE_CODE}")
            print(f"3. 获取 API Key 并设置环境变量：export API_KEY=\"sk-xxx\"")
            print("\n💡 使用邀请码注册可获得额外免费额度！")
            raise ValueError("API Key 未设置")
        
        # 获取视频信息
        video_info = self.get_video_info(share_url)
        video_id = video_info["video_id"]
        
        # 创建输出目录
        output_path = Path(output_dir) / video_id
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 下载视频到临时目录
        temp_dir = tempfile.mkdtemp()
        try:
            video_file = self.download_video(share_url, temp_dir)
            
            # 提取音频
            audio_file = self._extract_audio(video_file, temp_dir)
            
            # 检测音频时长和大小
            duration, file_size = self._get_audio_info(audio_file)
            
            # 语音识别
            if duration > 3600 or file_size > 50 * 1024 * 1024:
                print(f"\n⚠️  音频文件较大（{duration:.1f}分钟，{file_size/1024/1024:.1f}MB）")
                print("将自动分段处理...")
                transcript = self._transcribe_large_audio(audio_file)
            else:
                transcript = self._transcribe_audio(audio_file)
            
            # 保存文案
            transcript_file = output_path / "transcript.md"
            self._save_transcript(transcript_file, video_info, transcript)
            
            # 保存视频（可选）
            if save_video:
                final_video = output_path / f"{video_id}.mp4"
                shutil.copy(video_file, final_video)
                print(f"视频已保存到：{final_video}")
            
            print(f"\n✅ 文案已保存到：{transcript_file}")
            
            return {
                "video_id": video_id,
                "title": video_info["title"],
                "text": transcript,
                "output_path": str(transcript_file),
                "duration": duration
            }
            
        finally:
            # 清理临时文件
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _resolve_short_url(self, share_url: str) -> str:
        """解析短链接重定向"""
        try:
            response = self.session.get(share_url, allow_redirects=False)
            if response.status_code in [301, 302]:
                return response.headers.get("Location", share_url)
        except Exception as e:
            print(f"解析链接失败：{e}")
        return share_url
    
    def _fetch_video_data(self, url: str) -> Dict:
        """获取视频页面数据"""
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        
        # 从 HTML 中提取 JSON 数据
        html = response.text
        json_match = re.search(r'\{.*"aweme_id".*\}', html)
        
        if json_match:
            return json.loads(json_match.group())
        
        raise ValueError("无法解析视频数据，请检查链接是否有效")
    
    def _get_download_url(self, video_data: Dict) -> str:
        """获取无水印下载链接"""
        # 优先获取无水印播放地址
        video = video_data.get("video", {})
        play_addr = video.get("play_addr", {})
        
        if isinstance(play_addr, dict):
            url_list = play_addr.get("url_list", [])
            if url_list:
                return url_list[0]
        
        # 备用：下载地址
        download_addr = video.get("download_addr", {})
        if isinstance(download_addr, dict):
            url_list = download_addr.get("url_list", [])
            if url_list:
                return url_list[0]
        
        raise ValueError("无法获取视频下载地址")
    
    def _extract_audio(self, video_file: str, output_dir: str) -> str:
        """从视频中提取音频"""
        # 检查 FFmpeg
        ffmpeg_available, version = check_ffmpeg()
        
        if not ffmpeg_available:
            auto_install_ffmpeg()
            # 再次检查
            ffmpeg_available, version = check_ffmpeg()
            
            if not ffmpeg_available:
                raise RuntimeError(
                    "FFmpeg 未安装，无法提取音频。\n"
                    "请运行以下命令安装 FFmpeg:\n"
                    "  - macOS: brew install ffmpeg\n"
                    "  - Ubuntu: apt install ffmpeg\n"
                    "  - 或运行：python scripts/install_ffmpeg.py"
                )
        
        audio_file = Path(output_dir) / "audio.mp3"
        
        cmd = [
            "ffmpeg", "-i", video_file,
            "-vn", "-acodec", "libmp3lame",
            "-ab", "128k", "-ar", "16000",
            "-y", str(audio_file)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        return str(audio_file)
    
    def _get_audio_info(self, audio_file: str) -> Tuple[float, int]:
        """获取音频时长和文件大小"""
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        file_size = os.path.getsize(audio_file)
        
        return duration, file_size
    
    def _transcribe_audio(self, audio_file: str) -> str:
        """语音识别（单文件）"""
        with open(audio_file, "rb") as f:
            files = {"audio": f}
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {"model": self.SILICONFLOW_MODEL}
            
            response = self.session.post(
                self.SILICONFLOW_API_URL,
                headers=headers,
                files=files,
                data=data
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("text", "")
    
    def _transcribe_large_audio(self, audio_file: str) -> str:
        """语音识别（大文件分段处理）"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # 分割音频（每段 9 分钟）
            segments = self._split_audio(audio_file, temp_dir, segment_duration=540)
            
            # 逐段识别
            transcripts = []
            for i, segment in enumerate(segments, 1):
                print(f"\n识别第 {i}/{len(segments)} 段...")
                text = self._transcribe_audio(segment)
                transcripts.append(text)
                time.sleep(0.5)  # 避免请求过快
            
            # 合并结果
            return "\n\n".join(transcripts)
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _split_audio(self, audio_file: str, output_dir: str, 
                     segment_duration: int = 540) -> list:
        """分割音频文件"""
        segments = []
        
        cmd = [
            "ffmpeg", "-i", audio_file,
            "-f", "segment",
            "-segment_time", str(segment_duration),
            "-c", "copy",
            f"{output_dir}/segment_%03d.mp3"
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        # 获取分割后的文件
        for f in sorted(Path(output_dir).glob("segment_*.mp3")):
            segments.append(str(f))
        
        return segments
    
    def _save_transcript(self, output_file: Path, video_info: Dict, text: str):
        """保存文案为 Markdown 格式"""
        content = f"""# {video_info['title']}

| 属性 | 值 |
|------|-----|
| 视频 ID | `{video_info['video_id']}` |
| 提取时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 下载链接 | [点击下载]({video_info['download_url']}) |
| 分享链接 | {video_info['share_url']} |

---

## 文案内容

{text}

---

**提取工具:** 抖音文案提取工具  
**语音识别:** 硅基流动 SenseVoice API  
**邀请码:** {self.INVITE_CODE}（注册获取免费额度）
"""
        
        output_file.write_text(content, encoding="utf-8")


def print_help():
    """打印帮助信息"""
    help_text = """
抖音文案提取工具 - 使用指南

📝 基本用法:
  python douyin_extractor.py -l "抖音分享链接" -a extract

🔧 可用操作:
  info     - 获取视频信息（无需 API）
  download - 下载无水印视频（无需 API）
  extract  - 提取文案（需要 API Key）

🎓 首次使用:
  1. 访问：https://cloud.siliconflow.cn/i/84kySW0S
  2. 使用邀请码 84kySW0S 注册
  3. 获取 API Key
  4. 设置环境变量：export API_KEY="sk-xxx"

📦 参数说明:
  -l, --link     抖音分享链接（必填）
  -a, --action   操作类型：info/download/extract（必填）
  -o, --output   输出目录（默认：./output）
  --save-video   提取文案时同时保存视频
  -q, --quiet    安静模式（减少输出）

💡 示例:
  # 获取视频信息
  python douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a info
  
  # 下载视频
  python douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a download -o ./videos
  
  # 提取文案
  export API_KEY="sk-xxx"
  python douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a extract -o ./output
  
  # 提取文案并保存视频
  python douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a extract -o ./output --save-video
"""
    print(help_text)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="抖音文案提取工具",
        add_help=False
    )
    parser.add_argument("-l", "--link", type=str, help="抖音分享链接")
    parser.add_argument("-a", "--action", type=str, 
                       choices=["info", "download", "extract"],
                       help="操作类型")
    parser.add_argument("-o", "--output", type=str, default="./output",
                       help="输出目录")
    parser.add_argument("--save-video", action="store_true",
                       help="提取文案时同时保存视频")
    parser.add_argument("-q", "--quiet", action="store_true",
                       help="安静模式")
    parser.add_argument("-h", "--help", action="store_true",
                       help="显示帮助信息")
    
    args = parser.parse_args()
    
    if args.help or not args.link or not args.action:
        print_help()
        return
    
    extractor = DouyinExtractor()
    
    try:
        if args.action == "info":
            info = extractor.get_video_info(args.link)
            print(f"\n视频 ID: {info['video_id']}")
            print(f"标题：{info['title']}")
            print(f"下载链接：{info['download_url']}")
            
        elif args.action == "download":
            video_path = extractor.download_video(args.link, args.output)
            print(f"\n✅ 视频已保存到：{video_path}")
            
        elif args.action == "extract":
            result = extractor.extract_text(
                args.link, 
                args.output, 
                args.save_video
            )
            print(f"\n✅ 文案提取完成！")
            print(f"视频标题：{result['title']}")
            print(f"文案路径：{result['output_path']}")
            print(f"视频时长：{result['duration']:.1f}秒")
            
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        if not extractor.api_key and args.action == "extract":
            print(f"\n💡 请先获取 API Key：{extractor.REGISTER_URL}")
            print(f"   使用邀请码注册：{extractor.INVITE_CODE}")


if __name__ == "__main__":
    main()
