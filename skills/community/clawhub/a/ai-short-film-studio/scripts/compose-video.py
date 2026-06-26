#!/usr/bin/env python3
"""
AI短剧 旁白+字幕+背景音乐 合成模板

用法:
  python3 compose-video.py \
    --base ./my-project \
    --storyboard ./my-project/storyboard.json \
    --output ./my-project/最终成片.mp4 \
    --voice zh-CN-YunjianNeural \
    --rate -5%

功能:
  1. edge-tts 生成中文旁白（自动适配时长）
  2. Pillow 生成字幕PNG（白色+黑色描边）
  3. FFmpeg 逐段合成（视频+旁白+字幕）
  4. FFmpeg 生成柔和背景音乐（C+E+G三和弦）
  5. 最终混音（旁白1.0 + BGM 0.18）

依赖:
  - edge-tts: pip install edge-tts
  - Pillow: pip install Pillow
  - FFmpeg + ffprobe (macOS: /opt/homebrew/bin/ffmpeg)
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    import edge_tts
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("   安装: pip install edge-tts Pillow")
    sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser(description="AI短剧旁白+字幕+背景音乐合成")
    p.add_argument("--base", required=True, help="项目根目录")
    p.add_argument("--storyboard", required=True, help="storyboard.json 路径")
    p.add_argument("--output", required=True, help="输出文件路径")
    p.add_argument("--voice", default="zh-CN-YunjianNeural", help="TTS音色 (默认: 云健男声)")
    p.add_argument("--rate", default="-5%", help="TTS语速 (默认: -5%%)")
    p.add_argument("--segment-dur", type=float, default=10.0, help="每段视频时长(秒)")
    p.add_argument("--video-w", type=int, default=1280, help="视频宽度")
    p.add_argument("--video-h", type=int, default=720, help="视频高度")
    p.add_argument("--bgm-volume", type=float, default=0.18, help="BGM音量 (0-1)")
    return p.parse_args()


def get_duration(filepath, ffprobe_path):
    """用ffprobe获取媒体时长"""
    result = subprocess.run(
        [ffprobe_path, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(filepath)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def find_ffmpeg():
    """查找FFmpeg路径"""
    for p in ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg", "ffmpeg"]:
        try:
            subprocess.run([p, "-version"], capture_output=True)
            return p
        except (FileNotFoundError, OSError):
            continue
    return "ffmpeg"


def find_ffprobe():
    for p in ["/opt/homebrew/bin/ffprobe", "/usr/local/bin/ffprobe", "ffprobe"]:
        try:
            subprocess.run([p, "-version"], capture_output=True)
            return p
        except (FileNotFoundError, OSError):
            continue
    return "ffprobe"


def find_font():
    """查找中文字体"""
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


# ===== Step 1: TTS配音生成 =====
async def generate_tts(scenes, audio_dir, tts_voice, tts_rate, seg_dur, ffprobe_path):
    """为每段旁白生成TTS音频"""
    print("\n" + "=" * 60)
    print("Step 1: 生成TTS旁白配音")
    print("=" * 60)

    durations = []
    for scene in scenes:
        sid = scene["id"]
        text = scene["narration"]
        title = scene.get("title", f"镜头{sid}")
        out_file = audio_dir / f"narration_{sid:02d}.mp3"

        if out_file.exists():
            dur = get_duration(out_file, ffprobe_path)
            print(f"  ✅ [{sid:02d}] {title} — 已存在 ({dur:.1f}s)")
            durations.append(dur)
            continue

        print(f"  🎤 [{sid:02d}] {title} — 生成中...")

        # 根据字数调整语速
        char_count = len(text)
        rate = tts_rate
        if char_count > 40:
            rate = "+5%"
        elif char_count > 30:
            rate = "+0%"

        try:
            comm = edge_tts.Communicate(text, tts_voice, rate=rate)
            await comm.save(str(out_file))
            dur = get_duration(out_file, ffprobe_path)

            # 如果TTS超过视频时长，加速重生成
            if dur > seg_dur:
                print(f"     ⚠️  时长{dur:.1f}s > {seg_dur}s，加速重生成...")
                faster_rate = f"+{10 + int((dur - seg_dur + 1) * 15)}%"
                comm2 = edge_tts.Communicate(text, tts_voice, rate=faster_rate)
                await comm2.save(str(out_file))
                dur = get_duration(out_file, ffprobe_path)

            print(f"     ✅ 完成 ({dur:.1f}s, {char_count}字)")
            durations.append(dur)
        except Exception as e:
            print(f"     ❌ 失败: {e}")
            durations.append(seg_dur)

    return durations


# ===== Step 2: 字幕PNG生成 =====
def generate_subtitles(scenes, sub_dir, video_w, font_path):
    """为每段生成字幕PNG透明图"""
    print("\n" + "=" * 60)
    print("Step 2: 生成字幕叠加层")
    print("=" * 60)

    if not font_path:
        print("  ⚠️  未找到中文字体，跳过字幕生成")
        return

    font_main = ImageFont.truetype(font_path, 42)

    for scene in scenes:
        sid = scene["id"]
        text = scene["narration"]
        title = scene.get("title", f"镜头{sid}")
        out_file = sub_dir / f"subtitle_{sid:02d}.png"

        if out_file.exists():
            continue

        print(f"  📝 [{sid:02d}] {title}")

        # 文本换行：超过18字在标点处换行
        lines = []
        current = ""
        for char in text:
            current += char
            if len(current) >= 18 and char in "，。！？、；：":
                lines.append(current)
                current = ""
        if current:
            lines.append(current)

        if len(lines) > 3:
            lines = lines[:3]

        line_height = 56
        total_h = line_height * len(lines) + 40
        img = Image.new("RGBA", (video_w, total_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        y = 10
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_main)
            text_w = bbox[2] - bbox[0]
            x = (video_w - text_w) // 2

            # 黑色描边（8方向）
            for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2),(-2,2),(2,-2)]:
                draw.text((x+dx, y+dy), line, fill=(0,0,0,220), font=font_main)
            # 白色主文字
            draw.text((x, y), line, fill=(255,255,255,255), font=font_main)
            y += line_height

        img.save(str(out_file))

    print(f"  ✅ 全部{len(scenes)}段字幕生成完成")


# ===== Step 3: 逐段合成 =====
def compose_segments(scenes, video_dir, audio_dir, sub_dir, out_dir,
                     video_w, video_h, seg_dur, ffmpeg_path, ffprobe_path):
    """将每段视频与TTS音频和字幕合成"""
    print("\n" + "=" * 60)
    print("Step 3: 逐段合成（视频+旁白+字幕）")
    print("=" * 60)

    seg_files = []
    for scene in scenes:
        sid = scene["id"]
        title = scene.get("title", f"镜头{sid}")
        video_file = video_dir / f"{sid:02d}-{title}.mp4"
        audio_file = audio_dir / f"narration_{sid:02d}.mp3"
        sub_file = sub_dir / f"subtitle_{sid:02d}.png"
        out_file = out_dir / f"seg_{sid:02d}.mp4"

        if not video_file.exists():
            # 尝试不带title的文件名
            for f in video_dir.glob(f"{sid:02d}-*.mp4"):
                video_file = f
                break

        if not video_file.exists():
            print(f"  ❌ [{sid:02d}] 视频不存在: {video_file}")
            continue

        seg_files.append(str(out_file))
        if out_file.exists():
            print(f"  ✅ [{sid:02d}] {title} — 已存在")
            continue

        print(f"  🎬 [{sid:02d}] {title} — 合成中...")

        tts_dur = get_duration(audio_file, ffprobe_path) if audio_file.exists() else seg_dur
        target_dur = min(tts_dur + 0.5, seg_dur)

        # 构建FFmpeg命令（带字幕）
        cmd = [
            ffmpeg_path, "-y",
            "-i", str(video_file),
            "-i", str(audio_file),
        ]
        if sub_file.exists():
            cmd.extend(["-i", str(sub_file)])

        filters = f"[0:v]trim=duration={target_dur},setpts=PTS-STARTPTS,scale={video_w}:{video_h}[vbase]"
        if sub_file.exists():
            filters += f";[vbase][2:v]overlay=0:H-h-40:format=auto[vout]"
            cmd.extend([
                "-filter_complex", filters,
                "-map", "[vout]",
            ])
        else:
            cmd.extend([
                "-filter_complex", filters,
                "-map", "[vbase]",
            ])

        cmd.extend([
            "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
            "-shortest",
            str(out_file)
        ])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # 降级：不带字幕
            cmd2 = [
                ffmpeg_path, "-y",
                "-i", str(video_file),
                "-i", str(audio_file),
                "-t", str(target_dur),
                "-c:v", "libx264", "-preset", "fast", "-crf", "22",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k",
                "-shortest",
                str(out_file)
            ]
            result2 = subprocess.run(cmd2, capture_output=True, text=True)
            if result2.returncode != 0:
                print(f"     ❌ 合成失败: {result2.stderr[-200:]}")
                continue

        dur = get_duration(out_file, ffprobe_path)
        print(f"     ✅ 合成完成 ({dur:.1f}s)")

    return seg_files


# ===== Step 4: 背景音乐 =====
def generate_bgm(total_duration, audio_dir, ffmpeg_path):
    """用FFmpeg生成柔和背景音乐（C+E+G三和弦）"""
    print("\n" + "=" * 60)
    print("Step 4: 生成背景音乐")
    print("=" * 60)

    bgm_file = audio_dir / "bgm.mp3"
    if bgm_file.exists():
        print(f"  ✅ 背景音乐已存在")
        return str(bgm_file)

    dur = int(total_duration) + 5
    print(f"  🎵 生成{dur}秒柔和背景音乐...")

    cmd = [
        ffmpeg_path, "-y",
        "-f", "lavfi", "-i",
        f"sine=frequency=261.63:duration={dur},volume=0.15,afade=t=in:st=0:d=3,afade=t=out:st={dur-5}:d=5",
        "-f", "lavfi", "-i",
        f"sine=frequency=329.63:duration={dur},volume=0.10,afade=t=in:st=0:d=4,afade=t=out:st={dur-5}:d=5",
        "-f", "lavfi", "-i",
        f"sine=frequency=392.00:duration={dur},volume=0.08,afade=t=in:st=0:d=5,afade=t=out:st={dur-5}:d=5",
        "-filter_complex",
        "[0:a][1:a][2:a]amix=inputs=3:duration=longest:normalize=0,lowpass=f=800,aresample=44100[a]",
        "-map", "[a]",
        "-c:a", "mp3", "-b:a", "128k",
        str(bgm_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ 背景音乐生成失败: {result.stderr[-200:]}")
        return None

    print(f"  ✅ 背景音乐生成完成")
    return str(bgm_file)


# ===== Step 5: 最终合成 =====
def final_compose(seg_files, bgm_file, out_dir, output_file, bgm_volume,
                  ffmpeg_path, ffprobe_path):
    """拼接所有片段，混入背景音乐"""
    print("\n" + "=" * 60)
    print("Step 5: 最终合成（拼接+背景音乐）")
    print("=" * 60)

    # 拼接
    concat_list = out_dir / "concat_list.txt"
    with open(concat_list, "w") as f:
        for seg in seg_files:
            f.write(f"file '{seg}'\n")

    video_concat = out_dir / "video_concat.mp4"
    print("  📦 拼接视频片段...")
    cmd = [ffmpeg_path, "-y", "-f", "concat", "-safe", "0",
           "-i", str(concat_list), "-c", "copy", str(video_concat)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("  ⚠️ copy模式失败，重编码...")
        cmd = [ffmpeg_path, "-y", "-f", "concat", "-safe", "0",
               "-i", str(concat_list),
               "-c:v", "libx264", "-preset", "fast", "-crf", "22",
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
               str(video_concat)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ❌ 拼接失败: {result.stderr[-300:]}")
            return None

    total_dur = get_duration(video_concat, ffprobe_path)
    print(f"  ✅ 视频拼接完成 ({total_dur:.1f}s)")

    # 混入BGM
    final_file = Path(output_file)
    print(f"  🎵 混入背景音乐（音量{bgm_volume}）...")

    if bgm_file:
        cmd = [
            ffmpeg_path, "-y",
            "-i", str(video_concat),
            "-i", str(bgm_file),
            "-filter_complex",
            f"[1:a]volume={bgm_volume}[bgm];"
            f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            str(final_file)
        ]
    else:
        cmd = [ffmpeg_path, "-y", "-i", str(video_concat), "-c", "copy", str(final_file)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        cmd = [ffmpeg_path, "-y", "-i", str(video_concat),
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(final_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ❌ 最终合成失败: {result.stderr[-300:]}")
            return None

    final_dur = get_duration(final_file, ffprobe_path)
    final_size = os.path.getsize(final_file) / (1024 * 1024)
    print(f"  ✅ 最终合成完成！")
    print(f"     时长: {final_dur:.1f}s ({final_dur/60:.1f}分钟)")
    print(f"     大小: {final_size:.1f} MB")
    print(f"     文件: {final_file}")
    return str(final_file)


# ===== 主流程 =====
async def main():
    args = parse_args()

    base = Path(args.base)
    video_dir = base / "videos"
    audio_dir = base / "audio"
    sub_dir = base / "subtitles"
    out_dir = base / "output"

    for d in [audio_dir, sub_dir, out_dir]:
        d.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = find_ffmpeg()
    ffprobe_path = find_ffprobe()
    font_path = find_font()

    print(f"\n🎬 AI短剧旁白+字幕+背景音乐合成")
    print(f"   项目目录: {base}")
    print(f"   视频目录: {video_dir}")
    print(f"   FFmpeg: {ffmpeg_path}")
    print(f"   字体: {font_path or '未找到'}")

    with open(args.storyboard, "r", encoding="utf-8") as f:
        scenes = json.load(f)
    print(f"   镜头数: {len(scenes)}")

    # Step 1: TTS
    tts_durations = await generate_tts(
        scenes, audio_dir, args.voice, args.rate, args.segment_dur, ffprobe_path)

    # Step 2: 字幕
    generate_subtitles(scenes, sub_dir, args.video_w, font_path)

    # Step 3: 逐段合成
    seg_files = compose_segments(
        scenes, video_dir, audio_dir, sub_dir, out_dir,
        args.video_w, args.video_h, args.segment_dur, ffmpeg_path, ffprobe_path)

    if not seg_files:
        print("\n❌ 没有可合成的片段！")
        return

    # Step 4: 背景音乐
    total_dur = len(seg_files) * args.segment_dur
    bgm_file = generate_bgm(total_dur, audio_dir, ffmpeg_path)

    # Step 5: 最终合成
    final = final_compose(seg_files, bgm_file, out_dir, args.output,
                          args.bgm_volume, ffmpeg_path, ffprobe_path)

    if final:
        print(f"\n🎉 全部完成！最终文件: {final}")


if __name__ == "__main__":
    asyncio.run(main())
