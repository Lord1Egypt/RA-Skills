#!/usr/bin/env python3
"""Cut Video — 按时间轴剪切视频 (v2: 支持 EDL JSON 输入)"""
import argparse, os, subprocess, sys, shutil, json

def cut_single(input_file: str, start: float, duration: float, output: str) -> bool:
    """使用 FFmpeg 无损剪切一段视频。"""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", input_file,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac",
        "-avoid_negative_ts", "make_zero",
        output
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def cut_segments(input_file: str, segments: list, output_dir: str) -> list:
    """按多段列表剪切视频。"""
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(input_file))[0]
    results = []
    for i, (start, end) in enumerate(segments):
        duration = end - start
        out = os.path.join(output_dir, f"{base}_clip{i+1}.mp4")
        ok = cut_single(input_file, start, duration, out)
        results.append((out, ok))
        print(f"  片段{i+1}: {start}s-{end}s -> {out} [{'OK' if ok else 'FAIL'}]")
    return results

def parse_segments(seg_str: str) -> list:
    """解析 '0-30,60-90,120-150' 格式。"""
    result = []
    for part in seg_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            result.append((float(start.strip()), float(end.strip())))
    return result

def cut_from_edl(input_file: str, edl_path: str, output_dir: str) -> list:
    """从 EDL JSON 文件读取剪切指令并执行。"""
    with open(edl_path, "r", encoding="utf-8") as f:
        edl = json.load(f)

    segs = []
    for edit in edl.get("edits", []):
        if edit.get("type") == "keep":
            segs.append((edit["start"], edit["end"]))

    if not segs:
        print("EDL 中没有 keep 指令", file=sys.stderr)
        return []

    return cut_segments(input_file, segs, output_dir)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="视频剪切工具 (v2)")
    p.add_argument("--input", required=True, help="输入视频文件")
    p.add_argument("--start", type=float, default=None, help="开始时间（秒）")
    p.add_argument("--duration", type=float, default=None, help="持续时间（秒）")
    p.add_argument("--segments", default="", help="多段格式: 0-30,60-90,120-150")
    p.add_argument("--edl", default="", help="EDL JSON 文件路径 (v2 新增)")
    p.add_argument("--output", required=True, help="输出文件或目录")
    args = p.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("ffmpeg"):
        print("错误: ffmpeg 未安装", file=sys.stderr)
        sys.exit(1)

    # EDL 模式
    if args.edl:
        if not os.path.exists(args.edl):
            print(f"错误: EDL 文件不存在: {args.edl}", file=sys.stderr)
            sys.exit(1)
        print(f"从 EDL 文件剪切: {args.edl}")
        results = cut_from_edl(args.input, args.edl, args.output)
        ok = all(r[1] for r in results)
        print(f"\n完成: {sum(r[1] for r in results)}/{len(results)} 成功")
        sys.exit(0 if ok else 1)

    if args.segments:
        segs = parse_segments(args.segments)
        print(f"将视频切分为 {len(segs)} 段...")
        results = cut_segments(args.input, segs, args.output)
        ok = all(r[1] for r in results)
        print(f"\n完成: {sum(r[1] for r in results)}/{len(results)} 成功")
        sys.exit(0 if ok else 1)
    else:
        if args.start is None or args.duration is None:
            print("错误: 需要指定 --start 和 --duration，或使用 --segments 或 --edl", file=sys.stderr)
            sys.exit(1)
        print(f"剪切: {args.start}s + {args.duration}s -> {args.output}")
        ok = cut_single(args.input, args.start, args.duration, args.output)
        print(f"结果: {'成功' if ok else '失败'}")
        sys.exit(0 if ok else 1)
