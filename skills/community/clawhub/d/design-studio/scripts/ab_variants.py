#!/usr/bin/env python3
"""
Генератор A/B вариантов обложки.
Создаёт 3-4 варианта одной обложки с разными палитрами для сравнения.
Прогоняет каждый через check_design.py и выводит таблицу с оценками.
"""

import argparse
import os
import sys

# Добавляем директорию скриптов в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_marketplace_cover import создать_обложку, STYLE_PALETTES
from check_design import проверить_дизайн


# Палитры для A/B тестирования (tech, business, creative, minimal)
AB_ПАЛИТРЫ = ["tech", "business", "creative", "minimal"]


def генерировать_варианты(title, marketplace, subtitle=None, variants=4, output_dir="ab_variants"):
    """
    Генерирует несколько вариантов обложки с разными палитрами.

    Args:
        title: Текст заголовка
        marketplace: Биржа (fiverr|kwork|freelanceru|upwork)
        subtitle: Подзаголовок (опционально)
        variants: Количество вариантов (1-4)
        output_dir: Директория для результатов
    """
    # Ограничиваем количество вариантов количеством доступных палитр
    variants = min(variants, len(AB_ПАЛИТРЫ))

    os.makedirs(output_dir, exist_ok=True)

    результаты = []

    print(f"Генерация {variants} вариантов для «{title}»")
    print(f"Биржа: {marketplace}")
    print("=" * 60)

    for i in range(variants):
        палитра = AB_ПАЛИТРЫ[i]
        файл = os.path.join(output_dir, f"variant_{i + 1}.png")

        print(f"\n--- Вариант {i + 1}: палитра «{палитра}» ---")

        # Генерируем обложку
        создать_обложку(
            marketplace=marketplace,
            title=title,
            subtitle=subtitle,
            style=палитра,
            output=файл,
        )

        # Проверяем качество
        print(f"\nПроверка варианта {i + 1}:")
        оценка = проверить_дизайн(файл)

        результаты.append({
            "номер": i + 1,
            "палитра": палитра,
            "файл": файл,
            "оценка": оценка,
        })

    # Находим лучший вариант
    лучший = max(результаты, key=lambda x: x["оценка"])

    # Выводим итоговую таблицу
    print("\n" + "=" * 60)
    print("СВОДНАЯ ТАБЛИЦА A/B ВАРИАНТОВ")
    print("=" * 60)
    print(f"{'Вариант':<10} {'Палитра':<12} {'Оценка':<8} {'Статус'}")
    print("-" * 45)

    for р in результаты:
        статус = "★ ЛУЧШИЙ" if р["номер"] == лучший["номер"] else ""
        print(f"  {р['номер']:<8} {р['палитра']:<12} {р['оценка']:<8} {статус}")

    print("-" * 45)
    print(f"\nЛучший вариант: №{лучший['номер']} (палитра «{лучший['палитра']}», оценка {лучший['оценка']}/10)")
    print(f"Файл: {лучший['файл']}")

    # Сохраняем отчёт
    отчёт_путь = os.path.join(output_dir, "report.txt")
    with open(отчёт_путь, "w", encoding="utf-8") as f:
        f.write(f"A/B тестирование обложки\n")
        f.write(f"Заголовок: {title}\n")
        if subtitle:
            f.write(f"Подзаголовок: {subtitle}\n")
        f.write(f"Биржа: {marketplace}\n")
        f.write(f"Количество вариантов: {variants}\n")
        f.write(f"\n{'Вариант':<10} {'Палитра':<12} {'Оценка':<8} {'Статус'}\n")
        f.write("-" * 45 + "\n")
        for р in результаты:
            статус = "★ ЛУЧШИЙ" if р["номер"] == лучший["номер"] else ""
            f.write(f"  {р['номер']:<8} {р['палитра']:<12} {р['оценка']:<8} {статус}\n")
        f.write(f"\nЛучший: вариант №{лучший['номер']} — {лучший['палитра']} ({лучший['оценка']}/10)\n")

    print(f"Отчёт сохранён: {отчёт_путь}")

    return результаты


def main():
    parser = argparse.ArgumentParser(
        description="Генерация A/B вариантов обложки с разными палитрами"
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
        "--marketplace", required=True,
        choices=["fiverr", "kwork", "freelanceru", "upwork"],
        help="Биржа (определяет размер)"
    )
    parser.add_argument(
        "--variants", type=int, default=4,
        choices=[1, 2, 3, 4],
        help="Количество вариантов (по умолчанию 4)"
    )
    parser.add_argument(
        "--output-dir", default="ab_variants",
        help="Директория для результатов"
    )
    args = parser.parse_args()

    генерировать_варианты(
        title=args.title,
        marketplace=args.marketplace,
        subtitle=args.subtitle,
        variants=args.variants,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
