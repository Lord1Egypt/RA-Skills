#!/usr/bin/env python3
"""
抖音视频 → 完整报告（升级版）
流程: Playwright抓视频 → ffmpeg抽帧 → image-understanding画面分析 → speech-to-text语音转文字 → 两路合并 → 生成HTML报告
用法: python3 douyin_pipeline.py <抖音URL> [报告标题]
"""
import asyncio, sys, os, subprocess, base64
from playwright.async_api import async_playwright

TMP = "/tmp"
WORKSPACE = "/home/gem/workspace/agent/workspace"

def run(cmd, timeout=60):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr

async def get_video_info(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox','--disable-setuid-sandbox','--disable-blink-features=AutomationControlled']
        )
        ctx = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            viewport={'width':390,'height':844}, locale='zh-CN'
        )
        page = await ctx.new_page()
        print(f"🚀 访问: {url}")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await asyncio.sleep(4)
        title = await page.title()
        video_url = await page.evaluate("""
            () => {
                const v = document.querySelector('video');
                if (v && v.src && v.src.includes('douyin')) return v.src;
                return null;
            }
        """)
        if not video_url:
            scripts = await page.query_selector_all('script')
            for s in scripts:
                txt = await s.inner_text() if hasattr(s,'inner_text') else ''
                if 'playwm' in txt or '.mp4' in txt:
                    import re
                    m = re.search(r'(https?://[^\s"\'\\]+\.mp4[^\s"\'\\]*)', txt)
                    if m: return m.group(1)
        await browser.close()
        return {'title': title, 'video_url': video_url}

def download_video(url, path):
    print(f"📥 下载视频...")
    code, _, err = run(
        f'curl -L -o "{path}" --max-time 120 -s '
        f'-H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" '
        f'-H "Referer: https://www.douyin.com/" '
        f'"{url}"', timeout=130
    )
    if code == 0:
        size = os.path.getsize(path)/(1024*1024)
        print(f"✅ 视频下载完成: {size:.1f} MB")
        return True
    print(f"❌ 下载失败: {err[-200:]}")
    return False

def extract_frames(video_path, frame_dir, interval=5):
    """每隔interval秒抽一帧，保存为jpg"""
    os.makedirs(frame_dir, exist_ok=True)
    # 获取视频时长
    code, out, _ = run(f'ffprobe -v quiet -show_entries format=duration -of csv=p=0 "{video_path}"')
    duration = float(out.strip()) if code == 0 else 60
    fps = 1.0 / interval
    cmd = f'ffmpeg -i "{video_path}" -vf "fps={fps},scale=720:-1" "{frame_dir}/frame_%03d.jpg" -y 2>&1 | tail -2'
    code, _, err = run(cmd, timeout=120)
    frames = sorted([f for f in os.listdir(frame_dir) if f.endswith('.jpg')])
    print(f"✅ 抽帧完成: {len(frames)} 帧")
    return frames

def extract_audio(video_path, audio_path):
    print(f"🎵 提取音频...")
    code, _, err = run(
        f'ffmpeg -i "{video_path}" -vn -acodec libmp3lame -q:a 2 "{audio_path}" -y',
        timeout=300
    )
    if code == 0:
        print(f"✅ 音频提取完成: {os.path.getsize(audio_path)/1024/1024:.1f} MB")
        return True
    print(f"❌ 音频失败: {err[-200:]}")
    return False

def transcribe(audio_path):
    print(f"🎙️ 语音转文字...")
    code, out, err = run(
        f'miaoda-studio-cli speech-to-text --file "{audio_path}" --lang zh --output text',
        timeout=600
    )
    if code == 0 and out.strip():
        print(f"✅ 转录完成: {len(out)} 字符")
        return out.strip()
    print(f"❌ 转录失败: {err[-200:]}")
    return None

def analyze_frames(frame_dir, frames):
    """调用 image-understanding 分析每帧画面"""
    print(f"🖼️ 分析画面中（共{len(frames)}帧）...")
    results = []
    for i, fname in enumerate(frames):
        fpath = os.path.join(frame_dir, fname)
        cmd = f'miaoda-studio-cli image-understanding --image "{fpath}" --prompt "简述这张视频截图的画面内容，包括人物动作、屏幕文字、数据图表等所有视觉信息。" --output text'
        code, out, err = run(cmd, timeout=60)
        if code == 0 and out.strip():
            results.append(f"[帧{i+1}] {out.strip()}")
            print(f"  帧{i+1}/{len(frames)} 完成")
        else:
            print(f"  帧{i+1} 失败，尝试备用...")
            # 备用：用base64读取后通过文件方式
            with open(fpath, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            print(f"  帧{i+1}: (图片 {os.path.getsize(fpath)//1024}KB)")
            results.append(f"[帧{i+1}] {fname} ({os.path.getsize(fpath)//1024}KB)")
    return "\n".join(results)

async def main():
    if len(sys.argv) < 2:
        print("用法: python3 douyin_pipeline.py <抖音URL>")
        sys.exit(1)

    url = sys.argv[1].strip()
    report_title = sys.argv[2] if len(sys.argv) > 2 else "视频报告"

    video_path = f"{TMP}/douyin_v2_video.mp4"
    audio_path = f"{TMP}/douyin_v2_audio.mp3"
    frame_dir  = f"{TMP}/douyin_v2_frames"
    transcript_path = f"{WORKSPACE}/transcript.txt"

    # Step 1: 抓视频直链
    print("\n" + "="*50)
    print("STEP 1: Playwright 抓视频直链")
    print("="*50)
    info = await get_video_info(url)
    if not info['video_url']:
        print("❌ 无法获取视频直链")
        sys.exit(1)
    print(f"📌 标题: {info['title']}")

    # Step 2: 下载视频
    print("\n" + "="*50)
    print("STEP 2: 下载视频")
    print("="*50)
    if not download_video(info['video_url'], video_path):
        sys.exit(1)

    # Step 3: 提取音频
    print("\n" + "="*50)
    print("STEP 3: 提取音频")
    print("="*50)
    if not extract_audio(video_path, audio_path):
        sys.exit(1)

    # Step 4: 抽帧
    print("\n" + "="*50)
    print("STEP 4: ffmpeg 抽帧（每5秒1帧）")
    print("="*50)
    frames = extract_frames(video_path, frame_dir, interval=5)

    # Step 5: 语音转文字
    print("\n" + "="*50)
    print("STEP 5: 语音转文字")
    print("="*50)
    transcript = transcribe(audio_path)
    if not transcript:
        print("⚠️ 转录失败，继续画面分析")

    # Step 6: 画面分析
    print("\n" + "="*50)
    print("STEP 6: 逐帧画面 AI 分析")
    print("="*50)
    frame_analysis = analyze_frames(frame_dir, frames)

    # 保存分析结果
    with open(transcript_path.replace('transcript','analysis'), 'w') as f:
        f.write(f"标题: {info['title']}\n\n=== 画面分析 ===\n{frame_analysis}\n\n=== 语音转录 ===\n{transcript or '（语音转录失败）'}")

    print(f"\n✅ 全流程完成！")
    print(f"📄 画面分析: {len(frame_analysis)} 字符")
    if transcript:
        print(f"📄 语音转录: {len(transcript)} 字符")
    print(f"📁 输出目录: {frame_dir}")
    print("\n下一步: AI 根据画面分析+语音转录生成完整报告")

if __name__ == "__main__":
    asyncio.run(main())
