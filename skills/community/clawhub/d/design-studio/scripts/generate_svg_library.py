#!/usr/bin/env python3
"""
Генератор SVG-библиотеки элементов для дизайн-студии.
Создаёт иконки, значки, фигуры и рамки в формате SVG через svgwrite.
Все элементы: чистые, минималистичные, масштабируемые.
Цвет по умолчанию: #FFFFFF. Размер viewBox: 100×100.
"""

import argparse
import os
import sys

try:
    import svgwrite
except ImportError:
    print("Ошибка: svgwrite не установлен. Установите: pip install svgwrite")
    sys.exit(1)

# Базовая директория для SVG-библиотеки
DEFAULT_OUTPUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "references", "svg_elements"
)

# Цвет по умолчанию
DEFAULT_COLOR = "#FFFFFF"
VIEWBOX = "0 0 100 100"
SIZE = ("100", "100")


def создать_svg(имя_файла, output_dir):
    """Создание чистого SVG-документа с viewBox 100×100."""
    путь = os.path.join(output_dir, имя_файла)
    os.makedirs(os.path.dirname(путь), exist_ok=True)
    dwg = svgwrite.Drawing(
        путь,
        size=SIZE,
        viewBox=VIEWBOX,
    )
    return dwg, путь


# ============================
# ИКОНКИ (icons/)
# ============================

def иконка_звезда(output_dir):
    """Пятиконечная звезда."""
    dwg, путь = создать_svg("icons/star.svg", output_dir)
    import math
    # Вершины пятиконечной звезды
    points = []
    cx, cy, r_outer, r_inner = 50, 50, 40, 16
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = r_outer if i % 2 == 0 else r_inner
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    dwg.add(dwg.polygon(points, fill=DEFAULT_COLOR, stroke="none"))
    dwg.save()
    return путь


def иконка_галочка(output_dir):
    """Галочка (checkmark)."""
    dwg, путь = создать_svg("icons/checkmark.svg", output_dir)
    dwg.add(dwg.polyline(
        points=[(20, 55), (40, 75), (80, 25)],
        fill="none", stroke=DEFAULT_COLOR,
        stroke_width=8, stroke_linecap="round", stroke_linejoin="round"
    ))
    dwg.save()
    return путь


def иконка_стрелка_вправо(output_dir):
    """Стрелка вправо."""
    dwg, путь = создать_svg("icons/arrow_right.svg", output_dir)
    # Линия
    dwg.add(dwg.line(
        start=(20, 50), end=(80, 50),
        stroke=DEFAULT_COLOR, stroke_width=6, stroke_linecap="round"
    ))
    # Наконечник
    dwg.add(dwg.polyline(
        points=[(60, 30), (80, 50), (60, 70)],
        fill="none", stroke=DEFAULT_COLOR,
        stroke_width=6, stroke_linecap="round", stroke_linejoin="round"
    ))
    dwg.save()
    return путь


def иконка_код(output_dir):
    """Угловые скобки кода < >."""
    dwg, путь = создать_svg("icons/code_brackets.svg", output_dir)
    # Левая скобка <
    dwg.add(dwg.polyline(
        points=[(35, 25), (15, 50), (35, 75)],
        fill="none", stroke=DEFAULT_COLOR,
        stroke_width=6, stroke_linecap="round", stroke_linejoin="round"
    ))
    # Правая скобка >
    dwg.add(dwg.polyline(
        points=[(65, 25), (85, 50), (65, 75)],
        fill="none", stroke=DEFAULT_COLOR,
        stroke_width=6, stroke_linecap="round", stroke_linejoin="round"
    ))
    # Слэш /
    dwg.add(dwg.line(
        start=(55, 20), end=(45, 80),
        stroke=DEFAULT_COLOR, stroke_width=4, stroke_linecap="round"
    ))
    dwg.save()
    return путь


