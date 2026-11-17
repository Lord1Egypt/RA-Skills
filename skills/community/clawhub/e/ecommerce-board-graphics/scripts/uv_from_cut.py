# -*- coding: utf-8 -*-
"""uv card from PSD cutout: dim png + glow only on cutout pattern"""
import numpy as np
from PIL import Image, ImageFilter
from psd_cutout import cutout_layer

def uv_from_cut(png_path, psd_path):
    png = Image.open(png_path).convert("RGBA")
    cut = cutout_layer(psd_path)
    if cut is None:
        return png.convert("RGB")
    # resize cut to png size
    cut = cut.resize(png.size, Image.LANCZOS)
    cut_rgb = cut.convert("RGB")
    alpha = np.array(cut.split()[3]).astype(np.float32) / 255.0
    arr = np.array(png.convert("RGB")).astype(np.float32)

    # tight glow: small blur, higher threshold -> glow hugs the cutout shape
    glow = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
    glow_arr = np.array(glow).astype(np.float32) / 255.0
    glow_arr = np.clip((glow_arr - 0.2) / 0.8, 0, 1) ** 1.0

    # dim base (lighter than before so bg stays readable)
    dark = arr * 0.5
    # emissive: cutout color boosted toward violet-white
    cut_b = np.array(cut_rgb).astype(np.float32)
    cut_boost = np.clip(cut_b * 1.45 + np.array([28, 10, 54]), 0, 255)
    a = glow_arr[..., None]
    out = dark * (1 - a) + cut_boost * a
    # strong core keeps original boosted fluoro color
    core = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
    core_arr = np.array(core).astype(np.float32) / 255.0
    cb = (core_arr > 0.55)[..., None].astype(np.float32) * 0.5
    orig_b = np.clip(cut_b * 1.55, 0, 255)
    out = out * (1 - cb) + orig_b * cb
    # gentle violet ambient inside cutout region only (tight)
    ambient = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
    amb = np.array(ambient).astype(np.float32) / 255.0
    out += np.stack([np.full_like(arr[..., 0], 34),
                     np.full_like(arr[..., 1], 9),
                     np.full_like(arr[..., 2], 52)], axis=-1) * (0.04 * amb[..., None])
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

if __name__ == "__main__":
    png = r"C:\Users\terri\Desktop\1\A5尺寸（129张）\普卡荧光（104张）\2B（1张）\19.png"
    psd = r"C:\Users\terri\Desktop\1\A5尺寸（129张）\普卡荧光（104张）\2B（1张）\19.psd"
    uv = uv_from_cut(png, psd)
    uv.thumbnail((420, 420))
    n = Image.open(png).convert("RGB")
    n.thumbnail((420, 420))
    combo = Image.new("RGB", (n.width * 2 + 8, max(n.height, uv.height)), (30, 30, 40))
    combo.paste(n, (0, 0))
    combo.paste(uv, (n.width + 8, 0))
    combo.save(r"C:\Users\terri\Doubao\chats\2026-09-11\new-chat\uv3_2b.png")
    print("saved", combo.size)
