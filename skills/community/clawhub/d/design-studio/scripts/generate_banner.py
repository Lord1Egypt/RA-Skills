#!/usr/bin/env python3
"""
Генератор профессиональных баннеров.

Создаёт баннеры с правильной типографикой, сеткой и цветовой палитрой.
Применяет правила из design-rules.md автоматически.

Использование:
    python3 generate_banner.py "Заголовок" --subtitle "Подзаголовок" --output banner.png
    python3 generate_banner.py "DevOps Engineer" --size 1584x396 --style dark --palette cyber
    python3 generate_banner.py "Портфолио" --size 1280x720 --palette minimal --accent "#FF6600"
"""

import argparse
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# === Палитры ===

ПАЛИТРЫ = {
    "cyber": {
        "bg": (13, 17, 23),
        "surface": (22, 27, 34),
        "text": (230, 237, 243),
        "accent1": (88, 166, 255),
        "accent2": (63, 185, 80),
    },
    "neon": {
        "bg": (26, 26, 46),
        "surface": (22, 33, 62),
        "text": (234, 234, 234),
        "accent1": (233, 69, 96),
        "accent2": (15, 52, 96),
    },
    "corporate": {
        "bg": (255, 255, 255),
        "surface": (248, 250, 252),
        "text": (30, 41, 59),
        "accent1": (37, 99, 235),
        "accent2": (100, 116, 139),
    },
    "premium": {
        "bg": (15, 23, 42),
        "surface": (30, 41, 59),
        "text": (241, 245, 249),
        "accent1": (212, 175, 55),
        "accent2": (148, 163, 184),
    },
    "minimal": {
        "bg": (255, 255, 255),
        "surface": (245, 245, 245),
        "text": (23, 23, 23),
        "accent1": (0, 0, 0),
        "accent2": (115, 115, 115),
    },
    "dark_minimal": {
        "bg": (18, 18, 18),
        "surface": (30, 30, 30),
        "text": (224, 224, 224),
        "accent1": (255, 255, 255),
        "accent2": (102, 102, 102),
    },
    "creative": {
        "bg": (255, 255, 255),
        "surface": (255, 247, 237),
        "text": (28, 25, 23),
        "accent1": (249, 115, 22),
        "accent2": (139, 92, 246),
    },
    "future": {
        "bg": (15, 15, 35),
        "surface": (26, 26, 62),
        "text": (240, 240, 240),
        "accent1": (124, 58, 237),
        "accent2": (6, 182, 212),
    },
}

# === Стандартные размеры ===

РАЗМЕРЫ = {
    "github": (1584, 396),
    "youtube": (2560, 1440),
    "twitter": (1500, 500),
    "fiverr": (1280, 769),
    "kwork": (920, 520),
    "instagram": (1080, 1080),
    "telegram": (1280, 720),
    "web": (1920, 600),
    "linkedin": (1584, 396),
    "hd": (1920, 1080),
}


def найти_шрифт(имя, bold=False):
    """Ищет шрифт в системе через fc-match."""
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
    # Фоллбэк
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def загрузить_шрифт(имя, размер, bold=False):
    """Загружает шрифт указанного размера."""
    путь = найти_шрифт(имя, bold)
    try:
        return ImageFont.truetype(путь, размер)
    except Exception:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", размер
        )


def размер_кратный_4(базовый, множитель=1.0):
    """Возвращает размер шрифта кратный 4px."""
    return max(12, round(базовый * множитель / 4) * 4)


