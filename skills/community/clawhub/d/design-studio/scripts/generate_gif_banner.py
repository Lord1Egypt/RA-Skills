#!/usr/bin/env python3
"""
Генератор анимированных GIF-баннеров.
Создаёт GIF из нескольких кадров с анимациями: fade_in, slide, pulse, typewriter.
Использует Pillow для генерации кадров.
"""

import argparse
import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

# Добавляем директорию скриптов в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_marketplace_cover import (
    hex_в_rgb, загрузить_шрифт, размер_кратный_4, STYLE_PALETTES,
)


def разобрать_размер(size_str):
    """Парсит строку размера 'WxH' в кортеж (width, height)."""
    parts = size_str.lower().split("x")
    if len(parts) != 2:
        raise ValueError(f"Неверный формат размера: {size_str}. Ожидается WxH, например 1280x769")
    return int(parts[0]), int(parts[1])


def создать_фон(width, height, palette):
    """Создаёт фоновый кадр с градиентом."""
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)

    c1 = hex_в_rgb(palette["bg1"])
    c2 = hex_в_rgb(palette["bg2"])

    for y in range(height):
        t = y / max(1, height - 1)
        for x in range(width):
            tx = x / max(1, width - 1)
            t_mix = t * 0.65 + tx * 0.35
            r = int(c1[0] + (c2[0] - c1[0]) * t_mix)
            g = int(c1[1] + (c2[1] - c1[1]) * t_mix)
            b = int(c1[2] + (c2[2] - c1[2]) * t_mix)
            draw.point((x, y), fill=(r, g, b, 255))

    return img


def рассчитать_позиции_текста(width, height, title, subtitle, шрифт_заголовка, шрифт_подзаголовка):
    """Рассчитывает позиции для заголовка и подзаголовка (центрирование)."""
    tmp = Image.new("RGBA", (1, 1))
    tmp_draw = ImageDraw.Draw(tmp)

    bbox_title = tmp_draw.textbbox((0, 0), title, font=шрифт_заголовка)
    title_w = bbox_title[2] - bbox_title[0]
    title_h = bbox_title[3] - bbox_title[1]

    sub_w, sub_h = 0, 0
    if subtitle:
        bbox_sub = tmp_draw.textbbox((0, 0), subtitle, font=шрифт_подзаголовка)
        sub_w = bbox_sub[2] - bbox_sub[0]
        sub_h = bbox_sub[3] - bbox_sub[1]

    отступ = размер_кратный_4(16) if subtitle else 0
    total_h = title_h + (отступ + sub_h if subtitle else 0)

    title_x = (width - title_w) // 2
    title_y = (height - total_h) // 2

    sub_x = (width - sub_w) // 2 if subtitle else 0
    sub_y = title_y + title_h + отступ if subtitle else 0

    return {
        "title_x": title_x, "title_y": title_y,
        "title_w": title_w, "title_h": title_h,
        "sub_x": sub_x, "sub_y": sub_y,
        "sub_w": sub_w, "sub_h": sub_h,
    }


def анимация_fade_in(фон, title, subtitle, palette, шрифт_заголовка, шрифт_подзаголовка, кол_кадров):
    """Текст плавно появляется (alpha от 0 до 255)."""
    width, height = фон.size
    позиции = рассчитать_позиции_текста(width, height, title, subtitle, шрифт_заголовка, шрифт_подзаголовка)
    text_color = hex_в_rgb(palette["text"])
    text_secondary = hex_в_rgb(palette["text_secondary"])

    кадры = []
    for i in range(кол_кадров):
        t = i / max(1, кол_кадров - 1)
        alpha = int(255 * t)

        кадр = фон.copy()
        текст_слой = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(текст_слой)

        # Заголовок
        draw.text(
            (позиции["title_x"], позиции["title_y"]),
            title, font=шрифт_заголовка,
            fill=text_color + (alpha,)
        )

        # Подзаголовок (появляется с задержкой)
        if subtitle:
            sub_alpha = int(255 * max(0, (t - 0.3) / 0.7))
            draw.text(
                (позиции["sub_x"], позиции["sub_y"]),
                subtitle, font=шрифт_подзаголовка,
                fill=text_secondary + (sub_alpha,)
            )

        кадр = Image.alpha_composite(кадр, текст_слой)
        кадры.append(кадр.convert("RGB"))

    return кадры


