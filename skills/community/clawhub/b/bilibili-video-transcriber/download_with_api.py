#!/usr/bin/env python3
"""使用 bilibili-api 下载音频并转写"""
import asyncio
import os
import sys

output_dir = "/root/.openclaw/workspace/skills/bilibili-video-transcriber/bilibili_transcripts"
bvid = "BV1QWd8BCEH7"

async def main():
    try:
        from bilibili_api import video, sync, Credential
        from bilibili_api.utils.network import get_session
        
        print(f"🎬 处理视频：{bvid}")
        print("=" * 60)
        
        # 创建视频对象（不使用 Credential，尝试公开访问）
        v = video.Video(bvid=bvid)
        
        # 获取视频信息
        info = await v.get_info()
        print(f"✅ 视频标题：{info['title']}")
        print(f"✅ 视频时长：{info['duration']} 秒")
        
        # 获取下载 URL
        pages = await v.get_pages()
        cid = pages[0]['cid']
        print(f"✅ CID: {cid}")
        
        # 尝试获取播放 URL
        play_url = await v.get_play_url(cid=cid)
        print(f"✅ 获取到播放 URL")
        
        # 获取音频 URL
        if 'dash' in play_url and 'audio' in play_url['dash']:
            audio_url = play_url['dash']['audio'][0]['baseUrl']
            print(f"🔊 音频 URL 已获取")
            
            # 使用 yt-dlp 下载（带正确的 headers）
            import subprocess
            audio_file = os.path.join(output_dir, "raspberry_zero.mp3")
            
            os.makedirs(output_dir, exist_ok=True)
            
            print(f"⬇️  下载音频中...")
            cmd = [
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "-o", audio_file,
                "--add-headers", "Referer:https://www.bilibili.com/",
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                audio_url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print(f"✅ 音频下载完成：{audio_file}")
                
                # 使用 whisper 转写
                print(f"🎤 开始语音转写...")
                transcript_cmd = [
                    "whisper",
                    audio_file,
                    "--model", "base",
                    "--language", "zh",
                    "--output_dir", output_dir,
                    "--output_format", "txt"
                ]
                result2 = subprocess.run(transcript_cmd, capture_output=True, text=True, timeout=600)
                
                if result2.returncode == 0:
                    print(f"✅ 转写完成！")
                    # 读取并显示结果
                    transcript_file = os.path.join(output_dir, "raspberry_zero.txt")
                    if os.path.exists(transcript_file):
                        with open(transcript_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        print(f"\n📄 转写内容:\n{content[:1000]}...")
                else:
                    print(f"❌ 转写失败：{result2.stderr}")
            else:
                print(f"❌ 下载失败：{result.stderr}")
        else:
            print(f"❌ 无法获取音频 URL")
            print(f"播放 URL: {play_url}")
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