def иконка_молния(output_dir):
    """Молния / lightning bolt."""
    dwg, путь = создать_svg("icons/lightning.svg", output_dir)
    dwg.add(dwg.polygon(
        points=[(55, 5), (25, 52), (45, 52), (40, 95), (75, 42), (52, 42)],
        fill=DEFAULT_COLOR, stroke="none"
    ))
    dwg.save()
    return путь


def иконка_шестерёнка(output_dir):
    """Шестерёнка / gear."""
    dwg, путь = создать_svg("icons/gear.svg", output_dir)
    import math
    cx, cy = 50, 50
    # Внешний контур с зубцами
    points = []
    teeth = 8
    r_outer = 42
    r_inner = 32
    r_tooth = 38
    for i in range(teeth * 2):
        angle = math.radians(i * 360 / (teeth * 2) - 90)
        r = r_outer if i % 2 == 0 else r_tooth
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    dwg.add(dwg.polygon(points, fill=DEFAULT_COLOR, stroke="none"))
    # Внутреннее отверстие (круг)
    dwg.add(dwg.circle(center=(cx, cy), r=15, fill="black"))
    # Чтобы отверстие было прозрачным, используем маску
    # Альтернатива: рисуем через path
    dwg.save()
    return путь


def иконка_график(output_dir):
    """График вверх / chart up."""
    dwg, путь = создать_svg("icons/chart_up.svg", output_dir)
    # Оси
    dwg.add(dwg.line(
        start=(15, 85), end=(15, 15),
        stroke=DEFAULT_COLOR, stroke_width=4, stroke_linecap="round"
    ))
    dwg.add(dwg.line(
        start=(15, 85), end=(85, 85),
        stroke=DEFAULT_COLOR, stroke_width=4, stroke_linecap="round"
    ))
    # Линия графика (восходящая)
    dwg.add(dwg.polyline(
        points=[(20, 70), (35, 55), (50, 60), (65, 35), (80, 20)],
        fill="none", stroke=DEFAULT_COLOR,
        stroke_width=5, stroke_linecap="round", stroke_linejoin="round"
    ))
    # Стрелка на конце
    dwg.add(dwg.polyline(
        points=[(72, 18), (80, 20), (78, 28)],
        fill="none", stroke=DEFAULT_COLOR,
        stroke_width=4, stroke_linecap="round", stroke_linejoin="round"
    ))
    dwg.save()
    return путь


def иконка_доллар(output_dir):
    """Символ доллара."""
    dwg, путь = создать_svg("icons/dollar.svg", output_dir)
    # Вертикальная линия
    dwg.add(dwg.line(
        start=(50, 15), end=(50, 85),
        stroke=DEFAULT_COLOR, stroke_width=5, stroke_linecap="round"
    ))
    # Верхняя дуга S
    dwg.add(dwg.path(
        d="M 65,32 C 65,22 55,20 50,20 C 40,20 32,25 32,35 C 32,45 42,48 50,50",
        fill="none", stroke=DEFAULT_COLOR,
        stroke_width=5, stroke_linecap="round"
    ))
    # Нижняя дуга S
    dwg.add(dwg.path(
        d="M 35,68 C 35,78 45,80 50,80 C 60,80 68,75 68,65 C 68,55 58,52 50,50",
        fill="none", stroke=DEFAULT_COLOR,
        stroke_width=5, stroke_linecap="round"
    ))
    dwg.save()
    return путь


def иконка_часы(output_dir):
    """Часы / clock."""
    dwg, путь = создать_svg("icons/clock.svg", output_dir)
    # Циферблат
    dwg.add(dwg.circle(
        center=(50, 50), r=38,
        fill="none", stroke=DEFAULT_COLOR, stroke_width=5
    ))
    # Часовая стрелка
    dwg.add(dwg.line(
        start=(50, 50), end=(50, 28),
        stroke=DEFAULT_COLOR, stroke_width=5, stroke_linecap="round"
    ))
    # Минутная стрелка
    dwg.add(dwg.line(
        start=(50, 50), end=(68, 50),
        stroke=DEFAULT_COLOR, stroke_width=4, stroke_linecap="round"
    ))
    # Центральная точка
    dwg.add(dwg.circle(center=(50, 50), r=3, fill=DEFAULT_COLOR))
    dwg.save()
    return путь


