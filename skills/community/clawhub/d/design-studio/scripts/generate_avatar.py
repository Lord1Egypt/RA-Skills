#!/usr/bin/env python3
"""
Генератор профессиональных аватарок.

Создаёт квадратные аватарки с инициалами, градиентным фоном
и профессиональной типографикой.

Использование:
    python3 generate_avatar.py "ИФ" --output avatar.png
    python3 generate_avatar.py "AB" --style gradient --palette cyber --size 1024
    python3 generate_avatar.py "OK" --style circle --bg "#2563EB" --fg "#FFFFFF"
"""

import argparse
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont


# === Палитры для аватарок ===

ПАЛИТРЫ = {
    "cyber": {"bg1": (13, 17, 23), "bg2": (22, 33, 62), "fg": (88, 166, 255)},
    "neon": {"bg1": (26, 26, 46), "bg2": (60, 20, 60), "fg": (233, 69, 96)},
    "corporate": {"bg1": (37, 99, 235), "bg2": (30, 58, 138), "fg": (255, 255, 255)},
    "premium": {"bg1": (15, 23, 42), "bg2": (30, 41, 59), "fg": (212, 175, 55)},
    "minimal": {"bg1": (23, 23, 23), "bg2": (50, 50, 50), "fg": (255, 255, 255)},
    "creative": {"bg1": (249, 115, 22), "bg2": (234, 88, 12), "fg": (255, 255, 255)},
    "future": {"bg1": (124, 58, 237), "bg2": (79, 70, 229), "fg": (255, 255, 255)},
    "green": {"bg1": (22, 163, 74), "bg2": (21, 128, 61), "fg": (255, 255, 255)},
    "red": {"bg1": (220, 38, 38), "bg2": (185, 28, 28), "fg": (255, 255, 255)},
    "ocean": {"bg1": (6, 182, 212), "bg2": (14, 116, 144), "fg": (255, 255, 255)},
}


def найти_шрифт(имя, bold=True):
    """Ищет шрифт в системе."""
    стиль = "Bold" if bold else "Regular"
    try:
        result = subprocess.run(
            ["fc-match", "--format=%{file}", f"{имя}:style={стиль}"],
            capture_output=True, text=True, timeout=5,
        )
        путь = result.stdout.strip()
        if путь:
            return путь
    except Exception:
        pass
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def hex_в_rgb(hex_str):
    """Конвертирует HEX в RGB кортеж."""
    hex_clean = hex_str.lstrip("#")
    return tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))


def создать_градиент(size, цвет1, цвет2, направление="diagonal"):
    """Создаёт градиентное изображение."""
    img = Image.new("RGB", (size, size))
    pixels = img.load()

    for y in range(size):
        for x in range(size):
            if направление == "diagonal":
                t = (x + y) / (2 * size)
            elif направление == "vertical":
                t = y / size
            elif направление == "horizontal":
                t = x / size
            elif направление == "radial":
                cx, cy = size / 2, size / 2
                dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                t = min(1.0, dist / (size * 0.7))
            else:
                t = y / size

            r = int(цвет1[0] * (1 - t) + цвет2[0] * t)
            g = int(цвет1[1] * (1 - t) + цвет2[1] * t)
            b = int(цвет1[2] * (1 - t) + цвет2[2] * t)
            pixels[x, y] = (r, g, b)

    return img


