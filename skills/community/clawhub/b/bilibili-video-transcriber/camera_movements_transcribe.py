#!/usr/bin/env python3
"""快速处理 B 站视频 - 镜头运镜提示词"""
import asyncio
import os
import sys
import subprocess

output_dir = "/root/.openclaw/workspace/skills/bilibili-video-transcriber/bilibili_transcripts"
bvid = "BV1wRiZBbEoy"
cid = 35216493188

async def main():
    try:
        from bilibili_api.video import Video
        
        print(f"🎬 处理视频：{bvid}")
        print("=" * 60)
        
        v = Video(bvid=bvid)
        info = await v.get_info()
        print(f"✅ 视频标题：{info['title']}")
        print(f"✅ 视频时长：{info['duration']} 秒")
        
        # 获取下载 URL
        download_url = await v.get_download_url(cid=cid)
        
        if isinstance(download_url, dict) and 'dash' in download_url and 'audio' in download_url['dash']:
            audio_url = download_url['dash']['audio'][0]['baseUrl']
            print(f"🔊 音频 URL 已获取")
            
            # 下载音频
            audio_file = os.path.join(output_dir, "camera_movements.mp3")
            os.makedirs(output_dir, exist_ok=True)
            
            print(f"⬇️  下载音频中...")
            cmd = [
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "-o", audio_file,
                "--add-headers", "Referer:https://www.bilibili.com/",
                "--user-agent", "Mozilla/5.0",
                audio_url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0 or os.path.exists(audio_file):
                print(f"✅ 音频下载完成：{audio_file}")
                
                # 使用 whisper tiny 快速转写
                print(f"🎤 开始语音转写（约需 5-8 分钟）...")
                transcript_cmd = [
                    "whisper",
                    audio_file,
                    "--model", "tiny",
                    "--language", "zh",
                    "--output_dir", output_dir,
                    "--output_format", "txt"
                ]
                result2 = subprocess.run(transcript_cmd, capture_output=True, text=True, timeout=600)
                
                if result2.returncode == 0:
                    print(f"✅ 转写完成！")
                    for f in os.listdir(output_dir):
                        if f.startswith("camera_movements") and f.endswith(".txt"):
                            with open(os.path.join(output_dir, f), 'r', encoding='utf-8') as file:
                                content = file.read()
                            print(f"\n📝 转写内容:\n{content[:800]}...")
                            return
                else:
                    print(f"❌ 转写失败：{result2.stderr[:500]}")
            else:
                print(f"❌ 下载失败：{result.stderr[:500]}")
        else:
            print(f"❌ 无法获取音频 URL")
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
