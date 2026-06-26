#!/usr/bin/env python3
"""
Генератор мокапов устройств.
Размещает изображение на программно отрисованных мокапах (ноутбук, телефон, планшет и др.).
Все мокапы рисуются через Pillow — внешние файлы не требуются.
"""

import argparse
import os
import sys
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# === Конфигурация устройств ===
DEVICES = {
    "laptop": {
        "name": "Ноутбук",
        "output_size": (1920, 1080),
        "screen_ratio": (16, 10),      # Пропорции экрана
        "bezel": 16,                    # Толщина рамки (px при масштабе 1)
        "corner_radius": 12,           # Скругление углов
        "chin": 40,                     # Нижняя панель (основание)
        "base_height": 20,             # Высота основания ноутбука
        "base_width_ratio": 1.15,      # Основание шире экрана
        "screen_scale": 0.55,          # Масштаб экрана относительно холста
    },
    "phone": {
        "name": "Телефон",
        "output_size": (1200, 800),
        "screen_ratio": (9, 19.5),
        "bezel": 12,
        "corner_radius": 28,
        "chin": 0,
        "screen_scale": 0.65,
    },
    "tablet": {
        "name": "Планшет",
        "output_size": (1920, 1080),
        "screen_ratio": (4, 3),
        "bezel": 20,
        "corner_radius": 20,
        "chin": 0,
        "screen_scale": 0.60,
    },
    "monitor": {
        "name": "Монитор",
        "output_size": (1920, 1080),
        "screen_ratio": (16, 9),
        "bezel": 10,
        "corner_radius": 8,
        "chin": 30,
        "stand_width": 80,
        "stand_height": 60,
        "base_width": 200,
        "base_height": 12,
        "screen_scale": 0.55,
    },
    "hand_phone": {
        "name": "Телефон в руке",
        "output_size": (1200, 800),
        "screen_ratio": (9, 19.5),
        "bezel": 10,
        "corner_radius": 28,
        "chin": 0,
        "screen_scale": 0.55,
        "tilt_angle": 5,                # Наклон в градусах
    },
}

# === Цвета фона ===
BACKGROUNDS = {
    "white": {"color": (255, 255, 255)},
    "dark": {"color": (18, 18, 18)},
    "gradient": {"color1": (245, 247, 250), "color2": (226, 232, 240)},
}

# Цвета устройств
DEVICE_COLOR = (45, 45, 50)         # Основной цвет корпуса
DEVICE_COLOR_LIGHT = (65, 65, 70)   # Светлая часть корпуса
SCREEN_BORDER = (30, 30, 35)        # Цвет внутренней рамки экрана


def hex_в_rgb(hex_str):
    """Конвертация HEX в RGB."""
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def создать_фон(width, height, bg_type):
    """Создание фонового изображения."""
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)

    if bg_type == "gradient":
        c1 = BACKGROUNDS["gradient"]["color1"]
        c2 = BACKGROUNDS["gradient"]["color2"]
        for y in range(height):
            t = y / max(1, height - 1)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    else:
        color = BACKGROUNDS.get(bg_type, BACKGROUNDS["white"])["color"]
        draw.rectangle([0, 0, width, height], fill=color + (255,))

    return img


def нарисовать_прямоугольник_со_скруглением(draw, bbox, radius, fill, outline=None):
    """Рисование прямоугольника с закруглёнными углами."""
    x1, y1, x2, y2 = bbox
    r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)

    # Основной прямоугольник (без углов)
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)

    # Закруглённые углы
    draw.pieslice([x1, y1, x1 + 2 * r, y1 + 2 * r], 180, 270, fill=fill)
    draw.pieslice([x2 - 2 * r, y1, x2, y1 + 2 * r], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2 * r, x1 + 2 * r, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2 * r, y2 - 2 * r, x2, y2], 0, 90, fill=fill)


def добавить_тень(img, offset=8, blur_radius=15, shadow_color=(0, 0, 0, 60)):
    """Добавление тени к непрозрачным пикселям изображения."""
    # Создаём маску тени из альфа-канала
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)

    # Извлекаем альфа-канал
    if img.mode == "RGBA":
        alpha = img.split()[3]
    else:
        alpha = Image.new("L", img.size, 255)

    # Тень — это размытый альфа-канал со смещением
    shadow_alpha = Image.new("L", img.size, 0)
    shadow_alpha.paste(alpha, (offset, offset))
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(blur_radius))

    # Создаём слой тени
    shadow_layer = Image.new("RGBA", img.size, shadow_color[:3] + (0,))
    shadow_layer.putalpha(shadow_alpha)

    # Композитим: фон → тень → изображение
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result = Image.alpha_composite(result, shadow_layer)
    result = Image.alpha_composite(result, img)
    return result


