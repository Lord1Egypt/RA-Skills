"""视频号竖屏切片流水线: 切片 -> 横转竖(模糊背景填充) -> 烧中文字幕 -> 竖屏封面

用法:
    python scripts/slice_vertical.py                  # 默认: 裁掉源底部内嵌字幕带 + 烧大字幕
    python scripts/slice_vertical.py --no-crop        # 不裁源(技能原样), 用于对比
    python scripts/slice_vertical.py --tag _v2        # 输出文件名后缀
"""
import json, os, subprocess, sys

FFMPEG = "bin/ffmpeg.exe"
SRC = "download/src.mp4"
OUT_DIR = "output"
TRANSCRIPT = "download/src_transcript.json"

# 源视频底部"内嵌字幕带"高度(像素, 1280x720 基准)。
# 图文轮播/静态幻灯片类源片, 画面下方常自带宽 = 1280 的内嵌字幕;
# 若不裁掉, 外烧字幕就与它重复(一屏两套字幕)。
# 用 scripts/probe_subs_band.py 量出内容带范围后再定这个值。
# 0 = 不裁(技能原样行为)。
DROP_BOTTOM = 120

# 选段由 LLM 根据转写内容填写: (start_sec, end_sec, 标题, 封面金句)
CLIPS = [
    (1080.4, 1177.4, "01数据会撒谎", "统计数据看起来最科学，但它经常撒谎"),
]


def sec_to_srt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def build_clip_srt(segments, start, end, path):
    """截取 [start,end] 区间的字幕, 时间轴偏移到 0, 输出 SRT"""
    lines, idx = [], 1
    for seg in segments:
        s, e, txt = seg["start"], seg["end"], seg["text"]
        if e <= start or s >= end:
            continue
        s2, e2 = max(s, start) - start, min(e, end) - start
        if e2 - s2 <= 0.05:
            continue
        lines += [str(idx), f"{sec_to_srt(s2)} --> {sec_to_srt(e2)}", txt, ""]
        idx += 1
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return idx - 1


def make_vertical(src, srt, out, start=None, end=None, drop_bottom=DROP_BOTTOM):
    """横转竖: (可选)裁掉源内嵌字幕带 + 模糊背景填充 + 源画面居中 + 烧中文字幕"""
    srt_esc = srt.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    # libass 默认 PlayResY=288, 实际像素 = 值*1920/288≈6.67倍:
    # FontSize=12→约80px, MarginV=38→约253px(字幕落在下方模糊区, 不挡源画面)
    style = "FontSize=12,FontName=Microsoft YaHei,PrimaryColour=&H00FFFFFF," \
            "OutlineColour=&H00000000,Outline=2,Alignment=2,MarginV=38,Spacing=1"
    pre = f"crop=iw:ih-{drop_bottom}:0:0," if drop_bottom else ""
    vf = (
        pre +
        "split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,gblur=sigma=28,eq=brightness=-0.06[bgout];"
        "[fg]scale=1080:-2[fgout];"
        f"[bgout][fgout]overlay=(W-w)/2:(H-h)/2,subtitles='{srt_esc}':force_style='{style}'"
    )
    cmd = [FFMPEG, "-y"]
    if start is not None:
        cmd += ["-ss", str(start)]
    if end is not None:
        cmd += ["-to", str(end)]
    cmd += ["-i", src, "-vf", vf,
            "-c:v", "libx264", "-crf", "23", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FFMPEG ERROR:\n", r.stderr[-1500:])
    return r.returncode


def main():
    args = sys.argv[1:]
    tag = ""
    drop = DROP_BOTTOM
    if "--no-crop" in args:
        drop = 0
    if "--tag" in args:
        tag = args[args.index("--tag") + 1]
    os.makedirs(OUT_DIR, exist_ok=True)
    segments = json.load(open(TRANSCRIPT, encoding="utf-8"))
    print(f"loaded {len(segments)} transcript segments | drop_bottom={drop} | tag='{tag}'")
    for i, (start, end, title, quote) in enumerate(CLIPS, 1):
        srt = os.path.join(OUT_DIR, f"clip{i}.srt")
        if os.path.exists(srt):
            # 已存在精转字幕(small模型+术语修正), 直接复用, 不覆盖
            n = open(srt, encoding="utf-8").read().count("-->")
            print(f"[{i}] use refined srt (skip rebuild)")
        else:
            n = build_clip_srt(segments, start, end, srt)
        out = os.path.join(OUT_DIR, f"clip{i}_{title}{tag}.mp4")
        print(f"[{i}] {start}s-{end}s ({end-start:.0f}s) subs={n} -> {out}", flush=True)
        rc = make_vertical(SRC, srt, out, start, end, drop)
        sz = os.path.getsize(out) / 1e6 if os.path.exists(out) else 0
        print(f"    rc={rc} exists={os.path.exists(out)} size={sz:.2f}MB", flush=True)


if __name__ == "__main__":
    main()
