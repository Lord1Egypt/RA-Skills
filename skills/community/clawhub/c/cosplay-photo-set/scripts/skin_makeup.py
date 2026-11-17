# -*- coding: utf-8 -*-
"""肤色"化妆"后处理：把腿部/脚部偏暗、发灰、褐色斑驳的皮肤，统一到脸/手臂的干净肤色。

思路（模拟上妆，不是磨皮）：
  1. 皮肤遮罩（RGB + Lab 双规则，色相排除青蓝色头发/背景、低饱和银色鞋带）
  2. Lab 空间做频率分离：低频 = 整体明暗与色斑，高频 = 毛孔/皮肤纹理
  3. 低频：明度向参考肤色抬升并压缩明暗落差（粉底均匀肤色），a*/b* 向参考色收拢（压掉褐/红斑）
  4. 高频：保留明度纹理，色度细节衰减（去掉褐色噪点，保留毛孔）
  5. 腿部（下半身）加权更强，按画幅纵向平滑过渡，避免腰部出现接缝

用法:
  python skin_makeup.py in.png out.jpg [--strength 0.85] [--legs 1.3] [--debug mask.png]
"""
import os, sys, argparse
import numpy as np
from PIL import Image

# ---------- 色彩空间 ----------
M_RGB2XYZ = np.array([[0.4124564, 0.3575761, 0.1804375],
                      [0.2126729, 0.7151522, 0.0721750],
                      [0.0193339, 0.1191920, 0.9503041]], np.float32)
WHITE = np.array([0.95047, 1.0, 1.08883], np.float32)


def srgb_to_lab(rgb):
    m = rgb.reshape(-1, 3)
    m = np.where(m <= 0.04045, m / 12.92, ((m + 0.055) / 1.055) ** 2.4)
    xyz = (m @ M_RGB2XYZ.T) / WHITE
    d = 6 / 29
    f = np.where(xyz > d ** 3, np.cbrt(xyz), xyz / (3 * d * d) + 4 / 29)
    lab = np.stack([116 * f[:, 1] - 16,
                    500 * (f[:, 0] - f[:, 1]),
                    200 * (f[:, 1] - f[:, 2])], 1)
    return lab.reshape(rgb.shape)


def lab_to_srgb(lab):
    m = lab.reshape(-1, 3).copy()
    fy = (m[:, 0] + 16) / 116
    fx = fy + m[:, 1] / 500
    fz = fy - m[:, 2] / 200
    d = 6 / 29
    f = np.stack([fx, fy, fz], 1)
    xyz = np.where(f > d, f ** 3, 3 * d * d * (f - 4 / 29)) * WHITE
    rgb = xyz @ np.linalg.inv(M_RGB2XYZ).T
    rgb = np.clip(rgb, 0, None)
    rgb = np.where(rgb <= 0.0031308, rgb * 12.92, 1.055 * rgb ** (1 / 2.4) - 0.055)
    return np.clip(rgb, 0, 1).reshape(lab.shape)


# ---------- 快速模糊（三次盒式 ≈ 高斯） ----------
def _box(a, r):
    if r < 1:
        return a
    k = 2 * r + 1
    p = np.pad(a, ((r, r), (r, r)) + ((0, 0),) * (a.ndim - 2), mode="edge")
    c = np.cumsum(np.cumsum(p, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)) + ((0, 0),) * (a.ndim - 2))
    s = c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]
    return s / (k * k)


def blur(a, sigma):
    if sigma <= 0.5:
        return a
    r = max(1, int(round(sigma * 1.1)))
    out = a
    for _ in range(3):
        out = _box(out, r)
    return out.astype(np.float32)