def иконка_щит(output_dir):
    """Щит / shield."""
    dwg, путь = создать_svg("icons/shield.svg", output_dir)
    dwg.add(dwg.path(
        d="M 50,10 L 82,25 L 82,50 C 82,72 68,85 50,92 C 32,85 18,72 18,50 L 18,25 Z",
        fill=DEFAULT_COLOR, stroke="none"
    ))
    dwg.save()
    return путь


# ============================
# ЗНАЧКИ (badges/)
# ============================

def значок_бестселлер(output_dir):
    """Значок «Бестселлер» — лента со звездой."""
    dwg, путь = создать_svg("badges/bestseller.svg", output_dir)
    import math
    # Круг-основа
    dwg.add(dwg.circle(center=(50, 42), r=32, fill=DEFAULT_COLOR))
    # Лента снизу
    dwg.add(dwg.polygon(
        points=[(30, 65), (50, 90), (70, 65), (70, 75), (50, 95), (30, 75)],
        fill=DEFAULT_COLOR, stroke="none"
    ))
    # Звезда внутри (тёмная)
    points = []
    cx, cy, r_outer, r_inner = 50, 40, 18, 7
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = r_outer if i % 2 == 0 else r_inner
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    dwg.add(dwg.polygon(points, fill="black", stroke="none"))
    dwg.save()
    return путь


def значок_новый(output_dir):
    """Значок «NEW» — прямоугольник с текстом."""
    dwg, путь = создать_svg("badges/new.svg", output_dir)
    dwg.add(dwg.rect(
        insert=(10, 30), size=(80, 40),
        rx=8, ry=8, fill=DEFAULT_COLOR
    ))
    dwg.add(dwg.text(
        "NEW", insert=(50, 57),
        text_anchor="middle",
        font_size="22", font_weight="bold",
        font_family="sans-serif", fill="black"
    ))
    dwg.save()
    return путь


def значок_премиум(output_dir):
    """Значок «Premium» — ромб с короной."""
    dwg, путь = создать_svg("badges/premium.svg", output_dir)
    # Ромб
    dwg.add(dwg.polygon(
        points=[(50, 8), (90, 50), (50, 92), (10, 50)],
        fill=DEFAULT_COLOR, stroke="none"
    ))
    # Корона (упрощённая, тёмная)
    dwg.add(dwg.polygon(
        points=[(30, 55), (35, 38), (42, 48), (50, 32), (58, 48), (65, 38), (70, 55)],
        fill="black", stroke="none"
    ))
    dwg.save()
    return путь


def значок_верификация(output_dir):
    """Значок «Verified» — круг с галочкой."""
    dwg, путь = создать_svg("badges/verified.svg", output_dir)
    dwg.add(dwg.circle(center=(50, 50), r=40, fill=DEFAULT_COLOR))
    dwg.add(dwg.polyline(
        points=[(28, 50), (42, 65), (72, 35)],
        fill="none", stroke="black",
        stroke_width=8, stroke_linecap="round", stroke_linejoin="round"
    ))
    dwg.save()
    return путь


def значок_горячее(output_dir):
    """Значок «Hot» — пламя."""
    dwg, путь = создать_svg("badges/hot.svg", output_dir)
    dwg.add(dwg.path(
        d="M 50,8 C 55,30 72,35 72,55 C 72,72 62,88 50,90 "
          "C 38,88 28,72 28,55 C 28,35 45,30 50,8 Z",
        fill=DEFAULT_COLOR, stroke="none"
    ))
    # Внутреннее пламя (тёмное)
    dwg.add(dwg.path(
        d="M 50,40 C 52,50 60,52 60,62 C 60,72 55,78 50,80 "
          "C 45,78 40,72 40,62 C 40,52 48,50 50,40 Z",
        fill="black", stroke="none"
    ))
    dwg.save()
    return путь


