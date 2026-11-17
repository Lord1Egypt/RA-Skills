#!/usr/bin/env python3
"""Burn Subtitles — SRT字幕烧录到视频 (v2: 支持风格预设)"""
import argparse, os, subprocess, shutil, sys, json

def load_style_preset(style_name: str, style_file: str = None) -> dict:
    """加载字幕风格预设。"""
    default_styles = {
        "default": {"font": "Arial", "size": 20, "color": "FFFFFF", "outline": 1, "margin_v": 50},
        "netflix": {"font": "Arial", "size": 16, "color": "FFFFFF", "outline": 2, "margin_v": 60},
        "douyin": {"font": "PingFang SC", "size": 24, "color": "FFFFFF", "outline": 2, "margin_v": 80},
        "bilibili": {"font": "PingFang SC", "size": 18, "color": "FFFFFF", "outline": 1, "margin_v": 40},
        "youtube": {"font": "Roboto", "size": 18, "color": "FFFFFF", "outline": 1, "margin_v": 50},
        "minimal": {"font": "Helvetica", "size": 14, "color": "FFFFFF", "outline": 0, "margin_v": 30},
    }
    if style_name in default_styles:
        return default_styles[style_name]

    # 尝试从文件加载
    if style_file and os.path.exists(style_file):
        with open(style_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            styles = data.get("styles", {})
            if style_name in styles:
                s = styles[style_name]
                return {
                    "font": s.get("font", "Arial"),
                    "size": s.get("size", 20),
                    "color": s.get("color", "FFFFFF").replace("#", ""),
                    "outline": s.get("outline", 1),
                    "margin_v": s.get("margin_v", 50),
                }
    return default_styles["default"]


def burn_subtitles(input_file: str, srt_file: str, output: str,
                   font: str = "Arial", size: int = 24, color: str = "white",
                   outline: int = 1, margin_v: int = 50) -> bool:
    """使用 FFmpeg 将 SRT 字幕烧录到视频。"""
    if not os.path.exists(srt_file):
        print(f"错误: 字幕文件不存在: {srt_file}", file=sys.stderr)
        return False

    # 检查字幕编码
    try:
        with open(srt_file, "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError:
        # 尝试 GBK
        tmp = srt_file + ".utf8.srt"
        with open(srt_file, "r", encoding="gbk", errors="ignore") as src:
            content = src.read()
        with open(tmp, "w", encoding="utf-8") as dst:
            dst.write(content)
        srt_file = tmp

    # 构建 force_style
    style_parts = [
        f"FontName={font}",
        f"FontSize={size}",
        f"PrimaryColour=&H{color}&",
        f"Outline={outline}",
        f"Alignment=2",
        f"MarginV={margin_v}",
    ]
    force_style = ",".join(style_parts)

    filter_str = f"subtitles='{srt_file}':force_style='{force_style}'"
    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-vf", filter_str,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac",
        output
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and "Unable to parse option" in result.stderr:
        # fallback: 简化滤镜
        cmd = [
            "ffmpeg", "-y",
            "-i", input_file,
            "-vf", f"subtitles='{srt_file}'",
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac",
            output
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="烧录字幕到视频 (v2: 风格预设)")
    p.add_argument("--input", required=True, help="输入视频")
    p.add_argument("--srt", required=True, help="SRT字幕文件")
    p.add_argument("--output", required=True, help="输出视频")
    p.add_argument("--font", default="Arial", help="字体")
    p.add_argument("--size", type=int, default=None, help="字号 (覆盖风格预设)")
    p.add_argument("--color", default=None, help="颜色(white/yellow/cyan)")
    p.add_argument("--style", default="default",
                   choices=["default", "netflix", "douyin", "bilibili", "youtube", "minimal"],
                   help="字幕风格预设")
    p.add_argument("--style-file", default=None, help="自定义风格 JSON 文件")
    args = p.parse_args()

    import shutil as _sh
    if not _sh.which("ffmpeg"):
        print("错误: ffmpeg 未安装", file=sys.stderr)
        sys.exit(1)

    # 加载风格预设
    style = load_style_preset(args.style, args.style_file)
    font = args.font if args.font != "Arial" else style.get("font", "Arial")
    size = args.size if args.size else style.get("size", 20)
    color = args.color if args.color else style.get("color", "FFFFFF")
    outline = style.get("outline", 1)
    margin_v = style.get("margin_v", 50)

    print(f"字幕风格: {args.style} (font={font}, size={size}, outline={outline})")
    ok = burn_subtitles(args.input, args.srt, args.output,
                         font, size, color, outline, margin_v)
    print(f"结果: {'成功' if ok else '失败'}")
    if not ok:
        print("错误信息:", file=sys.stderr)
        sys.exit(1)
