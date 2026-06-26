#!/usr/bin/env python3
"""
视频音频提取和转录工具
支持从网页下载视频，提取音频，并使用 FunASR 转录
"""

import os
import sys
import subprocess
import tempfile
import re
from urllib.parse import urljoin, urlparse

try:
    import requests
    from funasr import AutoModel
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请安装: pip install requests funasr")
    sys.exit(1)


class VideoTranscriber:
    """视频转录器"""
    
    def __init__(self):
        self.model = None
        self.temp_dir = tempfile.mkdtemp(prefix="video_transcribe_")
        
    def load_model(self):
        """加载 FunASR 模型"""
        if self.model is None:
            print("📦 加载 FunASR 模型（SenseVoiceSmall）...")
            self.model = AutoModel(
                model="iic/SenseVoiceSmall",
                vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
                disable_update=True,  # 禁用更新检查，减少内存占用
            )
            print("✅ 模型加载完成")
    
    def download_video(self, url, output_path=None):
        """下载视频"""
        if output_path is None:
            output_path = os.path.join(self.temp_dir, "video.mp4")
        
        print(f"📥 下载视频: {url}")
        
        # 使用 yt-dlp 或 ffmpeg
        try:
            # 优先使用 yt-dlp
            cmd = [
                "yt-dlp",
                "-f", "bestaudio/best",
                "-o", output_path,
                url
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 视频已保存: {output_path}")
            return output_path
        except subprocess.CalledProcessError:
            # 回退到 ffmpeg
            try:
                cmd = ["ffmpeg", "-i", url, "-c", "copy", output_path, "-y"]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✅ 视频已保存: {output_path}")
                return output_path
            except subprocess.CalledProcessError as e:
                print(f"❌ 下载失败: {e}")
                return None
        except FileNotFoundError:
            print("❌ 未找到 yt-dlp 或 ffmpeg")
            print("请安装: apt install yt-dlp ffmpeg")
            return None
    
    def extract_audio(self, video_path, output_path=None):
        """从视频中提取音频"""
        if output_path is None:
            output_path = os.path.join(self.temp_dir, "audio.wav")
        
        print(f"🎵 提取音频...")
        
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vn",  # 不包含视频
                "-acodec", "pcm_s16le",  # PCM 16-bit
                "-ar", "16000",  # 16kHz 采样率
                "-ac", "1",  # 单声道
                "-y",  # 覆盖输出文件
                output_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 音频已提取: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 音频提取失败: {e}")
            return None
        except FileNotFoundError:
            print("❌ 未找到 ffmpeg")
            print("请安装: apt install ffmpeg")
            return None
    
    def transcribe_audio(self, audio_path):
        """转录音频"""
        print(f"🎙️ 转录音频...")
        
        self.load_model()
        
        try:
            result = self.model.generate(input=audio_path, batch_size_s=300)
            
            if result and result[0]:
                text = result[0]["text"]
                print(f"✅ 转录完成")
                return text
            else:
                print("❌ 转录失败：无结果")
                return None
        except Exception as e:
            print(f"❌ 转录失败: {e}")
            return None
    
    def process_video(self, video_url, keep_files=False):
        """处理视频：下载 -> 提取音频 -> 转录"""
        print("=" * 50)
        print("🎬 视频转录工具")
        print("=" * 50)
        print()
        
        # 下载视频
        video_path = self.download_video(video_url)
        if not video_path:
            return None
        
        # 提取音频
        audio_path = self.extract_audio(video_path)
        if not audio_path:
            return None
        
        # 转录（使用较小的批处理大小降低内存占用）
        text = self.transcribe_audio(audio_path)
        
        # 清理临时文件
        if not keep_files:
            print()
            print("🧹 清理临时文件...")
            import shutil
            try:
                shutil.rmtree(self.temp_dir)
                print("✅ 临时文件已清理")
            except Exception as e:
                print(f"⚠️ 清理失败: {e}")
        
        return text
    
    def cleanup(self):
        """清理临时文件"""
        import shutil
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception:
            pass


def extract_video_urls(html_content):
    """从 HTML 中提取视频 URL"""
    urls = []
    
    # 匹配 video 标签
    video_pattern = r'<video[^>]*>\s*<source[^>]*src=["\']([^"\']+)["\']'
    urls.extend(re.findall(video_pattern, html_content))
    
    # 匹配 iframe (YouTube, Bilibili 等)
    iframe_pattern = r'<iframe[^>]*src=["\']([^"\']+)["\']'
    iframes = re.findall(iframe_pattern, html_content)
    urls.extend(iframes)
    
    # 匹配直接的视频链接
    direct_pattern = r'(https?://[^\s<>"]+\.(?:mp4|webm|ogg|avi|mov|flv))'
    urls.extend(re.findall(direct_pattern, html_content))
    
    return list(set(urls))  # 去重


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="视频转录工具")
    parser.add_argument("url", nargs="?", help="视频 URL 或网页 URL")
    parser.add_argument("--extract", "-e", action="store_true", 
                       help="从网页中提取视频 URL")
    parser.add_argument("--keep", "-k", action="store_true",
                       help="保留临时文件")
    parser.add_argument("--audio", "-a", help="直接转录音频文件")
    
    args = parser.parse_args()
    
    transcriber = VideoTranscriber()
    
    try:
        # 直接转录音频文件
        if args.audio:
            text = transcriber.transcribe_audio(args.audio)
            if text:
                print("\n" + "=" * 50)
                print("📝 转录结果：")
                print("=" * 50)
                print(text)
                print("=" * 50)
            return
        
        # 处理视频 URL
        if args.url:
            # 如果是网页 URL，先提取视频
            if args.extract:
                print(f"🔍 分析网页: {args.url}")
                response = requests.get(args.url, timeout=10)
                video_urls = extract_video_urls(response.text)
                
                if not video_urls:
                    print("❌ 未找到视频")
                    return
                
                print(f"✅ 找到 {len(video_urls)} 个视频：")
                for i, url in enumerate(video_urls, 1):
                    print(f"  {i}. {url}")
                
                # 使用第一个视频
                video_url = video_urls[0]
                print(f"\n🎬 处理第一个视频...")
            else:
                video_url = args.url
            
            # 转录
            text = transcriber.process_video(video_url, keep_files=args.keep)
            
            if text:
                print("\n" + "=" * 50)
                print("📝 转录结果：")
                print("=" * 50)
                print(text)
                print("=" * 50)
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        transcriber.cleanup()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        transcriber.cleanup()
        sys.exit(1)
    
    finally:
        transcriber.cleanup()


if __name__ == "__main__":
    main()
