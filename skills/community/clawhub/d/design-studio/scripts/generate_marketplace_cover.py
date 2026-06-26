#!/usr/bin/env python3
"""
Генератор обложек для фриланс-бирж.
Создаёт профессиональные обложки с учётом требований каждой площадки.
Использует правила из references/design-rules.md и палитры из references/color-palettes.md.
"""

import argparse
import subprocess
import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# === Размеры по биржам ===
MARKETPLACE_SIZES = {
    "fiverr":      (1280, 769),
    "kwork":       (1200, 800),
    "freelanceru": (1200, 800),
    "upwork":      (1584, 396),
}

# === Палитры стилей ===
STYLE_PALETTES = {
    "tech": {
        "bg1": "#0D1117",
        "bg2": "#1A1A2E",
        "accent1": "#00D4FF",
        "accent2": "#7C3AED",
        "text": "#F0F6FC",
        "text_secondary": "#8B949E",
    },
    "business": {
        "bg1": "#1E3A5F",
        "bg2": "#0F2440",
        "accent1": "#3B82F6",
        "accent2": "#F59E0B",
        "text": "#FFFFFF",
        "text_secondary": "#CBD5E1",
    },
    "creative": {
        "bg1": "#2D1B69",
        "bg2": "#1A0533",
        "accent1": "#FF6B6B",
        "accent2": "#4ECDC4",
        "text": "#FFFFFF",
        "text_secondary": "#C4B5FD",
    },
    "minimal": {
        "bg1": "#FFFFFF",
        "bg2": "#F1F5F9",
        "accent1": "#0F172A",
        "accent2": "#3B82F6",
        "text": "#0F172A",
        "text_secondary": "#64748B",
    },
}


def hex_в_rgb(hex_str):
    """Конвертация HEX в RGB кортеж."""
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def найти_шрифт(имя, bold=False):
    """Поиск шрифта через fc-match, возврат пути к файлу."""
    стиль = "Bold" if bold else "Regular"
    try:
        результат = subprocess.run(
            ["fc-match", f"{имя}:style={стиль}", "--format=%{file}"],
            capture_output=True, text=True, timeout=5
        )
        if результат.returncode == 0 and результат.stdout.strip():
            путь = результат.stdout.strip()
            if os.path.exists(путь):
                return путь
    except Exception:
        pass
    # Фоллбэк на DejaVu Sans
    for путь in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(путь):
            return путь
    return None


def загрузить_шрифт(имя, размер, bold=False):
    """Загрузка шрифта с указанным размером."""
    путь = найти_шрифт(имя, bold)
    if путь:
        try:
            return ImageFont.truetype(путь, размер)
        except Exception:
            pass
    return ImageFont.load_default()


def размер_кратный_4(базовый):
    """Округление размера до ближайшего кратного 4."""
    return max(4, round(базовый / 4) * 4)


