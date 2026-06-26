#!/usr/bin/env python3
"""
Добавление водяного знака на изображение.
Поддерживает режимы: одиночный (bottom_right, bottom_left, center) и tile (по всей картинке).
Использует Pillow с alpha compositing.
"""

import argparse
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Добавляем директорию скриптов в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_marketplace_cover import hex_в_rgb, загрузить_шрифт


def добавить_водяной_знак(image_path, text="© AlexKZ AI", position="bottom_right",
                          opacity=0.3, font_size=24, color="#FFFFFF", output=None):
    """
    Добавляет водяной знак на изображение.

    Args:
        image_path: Путь к исходному изображению
        text: Текст водяного знака
        position: Позиция (bottom_right|bottom_left|center|tile)
        opacity: Прозрачность 0.0-1.0
        font_size: Размер шрифта
        color: Цвет в HEX
        output: Путь для сохранения (если None — перезаписывает исходный)
    """
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Ошибка: не удалось открыть {image_path}: {e}")
        sys.exit(1)

    width, height = img.size
    rgb = hex_в_rgb(color)
    alpha = int(255 * max(0.0, min(1.0, opacity)))
    fill_color = rgb + (alpha,)

    # Загружаем шрифт
    шрифт = загрузить_шрифт("Open Sans", font_size, bold=False)

    # Создаём слой водяного знака
    wm_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    wm_draw = ImageDraw.Draw(wm_layer)

    # Получаем размер текста
    bbox = wm_draw.textbbox((0, 0), text, font=шрифт)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    отступ = 20  # Отступ от краёв

    if position == "bottom_right":
        x = width - text_w - отступ
        y = height - text_h - отступ
        wm_draw.text((x, y), text, font=шрифт, fill=fill_color)

    elif position == "bottom_left":
        x = отступ
        y = height - text_h - отступ
        wm_draw.text((x, y), text, font=шрифт, fill=fill_color)

    elif position == "center":
        x = (width - text_w) // 2
        y = (height - text_h) // 2
        wm_draw.text((x, y), text, font=шрифт, fill=fill_color)

    elif position == "tile":
        # Повторяющийся водяной знак по диагонали
        _нарисовать_тайловый_водяной_знак(wm_layer, text, шрифт, fill_color, text_w, text_h)

    else:
        print(f"Ошибка: неизвестная позиция '{position}'")
        sys.exit(1)

    # Накладываем водяной знак
    result = Image.alpha_composite(img, wm_layer)

    # Сохраняем
    save_path = output or image_path
    save_dir = os.path.dirname(save_path)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    result.convert("RGB").save(save_path, "PNG", quality=95)
    print(f"Водяной знак добавлен: {save_path}")
    print(f"Режим: {position}, прозрачность: {opacity}")

    return save_path


def _нарисовать_тайловый_водяной_знак(layer, text, шрифт, fill_color, text_w, text_h):
    """Рисует повторяющийся водяной знак по диагонали (как у фотостоков)."""
    width, height = layer.size

    # Создаём один тайл с повёрнутым текстом
    угол = -30  # Градусы наклона

    # Шаг между повторениями
    шаг_x = int(text_w * 2.0)
    шаг_y = int(text_h * 4.0)

    # Создаём одиночный тайл текста с поворотом
    # Размер тайла с запасом для поворота
    диагональ = int(math.sqrt(text_w ** 2 + text_h ** 2)) + 20
    тайл = Image.new("RGBA", (диагональ, диагональ), (0, 0, 0, 0))
    тайл_draw = ImageDraw.Draw(тайл)

    # Рисуем текст по центру тайла
    tx = (диагональ - text_w) // 2
    ty = (диагональ - text_h) // 2
    тайл_draw.text((tx, ty), text, font=шрифт, fill=fill_color)

    # Поворачиваем тайл
    тайл_повёрнутый = тайл.rotate(угол, resample=Image.BICUBIC, expand=False)
    tw, th = тайл_повёрнутый.size

    # Заполняем всё изображение тайлами
    for y in range(-th, height + th, шаг_y):
        for x in range(-tw, width + tw, шаг_x):
            # Смещение чётных строк для шахматного порядка
            row = y // шаг_y
            смещение = шаг_x // 2 if row % 2 else 0
            layer.paste(тайл_повёрнутый, (x + смещение, y), тайл_повёрнутый)


def main():
    parser = argparse.ArgumentParser(
        description="Добавление водяного знака на изображение"
    )
    parser.add_argument(
        "--image", required=True,
        help="Путь к исходному изображению"
    )
    parser.add_argument(
        "--text", default="© AlexKZ AI",
        help="Текст водяного знака (по умолчанию '© AlexKZ AI')"
    )
    parser.add_argument(
        "--position", default="bottom_right",
        choices=["bottom_right", "bottom_left", "center", "tile"],
        help="Позиция водяного знака"
    )
    parser.add_argument(
        "--opacity", type=float, default=0.3,
        help="Прозрачность 0.0-1.0 (по умолчанию 0.3)"
    )
    parser.add_argument(
        "--font-size", type=int, default=24,
        help="Размер шрифта (по умолчанию 24)"
    )
    parser.add_argument(
        "--color", default="#FFFFFF",
        help="Цвет в HEX (по умолчанию #FFFFFF)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Путь для сохранения (по умолчанию перезаписывает исходный)"
    )
    args = parser.parse_args()

    добавить_водяной_знак(
        image_path=args.image,
        text=args.text,
        position=args.position,
        opacity=args.opacity,
        font_size=args.font_size,
        color=args.color,
        output=args.output,
    )


if __name__ == "__main__":
    main()
