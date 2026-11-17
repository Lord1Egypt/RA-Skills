#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把示例预览图合成为 README 顶部演示 GIF（可复现：python make-demo-gif.py）。

依赖：Pillow（pip install pillow）。
预览图由 tools/ggb-export 真机导出时生成（--png 参数），本脚本负责裁白边 + 统一画布 + 合成。
"""
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))

FRAMES = [
    ("demo1-derivative-definition.png", "① 导数定义：割线趋近切线"),
    ("demo2-linear-transform.png", "② 线性变换：矩阵作用于单位正方形"),
    ("demo3-sphere-cross-section.png", "③ 球面截交：平面截球面的交线圆（3D）"),
    ("demo4-button-secant.png", "④ 按钮割线：按钮控制取点"),
    ("demo5-polygon-circle.png", "⑤ 正 n 边形逼近圆 + 面积对比"),
    ("demo6-taylor.png", "⑥ 泰勒多项式逐阶逼近"),
    ("demo7-coin-toss.png", "⑦ 抛硬币频率模拟与重置"),
]

WIDTH = 720           # 输出宽度
CONTENT_H = 620       # 内容区统一高度（各帧缩放后居中放置，避免切换跳动）
DURATION = 1500       # 每帧毫秒
CAPTION_H = 44        # 顶部说明条高度

# 个别帧的人工裁切修正（相对坐标 left/top/right/bottom），用于去掉构件偏小的空白区域
FRAME_CROPS = {
    "demo3-sphere-cross-section.png": (0.12, 0.20, 0.88, 0.84),
}


def load_font(size=26):
    for path in (
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def trim_whitespace(im, pad=14, tol=10):
    """裁掉四周接近纯白的留白（GeoGebra 画布截图常带大块空白）。"""
    inv = ImageOps.invert(im.convert("L"))
    mask = inv.point(lambda p: 255 if p > tol else 0)
    box = mask.getbbox()
    if not box:
        return im
    l, t, r, b = box
    return im.crop(
        (
            max(0, l - pad),
            max(0, t - pad),
            min(im.width, r + pad),
            min(im.height, b + pad),
        )
    )


def main():
    font = load_font()
    frames = []
    for name, caption in FRAMES:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            raise SystemExit("缺少预览图：" + path)
        im = Image.open(path).convert("RGB")
        crop = FRAME_CROPS.get(name)
        if crop:
            w0, h0 = im.size
            im = im.crop(
                (
                    int(crop[0] * w0),
                    int(crop[1] * h0),
                    int(crop[2] * w0),
                    int(crop[3] * h0),
                )
            )
        im = trim_whitespace(im)
        im.thumbnail((WIDTH, CONTENT_H), Image.LANCZOS)

        canvas = Image.new("RGB", (WIDTH, CONTENT_H + CAPTION_H), (255, 255, 255))
        x = (WIDTH - im.width) // 2
        y = CAPTION_H + (CONTENT_H - im.height) // 2
        canvas.paste(im, (x, y))

        draw = ImageDraw.Draw(canvas)
        draw.rectangle([0, 0, WIDTH, CAPTION_H], fill=(31, 41, 55))
        draw.text((14, 8), caption, font=font, fill=(255, 255, 255))
        frames.append(canvas.convert("P", palette=Image.ADAPTIVE, colors=256))

    out = os.path.join(HERE, "demo.gif")
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print("saved:", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