def относительная_яркость(r, g, b):
    """Расчёт относительной яркости по WCAG 2.0."""
    def линейный(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * линейный(r) + 0.7152 * линейный(g) + 0.0722 * линейный(b)


def контраст_цветов(c1, c2):
    """Коэффициент контраста между двумя цветами."""
    l1 = относительная_яркость(*c1)
    l2 = относительная_яркость(*c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def создать_градиент(draw, width, height, color1, color2, angle=135):
    """Рисование градиента на холсте."""
    c1 = hex_в_rgb(color1)
    c2 = hex_в_rgb(color2)
    # Расчёт направления градиента
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    for y in range(height):
        for x in range(width):
            # Нормализованная позиция вдоль оси градиента
            t = (x * cos_a + y * sin_a) / (width * abs(cos_a) + height * abs(sin_a))
            t = max(0.0, min(1.0, t))
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            draw.point((x, y), fill=(r, g, b))


def создать_градиент_быстрый(width, height, color1, color2, angle=135):
    """Быстрое создание градиента через построчное заполнение."""
    img = Image.new("RGB", (width, height))
    c1 = hex_в_rgb(color1)
    c2 = hex_в_rgb(color2)

    for y in range(height):
        t = y / max(1, height - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        for x in range(width):
            # Добавляем горизонтальную составляющую для диагональности
            tx = x / max(1, width - 1)
            t_combined = t * 0.6 + tx * 0.4  # Диагональный микс
            r2 = int(c1[0] + (c2[0] - c1[0]) * t_combined)
            g2 = int(c1[1] + (c2[1] - c1[1]) * t_combined)
            b2 = int(c1[2] + (c2[2] - c1[2]) * t_combined)
            img.putpixel((x, y), (r2, g2, b2))
    return img


def нарисовать_декор_tech(draw, width, height, palette):
    """Декоративные элементы для стиля tech: точки, линии, сетка."""
    accent = hex_в_rgb(palette["accent1"])
    accent_alpha = accent + (40,)

    # Сетка из точек
    шаг = размер_кратный_4(min(width, height) // 20)
    for x in range(шаг, width, шаг):
        for y in range(шаг, height, шаг):
            r = 2
            draw.ellipse([x - r, y - r, x + r, y + r], fill=accent_alpha)

    # Угловые линии
    длина = min(width, height) // 4
    толщина = 2
    # Верхний левый
    draw.line([(0, длина), (0, 0), (длина, 0)], fill=accent + (80,), width=толщина)
    # Нижний правый
    draw.line([(width, height - длина), (width, height), (width - длина, height)],
              fill=accent + (80,), width=толщина)


def нарисовать_декор_business(draw, width, height, palette):
    """Декоративные элементы для стиля business: прямоугольники, полосы."""
    accent = hex_в_rgb(palette["accent2"])

    # Горизонтальные полосы справа
    for i in range(3):
        y_pos = height // 4 + i * (height // 8)
        x_start = int(width * 0.75)
        draw.rectangle(
            [x_start, y_pos, width, y_pos + 2],
            fill=accent + (60,)
        )

    # Круг в правом верхнем углу
    радиус = min(width, height) // 3
    draw.ellipse(
        [width - радиус // 2, -радиус // 2, width + радиус // 2, радиус // 2],
        fill=hex_в_rgb(palette["accent1"]) + (25,)
    )


def нарисовать_декор_creative(draw, width, height, palette):
    """Декоративные элементы для стиля creative: круги, волны."""
    accent1 = hex_в_rgb(palette["accent1"])
    accent2 = hex_в_rgb(palette["accent2"])

    # Декоративные круги
    позиции = [
        (int(width * 0.85), int(height * 0.2), min(width, height) // 5),
        (int(width * 0.1), int(height * 0.8), min(width, height) // 7),
        (int(width * 0.75), int(height * 0.75), min(width, height) // 9),
    ]
    for x, y, r in позиции:
        цвет = accent1 if позиции.index((x, y, r)) % 2 == 0 else accent2
        draw.ellipse([x - r, y - r, x + r, y + r], fill=цвет + (35,))

    # Диагональные линии
    for i in range(5):
        offset = i * (width // 10)
        draw.line(
            [(width - offset, 0), (width, offset)],
            fill=accent2 + (20,), width=1
        )


def нарисовать_декор_minimal(draw, width, height, palette):
    """Декоративные элементы для стиля minimal: одна линия, точка."""
    accent = hex_в_rgb(palette["accent2"])

    # Тонкая горизонтальная линия
    y_pos = int(height * 0.7)
    x_start = int(width * 0.1)
    x_end = int(width * 0.9)
    draw.line([(x_start, y_pos), (x_end, y_pos)], fill=accent + (100,), width=1)

    # Акцентная точка
    r = размер_кратный_4(min(width, height) // 30)
    draw.ellipse(
        [x_start - r, y_pos - r, x_start + r, y_pos + r],
        fill=accent + (180,)
    )


def нарисовать_нижний_бар(draw, width, height, palette, style):
    """Нижний акцентный бар — общий для всех стилей."""
    высота_бара = размер_кратный_4(max(4, height // 50))
    accent = hex_в_rgb(palette["accent1"])

    if style == "minimal":
        # Для минимализма — тонкая линия
        draw.rectangle(
            [0, height - 2, width, height],
            fill=accent
        )
    else:
        # Градиентный бар
        accent2 = hex_в_rgb(palette["accent2"])
        for x in range(width):
            t = x / max(1, width - 1)
            r = int(accent[0] + (accent2[0] - accent[0]) * t)
            g = int(accent[1] + (accent2[1] - accent[1]) * t)
            b = int(accent[2] + (accent2[2] - accent[2]) * t)
            draw.rectangle(
                [x, height - высота_бара, x + 1, height],
                fill=(r, g, b)
            )


def создать_обложку(marketplace, title, subtitle=None, style="tech", output="cover.png"):
    """
    Главная функция генерации обложки для биржи.

    Args:
        marketplace: fiverr|kwork|freelanceru|upwork
        title: Текст заголовка
        subtitle: Текст подзаголовка (опционально)
        style: tech|business|creative|minimal
        output: Путь для сохранения
    """
    # Определяем размеры
    if marketplace not in MARKETPLACE_SIZES:
        print(f"Ошибка: неизвестная биржа '{marketplace}'")
        print(f"Доступные: {', '.join(MARKETPLACE_SIZES.keys())}")
        sys.exit(1)

    width, height = MARKETPLACE_SIZES[marketplace]
    palette = STYLE_PALETTES.get(style, STYLE_PALETTES["tech"])

    print(f"Создание обложки для {marketplace} ({width}×{height})")
    print(f"Стиль: {style}")

    # === Фон с градиентом ===
    img = Image.new("RGBA", (width, height))
    bg = Image.new("RGBA", (width, height))
    bg_draw = ImageDraw.Draw(bg)

    # Заливка градиентом
    c1 = hex_в_rgb(palette["bg1"])
    c2 = hex_в_rgb(palette["bg2"])
    for y in range(height):
        t = y / max(1, height - 1)
        # Диагональный градиент
        for x in range(width):
            tx = x / max(1, width - 1)
            t_mix = t * 0.65 + tx * 0.35
            r = int(c1[0] + (c2[0] - c1[0]) * t_mix)
            g = int(c1[1] + (c2[1] - c1[1]) * t_mix)
            b = int(c1[2] + (c2[2] - c1[2]) * t_mix)
            bg_draw.point((x, y), fill=(r, g, b, 255))

    img = Image.alpha_composite(img, bg)
    draw = ImageDraw.Draw(img)

    # === Декоративные элементы ===
    декор_слой = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    декор_draw = ImageDraw.Draw(декор_слой)

    декор_функции = {
        "tech": нарисовать_декор_tech,
        "business": нарисовать_декор_business,
        "creative": нарисовать_декор_creative,
        "minimal": нарисовать_декор_minimal,
    }
    if style in декор_функции:
        декор_функции[style](декор_draw, width, height, palette)

    img = Image.alpha_composite(img, декор_слой)
    draw = ImageDraw.Draw(img)

    # === Нижний бар ===
    бар_слой = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    бар_draw = ImageDraw.Draw(бар_слой)
    нарисовать_нижний_бар(бар_draw, width, height, palette, style)
    img = Image.alpha_composite(img, бар_слой)
    draw = ImageDraw.Draw(img)

    # === Типографика ===
    # Безопасная зона: 10% отступ
    safe_x = int(width * 0.10)
    safe_y = int(height * 0.10)
    safe_w = width - 2 * safe_x
    safe_h = height - 2 * safe_y

    # Размер заголовка: ~12% от минимальной стороны
    базовый_размер = min(width, height)
    размер_заголовка = размер_кратный_4(int(базовый_размер * 0.12))

    # Для Upwork (узкий баннер) — увеличиваем
    if marketplace == "upwork":
        размер_заголовка = размер_кратный_4(int(height * 0.28))

    # Загрузка шрифтов (максимум 2 по правилам)
    шрифт_заголовка = загрузить_шрифт("Montserrat", размер_заголовка, bold=True)
    
    # Автоуменьшение заголовка если не влезает в safe zone
    _tmp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while размер_заголовка > 24:
        _bbox = _tmp_draw.textbbox((0, 0), title, font=шрифт_заголовка)
        _tw = _bbox[2] - _bbox[0]
        if _tw <= safe_w - 40:  # 20px отступ с каждой стороны
            break
        размер_заголовка = размер_кратный_4(int(размер_заголовка * 0.85))
        шрифт_заголовка = загрузить_шрифт("Montserrat", размер_заголовка, bold=True)
    
    размер_подзаголовка = размер_кратный_4(int(размер_заголовка * 0.45))
    шрифт_подзаголовка = загрузить_шрифт("Open Sans", размер_подзаголовка, bold=False)

    text_color = hex_в_rgb(palette["text"])
    text_secondary = hex_в_rgb(palette["text_secondary"])

    # Проверка контраста WCAG AA (≥4.5:1)
    bg_средний = (
        (c1[0] + c2[0]) // 2,
        (c1[1] + c2[1]) // 2,
        (c1[2] + c2[2]) // 2,
    )
    contrast = контраст_цветов(text_color, bg_средний)
    if contrast < 4.5:
        # Инвертируем цвет текста для обеспечения контраста
        text_color = (0, 0, 0) if относительная_яркость(*bg_средний) > 0.5 else (255, 255, 255)
        print(f"Предупреждение: контраст скорректирован до {контраст_цветов(text_color, bg_средний):.1f}:1")

    # === Размещение текста ===
    текст_слой = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    текст_draw = ImageDraw.Draw(текст_слой)

    # Определяем вертикальную позицию (центрируем в safe zone)
    bbox_title = текст_draw.textbbox((0, 0), title, font=шрифт_заголовка)
    title_w = bbox_title[2] - bbox_title[0]
    title_h = bbox_title[3] - bbox_title[1]

    if subtitle:
        bbox_sub = текст_draw.textbbox((0, 0), subtitle, font=шрифт_подзаголовка)
        sub_w = bbox_sub[2] - bbox_sub[0]
        sub_h = bbox_sub[3] - bbox_sub[1]
        отступ = размер_кратный_4(16)  # Отступ между заголовком и подзаголовком
        total_h = title_h + отступ + sub_h
    else:
        total_h = title_h

    # Вертикальное центрирование
    start_y = safe_y + (safe_h - total_h) // 2

    # Горизонтальное центрирование заголовка
    title_x = safe_x + (safe_w - title_w) // 2
    title_y = start_y

    # Тень текста (для читаемости)
    shadow_offset = max(2, размер_заголовка // 30)
    shadow_color = (0, 0, 0, 80)
    текст_draw.text(
        (title_x + shadow_offset, title_y + shadow_offset),
        title, font=шрифт_заголовка, fill=shadow_color
    )
    # Основной заголовок
    текст_draw.text(
        (title_x, title_y),
        title, font=шрифт_заголовка, fill=text_color + (255,)
    )

    # Подзаголовок
    if subtitle:
        sub_x = safe_x + (safe_w - sub_w) // 2
        sub_y = title_y + title_h + отступ
        текст_draw.text(
            (sub_x + shadow_offset, sub_y + shadow_offset),
            subtitle, font=шрифт_подзаголовка, fill=shadow_color
        )
        текст_draw.text(
            (sub_x, sub_y),
            subtitle, font=шрифт_подзаголовка, fill=text_secondary + (255,)
        )
    else:
        # Акцентная линия под заголовком (если нет подзаголовка)
        линия_y = title_y + title_h + размер_кратный_4(12)
        линия_w = min(title_w // 3, 120)
        линия_x = title_x + (title_w - линия_w) // 2
        accent_rgb = hex_в_rgb(palette["accent1"])
        текст_draw.rectangle(
            [линия_x, линия_y, линия_x + линия_w, линия_y + 4],
            fill=accent_rgb + (200,)
        )

    img = Image.alpha_composite(img, текст_слой)

    # === Сохранение ===
    # Создаём директорию если нужно
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Конвертируем в RGB для PNG без альфа-канала
    final = img.convert("RGB")
    final.save(output, "PNG", quality=95)
    print(f"Обложка сохранена: {output}")
    print(f"Размер: {width}×{height}")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Генератор обложек для фриланс-бирж"
    )
    parser.add_argument(
        "--marketplace", required=True,
        choices=["fiverr", "kwork", "freelanceru", "upwork"],
        help="Биржа (определяет размер)"
    )
    parser.add_argument(
        "--title", required=True,
        help="Текст заголовка"
    )
    parser.add_argument(
        "--subtitle", default=None,
        help="Текст подзаголовка (опционально)"
    )
    parser.add_argument(
        "--style", default="tech",
        choices=["tech", "business", "creative", "minimal"],
        help="Стиль оформления"
    )
    parser.add_argument(
        "--output", default="cover.png",
        help="Путь для сохранения"
    )
    args = parser.parse_args()

    создать_обложку(
        marketplace=args.marketplace,
        title=args.title,
        subtitle=args.subtitle,
        style=args.style,
        output=args.output,
    )


if __name__ == "__main__":
    main()
