#!/usr/bin/env python3
"""
Массовая генерация обложек из CSV-файла.
Читает CSV, генерирует обложки, опционально добавляет водяной знак,
прогоняет через check_design и выводит сводку.
"""

import argparse
import csv
import os
import re
import sys

# Добавляем директорию скриптов в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_marketplace_cover import создать_обложку
from check_design import проверить_дизайн
from watermark import добавить_водяной_знак


def транслитерация(текст):
    """Простая транслитерация кириллицы в латиницу для имён файлов."""
    таблица = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
    результат = []
    for символ in текст.lower():
        if символ in таблица:
            результат.append(таблица[символ])
        elif символ.isalnum():
            результат.append(символ)
        elif символ in (" ", "-", "_"):
            результат.append("_")
    # Убираем повторяющиеся подчёркивания
    имя = re.sub(r"_+", "_", "".join(результат)).strip("_")
    return имя


def пакетная_генерация(csv_path, output_dir, marketplace, watermark=False):
    """
    Массовая генерация обложек из CSV.

    Args:
        csv_path: Путь к CSV-файлу
        output_dir: Директория для результатов
        marketplace: Биржа (fiverr|kwork|freelanceru|upwork)
        watermark: Добавлять ли водяной знак
    """
    # Проверяем CSV
    if not os.path.exists(csv_path):
        print(f"Ошибка: файл не найден: {csv_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # Читаем CSV
    записи = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                записи.append(row)
    except Exception as e:
        print(f"Ошибка чтения CSV: {e}")
        sys.exit(1)

    if not записи:
        print("CSV-файл пуст или не содержит данных")
        sys.exit(1)

    print(f"Найдено записей: {len(записи)}")
    print(f"Биржа: {marketplace}")
    print(f"Водяной знак: {'да' if watermark else 'нет'}")
    print("=" * 60)

    результаты = []
    ошибки = 0

    for i, запись in enumerate(записи, 1):
        title = запись.get("title", "").strip()
        subtitle = запись.get("subtitle", "").strip() or None
        style = запись.get("style", "tech").strip()

        if not title:
            print(f"\n[{i}/{len(записи)}] Пропуск: пустой заголовок")
            ошибки += 1
            continue

        # Имя файла: порядковый номер + транслитерация заголовка
        slug = транслитерация(title)[:40]  # Ограничиваем длину
        имя_файла = f"{i:03d}_{slug}.png"
        путь = os.path.join(output_dir, имя_файла)

        print(f"\n[{i}/{len(записи)}] «{title}»")
        print(f"  Стиль: {style}, файл: {имя_файла}")

        try:
            # Генерируем обложку
            создать_обложку(
                marketplace=marketplace,
                title=title,
                subtitle=subtitle,
                style=style,
                output=путь,
            )

            # Добавляем водяной знак
            if watermark:
                добавить_водяной_знак(
                    image_path=путь,
                    text="© AlexKZ AI",
                    position="bottom_right",
                    opacity=0.3,
                    font_size=24,
                    output=путь,
                )

            # Проверяем качество
            оценка = проверить_дизайн(путь)

            результаты.append({
                "номер": i,
                "title": title,
                "style": style,
                "файл": имя_файла,
                "оценка": оценка,
            })

        except Exception as e:
            print(f"  Ошибка: {e}")
            ошибки += 1

    # Сводка
    if not результаты:
        print("\nНи одна обложка не была создана")
        sys.exit(1)

    оценки = [р["оценка"] for р in результаты]
    средняя = sum(оценки) / len(оценки)
    лучший = max(результаты, key=lambda x: x["оценка"])
    худший = min(результаты, key=lambda x: x["оценка"])

    print("\n" + "=" * 60)
    print("СВОДКА ПАКЕТНОЙ ГЕНЕРАЦИИ")
    print("=" * 60)
    print(f"  Создано обложек:  {len(результаты)}/{len(записи)}")
    if ошибки:
        print(f"  Ошибок:           {ошибки}")
    print(f"  Средняя оценка:   {средняя:.1f}/10")
    print(f"  Лучшая:           {лучший['оценка']}/10 — «{лучший['title']}» ({лучший['файл']})")
    print(f"  Худшая:           {худший['оценка']}/10 — «{худший['title']}» ({худший['файл']})")
    print(f"  Водяной знак:     {'да' if watermark else 'нет'}")

    print(f"\n{'№':<5} {'Файл':<35} {'Стиль':<12} {'Оценка'}")
    print("-" * 60)
    for р in результаты:
        print(f"  {р['номер']:<3} {р['файл']:<35} {р['style']:<12} {р['оценка']}/10")

    print(f"\nРезультаты в: {os.path.abspath(output_dir)}")

    return результаты


def main():
    parser = argparse.ArgumentParser(
        description="Массовая генерация обложек из CSV-файла"
    )
    parser.add_argument(
        "--csv", required=True,
        help="Путь к CSV-файлу (колонки: title, subtitle, style)"
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="Директория для результатов"
    )
    parser.add_argument(
        "--marketplace", required=True,
        choices=["fiverr", "kwork", "freelanceru", "upwork"],
        help="Биржа (определяет размер)"
    )
    parser.add_argument(
        "--watermark", action="store_true",
        help="Добавить водяной знак на каждую обложку"
    )
    args = parser.parse_args()

    пакетная_генерация(
        csv_path=args.csv,
        output_dir=args.output_dir,
        marketplace=args.marketplace,
        watermark=args.watermark,
    )


if __name__ == "__main__":
    main()