def анимация_slide(фон, title, subtitle, palette, шрифт_заголовка, шрифт_подзаголовка, кол_кадров):
    """Текст выезжает слева направо."""
    width, height = фон.size
    позиции = рассчитать_позиции_текста(width, height, title, subtitle, шрифт_заголовка, шрифт_подзаголовка)
    text_color = hex_в_rgb(palette["text"])
    text_secondary = hex_в_rgb(palette["text_secondary"])

    кадры = []
    for i in range(кол_кадров):
        t = i / max(1, кол_кадров - 1)
        # Функция замедления (ease-out)
        t_ease = 1 - (1 - t) ** 3

        кадр = фон.copy()
        текст_слой = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(текст_слой)

        # Заголовок выезжает слева
        start_x = -позиции["title_w"]
        current_x = int(start_x + (позиции["title_x"] - start_x) * t_ease)

        draw.text(
            (current_x, позиции["title_y"]),
            title, font=шрифт_заголовка,
            fill=text_color + (255,)
        )

        # Подзаголовок выезжает с задержкой
        if subtitle:
            t_sub = max(0, (t - 0.2) / 0.8)
            t_sub_ease = 1 - (1 - t_sub) ** 3
            sub_start_x = -позиции["sub_w"]
            sub_current_x = int(sub_start_x + (позиции["sub_x"] - sub_start_x) * t_sub_ease)

            draw.text(
                (sub_current_x, позиции["sub_y"]),
                subtitle, font=шрифт_подзаголовка,
                fill=text_secondary + (255,)
            )

        кадр = Image.alpha_composite(кадр, текст_слой)
        кадры.append(кадр.convert("RGB"))

    return кадры


def анимация_pulse(фон, title, subtitle, palette, шрифт_заголовка, шрифт_подзаголовка, кол_кадров):
    """Фон пульсирует яркостью, текст статичный."""
    width, height = фон.size
    позиции = рассчитать_позиции_текста(width, height, title, subtitle, шрифт_заголовка, шрифт_подзаголовка)
    text_color = hex_в_rgb(palette["text"])
    text_secondary = hex_в_rgb(palette["text_secondary"])

    c1 = hex_в_rgb(palette["bg1"])
    c2 = hex_в_rgb(palette["bg2"])

    # Статичный текстовый слой
    текст_слой = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(текст_слой)
    draw.text(
        (позиции["title_x"], позиции["title_y"]),
        title, font=шрифт_заголовка,
        fill=text_color + (255,)
    )
    if subtitle:
        draw.text(
            (позиции["sub_x"], позиции["sub_y"]),
            subtitle, font=шрифт_подзаголовка,
            fill=text_secondary + (255,)
        )

    кадры = []
    for i in range(кол_кадров):
        t = i / max(1, кол_кадров - 1)
        # Пульсация яркости (синусоида, 2 цикла за анимацию)
        pulse = 0.5 + 0.5 * math.sin(t * 2 * math.pi * 2)
        множитель = 0.85 + 0.3 * pulse  # от 0.85 до 1.15

        # Создаём фон с изменённой яркостью
        пульс_фон = Image.new("RGBA", (width, height))
        пульс_draw = ImageDraw.Draw(пульс_фон)
        for y in range(height):
            ty = y / max(1, height - 1)
            r = int(min(255, (c1[0] + (c2[0] - c1[0]) * ty) * множитель))
            g = int(min(255, (c1[1] + (c2[1] - c1[1]) * ty) * множитель))
            b = int(min(255, (c1[2] + (c2[2] - c1[2]) * ty) * множитель))
            пульс_draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        кадр = Image.alpha_composite(пульс_фон, текст_слой)
        кадры.append(кадр.convert("RGB"))

    return кадры


def анимация_typewriter(фон, title, subtitle, palette, шрифт_заголовка, шрифт_подзаголовка, кол_кадров):
    """Текст появляется побуквенно (эффект печатной машинки)."""
    width, height = фон.size
    text_color = hex_в_rgb(palette["text"])
    text_secondary = hex_в_rgb(palette["text_secondary"])

    всего_символов = len(title) + (len(subtitle) if subtitle else 0)
    # Кадры на заголовок и подзаголовок пропорционально
    кадров_на_заголовок = int(кол_кадров * len(title) / max(1, всего_символов))
    кадров_на_подзаголовок = кол_кадров - кадров_на_заголовок

    кадры = []

    for i in range(кол_кадров):
        кадр = фон.copy()
        текст_слой = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(текст_слой)

        # Сколько символов заголовка показывать
        if i < кадров_на_заголовок:
            показать_букв = int(len(title) * (i + 1) / кадров_на_заголовок)
            видимый_заголовок = title[:показать_букв]
            видимый_подзаголовок = ""
        else:
            видимый_заголовок = title
            if subtitle and кадров_на_подзаголовок > 0:
                j = i - кадров_на_заголовок
                показать_букв = int(len(subtitle) * (j + 1) / кадров_на_подзаголовок)
                видимый_подзаголовок = subtitle[:показать_букв]
            else:
                видимый_подзаголовок = subtitle or ""

        # Рассчитываем позиции для полного текста (чтобы текст не прыгал)
        позиции = рассчитать_позиции_текста(
            width, height, title, subtitle, шрифт_заголовка, шрифт_подзаголовка
        )

        # Рисуем видимую часть заголовка
        if видимый_заголовок:
            draw.text(
                (позиции["title_x"], позиции["title_y"]),
                видимый_заголовок, font=шрифт_заголовка,
                fill=text_color + (255,)
            )

            # Курсор (мигающий)
            if i < кадров_на_заголовок and i % 2 == 0:
                bbox = draw.textbbox((0, 0), видимый_заголовок, font=шрифт_заголовка)
                cursor_x = позиции["title_x"] + bbox[2] - bbox[0] + 4
                cursor_h = позиции["title_h"]
                draw.rectangle(
                    [cursor_x, позиции["title_y"], cursor_x + 3, позиции["title_y"] + cursor_h],
                    fill=hex_в_rgb(palette["accent1"]) + (200,)
                )

        # Рисуем видимую часть подзаголовка
        if видимый_подзаголовок:
            draw.text(
                (позиции["sub_x"], позиции["sub_y"]),
                видимый_подзаголовок, font=шрифт_подзаголовка,
                fill=text_secondary + (255,)
            )

        кадр = Image.alpha_composite(кадр, текст_слой)
        кадры.append(кадр.convert("RGB"))

    return кадры


