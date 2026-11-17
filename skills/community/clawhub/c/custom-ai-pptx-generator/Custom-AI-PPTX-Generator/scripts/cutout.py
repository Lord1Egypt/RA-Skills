"""Chroma-key the generated assets: remove flat green bg, kill the corner watermark, trim, export RGBA PNG."""
import os, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# Input/output dirs: override with env vars CUTOUT_IN / CUTOUT_OUT.
# Defaults are relative to this script; existing outputs are never overwritten
# (auto version bump via safe_save_path below).
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CUTOUT_IN", os.path.join(_SCRIPT_DIR, "assets"))
OUT = os.environ.get("CUTOUT_OUT", os.path.join(_SCRIPT_DIR, "output", "assets_clean"))
NAMES = ["hero", "flow", "sched", "clock", "trophy", "gear", "calcheck", "magnifier", "share", "robot"]
os.makedirs(OUT, exist_ok=True)


def safe_save_path(path):
    """Return a non-existing path: bump _v2/_v3... suffix instead of overwriting."""
    base, ext = os.path.splitext(path)
    cand, n = path, 1
    while os.path.exists(cand):
        n += 1
        cand = "%s_v%d%s" % (base, n, ext)
    return cand


def bg_color(a):
    k = 24
    c = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3),
                        a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    return np.median(c, axis=0)


def dilate(m, it=1):
    for _ in range(it):
        d = m.copy()
        d[1:, :] |= m[:-1, :]; d[:-1, :] |= m[1:, :]
        d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
        m = d
    return m


def process(name):
    f = sorted(glob.glob(os.path.join(ROOT, name, "*.png")))[0]
    a = np.asarray(Image.open(f).convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    bg = bg_color(a)

    dist = np.sqrt(((a - bg) ** 2).sum(-1))
    mx = a.max(-1); mn = a.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1e-6)

    # The chroma-key plane is one flat colour, including inside enclosed holes
    # (a gear's centre, the gap between three connected nodes). A tight colour match
    # removes all of it while leaving genuinely different artwork greens intact.
    alpha_full = np.clip((dist - 14.0) / 26.0, 0, 1)
    alpha = alpha_full.copy()

    # watermark: the generator stamps "AI生成 WORKBUDDY" into the bottom-right corner.
    # wipe that whole corner except for pixels that look like solid, saturated artwork.
    ys, xs = np.nonzero(np.ones((h, w), bool))
    corner = np.zeros((h, w), bool)
    corner[int(h * 0.84):, int(w * 0.74):] = True
    solid = (alpha_full > 0.92) & (sat > 0.55)
    wiped = int((corner & ~solid).sum())
    alpha = np.where(corner & ~solid, 0.0, alpha)

    # kill the green fringe: repaint the anti-aliased boundary ring with the nearest
    # solid artwork colour (4-neighbour colour diffusion) so compositing stays clean.
    core = alpha > 0.5
    if core.any():
        filled = core.copy()
        col = a.copy()
        for _ in range(6):
            ring = dilate(filled, 1) & ~filled
            if not ring.any():
                break
            cnt = np.zeros((h, w), np.float32)
            acc = np.zeros((h, w, 3), np.float32)
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                sh_f = np.roll(filled, (dy, dx), (0, 1)).astype(np.float32)
                sh_c = np.roll(col, (dy, dx), (0, 1))
                cnt += sh_f
                acc += sh_c * sh_f[..., None]
            m = ring & (cnt > 0)
            if not m.any():
                break
            col[m] = acc[m] / cnt[m][:, None]
            filled |= m
        a = col
    alpha = np.where(alpha < 0.10, 0.0, alpha)

    # remove tiny floating specks
    m = alpha > 0.35
    for _ in range(2):
        keep = dilate(m, 1)
        m = keep & (np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))).astype(np.float32) > 0)
    alpha = np.where(m | (alpha > 0.995), alpha, 0.0)

    rgba = Image.fromarray(np.dstack([np.clip(a, 0, 255).astype(np.uint8), (alpha * 255).astype(np.uint8)]), "RGBA")
    bbox = rgba.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    rgba.save(os.path.join(OUT, name + ".png"))

    # residual watermark check in the very corner of the trimmed image
    chk = np.asarray(rgba.getchannel("A")).astype(np.float32) / 255.0
    ch, cw = chk.shape
    corner = chk[int(ch * 0.86):, int(cw * 0.70):]
    print(f"{name:11s} {str((w, h)):12s} bg={tuple(int(v) for v in bg)} wiped={wiped} "
          f"-> {rgba.size} cornerMaxAlpha={corner.max():.3f}")


for n in NAMES:
    process(n)

# verification sheet on the slide background purple
tiles = [(n, Image.open(os.path.join(OUT, n + ".png")).convert("RGBA")) for n in NAMES]
CW, CH, cols = 340, 270, 5
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (CW * cols, CH * rows), (76, 60, 176))
d = ImageDraw.Draw(sheet)
for i, (n, im) in enumerate(tiles):
    t = im.copy(); t.thumbnail((CW - 24, CH - 46), Image.LANCZOS)
    x = (i % cols) * CW + 12; y = (i // cols) * CH + 36
    sheet.paste(t, (x, y), t)
    d.text((x, y - 24), f"{n} {im.size[0]}x{im.size[1]}", fill=(255, 255, 120))
p = safe_save_path(os.path.join(_SCRIPT_DIR, "output", "crops", "sheet_clean.png"))
os.makedirs(os.path.dirname(p), exist_ok=True)
sheet.save(p)
print("saved", p, sheet.size)