def нарисовать_декор(draw, size, палитра, стиль_декора):
    """Добавляет декоративные элементы на аватарку."""
    fg = палитра["fg"]

    if стиль_декора == "ring":
        # Тонкое кольцо по краю
        thickness = max(2, size // 80)
        margin = size // 20
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            outline=(*fg, 60), width=thickness,
        )

    elif стиль_декора == "corners":
        # Уголки
        length = size // 8
        thickness = max(2, size // 100)
        margin = size // 15
        corners = [
            # Верхний левый
            [(margin, margin), (margin + length, margin)],
            [(margin, margin), (margin, margin + length)],
            # Верхний правый
            [(size - margin - length, margin), (size - margin, margin)],
            [(size - margin, margin), (size - margin, margin + length)],
            # Нижний левый
            [(margin, size - margin), (margin + length, size - margin)],
            [(margin, size - margin - length), (margin, size - margin)],
            # Нижний правый
            [(size - margin - length, size - margin), (size - margin, size - margin)],
            [(size - margin, size - margin - length), (size - margin, size - margin)],
        ]
        for line in corners:
            draw.line(line, fill=(*fg, 80), width=thickness)

    elif стиль_декора == "dots":
        # Точки по периметру
        r = max(2, size // 150)
        margin = size // 10
        count = 12
        for i in range(count):
            angle = 2 * math.pi * i / count
            cx = size // 2 + int((size // 2 - margin) * math.cos(angle))
            cy = size // 2 + int((size // 2 - margin) * math.sin(angle))
            draw.ellipse(
                [cx - r, cy - r, cx + r, cy + r],
                fill=(*fg, 40),
            )


def создать_аватарку(
    текст,
    size=1024,
    палитра_имя="corporate",
    шрифт_имя="Montserrat",
    стиль="gradient",
    направление_градиента="diagonal",
    стиль_декора="none",
    bg_hex=None,
    fg_hex=None,
    выход="avatar.png",
):
    """Создаёт профессиональную аватарку с инициалами."""
    палитра = ПАЛИТРЫ.get(палитра_имя, ПАЛИТРЫ["corporate"]).copy()

    # Пользовательские цвета
    if bg_hex:
        rgb = hex_в_rgb(bg_hex)
        палитра["bg1"] = rgb
        палитра["bg2"] = tuple(max(0, c - 30) for c in rgb)
    if fg_hex:
        палитра["fg"] = hex_в_rgb(fg_hex)

    # Создаём фон
    if стиль in ("gradient", "circle"):
        img = создать_градиент(size, палитра["bg1"], палитра["bg2"], направление_градиента)
    else:
        img = Image.new("RGB", (size, size), палитра["bg1"])

    # Конвертируем в RGBA для прозрачности декора
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    # Круглая маска (для стиля circle)
    if стиль == "circle":
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        margin = size // 30
        mask_draw.ellipse([margin, margin, size - margin, size - margin], fill=255)
        # Создаём фон за кругом
        bg_img = Image.new("RGBA", (size, size), (*палитра["bg2"], 255))
        img = Image.composite(img, bg_img, mask)

    # Декоративные элементы
    if стиль_декора != "none":
        нарисовать_декор(draw_overlay, size, палитра, стиль_декора)
        img = Image.alpha_composite(img, overlay)

    # Текст
    draw = ImageDraw.Draw(img)

    # Размер шрифта: ~40% от размера аватарки, кратен 4
    базовый_размер = size * 0.4
    if len(текст) > 2:
        базовый_размер *= 2 / len(текст)
    размер_шрифта = max(12, round(базовый_размер / 4) * 4)

    font = ImageDraw.Draw(img)
    шрифт_путь = найти_шрифт(шрифт_имя, bold=True)
    try:
        font_obj = ImageFont.truetype(шрифт_путь, размер_шрифта)
    except Exception:
        font_obj = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            размер_шрифта,
        )

    # Центрирование текста
    bbox = draw.textbbox((0, 0), текст, font=font_obj)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) // 2
    y = (size - text_h) // 2 - bbox[1]  # Компенсация смещения baseline

    # Тень текста (для контраста)
    shadow_offset = max(2, size // 200)
    draw.text(
        (x + shadow_offset, y + shadow_offset), текст,
        fill=(0, 0, 0, 60), font=font_obj,
    )

    # Основной текст
    draw.text((x, y), текст, fill=палитра["fg"], font=font_obj)

    # Сохраняем
    img_rgb = img.convert("RGB")
    img_rgb.save(выход, "PNG", quality=95)
    print(f"Аватарка создана: {выход}")
    print(f"Размер: {size}×{size}")
    print(f"Текст: {текст}")
    print(f"Палитра: {палитра_имя}")
    return выход


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Генератор профессиональных аватарок")
    parser.add_argument("text", help="Текст/инициалы (1-4 символа)")
    parser.add_argument("--size", type=int, default=1024, help="Размер в пикселях (квадрат)")
    parser.add_argument(
        "--palette", "-p", default="corporate",
        help=f"Палитра: {', '.join(ПАЛИТРЫ.keys())}",
    )
    parser.add_argument("--font", default="Montserrat", help="Имя шрифта")
    parser.add_argument(
        "--style", default="gradient",
        choices=["gradient", "flat", "circle"],
        help="Стиль фона",
    )
    parser.add_argument(
        "--gradient", default="diagonal",
        choices=["diagonal", "vertical", "horizontal", "radial"],
        help="Направление градиента",
    )
    parser.add_argument(
        "--decor", default="none",
        choices=["none", "ring", "corners", "dots"],
        help="Декоративные элементы",
    )
    parser.add_argument("--bg", default=None, help="Цвет фона HEX (#2563EB)")
    parser.add_argument("--fg", default=None, help="Цвет текста HEX (#FFFFFF)")
    parser.add_argument("--output", "-o", default="avatar.png", help="Выходной файл")

    args = parser.parse_args()

    создать_аватарку(
        текст=args.text,
        size=args.size,
        палитра_имя=args.palette,
        шрифт_имя=args.font,
        стиль=args.style,
        направление_градиента=args.gradient,
        стиль_декора=args.decor,
        bg_hex=args.bg,
        fg_hex=args.fg,
        выход=args.output,
    )
