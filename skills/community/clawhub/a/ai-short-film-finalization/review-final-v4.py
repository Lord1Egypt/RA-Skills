#!/usr/bin/env python3
"""
导演级审查包生成器 v4
- 从最终成片中按镜头提取独立 clip / audio / frame
- 生成自包含 review.html（数据内联，无需服务器）
- 每镜头分画面/音频/字幕三部分独立审查
- 支持导演增删镜头、输入修改意见、导出可执行修改包
"""

import argparse
import json
import subprocess
import shutil
from pathlib import Path

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

HOOK_DUR = 2.5
CTA_DUR = 4.0


def get_duration(path):
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True
    )
    try:
        return float(r.stdout.strip())
    except (ValueError, IndexError):
        return 0.0


def pad2(n):
    return f"{n:02d}"


def build_manifest(project_root, final_video, output_dir):
    """构建审查 manifest，提取 clip/audio/frame。"""
    storyboard = project_root / "storyboard-v2.json"
    scenes = json.loads(storyboard.read_text(encoding="utf-8"))

    seg_dir = project_root / "final"
    clips_dir = output_dir / "clips"
    audio_dir = output_dir / "audio"
    frames_dir = output_dir / "frames"
    for d in [clips_dir, audio_dir, frames_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # 计算每镜头在最终成片中的时间戳
    cursor = HOOK_DUR  # hook 占用前 2.5s
    manifest = []

    for scene in scenes:
        sid = scene["id"]
        title = scene.get("title", f"镜头{sid}")
        seg_file = seg_dir / f"seg_{pad2(sid)}.mp4"

        if not seg_file.exists():
            print(f"  ⚠️ [{pad2(sid)}] {title} — 分段文件缺失，跳过")
            continue

        seg_dur = get_duration(seg_file)
        start_ts = cursor
        end_ts = cursor + seg_dur

        # 提取独立 clip
        clip_name = f"{pad2(sid)}-{title}.mp4"
        clip_path = clips_dir / clip_name
        if not clip_path.exists() or True:  # 总是重新提取
            cmd = [
                FFMPEG, "-y", "-ss", f"{start_ts:.3f}", "-t", f"{seg_dur:.3f}",
                "-i", str(final_video),
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                str(clip_path)
            ]
            subprocess.run(cmd, capture_output=True, text=True)

        # 提取独立 audio
        audio_name = f"{pad2(sid)}-{title}.mp3"
        audio_path = audio_dir / audio_name
        if not audio_path.exists() or True:
            cmd = [
                FFMPEG, "-y", "-ss", f"{start_ts:.3f}", "-t", f"{seg_dur:.3f}",
                "-i", str(final_video),
                "-vn", "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100",
                str(audio_path)
            ]
            subprocess.run(cmd, capture_output=True, text=True)

        # 提取中间帧
        frame_name = f"{pad2(sid)}-{title}.jpg"
        frame_path = frames_dir / frame_name
        mid_ts = start_ts + seg_dur / 2
        if not frame_path.exists() or True:
            cmd = [
                FFMPEG, "-y", "-ss", f"{mid_ts:.3f}",
                "-i", str(final_video),
                "-vframes", "1", "-q:v", "2",
                str(frame_path)
            ]
            subprocess.run(cmd, capture_output=True, text=True)

        entry = {
            "uid": f"shot-{sid}",
            "id": sid,
            "title": title,
            "is_new": False,
            "start_ts": round(start_ts, 2),
            "end_ts": round(end_ts, 2),
            "duration": round(seg_dur, 2),
            "era": scene.get("era", ""),
            "mood": scene.get("mood", ""),
            "shot_type": scene.get("shot_type", ""),
            "narration": scene.get("narration", ""),
            "subtitle_text": scene.get("narration", "").replace("，", "\n").replace("。", "\n").strip(),
            "prompt": scene.get("prompt", ""),
            "clip_path": f"clips/{clip_name}",
            "audio_path": f"audio/{audio_name}",
            "frame_path": f"frames/{frame_name}",
            "comp_status": {
                "video": "review",
                "audio": "review",
                "subtitle": "review"
            },
            "fix": {}
        }
        manifest.append(entry)
        cursor = end_ts
        print(f"  ✅ [{pad2(sid)}] {title} ({seg_dur:.2f}s, {start_ts:.1f}s–{end_ts:.1f}s)")

    return manifest


def generate_html(manifest, project_name, template_path, output_path):
    """读取模板 HTML，替换占位符，输出自包含审查页面。"""
    html = Path(template_path).read_text(encoding="utf-8")
    manifest_json = json.dumps(manifest, ensure_ascii=False, indent=2)
    html = html.replace("__MANIFEST_DATA__", manifest_json)
    html = html.replace("__PROJECT_NAME__", project_name)
    Path(output_path).write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="生成导演级审查包 v4")
    parser.add_argument("--project-root", default=".", help="项目根目录")
    parser.add_argument("--output", default="review-v4/", help="输出目录")
    parser.add_argument("--template-html", default=None, help="HTML 模板路径")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # 查找最终成片
    final_video = project_root / "final" / "侨女烈魂·李林_导演版_v4.mp4"
    if not final_video.exists():
        # 尝试其他版本
        for name in ["侨女烈魂·李林_导演版_v4.mp4", "侨女烈魂·李林_导演版_v3.mp4"]:
            candidate = project_root / "final" / name
            if candidate.exists():
                final_video = candidate
                break
        else:
            print(f"❌ 找不到最终成片: {final_video}")
            return

    project_name = project_root.name

    # 查找模板
    if args.template_html:
        template_path = Path(args.template_html)
    else:
        # 查找同目录下的模板
        template_path = project_root / "review-director-template.html"
        if not template_path.exists():
            # 查找 skill 目录
            template_path = Path.home() / ".workbuddy" / "skills" / "ai-short-film-finalization" / "ai-short-film-finalization" / "review-director-template.html"

    if not template_path.exists():
        print(f"❌ 找不到 HTML 模板: {template_path}")
        return

    print(f"🎬 生成导演级审查包 v4")
    print(f"   项目: {project_name}")
    print(f"   成片: {final_video}")
    print(f"   输出: {output_dir}")
    print(f"   模板: {template_path}")
    print()

    # 构建 manifest
    manifest = build_manifest(project_root, final_video, output_dir)

    # 生成 HTML
    html_path = output_dir / "review.html"
    generate_html(manifest, project_name, template_path, html_path)

    # 同时保存 manifest.json
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"\n🎉 审查包生成完成！")
    print(f"   审查页面: {html_path}")
    print(f"   Manifest: {manifest_path}")
    print(f"   镜头数: {len(manifest)}")


if __name__ == "__main__":
    main()
