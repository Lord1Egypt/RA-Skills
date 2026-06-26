#!/usr/bin/env python3
"""简化的 B 站转写脚本 - 使用 get_download_url"""
import asyncio
import os
import sys

output_dir = "/root/.openclaw/workspace/skills/bilibili-video-transcriber/bilibili_transcripts"
bvid = "BV1QWd8BCEH7"

async def main():
    try:
        from bilibili_api.video import Video
        
        print(f"🎬 处理视频：{bvid}")
        print("=" * 60)
        
        # 创建视频对象
        v = Video(bvid=bvid)
        
        # 获取视频信息
        info = await v.get_info()
        print(f"✅ 视频标题：{info['title']}")
        print(f"✅ 视频时长：{info['duration']} 秒")
        
        # 获取分 P 信息
        pages = await v.get_pages()
        cid = pages[0]['cid']
        print(f"✅ CID: {cid}")
        
        # 获取下载 URL
        print(f"⬇️  获取下载 URL...")
        download_url = await v.get_download_url(cid=cid)
        
        print(f"✅ 获取到下载 URL")
        
        # 解析下载 URL
        if isinstance(download_url, dict):
            if 'dash' in download_url and 'audio' in download_url['dash']:
                audio_url = download_url['dash']['audio'][0]['baseUrl']
                print(f"🔊 音频 URL 已获取")
                
                # 使用 yt-dlp 下载
                import subprocess
                audio_file = os.path.join(output_dir, "raspberry_zero.mp3")
                
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
                    
                    # 使用 whisper 转写
                    print(f"🎤 开始语音转写 (这可能需要几分钟)...")
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
                        # 查找输出文件
                        for f in os.listdir(output_dir):
                            if f.startswith("raspberry_zero") and f.endswith(".txt"):
                                transcript_file = os.path.join(output_dir, f)
                                with open(transcript_file, 'r', encoding='utf-8') as file:
                                    content = file.read()
                                print(f"\n📄 转写文件：{transcript_file}")
                                print(f"📝 内容预览:\n{content[:500]}...")
                                return
                    else:
                        print(f"❌ 转写失败：{result2.stderr[:500]}")
                else:
                    print(f"❌ 下载失败：{result.stderr[:500]}")
            else:
                print(f"❌ 无法获取音频 URL")
                print(f"下载 URL 结构：{list(download_url.keys())}")
        else:
            print(f"❌ 下载 URL 格式异常：{type(download_url)}")
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
