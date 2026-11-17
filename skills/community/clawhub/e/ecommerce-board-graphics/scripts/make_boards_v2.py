# -*- coding: utf-8 -*-
"""v2 boards: INNER border (image fills canvas, gold frame overlays edge, no white margin)
   - portrait image -> portrait canvas 1052x1494, vertical border
   - landscape image -> landscape canvas 1494x1052, border rotated 90 deg
   - image stretched to fill entire canvas (slight deformation ok)
   参数化版: python make_boards_v2.py [ROOT] [OUT] [BORDER]
"""
import os, re, sys
from PIL import Image

BORDER = sys.argv[3] if len(sys.argv) > 3 else r"D:\UserFolders\Desktop\包边.png"
ROOT = sys.argv[1] if len(sys.argv) > 1 else r"D:\UserFolders\Desktop\ff卡\新批次\A5尺寸（129张）\普卡荧光（104张）"
OUT = sys.argv[2] if len(sys.argv) > 2 else r"D:\UserFolders\Desktop\workspace\A5包边板子\v2"
os.makedirs(OUT, exist_ok=True)

def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

def make_board(png_path, border_path, out_path, portrait=(1052, 1494), landscape=(1494, 1052)):
    """单张板子: 内包边, 横竖自适应。返回 (是否横版, 输出路径)"""
    img = Image.open(png_path).convert("RGBA")
    iw, ih = img.size
    border = Image.open(border_path).convert("RGBA")
    if iw > ih:
        W, H = landscape
        frame = border.rotate(90, expand=True)
    else:
        W, H = portrait
        frame = border
    img = img.resize((W, H), Image.LANCZOS)
    frame = frame.resize((W, H), Image.LANCZOS)
    board = img.copy()
    board.paste(frame, (0, 0), frame)
    board.convert("RGB").save(out_path)
    return iw > ih, out_path

if __name__ == "__main__":
    subs = [d for d in sorted(os.listdir(ROOT)) if os.path.isdir(os.path.join(ROOT, d))]
    border = Image.open(BORDER).convert("RGBA")
    border_rot = border.rotate(90, expand=True)
    for i, s in enumerate(subs, 1):
        d = os.path.join(ROOT, s)
        pngs = sorted([f for f in os.listdir(d) if f.lower().endswith(".png")], key=natkey)
        if not pngs:
            print("skip", s); continue
        p = os.path.join(d, pngs[0])
        img = Image.open(p).convert("RGBA")
        iw, ih = img.size
        if iw > ih:
            W, H = 1494, 1052
            frame = border_rot
        else:
            W, H = 1052, 1494
            frame = border
        img = img.resize((W, H), Image.LANCZOS)
        board = img.copy()
        board.paste(frame, (0, 0), frame)
        name = s.replace("（", "(").replace("）", ")")
        out = os.path.join(OUT, "A5板子%02d_%s.png" % (i, name))
        board.convert("RGB").save(out)
        print("生成 %s  %dx%d -> %dx%d %s" % (os.path.basename(out), iw, ih, W, H, "横" if iw > ih else "竖"))
    print("done ->", OUT)