# ============================
# ФИГУРЫ (shapes/)
# ============================

def фигура_круг(output_dir):
    """Круг."""
    dwg, путь = создать_svg("shapes/circle.svg", output_dir)
    dwg.add(dwg.circle(center=(50, 50), r=40, fill=DEFAULT_COLOR))
    dwg.save()
    return путь


def фигура_шестиугольник(output_dir):
    """Правильный шестиугольник."""
    dwg, путь = создать_svg("shapes/hexagon.svg", output_dir)
    import math
    points = []
    for i in range(6):
        angle = math.radians(i * 60 - 30)
        x = 50 + 42 * math.cos(angle)
        y = 50 + 42 * math.sin(angle)
        points.append((x, y))
    dwg.add(dwg.polygon(points, fill=DEFAULT_COLOR, stroke="none"))
    dwg.save()
    return путь


def фигура_ромб(output_dir):
    """Ромб / diamond."""
    dwg, путь = создать_svg("shapes/diamond.svg", output_dir)
    dwg.add(dwg.polygon(
        points=[(50, 5), (95, 50), (50, 95), (5, 50)],
        fill=DEFAULT_COLOR, stroke="none"
    ))
    dwg.save()
    return путь


def фигура_волна(output_dir):
    """Волнистый разделитель."""
    dwg, путь = создать_svg("shapes/wave_divider.svg", output_dir)
    dwg.add(dwg.path(
        d="M 0,60 C 15,40 30,70 50,50 C 70,30 85,60 100,45 L 100,100 L 0,100 Z",
        fill=DEFAULT_COLOR, stroke="none"
    ))
    dwg.save()
    return путь


def фигура_угловой_декор(output_dir):
    """Угловое украшение (для углов дизайна)."""
    dwg, путь = создать_svg("shapes/corner_decoration.svg", output_dir)
    # Линии в углу
    dwg.add(dwg.line(
        start=(5, 5), end=(5, 40),
        stroke=DEFAULT_COLOR, stroke_width=3, stroke_linecap="round"
    ))
    dwg.add(dwg.line(
        start=(5, 5), end=(40, 5),
        stroke=DEFAULT_COLOR, stroke_width=3, stroke_linecap="round"
    ))
    # Точка в углу
    dwg.add(dwg.circle(center=(5, 5), r=4, fill=DEFAULT_COLOR))
    # Декоративные элементы
    dwg.add(dwg.line(
        start=(12, 12), end=(12, 30),
        stroke=DEFAULT_COLOR, stroke_width=1.5, stroke_linecap="round"
    ))
    dwg.add(dwg.line(
        start=(12, 12), end=(30, 12),
        stroke=DEFAULT_COLOR, stroke_width=1.5, stroke_linecap="round"
    ))
    dwg.save()
    return путь


# ============================
# РАМКИ (frames/)
# ============================

def рамка_простая(output_dir):
    """Простая прямоугольная рамка."""
    dwg, путь = создать_svg("frames/simple_frame.svg", output_dir)
    dwg.add(dwg.rect(
        insert=(5, 5), size=(90, 90),
        fill="none", stroke=DEFAULT_COLOR, stroke_width=3
    ))
    dwg.save()
    return путь


def рамка_скруглённая(output_dir):
    """Рамка с закруглёнными углами."""
    dwg, путь = создать_svg("frames/rounded_frame.svg", output_dir)
    dwg.add(dwg.rect(
        insert=(5, 5), size=(90, 90),
        rx=12, ry=12,
        fill="none", stroke=DEFAULT_COLOR, stroke_width=3
    ))
    dwg.save()
    return путь