# Реестр анимаций
АНИМАЦИИ = {
    "fade_in": анимация_fade_in,
    "slide": анимация_slide,
    "pulse": анимация_pulse,
    "typewriter": анимация_typewriter,
}


def создать_gif_баннер(title, subtitle=None, size="1280x769", style="fade_in",
                       palette="tech", duration=3000, fps=10, output="banner.gif"):
    """
    Создаёт анимированный GIF-баннер.

    Args:
        title: Текст заголовка
        subtitle: Подзаголовок (опционально)
        size: Размер в формате WxH
        style: Стиль анимации (fade_in|slide|pulse|typewriter)
        palette: Палитра (tech|business|creative|minimal)
        duration: Общая длительность в мс
        fps: Кадров в секунду
        output: Путь для сохранения GIF
    """
    width, height = разобрать_размер(size)
    палитра = STYLE_PALETTES.get(palette, STYLE_PALETTES["tech"])
    кол_кадров = max(2, int(duration / 1000 * fps))
    задержка_кадра = max(20, duration // кол_кадров)  # мс между кадрами

    print(f"Создание GIF-баннера: {width}×{height}")
    print(f"Анимация: {style}, палитра: {palette}")
    print(f"Кадров: {кол_кадров}, FPS: {fps}, длительность: {duration}мс")

    # Размеры шрифтов
    базовый_размер = min(width, height)
    размер_заголовка = размер_кратный_4(int(базовый_размер * 0.12))
    размер_подзаголовка = размер_кратный_4(int(размер_заголовка * 0.45))

    # Загрузка шрифтов
    шрифт_заголовка = загрузить_шрифт("PT Sans", размер_заголовка, bold=True)
    шрифт_подзаголовка = загрузить_шрифт("Open Sans", размер_подзаголовка, bold=False)

    # Создаём фон
    фон = создать_фон(width, height, палитра)

    # Генерируем кадры анимации
    if style not in АНИМАЦИИ:
        print(f"Ошибка: неизвестный стиль анимации '{style}'")
        print(f"Доступные: {', '.join(АНИМАЦИИ.keys())}")
        sys.exit(1)

    кадры = АНИМАЦИИ[style](
        фон, title, subtitle, палитра,
        шрифт_заголовка, шрифт_подзаголовка, кол_кадров
    )

    # Сохраняем GIF
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    кадры[0].save(
        output,
        save_all=True,
        append_images=кадры[1:],
        duration=задержка_кадра,
        loop=0,
        optimize=True,
    )

    print(f"GIF сохранён: {output}")
    print(f"Размер файла: {os.path.getsize(output) / 1024:.1f} КБ")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Генератор анимированных GIF-баннеров"
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
        "--size", default="1280x769",
        help="Размер WxH (по умолчанию 1280x769)"
    )
    parser.add_argument(
        "--style", default="fade_in",
        choices=["fade_in", "slide", "pulse", "typewriter"],
        help="Стиль анимации"
    )
    parser.add_argument(
        "--palette", default="tech",
        choices=["tech", "business", "creative", "minimal"],
        help="Палитра цветов"
    )
    parser.add_argument(
        "--duration", type=int, default=3000,
        help="Общая длительность в мс (по умолчанию 3000)"
    )
    parser.add_argument(
        "--fps", type=int, default=10,
        help="Кадров в секунду (по умолчанию 10)"
    )
    parser.add_argument(
        "--output", default="banner.gif",
        help="Путь для сохранения GIF"
    )
    args = parser.parse_args()

    создать_gif_баннер(
        title=args.title,
        subtitle=args.subtitle,
        size=args.size,
        style=args.style,
        palette=args.palette,
        duration=args.duration,
        fps=args.fps,
        output=args.output,
    )


if __name__ == "__main__":
    main()