def нарисовать_декоративные_элементы(draw, width, height, палитра, стиль):
    """Добавляет декоративные геометрические элементы."""
    accent1 = палитра["accent1"]
    accent2 = палитра["accent2"]

    if стиль == "geometric":
        # Круги в углах
        r = min(width, height) // 6
        # Правый верхний — полукруг
        draw.ellipse(
            [width - r, -r // 2, width + r // 2, r],
            fill=(*accent1, 40),
        )
        # Левый нижний — полукруг
        draw.ellipse(
            [-r // 2, height - r, r, height + r // 2],
            fill=(*accent2, 40),
        )

    elif стиль == "lines":
        # Горизонтальные линии-акценты
        y_pos = height * 0.85
        line_w = width * 0.3
        draw.line(
            [(width * 0.1, y_pos), (width * 0.1 + line_w, y_pos)],
            fill=accent1, width=3,
        )
        draw.line(
            [(width * 0.1, y_pos + 8), (width * 0.1 + line_w * 0.6, y_pos + 8)],
            fill=accent2, width=2,
        )

    elif стиль == "dots":
        # Сетка точек
        шаг = max(40, min(width, height) // 15)
        for x in range(шаг, width, шаг):
            for y in range(шаг, height, шаг):
                opacity = 15 + int(20 * math.sin(x * 0.01) * math.cos(y * 0.01))
                r = 2
                draw.ellipse(
                    [x - r, y - r, x + r, y + r],
                    fill=(*accent1, max(5, min(40, opacity))),
                )

    elif стиль == "gradient_bar":
        # Градиентная полоса снизу
        bar_h = max(4, height // 80)
        for x in range(width):
            t = x / width
            r = int(accent1[0] * (1 - t) + accent2[0] * t)
            g = int(accent1[1] * (1 - t) + accent2[1] * t)
            b = int(accent1[2] * (1 - t) + accent2[2] * t)
            draw.line([(x, height - bar_h), (x, height)], fill=(r, g, b))


def создать_баннер(
    заголовок,
    подзаголовок="",
    размер=(1584, 396),
    палитра_имя="cyber",
    шрифт_заголовок="Montserrat",
    шрифт_текст="Open Sans",
    стиль_декора="geometric",
    акцент_hex=None,
    выход="banner.png",
):
    """Создаёт профессиональный баннер."""
    width, height = размер
    палитра = ПАЛИТРЫ.get(палитра_имя, ПАЛИТРЫ["cyber"]).copy()

    # Пользовательский акцент
    if акцент_hex:
        hex_clean = акцент_hex.lstrip("#")
        палитра["accent1"] = tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))

    # Создаём изображение с альфа-каналом для декора
    img = Image.new("RGBA", (width, height), (*палитра["bg"], 255))
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    # Декоративные элементы (на оверлее с прозрачностью)
    нарисовать_декоративные_элементы(draw_overlay, width, height, палитра, стиль_декора)
    img = Image.alpha_composite(img, overlay)

    # Основной холст для текста
    draw = ImageDraw.Draw(img)

    # Размеры шрифтов (кратны 4px, пропорциональны размеру баннера)
    базовый = min(width, height) * 0.12
    размер_заг = размер_кратный_4(базовый, 1.0)
    размер_подзаг = размер_кратный_4(базовый, 0.45)

    font_title = загрузить_шрифт(шрифт_заголовок, размер_заг, bold=True)
    font_sub = загрузить_шрифт(шрифт_текст, размер_подзаг, bold=False)

    # Безопасная зона (10% от краёв)
    safe_x = int(width * 0.10)
    safe_y = int(height * 0.10)
    safe_w = width - 2 * safe_x
    safe_h = height - 2 * safe_y

    # Вычисляем позиции текста (центрирование в безопасной зоне)
    title_bbox = draw.textbbox((0, 0), заголовок, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]

    # Общая высота контента
    gap = max(8, размер_подзаг // 2)  # Отступ между заголовком и подзаголовком кратен 8
    gap = (gap // 8) * 8
    total_h = title_h
    if подзаголовок:
        sub_bbox = draw.textbbox((0, 0), подзаголовок, font=font_sub)
        sub_h = sub_bbox[3] - sub_bbox[1]
        sub_w = sub_bbox[2] - sub_bbox[0]
        total_h += gap + sub_h

    # Центрируем по вертикали
    start_y = safe_y + (safe_h - total_h) // 2

    # Заголовок по центру
    title_x = safe_x + (safe_w - title_w) // 2
    draw.text((title_x, start_y), заголовок, fill=палитра["text"], font=font_title)

    # Подзаголовок
    if подзаголовок:
        sub_x = safe_x + (safe_w - sub_w) // 2
        sub_y = start_y + title_h + gap
        draw.text(
            (sub_x, sub_y), подзаголовок,
            fill=палитра["accent2"], font=font_sub,
        )

    # Акцентная линия под заголовком
    line_y = start_y + title_h + gap // 3
    line_w = min(title_w * 0.4, safe_w * 0.3)
    line_x = safe_x + (safe_w - line_w) // 2
    if not подзаголовок:
        draw.line(
            [(line_x, line_y), (line_x + line_w, line_y)],
            fill=палитра["accent1"], width=max(2, height // 100),
        )

    # Конвертируем в RGB и сохраняем
    img_rgb = img.convert("RGB")
    img_rgb.save(выход, "PNG", quality=95)
    print(f"Баннер создан: {выход}")
    print(f"Размер: {width}×{height}")
    print(f"Палитра: {палитра_имя}")
    print(f"Шрифты: {шрифт_заголовок} (заголовок) + {шрифт_текст} (текст)")
    return выход


def разобрать_размер(s):
    """Парсит строку размера '1920x1080' или имя пресета."""
    if s in РАЗМЕРЫ:
        return РАЗМЕРЫ[s]
    parts = s.lower().split("x")
    if len(parts) == 2:
        return (int(parts[0]), int(parts[1]))
    raise ValueError(f"Неизвестный размер: {s}. Доступные: {', '.join(РАЗМЕРЫ.keys())}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Генератор профессиональных баннеров")
    parser.add_argument("title", help="Текст заголовка")
    parser.add_argument("--subtitle", "-s", default="", help="Текст подзаголовка")
    parser.add_argument(
        "--size", default="github",
        help=f"Размер: WxH или пресет ({', '.join(РАЗМЕРЫ.keys())})",
    )
    parser.add_argument(
        "--palette", "-p", default="cyber",
        help=f"Палитра: {', '.join(ПАЛИТРЫ.keys())}",
    )
    parser.add_argument("--title-font", default="Montserrat", help="Шрифт заголовка")
    parser.add_argument("--text-font", default="Open Sans", help="Шрифт текста")
    parser.add_argument(
        "--decor", default="geometric",
        choices=["geometric", "lines", "dots", "gradient_bar", "none"],
        help="Стиль декоративных элементов",
    )
    parser.add_argument("--accent", default=None, help="Акцентный цвет HEX (#FF6600)")
    parser.add_argument("--output", "-o", default="banner.png", help="Выходной файл")

    args = parser.parse_args()
    размер = разобрать_размер(args.size)

    создать_баннер(
        заголовок=args.title,
        подзаголовок=args.subtitle,
        размер=размер,
        палитра_имя=args.palette,
        шрифт_заголовок=args.title_font,
        шрифт_текст=args.text_font,
        стиль_декора=args.decor,
        акцент_hex=args.accent,
        выход=args.output,
    )
