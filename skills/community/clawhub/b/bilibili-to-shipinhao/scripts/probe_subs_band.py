"""探测源视频内嵌字幕带位置: 采样多帧, 找出底部有内容的像素行范围(排除左上角水印)"""
import os, subprocess, sys
from PIL import Image

FFMPEG = "bin/ffmpeg.exe"
SRC = sys.argv[1] if len(sys.argv) > 1 else "download/src.mp4"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 24
TMP = "download/_probe.png"

dur = 1267.0
rows_hit = {}
for k in range(N):
    t = dur * (k + 0.5) / N
    subprocess.run([FFMPEG, "-y", "-ss", f"{t:.1f}", "-i", SRC, "-frames:v", "1",
                    "-q:v", "2", TMP], capture_output=True)
    im = Image.open(TMP).convert("RGB")
    W, H = im.size
    px = im.load()
    # 背景色取中部空白区域采样(row y=0.62H, x 附近左侧)
    bg = px[int(W * 0.05), int(H * 0.62)]
    for y in range(int(H * 0.55), H):
        cnt = 0
        for x in range(W):
            if x < int(W * 0.25) and y < int(H * 0.12):
                continue  # 跳过左上角频道水印
            r, g, b = px[x, y]
            if abs(r - bg[0]) > 28 or abs(g - bg[1]) > 28 or abs(b - bg[2]) > 28:
                cnt += 1
        if cnt > 12:
            rows_hit[y] = rows_hit.get(y, 0) + 1

if rows_hit:
    ys = sorted(rows_hit)
    print(f"帧尺寸 {W}x{H}, 采样 {N} 帧")
    print(f"底部内容行范围(≥2帧命中): {min(ys)} ~ {max(ys)}")
    # 连成段列出
    segs, s = [], ys[0]
    for a, b in zip(ys, ys[1:]):
        if b - a > 3:
            segs.append((s, a)); s = b
    segs.append((s, ys[-1]))
    for s0, s1 in segs:
        hi = max(rows_hit[y] for y in range(s0, s1 + 1) if y in rows_hit)
        print(f"  内容带 y ∈ [{s0}, {s1}]  最多 {hi}/{N} 帧命中")
else:
    print("底部未检测到内容(可能全为空白)")