# ---------- 皮肤遮罩 ----------
def skin_mask(rgb, lab, H):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    rule_rgb = (r > 0.20) & (r > g + 0.005) & (g >= b - 0.03) & (sat > 0.075) & (sat < 0.62)
    rule_lab = (L > 20) & (L < 98) & (A > 3) & (A < 28) & (B > 0) & (B < 34)
    m = (rule_rgb | rule_lab) & (L > 18) & (L < 99)
    # 排除极低饱和（银饰/白裙）与近乎无彩度的金属件
    m &= ~((sat < 0.075) & (L > 60))
    chroma = np.sqrt(A ** 2 + B ** 2)
    m &= ~((chroma < 7.5) & (L > 50))
    # 排除背景：逐行取左右边缘 2% 的中位色作为该行背景色，ΔE 太近的判为背景
    W = rgb.shape[1]
    edge = max(4, int(W * 0.02))
    bg = np.median(np.concatenate([lab[:, :edge], lab[:, -edge:]], axis=1), axis=1)
    bg = blur(bg.reshape(H, 1, 3).astype(np.float32), 3)[:, 0, :]
    bgcol = bg[:, None, :]                                # (H,1,3)
    dist = np.sqrt((0.9 * (L - bgcol[..., 0])) ** 2 +
                   (1.6 * (A - bgcol[..., 1])) ** 2 +
                   (1.6 * (B - bgcol[..., 2])) ** 2)
    m &= dist > 7.0
    # 清理：闭运算补洞 + 开运算去碎点
    m = blur(m.astype(np.float32), max(2, H * 0.0035)) > 0.45
    m = blur(m.astype(np.float32), max(1, H * 0.0015)) > 0.30
    return m, sat, dist


def analyze(lab, mask, H, tag=""):
    rows = []
    for name, y0, y1 in [("face", 0.08, 0.17), ("arms/chest", 0.18, 0.33),
                         ("thigh", 0.40, 0.50), ("knee", 0.50, 0.56),
                         ("shin", 0.56, 0.64), ("foot", 0.64, 0.71)]:
        y0i, y1i = int(y0 * H), int(y1 * H)
        mm = mask[y0i:y1i]
        if mm.sum() < 300:
            continue
        v = lab[y0i:y1i][mm]
        rows.append((name, int(mm.sum()), np.median(v[:, 0]), v[:, 0].std(),
                     np.median(v[:, 1]), v[:, 2].std(), np.median(v[:, 2])))
    if tag:
        print("  [%s]" % tag)
        for name, n, L, sL, a, sB, b in rows:
            print("    %-11s n=%6d  L=%5.1f (sd %4.1f)  a=%5.1f  b=%5.1f (sd %4.1f)"
                  % (name, n, L, sL, a, b, sB))
    return rows


