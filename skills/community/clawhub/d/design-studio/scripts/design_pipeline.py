#!/usr/bin/env python3
"""
Автопайплайн дизайна: генерация → проверка → доработка → финал.
Объединяет все скрипты в единый процесс с автоматическим улучшением.
"""

import argparse
import os
import sys
import subprocess

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

# Путь к директории скриптов
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Импорт существующих модулей
sys.path.insert(0, SCRIPTS_DIR)

from check_design import (
    анализ_цветов,
    анализ_пустого_пространства,
    анализ_сложности,
    анализ_баланса,
    коэффициент_контраста as контраст_пара,
)
from generate_banner import создать_баннер
from generate_avatar import создать_аватарку


def импорт_обложки():
    """Ленивый импорт генератора обложек."""
    from generate_marketplace_cover import создать_обложку
    return создать_обложку


def оценить_изображение(путь):
    """
    Оценка качества изображения по метрикам check_design.py.
    Возвращает общий балл (1-10) и детали.
    Логика оценки повторяет проверить_дизайн() из check_design.py.
    """
    try:
        img = Image.open(путь)
    except Exception as e:
        print(f"Ошибка открытия {путь}: {e}")
        return 0, {}

    width, height = img.size

    # 1. Анализ цветов → оценка палитры
    цвета = анализ_цветов(img)
    n_цветов = цвета["уникальных_цветов"]
    if n_цветов < 3:
        балл_цветов = 5
    elif n_цветов <= 20:
        балл_цветов = 10
    elif n_цветов <= 50:
        балл_цветов = 8
    elif n_цветов <= 100:
        балл_цветов = 6
    else:
        балл_цветов = 4

    # 2. Контраст
    фон = цвета["фон"]
    макс_контраст = 1.0
    for (r, g, b), доля in цвета["топ_цвета"][1:]:
        к = контраст_пара(фон, (r, g, b))
        if к > макс_контраст:
            макс_контраст = к
    if макс_контраст >= 7.0:
        балл_контраста = 10
    elif макс_контраст >= 4.5:
        балл_контраста = 8
    elif макс_контраст >= 3.0:
        балл_контраста = 5
    else:
        балл_контраста = 3

    # 3. Пустое пространство
    доля_пустого = анализ_пустого_пространства(img)
    if 0.15 <= доля_пустого <= 0.60:
        балл_воздуха = 10
    elif 0.10 <= доля_пустого <= 0.70:
        балл_воздуха = 7
    elif доля_пустого < 0.10:
        балл_воздуха = 4
    else:
        балл_воздуха = 5

    # 4. Визуальная сложность
    сложность = анализ_сложности(img)
    if 0.03 <= сложность <= 0.25:
        балл_сложности = 10
    elif 0.02 <= сложность <= 0.35:
        балл_сложности = 7
    elif сложность < 0.02:
        балл_сложности = 5
    else:
        балл_сложности = 4

    # 5. Баланс
    дисбаланс = анализ_баланса(img)
    if дисбаланс <= 0.05:
        балл_баланса = 10
    elif дисбаланс <= 0.10:
        балл_баланса = 8
    elif дисбаланс <= 0.15:
        балл_баланса = 6
    else:
        балл_баланса = 4

    # 6. Размер (стандартные форматы)
    стандартные = [
        (1584, 396), (2560, 1440), (1500, 500), (1280, 769),
        (920, 520), (1080, 1080), (1280, 720), (1920, 600),
        (1200, 800), (1920, 1080), (1024, 1024), (512, 512),
    ]
    подходит = any(
        abs(width - w) < 10 and abs(height - h) < 10
        for w, h in стандартные
    )
    if подходит:
        балл_размера = 10
    elif width >= 800 and height >= 400:
        балл_размера = 8
    elif width >= 400 and height >= 200:
        балл_размера = 6
    else:
        балл_размера = 4

    # Общая оценка (среднее, как в check_design.py)
    все_баллы = [балл_цветов, балл_контраста, балл_воздуха,
                 балл_сложности, балл_баланса, балл_размера]
    общая = sum(все_баллы) / len(все_баллы)

    детали = {
        "палитра": балл_цветов,
        "контраст": балл_контраста,
        "воздух": балл_воздуха,
        "сложность": балл_сложности,
        "баланс": балл_баланса,
        "размер": балл_размера,
    }

    return round(общая, 1), детали


