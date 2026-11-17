# -*- coding: utf-8 -*-
"""uv effect v2: precise fluoro mask (purple/pink bright), smooth glow, dim rest"""
import numpy as np
from PIL import Image, ImageFilter

def uv_effect(img):
    im = img.convert("RGB")
    arr = np.array(im).astype(np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    diff = mx - mn
    hue = np.zeros_like(mx)
    m = diff > 0
    rm, gm, bm, mxm = r[m], g[m], b[m], mx[m]
    dm = diff[m]
    hue[m] = np.where(mxm == rm, ((gm - bm) / dm) % 6, hue[m])
    h2 = (bm - rm) / dm + 2
    hue[m] = np.where(mxm == gm, h2, hue[m])
    h3 = (rm - gm) / dm + 4
    hue[m] = np.where(mxm == bm, h3, hue[m])
    hue = hue / 6.0 * 360.0
    sat = np.where(mx > 0, diff / np.maximum(mx, 1e-6), 0) * 100.0
    val = mx / 255.0 * 100.0

    # fluoro mask: vivid purple/pink/violet + bright cool tones
    mask = (((hue >= 240) & (hue <= 350)) | ((hue >= 0) & (hue <= 20))) & \
           (sat >= 30) & (val >= 28)
    # keep only strong connected-ish cores: require val higher OR sat higher
    mask = mask & ((sat >= 45) | (val >= 55))
    # bright cyan/blue fluoro also glows (some UV inks are cyan/green)
    mask = mask | (((hue >= 160) & (hue <= 210)) & (sat >= 35) & (val >= 55))

    mask_img = Image.fromarray((mask.astype(np.uint8)) * 255)
    glow = mask_img.filter(ImageFilter.GaussianBlur(22))
    glow_arr = np.array(glow).astype(np.float32) / 255.0
    glow_arr = np.clip(glow_arr * 1.6, 0, 1)  # soft halo

    # dim base, slightly cool
    dark = arr * 0.42
    # fluorescent emissive color (violet-white)
    emiss = np.stack([np.full_like(dark[..., 0], 205),
                      np.full_like(dark[..., 1], 128),
                      np.full_like(dark[..., 2], 255)], axis=-1)
    a = glow_arr[..., None]
    out = dark * (1 - a) + emiss * a

    # keep original fluoro hue detail in the core (additive light)
    core = mask_img.filter(ImageFilter.GaussianBlur(6))
    core_arr = np.array(core).astype(np.float32) / 255.0
    boost = np.clip(arr * 1.55, 0, 255)
    cb = (core_arr > 0.45)[..., None].astype(np.float32) * 0.55
    out = out * (1 - cb) + boost * cb

    # faint global violet ambient
    out += np.stack([np.full_like(dark[..., 0], 70),
                     np.full_like(dark[..., 1], 18),
                     np.full_like(dark[..., 2], 110)], axis=-1) * 0.10
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

if __name__ == "__main__":
    import os
    tests = [("kafka", r"C:\Users\terri\Desktop\1\A5尺寸（129张）\普卡荧光（104张）\kafka（4张）\4.png"),
             ("albedo", r"C:\Users\terri\Desktop\1\A5尺寸（129张）\普卡荧光（104张）\albedo（14张）\16.png")]
    for name, p in tests:
        img = Image.open(p).convert("RGB")
        img.thumbnail((480, 480))
        uv = uv_effect(img)
        combo = Image.new("RGB", (img.width * 2 + 8, img.height), (30, 30, 40))
        combo.paste(img, (0, 0))
        combo.paste(uv, (img.width + 8, 0))
        combo.save(r"C:\Users\terri\Doubao\chats\2026-09-11\new-chat\uv2_%s.png" % name)
        print(name, "ok", combo.size)