def makeup(rgb, strength=0.35, leg_strength=0.75, leg_boost=1.25, verbose=True):
    H, W = rgb.shape[:2]
    lab = srgb_to_lab(rgb)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    mask, sat, bgdist = skin_mask(rgb, lab, H)
    if mask.sum() < 1000:
        if verbose:
            print("  !! 皮肤像素过少(%d)，跳过" % mask.sum())
        return rgb, mask
    # 参考肤色：上胸+手臂（这些区域在原始图里已经是“正常肤色”），比脸部高光更可靠
    band = np.zeros_like(mask)
    band[int(0.22 * H):int(0.35 * H)] = True
    ref = mask & band
    if ref.sum() < 800:
        band = np.zeros_like(mask)
        band[int(0.07 * H):int(0.30 * H)] = True
        ref = mask & band
    if ref.sum() < 800:
        ref = mask
    Lr = np.median(L[ref])
    Ar = np.median(A[ref])
    Br = np.median(B[ref])
    if verbose:
        print("  参考肤色: L=%.1f a=%.1f b=%.1f  (皮肤占比 %.1f%%)"
              % (Lr, Ar, Br, mask.mean() * 100))
        analyze(lab, mask, H, "before")

    # 四段频率分离：base=腿型光影，spot=整片暗/褐色斑，mid=斑块边界，fine=毛孔
    sig_fine = max(2.0, H * 0.0012)      # ≈3px  @2560
    sig_mid = max(6.0, H * 0.010)        # ≈26px
    sig_spot = max(12.0, H * 0.030)      # ≈77px
    sig_base = max(20.0, H * 0.060)      # ≈154px
    L_f = blur(L, sig_fine)
    L_m = blur(L, sig_mid)
    L_s = blur(L, sig_spot)
    L_b = blur(L, sig_base)
    A_f, A_m, A_s, A_b = (blur(A, s) for s in (sig_fine, sig_mid, sig_spot, sig_base))
    B_f, B_m, B_s, B_b = (blur(B, s) for s in (sig_fine, sig_mid, sig_spot, sig_base))

    # 下半身更强（腿部/脚部），按画幅纵向平滑过渡
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    legw = np.clip((y - 0.32) / 0.16, 0, 1) ** 1.1

    # 光影：按「皮肤自身低频亮度」和参考肤色的差做加法补偿——只平移曝光，
    # 不放大局部对比，毛孔/腿型阴影原样保留（乘法提亮会把褐斑衬得更脏）
    mb = np.maximum(blur(mask.astype(np.float32), sig_base), 1e-3)
    Lb_skin = blur(L * mask, sig_base) / mb
    Lt = Lr - 4.0 - 2.5 * legw
    L2 = L + np.clip(Lt - Lb_skin, 0.0, 16.0) * legw

    # 暗斑/暗环：轻微提一下「比自身低频更暗」的部分，不做大幅度磨平
    dspot = L_s - L_b
    L2 = L2 - np.minimum(dspot, 0.0) * (0.10 + 0.20 * legw) * legw

    # 色度：先在「皮肤自身的局部均值」上压掉小尺度偏色（褐斑/灰斑），
    # 再整体拉向参考色；只动颜色不动明暗，所以不会磨平腿型也不会发光
    Ab = blur(A * mask, sig_spot) / np.maximum(blur(mask.astype(np.float32), sig_spot), 1e-3)
    Bb = blur(B * mask, sig_spot) / np.maximum(blur(mask.astype(np.float32), sig_spot), 1e-3)
    A_loc = Ab + (A - Ab) * (0.45 - 0.15 * legw)
    B_loc = Bb + (B - Bb) * (0.40 - 0.15 * legw)
    At = Ar + 0.8 + 0.6 * legw
    Bt = Br + 0.6 + 1.0 * legw
    A2 = A + (A_loc - A + (At - Ab) * 0.60) * legw
    B2 = B + (B_loc - B + (Bt - Bb) * 0.60) * legw
    # 保护纹身/贴布/图案：偏离肤色色相过远的像素不参与色度修正
    dev = np.sqrt((A - Ab) ** 2 + (B - Bb) ** 2)
    keep = np.clip((14.0 - dev) / 6.0, 0.0, 1.0)
    A2 = A + (A2 - A) * keep
    B2 = B + (B2 - B) * keep

    lab2 = np.stack([L2, A2, B2], -1)
    out = lab_to_srgb(lab2)

    # 混合权重：只在皮肤遮罩内混合（硬截断），向内收 2px 再羽化；
    # 再用「离轮廓的距离」做淡出，避免整条腿被提亮后贴着背景发光
    # 混合权重：只在皮肤遮罩内混合（硬截断），按「到轮廓的像素距离」淡出，
    # 细小腿不会被整段压掉；贴边 1–6px 不动，保留原本的轮廓阴影，避免发光
    core = blur(mask.astype(np.float32), max(2, H * 0.0018)) > 0.60
    w = blur(core.astype(np.float32), max(1, H * 0.0010)) * (mask > 0.5)
    dist = np.zeros(mask.shape, np.float32)
    m0 = mask.copy()
    for _ in range(16):
        m0 = m0 & np.roll(m0, 1, 0) & np.roll(m0, -1, 0) & np.roll(m0, 1, 1) & np.roll(m0, -1, 1)
        dist += m0
    w = w * np.clip((dist - 1.0) / 5.0, 0.0, 1.0)
    w = np.clip(w, 0, 1) * (strength * (1.0 - legw) + leg_strength * legw)
    w = np.clip(w, 0, 0.92)[..., None]
    out = rgb * (1 - w) + out * w
    if verbose:
        lab3 = srgb_to_lab(out)
        analyze(lab3, mask, H, "after")
    return np.clip(out, 0, 1), mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--strength", type=float, default=0.35)
    ap.add_argument("--leg-strength", type=float, default=0.85)
    ap.add_argument("--legs", type=float, default=1.25)
    ap.add_argument("--quality", type=int, default=97)
    ap.add_argument("--debug", default="")
    a = ap.parse_args()
    rgb = np.asarray(Image.open(a.src).convert("RGB"), np.float32) / 255.0
    out, mask = makeup(rgb, a.strength, a.leg_strength, a.legs)
    im = Image.fromarray((out * 255 + 0.5).astype(np.uint8))
    if a.dst.lower().endswith((".jpg", ".jpeg")):
        im.save(a.dst, quality=a.quality, subsampling=0, optimize=True, progressive=True)
    else:
        im.save(a.dst)
    if a.debug:
        ov = (rgb * 255).astype(np.uint8).copy()
        ov[mask] = (0.35 * ov[mask] + 0.65 * np.array([255, 0, 255])).astype(np.uint8)
        Image.fromarray(ov).save(a.debug)
    print("saved", a.dst, os.path.getsize(a.dst) // 1024, "KB")


if __name__ == "__main__":
    main()
