#!/usr/bin/env python3
"""
面部细节拼接模板 — 将 4 张面部特写图拼成 2x2 参考板。

用法:
  python stitch_face_details.py <char_name> [--dir <图片目录>]

示例:
  python stitch_face_details.py 墨雪
  python stitch_face_details.py 墨将 --dir ./images/characters
"""
import argparse
import os
from PIL import Image

CANVAS_SIZE = 1024           # 输出画布尺寸
TILE_SIZE = 480              # 单张图 resize 尺寸（预留间距）
PADDING = 6                  # 图片间距
LABEL_HEIGHT = 28            # 底部标注栏高度

LABELS = ["眼部特写", "鼻部特写", "唇部特写", "耳侧特写"]


def load_image(path: str) -> Image.Image:
    img = Image.open(path)
    # 按 TILE_SIZE 短边等比缩放
    ratio = TILE_SIZE / min(img.size)
    new_size = (int(img.width * ratio), int(img.height * ratio))
    return img.resize(new_size, Image.LANCZOS)


def crop_center(img: Image.Image, size: int) -> Image.Image:
    """中心裁剪为 size x size 正方形。"""
    left = (img.width - size) // 2
    top = (img.height - size) // 2
    return img.crop((left, top, left + size, top + size))


def main():
    parser = argparse.ArgumentParser(description="面部细节拼接")
    parser.add_argument("char_name", help="角色名，如 墨雪")
    parser.add_argument("--dir", default="images/characters",
                        help="图片目录（默认 images/characters）")
    args = parser.parse_args()

    base = args.dir
    name = args.char_name
    detail_dir = os.path.join(base, f"{name}_details")
    tiles = []

    for i, label in enumerate(LABELS):
        path = os.path.join(detail_dir, f"{name}_detail_{i+1}.png")
        if not os.path.isfile(path):
            print(f"[WARN] 未找到: {path}")
            continue
        img = load_image(path)
        cropped = crop_center(img, TILE_SIZE)
        tiles.append((cropped, label))

    if len(tiles) < 4:
        print(f"[ERROR] 需要 4 张细节图，找到 {len(tiles)} 张")
        print(f"  预期路径: {detail_dir}/{name}_detail_1~4.png")
        return

    # 创建画布
    w = CANVAS_SIZE
    canvas = Image.new("RGB", (w, w), (240, 240, 240))

    # 2x2 布局
    positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
    tile_w = (w - PADDING * 3) // 2
    tile_h = (w - PADDING * 3 - LABEL_HEIGHT * 2) // 2

    for idx, ((col, row), (img_data, label)) in enumerate(zip(positions, tiles)):
        x = PADDING + col * (tile_w + PADDING)
        y = PADDING + row * (tile_h + LABEL_HEIGHT + PADDING)
        resized = img_data.resize((tile_w, tile_h), Image.LANCZOS)
        canvas.paste(resized, (x, y))

        # 标注栏
        label_y = y + tile_h
        for ly in range(label_y, label_y + LABEL_HEIGHT):
            for lx in range(x, x + tile_w):
                canvas.putpixel((lx, ly), (50, 50, 50))

    output_path = os.path.join(base, f"{name}_face_details.png")
    canvas.save(output_path)
    print(f"[OK] 已保存: {output_path}")


if __name__ == "__main__":
    main()