def мокап_ноутбук(user_image, config, canvas_w, canvas_h):
    """Создание мокапа ноутбука."""
    scale = config["screen_scale"]
    bezel = int(config["bezel"] * (canvas_h / 1080))
    corner_r = int(config["corner_radius"] * (canvas_h / 1080))

    # Размер экранной области (куда вставляем изображение)
    screen_w = int(canvas_w * scale)
    screen_h = int(screen_w * config["screen_ratio"][1] / config["screen_ratio"][0])

    # Размер корпуса (экран + безель)
    body_w = screen_w + bezel * 2
    body_h = screen_h + bezel * 2

    # Основание ноутбука
    base_h = int(config["base_height"] * (canvas_h / 1080))
    chin_h = int(config["chin"] * (canvas_h / 1080))
    base_w = int(body_w * config["base_width_ratio"])

    # Общая высота устройства
    total_h = body_h + chin_h + base_h

    # Создаём слой устройства
    device = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(device)

    # Позиция центрирования
    cx = canvas_w // 2
    cy = canvas_h // 2 - base_h

    body_x1 = cx - body_w // 2
    body_y1 = cy - body_h // 2
    body_x2 = body_x1 + body_w
    body_y2 = body_y1 + body_h

    # Рисуем корпус (экранная часть)
    нарисовать_прямоугольник_со_скруглением(
        d, [body_x1, body_y1, body_x2, body_y2],
        corner_r, fill=DEVICE_COLOR
    )

    # Внутренняя рамка экрана
    d.rectangle(
        [body_x1 + bezel, body_y1 + bezel,
         body_x2 - bezel, body_y2 - bezel],
        fill=SCREEN_BORDER
    )

    # Петля (chin) между экраном и основанием
    if chin_h > 0:
        d.rectangle(
            [body_x1, body_y2, body_x2, body_y2 + chin_h],
            fill=DEVICE_COLOR_LIGHT
        )
        # Индикатор камеры (точка вверху)
        cam_r = max(3, bezel // 4)
        d.ellipse(
            [cx - cam_r, body_y1 + bezel // 2 - cam_r,
             cx + cam_r, body_y1 + bezel // 2 + cam_r],
            fill=(80, 80, 85)
        )

    # Основание ноутбука
    base_x1 = cx - base_w // 2
    base_y1 = body_y2 + chin_h
    нарисовать_прямоугольник_со_скруглением(
        d, [base_x1, base_y1, base_x1 + base_w, base_y1 + base_h],
        4, fill=DEVICE_COLOR_LIGHT
    )

    # Вставляем пользовательское изображение
    resized = user_image.resize((screen_w, screen_h), Image.LANCZOS)
    device.paste(resized, (body_x1 + bezel, body_y1 + bezel))

    return device


def мокап_телефон(user_image, config, canvas_w, canvas_h):
    """Создание мокапа телефона."""
    scale = config["screen_scale"]
    bezel = int(config["bezel"] * (canvas_h / 800))
    corner_r = int(config["corner_radius"] * (canvas_h / 800))

    # Для телефона: высота определяет масштаб
    screen_h = int(canvas_h * scale)
    screen_w = int(screen_h * config["screen_ratio"][0] / config["screen_ratio"][1])

    body_w = screen_w + bezel * 2
    body_h = screen_h + bezel * 2

    device = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(device)

    cx = canvas_w // 2
    cy = canvas_h // 2

    body_x1 = cx - body_w // 2
    body_y1 = cy - body_h // 2

    # Корпус телефона
    нарисовать_прямоугольник_со_скруглением(
        d, [body_x1, body_y1, body_x1 + body_w, body_y1 + body_h],
        corner_r, fill=DEVICE_COLOR
    )

    # Экран (с небольшим скруглением)
    screen_r = max(4, corner_r - bezel)
    screen_x1 = body_x1 + bezel
    screen_y1 = body_y1 + bezel
    нарисовать_прямоугольник_со_скруглением(
        d, [screen_x1, screen_y1,
            screen_x1 + screen_w, screen_y1 + screen_h],
        screen_r, fill=SCREEN_BORDER
    )

    # Вырез камеры (notch) сверху
    notch_w = screen_w // 3
    notch_h = max(4, bezel // 2)
    notch_x = cx - notch_w // 2
    нарисовать_прямоугольник_со_скруглением(
        d, [notch_x, body_y1 + bezel, notch_x + notch_w, body_y1 + bezel + notch_h],
        notch_h // 2, fill=DEVICE_COLOR
    )

    # Боковая кнопка
    btn_h = body_h // 8
    btn_y = body_y1 + body_h // 3
    d.rectangle(
        [body_x1 + body_w, btn_y, body_x1 + body_w + 3, btn_y + btn_h],
        fill=DEVICE_COLOR_LIGHT
    )

    # Вставляем изображение
    resized = user_image.resize((screen_w, screen_h), Image.LANCZOS)
    device.paste(resized, (screen_x1, screen_y1))

    return device


def мокап_планшет(user_image, config, canvas_w, canvas_h):
    """Создание мокапа планшета."""
    scale = config["screen_scale"]
    bezel = int(config["bezel"] * (canvas_h / 1080))
    corner_r = int(config["corner_radius"] * (canvas_h / 1080))

    screen_h = int(canvas_h * scale)
    screen_w = int(screen_h * config["screen_ratio"][0] / config["screen_ratio"][1])

    body_w = screen_w + bezel * 2
    body_h = screen_h + bezel * 2

    device = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(device)

    cx = canvas_w // 2
    cy = canvas_h // 2

    body_x1 = cx - body_w // 2
    body_y1 = cy - body_h // 2

    # Корпус
    нарисовать_прямоугольник_со_скруглением(
        d, [body_x1, body_y1, body_x1 + body_w, body_y1 + body_h],
        corner_r, fill=DEVICE_COLOR
    )

    # Камера (точка вверху по центру)
    cam_r = max(3, bezel // 3)
    d.ellipse(
        [cx - cam_r, body_y1 + bezel // 2 - cam_r,
         cx + cam_r, body_y1 + bezel // 2 + cam_r],
        fill=(80, 80, 85)
    )

    # Экран
    screen_x1 = body_x1 + bezel
    screen_y1 = body_y1 + bezel
    d.rectangle(
        [screen_x1, screen_y1,
         screen_x1 + screen_w, screen_y1 + screen_h],
        fill=SCREEN_BORDER
    )

    resized = user_image.resize((screen_w, screen_h), Image.LANCZOS)
    device.paste(resized, (screen_x1, screen_y1))

    return device


def мокап_монитор(user_image, config, canvas_w, canvas_h):
    """Создание мокапа монитора на подставке."""
    scale = config["screen_scale"]
    bezel = int(config["bezel"] * (canvas_h / 1080))
    corner_r = int(config["corner_radius"] * (canvas_h / 1080))

    screen_w = int(canvas_w * scale)
    screen_h = int(screen_w * config["screen_ratio"][1] / config["screen_ratio"][0])

    body_w = screen_w + bezel * 2
    body_h = screen_h + bezel * 2
    chin_h = int(config["chin"] * (canvas_h / 1080))

    # Подставка
    stand_w = int(config["stand_width"] * (canvas_h / 1080))
    stand_h = int(config["stand_height"] * (canvas_h / 1080))
    base_plate_w = int(config["base_width"] * (canvas_h / 1080))
    base_plate_h = int(config["base_height"] * (canvas_h / 1080))

    device = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(device)

    cx = canvas_w // 2
    total_h = body_h + chin_h + stand_h + base_plate_h
    body_y1 = (canvas_h - total_h) // 2
    body_x1 = cx - body_w // 2

    # Корпус монитора
    нарисовать_прямоугольник_со_скруглением(
        d, [body_x1, body_y1, body_x1 + body_w, body_y1 + body_h],
        corner_r, fill=DEVICE_COLOR
    )

    # Подбородок
    if chin_h > 0:
        d.rectangle(
            [body_x1, body_y1 + body_h,
             body_x1 + body_w, body_y1 + body_h + chin_h],
            fill=DEVICE_COLOR_LIGHT
        )
        # Логотип (маленький прямоугольник)
        logo_w = 30
        logo_h = 4
        d.rectangle(
            [cx - logo_w // 2, body_y1 + body_h + chin_h // 2 - logo_h // 2,
             cx + logo_w // 2, body_y1 + body_h + chin_h // 2 + logo_h // 2],
            fill=(100, 100, 105)
        )

    # Ножка
    stand_top_y = body_y1 + body_h + chin_h
    d.rectangle(
        [cx - stand_w // 2, stand_top_y,
         cx + stand_w // 2, stand_top_y + stand_h],
        fill=DEVICE_COLOR_LIGHT
    )

    # Основание подставки
    base_y = stand_top_y + stand_h
    нарисовать_прямоугольник_со_скруглением(
        d, [cx - base_plate_w // 2, base_y,
            cx + base_plate_w // 2, base_y + base_plate_h],
        4, fill=DEVICE_COLOR
    )

    # Экран
    screen_x1 = body_x1 + bezel
    screen_y1 = body_y1 + bezel
    d.rectangle(
        [screen_x1, screen_y1,
         screen_x1 + screen_w, screen_y1 + screen_h],
        fill=SCREEN_BORDER
    )

    resized = user_image.resize((screen_w, screen_h), Image.LANCZOS)
    device.paste(resized, (screen_x1, screen_y1))

    return device


def мокап_рука_с_телефоном(user_image, config, canvas_w, canvas_h):
    """Создание мокапа телефона в руке (силуэт руки + телефон)."""
    # Сначала создаём обычный мокап телефона
    device = мокап_телефон(user_image, config, canvas_w, canvas_h)

    # Рисуем стилизованную руку
    d = ImageDraw.Draw(device)

    # Определяем позицию телефона
    scale = config["screen_scale"]
    bezel = int(config["bezel"] * (canvas_h / 800))
    screen_h = int(canvas_h * scale)
    screen_w = int(screen_h * config["screen_ratio"][0] / config["screen_ratio"][1])
    body_w = screen_w + bezel * 2
    body_h = screen_h + bezel * 2

    cx = canvas_w // 2
    cy = canvas_h // 2
    body_x1 = cx - body_w // 2
    body_y1 = cy - body_h // 2

    # Пальцы (овалы по бокам и снизу телефона)
    skin_color = (210, 180, 155, 200)

    # Большой палец слева
    thumb_w = body_w // 6
    thumb_h = body_h // 4
    thumb_x = body_x1 - thumb_w // 3
    thumb_y = cy + body_h // 8
    d.ellipse(
        [thumb_x, thumb_y, thumb_x + thumb_w, thumb_y + thumb_h],
        fill=skin_color
    )

    # Пальцы справа (4 пальца)
    finger_w = body_w // 8
    finger_h = body_h // 6
    for i in range(4):
        fy = body_y1 + body_h // 4 + i * (finger_h + 4)
        fx = body_x1 + body_w - finger_w // 4
        d.ellipse(
            [fx, fy, fx + finger_w, fy + finger_h],
            fill=skin_color
        )

    # Ладонь снизу
    palm_w = body_w
    palm_h = body_h // 5
    palm_x = body_x1
    palm_y = body_y1 + body_h - palm_h // 3
    d.ellipse(
        [palm_x - palm_w // 6, palm_y,
         palm_x + palm_w + palm_w // 6, palm_y + palm_h],
        fill=skin_color
    )

    return device


def создать_мокап(image_path, device="laptop", output="mockup.png", background="white"):
    """
    Главная функция создания мокапа.

    Args:
        image_path: Путь к изображению для размещения на мокапе
        device: Тип устройства (laptop|phone|tablet|monitor|hand_phone)
        output: Путь для сохранения результата
        background: Тип фона (white|dark|gradient)
    """
    if device not in DEVICES:
        print(f"Ошибка: неизвестное устройство '{device}'")
        print(f"Доступные: {', '.join(DEVICES.keys())}")
        sys.exit(1)

    config = DEVICES[device]
    canvas_w, canvas_h = config["output_size"]

    print(f"Создание мокапа: {config['name']}")
    print(f"Размер: {canvas_w}×{canvas_h}, фон: {background}")

    # Загружаем пользовательское изображение
    try:
        user_image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        sys.exit(1)

    # Создаём фон
    result = создать_фон(canvas_w, canvas_h, background)

    # Выбираем функцию мокапа
    мокап_функции = {
        "laptop": мокап_ноутбук,
        "phone": мокап_телефон,
        "tablet": мокап_планшет,
        "monitor": мокап_монитор,
        "hand_phone": мокап_рука_с_телефоном,
    }

    # Генерируем мокап устройства
    device_layer = мокап_функции[device](user_image, config, canvas_w, canvas_h)

    # Добавляем тень
    device_with_shadow = добавить_тень(device_layer, offset=10, blur_radius=20)

    # Композитим результат
    result = Image.alpha_composite(result, device_with_shadow)

    # Сохраняем
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    final = result.convert("RGB")
    final.save(output, "PNG", quality=95)
    print(f"Мокап сохранён: {output}")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Генератор мокапов устройств"
    )
    parser.add_argument(
        "--image", required=True,
        help="Путь к изображению для размещения на мокапе"
    )
    parser.add_argument(
        "--device", default="laptop",
        choices=["laptop", "phone", "tablet", "monitor", "hand_phone"],
        help="Тип устройства"
    )
    parser.add_argument(
        "--output", default="mockup.png",
        help="Путь для сохранения"
    )
    parser.add_argument(
        "--background", default="white",
        choices=["white", "dark", "gradient"],
        help="Фон вокруг мокапа"
    )
    args = parser.parse_args()

    создать_мокап(
        image_path=args.image,
        device=args.device,
        output=args.output,
        background=args.background,
    )


if __name__ == "__main__":
    main()