def рамка_техно(output_dir):
    """Техно-рамка с угловыми элементами и линиями."""
    dwg, путь = создать_svg("frames/tech_frame.svg", output_dir)
    # Основная рамка (пунктирная)
    dwg.add(dwg.rect(
        insert=(10, 10), size=(80, 80),
        fill="none", stroke=DEFAULT_COLOR, stroke_width=1,
        stroke_dasharray="4,3"
    ))
    # Угловые элементы — утолщённые линии
    длина = 20
    толщина = 3
    углы = [
        # Верхний левый
        [(5, 5), (5, 5 + длина)],
        [(5, 5), (5 + длина, 5)],
        # Верхний правый
        [(95, 5), (95, 5 + длина)],
        [(95, 5), (95 - длина, 5)],
        # Нижний левый
        [(5, 95), (5, 95 - длина)],
        [(5, 95), (5 + длина, 95)],
        # Нижний правый
        [(95, 95), (95, 95 - длина)],
        [(95, 95), (95 - длина, 95)],
    ]
    for start, end in углы:
        dwg.add(dwg.line(
            start=start, end=end,
            stroke=DEFAULT_COLOR, stroke_width=толщина, stroke_linecap="round"
        ))
    # Точки в углах
    for x, y in [(5, 5), (95, 5), (5, 95), (95, 95)]:
        dwg.add(dwg.circle(center=(x, y), r=2.5, fill=DEFAULT_COLOR))
    dwg.save()
    return путь


# ============================
# ГЕНЕРАЦИЯ ВСЕЙ БИБЛИОТЕКИ
# ============================

def генерировать_библиотеку(output_dir=None):
    """Генерация полной SVG-библиотеки."""
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT

    print(f"Генерация SVG-библиотеки в: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    # Все генераторы
    элементы = {
        "icons/star.svg": иконка_звезда,
        "icons/checkmark.svg": иконка_галочка,
        "icons/arrow_right.svg": иконка_стрелка_вправо,
        "icons/code_brackets.svg": иконка_код,
        "icons/lightning.svg": иконка_молния,
        "icons/gear.svg": иконка_шестерёнка,
        "icons/chart_up.svg": иконка_график,
        "icons/dollar.svg": иконка_доллар,
        "icons/clock.svg": иконка_часы,
        "icons/shield.svg": иконка_щит,
        "badges/bestseller.svg": значок_бестселлер,
        "badges/new.svg": значок_новый,
        "badges/premium.svg": значок_премиум,
        "badges/verified.svg": значок_верификация,
        "badges/hot.svg": значок_горячее,
        "shapes/circle.svg": фигура_круг,
        "shapes/hexagon.svg": фигура_шестиугольник,
        "shapes/diamond.svg": фигура_ромб,
        "shapes/wave_divider.svg": фигура_волна,
        "shapes/corner_decoration.svg": фигура_угловой_декор,
        "frames/simple_frame.svg": рамка_простая,
        "frames/rounded_frame.svg": рамка_скруглённая,
        "frames/tech_frame.svg": рамка_техно,
    }

    создано = 0
    for имя, функция in элементы.items():
        try:
            путь = функция(output_dir)
            print(f"  ✓ {имя}")
            создано += 1
        except Exception as e:
            print(f"  ✗ {имя}: {e}")

    print(f"\nСоздано: {создано}/{len(элементы)} элементов")
    print(f"Директория: {output_dir}")

    # Вывод структуры
    print("\nСтруктура:")
    for категория in ["icons", "badges", "shapes", "frames"]:
        кат_dir = os.path.join(output_dir, категория)
        if os.path.isdir(кат_dir):
            файлы = sorted(os.listdir(кат_dir))
            print(f"  {категория}/")
            for f in файлы:
                print(f"    {f}")

    return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Генератор SVG-библиотеки элементов"
    )
    parser.add_argument(
        "--output", default=None,
        help=f"Директория для сохранения (по умолчанию: {DEFAULT_OUTPUT})"
    )
    args = parser.parse_args()

    генерировать_библиотеку(output_dir=args.output)


if __name__ == "__main__":
    main()