def улучшить_контраст(путь, выход):
    """Повышение контраста изображения."""
    img = Image.open(путь)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.15)  # +15% контраста
    img.save(выход, "PNG", quality=95)
    return выход


def добавить_тень_тексту(путь, выход):
    """
    Добавление эффекта тени/глоу вокруг светлых областей.
    Улучшает читаемость текста на сложном фоне.
    """
    img = Image.open(путь).convert("RGBA")
    width, height = img.size

    # Создаём слой с лёгким затемнением по краям (виньетка)
    виньетка = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(виньетка)

    # Градиент от центра к краям
    center_x = width // 2
    center_y = height // 2
    max_dist = (center_x ** 2 + center_y ** 2) ** 0.5

    for y in range(0, height, 2):  # Через пиксель для скорости
        for x in range(0, width, 2):
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            t = dist / max_dist
            if t > 0.6:
                alpha = int((t - 0.6) * 60)  # Мягкая виньетка
                v_draw.rectangle([x, y, x + 1, y + 1], fill=(0, 0, 0, alpha))

    result = Image.alpha_composite(img, виньетка)
    result.convert("RGB").save(выход, "PNG", quality=95)
    return выход


def улучшить_яркость(путь, выход):
    """Коррекция яркости для лучшего баланса."""
    img = Image.open(путь)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.05)  # +5% яркости
    img.save(выход, "PNG", quality=95)
    return выход


def улучшить_резкость(путь, выход):
    """Лёгкое повышение резкости."""
    img = Image.open(путь)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)  # +20% резкости
    img.save(выход, "PNG", quality=95)
    return выход


def автоулучшение(путь, детали, итерация=1):
    """
    Автоматическое улучшение на основе слабых метрик.
    Возвращает путь к улучшенному файлу.
    """
    print(f"\n  Итерация улучшения #{итерация}")
    tmp = путь.replace(".png", f"_improved_{итерация}.png")

    улучшения = []

    # Если контраст/палитра низкие — подкрутить контраст
    if детали.get("контраст", 10) < 7 or детали.get("палитра", 10) < 7:
        улучшить_контраст(путь, tmp)
        путь = tmp
        улучшения.append("контраст +15%")

    # Если баланс плохой — добавить виньетку для фокусировки
    if детали.get("баланс", 10) < 6:
        добавить_тень_тексту(путь, tmp)
        путь = tmp
        улучшения.append("виньетка для фокуса")

    # Если сложность не в норме
    if детали.get("сложность", 10) < 5:
        улучшить_резкость(путь, tmp)
        путь = tmp
        улучшения.append("резкость +20%")

    # Если воздуха мало (всё слишком плотно)
    if детали.get("воздух", 10) < 5:
        улучшить_яркость(путь, tmp)
        путь = tmp
        улучшения.append("яркость +5%")

    if not улучшения:
        # Если ничего конкретного — общее улучшение контраста
        улучшить_контраст(путь, tmp)
        путь = tmp
        улучшения.append("общий контраст +15%")

    print(f"  Применено: {', '.join(улучшения)}")
    return путь


