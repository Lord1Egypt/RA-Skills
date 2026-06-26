#!/usr/bin/env python3
"""
audio_frames.py — 测量各段音频时长，并算出 F[] 帧边界数组
==============================================================

替代手工 ffprobe + python -c 那一长串，输出可以直接复制到 src/Scene.tsx。

两个子命令：

  1) measure  测 audio/ 下每段 m4a 的秒数，给出总时长
                用法：python3 audio_frames.py measure
                输出：每段时长 + 总时长（人类可读）+ JSON

  2) frames   从 measure 的结果（或你指定的 durations 列表）算出 F[] 数组
                用法：python3 audio_frames.py frames --total 5367
                或：  python3 audio_frames.py frames --durations 11.4,18.5,19.2 ...
                输出：F[] 数组（JS 数组字面量，可直接粘贴到 Scene.tsx）
                      + src/index.tsx 的 DURATION_IN_FRAMES 值

完整例子：换 voice 后重做音频
  1) 改 generate_audio.py 的 VOICE，重生
  2) python3 audio_frames.py measure
     → 输出每段秒数和总时长
  3) python3 audio_frames.py frames --total <视频帧数>
     或：如果你也要重新渲染视频：
        python3 audio_frames.py frames --total <新视频总帧数>
  4) 把输出的 F[] 粘到 src/Scene.tsx，把 DURATION_IN_FRAMES 粘到 src/index.tsx
  5) 重渲染 + 合并

模板版本：v1.0.3
"""
import argparse, json, os, subprocess, sys


def measure(audio_dir: str = "audio") -> list:
    """测 audio/ 下每段 m4a 的时长。返回 list[dict] 排序好的列表。

    自动过滤掉非场景文件：combined*.m4a、file_list.txt 等。
    判断标准：文件名不以下列前缀/全名开头/匹配：
      - 不含 "combined"（拼后的整段）
      - 不含 "_combined"（任何变体）
    """
    if not os.path.isdir(audio_dir):
        sys.exit(f"❌ 目录不存在: {audio_dir}")

    SKIP_SUBSTRINGS = ("combined", "concat", "full", "merged")
    files = sorted([
        f for f in os.listdir(audio_dir)
        if f.endswith(".m4a") and not any(s in f for s in SKIP_SUBSTRINGS)
    ])
    if not files:
        sys.exit(f"❌ {audio_dir}/ 下没有场景 m4a 文件（combined/concat/full/merged 都被过滤了）")

    out = []
    for fname in files:
        path = os.path.join(audio_dir, fname)
        try:
            dur = float(subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", path]
            ).decode().strip())
        except Exception as e:
            sys.exit(f"❌ ffprobe 失败: {fname}: {e}")
        out.append({"scene_id": fname[:-4], "file": fname, "duration_s": round(dur, 3)})

    return out


def calc_F(durations: list, total_frames: int) -> list:
    """从各段时长算 F[] 数组。"""
    if len(durations) < 1:
        sys.exit("❌ durations 不能为空")
    if total_frames < len(durations) + 1:
        sys.exit(f"❌ total_frames={total_frames} 太少（场景数 {len(durations)}）")

    total_s = sum(durations)
    F = [0]
    cum = 0.0
    for d in durations[:-1]:
        cum += d
        F.append(round(cum / total_s * total_frames))
    # 最后一个值兜底（不要让它等于 total_frames，否则 EndScene 出不来）
    F.append(total_frames - 10)
    return F


def cmd_measure(args):
    rows = measure(args.audio_dir)
    total = sum(r["duration_s"] for r in rows)

    print(f"📊 各段音频时长 ({len(rows)} 段)")
    print(f"{'scene_id':25s}  {'file':30s}  {'duration':>9s}")
    print("-" * 70)
    for r in rows:
        print(f"  {r['scene_id']:23s}  {r['file']:30s}  {r['duration_s']:>7.2f}s")
    print("-" * 70)
    print(f"  {'TOTAL':23s}  {'':30s}  {total:>7.2f}s  ({total/60:.2f} min)")
    print()

    # 复制粘贴用
    print("📋 复制粘贴（用于 frames --durations）：")
    durs = ",".join(f"{r['duration_s']}" for r in rows)
    print(f"  --durations {durs}")
    print()

    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump({"total_s": total, "scenes": rows}, f, indent=2, ensure_ascii=False)
        print(f"💾 写到 {args.json_out}")


def cmd_frames(args):
    if args.durations:
        durations = [float(x.strip()) for x in args.durations.split(",")]
    elif args.from_measure:
        # 从之前 measure --json-out 的输出读
        with open(args.from_measure) as f:
            data = json.load(f)
        durations = [s["duration_s"] for s in data["scenes"]]
        if not args.total:
            # 默认按 fps=30 算
            args.total = round(data["total_s"] * 30)
            print(f"ℹ️  --total 没指定，按 fps=30 × {data['total_s']:.2f}s = {args.total} 帧")
    else:
        sys.exit("❌ 必须指定 --durations 或 --from-measure")

    F = calc_F(durations, args.total)
    total_s = sum(durations)

    print(f"📐 帧边界（{len(durations)} 段 → {args.total} 帧 = {args.total/30:.2f}s）")
    print(f"   总音频: {total_s:.2f}s (视频: {args.total/30:.2f}s, 漂移 {(total_s - args.total/30)*1000:+.0f}ms)")
    print()
    print("📋 复制粘贴到 src/Scene.tsx 的 F[]：")
    print(f"  const F = {F};")
    print()
    print("📋 复制粘贴到 src/index.tsx 的 DURATION_IN_FRAMES：")
    print(f"  const DURATION_IN_FRAMES = {args.total};")
    print()
    print("💡 各段帧数（参考）：")
    cum = 0
    for i, d in enumerate(durations):
        n = F[i+1] - F[i] if i+1 < len(F) else args.total - F[i]
        print(f"   {i:02d}: {d:6.2f}s × 30fps = {d*30:6.1f}帧 (F[{i+1}] - F[{i}] = {n} 帧)")
    print()
    if abs(total_s - args.total/30) > 0.2:
        print(f"⚠️  音视频时长差 {abs(total_s - args.total/30):.2f}s 较大，建议：")
        print(f"   - 如果是边缘情况，Remotion 重渲染后用 ffprobe 确认实际帧数，再跑一次 frames")
        print(f"   - 或调 atempo 让音频总时长 ≈ {args.total/30:.2f}s")


def main():
    p = argparse.ArgumentParser(description="音频时长测量 + F[] 帧边界计算")
    sub = p.add_subparsers(dest="cmd", required=True)

    pm = sub.add_parser("measure", help="测 audio/ 下每段 m4a 的时长")
    pm.add_argument("--audio-dir", default="audio", help="音频目录（默认 audio/）")
    pm.add_argument("--json-out", help="同时写 JSON 快照（供 frames --from-measure 用）")
    pm.set_defaults(func=cmd_measure)

    pf = sub.add_parser("frames", help="从时长列表算 F[] 数组")
    pf.add_argument("--durations", help="逗号分隔的秒数列表，例如 11.4,18.5,19.2")
    pf.add_argument("--from-measure", help="measure --json-out 产出的 JSON 文件路径")
    pf.add_argument("--total", type=int, help="目标总帧数（例如第一遍渲染后用 ffprobe 得到的 nb_frames）")
    pf.add_argument("--fps", type=int, default=30, help="帧率（默认 30）")
    pf.set_defaults(func=cmd_frames)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