def пайплайн(task, marketplace=None, title=None, subtitle=None,
             style="tech", output="result.png", initials=None,
             palette=None, size=None):
    """
    Основной пайплайн: генерация → проверка → улучшение → финал.

    Args:
        task: Тип задачи (cover|avatar|banner)
        marketplace: Биржа (для cover)
        title: Заголовок
        subtitle: Подзаголовок
        style: Стиль
        output: Путь к финальному файлу
        initials: Инициалы (для avatar)
        palette: Палитра (для banner/avatar)
        size: Размер (для banner)
    """
    print("=" * 60)
    print(f"ПАЙПЛАЙН ДИЗАЙНА: {task.upper()}")
    print("=" * 60)

    # Промежуточный файл
    tmp_output = output.replace(".png", "_draft.png")

    # === ШАГ 1: Генерация ===
    print("\n[1/3] Генерация...")

    if task == "cover":
        if not marketplace:
            print("Ошибка: для cover нужен --marketplace")
            sys.exit(1)
        if not title:
            print("Ошибка: для cover нужен --title")
            sys.exit(1)
        создать_обложку = импорт_обложки()
        создать_обложку(
            marketplace=marketplace,
            title=title,
            subtitle=subtitle,
            style=style,
            output=tmp_output,
        )

    elif task == "banner":
        if not title:
            print("Ошибка: для banner нужен --title")
            sys.exit(1)
        kwargs = {
            "текст": title,
            "подзаголовок": subtitle or "",
            "выход": tmp_output,
        }
        if palette:
            kwargs["палитра"] = palette
        if size:
            kwargs["размер"] = size
        создать_баннер(**kwargs)

    elif task == "avatar":
        if not initials and not title:
            print("Ошибка: для avatar нужен --title (инициалы)")
            sys.exit(1)
        текст = initials or title
        kwargs = {
            "текст": текст,
            "выход": tmp_output,
        }
        if palette:
            kwargs["палитра"] = palette
        создать_аватарку(**kwargs)

    else:
        print(f"Ошибка: неизвестная задача '{task}'")
        sys.exit(1)

    # === ШАГ 2: Проверка ===
    print("\n[2/3] Проверка качества...")
    оценка, детали = оценить_изображение(tmp_output)
    print(f"  Оценка: {оценка}/10")
    for метрика, значение in детали.items():
        бар = "█" * int(значение) + "░" * (10 - int(значение))
        print(f"  {метрика:15s} [{бар}] {значение}/10")

    # === ШАГ 3: Доработка (если оценка < 7) ===
    текущий = tmp_output
    макс_итераций = 3
    итерация = 0

    while оценка < 7 and итерация < макс_итераций:
        итерация += 1
        print(f"\n[3/3] Автоулучшение (оценка {оценка} < 7)...")
        текущий = автоулучшение(текущий, детали, итерация)

        # Повторная проверка
        оценка, детали = оценить_изображение(текущий)
        print(f"  Новая оценка: {оценка}/10")
        for метрика, значение in детали.items():
            бар = "█" * int(значение) + "░" * (10 - int(значение))
            print(f"  {метрика:15s} [{бар}] {значение}/10")

    if оценка >= 7:
        print(f"\n✓ Качество достаточное: {оценка}/10")
    else:
        print(f"\n⚠ Достигнут лимит итераций. Оценка: {оценка}/10")

    # Сохраняем финальный результат
    from PIL import Image as PILImage
    final = PILImage.open(текущий)
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    final.save(output, "PNG", quality=95)

    # Очистка промежуточных файлов
    for f in [tmp_output] + [
        output.replace(".png", f"_improved_{i}.png") for i in range(1, макс_итераций + 1)
    ]:
        if f != output and os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass

    print(f"\nФинал: {output}")
    print(f"Итоговая оценка: {оценка}/10")
    print("=" * 60)

    return output, оценка


def main():
    parser = argparse.ArgumentParser(
        description="Автопайплайн дизайна: генерация → проверка → доработка"
    )
    parser.add_argument(
        "--task", required=True,
        choices=["cover", "avatar", "banner"],
        help="Тип задачи"
    )
    parser.add_argument(
        "--marketplace", default=None,
        choices=["fiverr", "kwork", "freelanceru", "upwork"],
        help="Биржа (для cover)"
    )
    parser.add_argument(
        "--title", default=None,
        help="Заголовок / инициалы"
    )
    parser.add_argument(
        "--subtitle", default=None,
        help="Подзаголовок"
    )
    parser.add_argument(
        "--style", default="tech",
        choices=["tech", "business", "creative", "minimal"],
        help="Стиль оформления (для cover)"
    )
    parser.add_argument(
        "--palette", default=None,
        help="Палитра (для banner/avatar)"
    )
    parser.add_argument(
        "--size", default=None,
        help="Размер (для banner, например 1920x1080)"
    )
    parser.add_argument(
        "--output", default="result.png",
        help="Путь для сохранения"
    )
    args = parser.parse_args()

    пайплайн(
        task=args.task,
        marketplace=args.marketplace,
        title=args.title,
        subtitle=args.subtitle,
        style=args.style,
        output=args.output,
        palette=args.palette,
        size=args.size,
    )


if __name__ == "__main__":
    main()
