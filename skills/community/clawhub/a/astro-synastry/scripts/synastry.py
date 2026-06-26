#!/usr/bin/env python3
"""
Synastry Calculator — compatibility analysis between two natal charts.
Uses planetary positions from natal_chart.py.
No external dependencies required.
"""

import math
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ─── Import natal chart functions ───
# We import from the sibling skill's script directory
import importlib.util
import os

# Load natal_chart module from astro-natal-chart skill
NATAL_CHART_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", "astro-natal-chart", "scripts", "natal_chart.py"
)
NATAL_CHART_PATH = os.path.normpath(NATAL_CHART_PATH)

spec = importlib.util.spec_from_file_location("natal_chart", NATAL_CHART_PATH)
nc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nc)

# ─── Constants ───

PLANETS = nc.PLANETS
SIGNS = nc.SIGNS

# Synastry orbs (tighter than natal)
SYNSTRY_ORBS = {
    "conjunction": 7,
    "opposition": 7,
    "trine": 6,
    "square": 6,
    "sextile": 4,
    "semisextile": 1.5,
    "semisquare": 1.5,
    "quincunx": 1.5,
}

# Aspect scoring
ASPECT_SCORES = {
    "conjunction": 3,    # Can be positive or negative depending on planets
    "trine": 5,          # Very harmonious
    "sextile": 3,        # Harmonious
    "opposition": -1,    # Mixed — can be complementary or conflicting
    "square": -3,        # Tension
    "semisextile": 1,    # Mild positive
    "semisquare": -1,    # Mild tension
    "quincunx": -1,      # Adjustment needed
}

# Key planet pairs and their weights
KEY_PAIRS = {
    ("Sun", "Sun"): 3.0,
    ("Moon", "Moon"): 3.0,
    ("Sun", "Moon"): 4.0,
    ("Moon", "Sun"): 4.0,
    ("Venus", "Mars"): 4.0,
    ("Mars", "Venus"): 4.0,
    ("Venus", "Venus"): 2.0,
    ("Mars", "Mars"): 2.0,
    ("Mercury", "Mercury"): 1.5,
    ("Jupiter", "Jupiter"): 1.5,
    ("Saturn", "Sun"): 2.5,
    ("Saturn", "Moon"): 2.5,
    ("Sun", "Saturn"): 2.5,
    ("Moon", "Saturn"): 2.5,
    ("Pluto", "Sun"): 2.0,
    ("Pluto", "Moon"): 2.0,
    ("Sun", "Pluto"): 2.0,
    ("Moon", "Pluto"): 2.0,
    ("Uranus", "Venus"): 1.5,
    ("Neptune", "Venus"): 1.5,
}

HOUSE_MEANINGS = {
    1: "личность и самовыражение",
    2: "финансы и ценности",
    3: "общение и окружение",
    4: "дом и семья",
    5: "романтика и творчество",
    6: "работа и здоровье",
    7: "партнёрство и брак",
    8: "трансформация и близость",
    9: "философия и путешествия",
    10: "карьера и статус",
    11: "друзья и надежды",
    12: "подсознание и уединение",
}


def normalize_degrees(deg):
    while deg < 0:
        deg += 360
    while deg >= 360:
        deg -= 360
    return deg


def calc_synastry_aspects(pos1, pos2):
    """Calculate aspects between two sets of planetary positions."""
    aspects = []
    for p1_name, p1_lon in pos1.items():
        for p2_name, p2_lon in pos2.items():
            if p1_name == p2_name:
                continue  # Skip same planet comparisons? No, keep them (Sun-Sun etc)

            diff = abs(p1_lon - p2_lon)
            if diff > 180:
                diff = 360 - diff

            aspect_types = [
                ("conjunction", 0),
                ("sextile", 60),
                ("square", 90),
                ("trine", 120),
                ("opposition", 180),
                ("semisextile", 30),
                ("semisquare", 45),
                ("quincunx", 150),
            ]

            for asp_name, asp_angle in aspect_types:
                orb = SYNSTRY_ORBS[asp_name]
                orb_diff = abs(diff - asp_angle)
                if orb_diff <= orb:
                    # Check if this is a key pair
                    pair_key = (p1_name, p2_name)
                    weight = KEY_PAIRS.get(pair_key, 1.0)

                    aspects.append({
                        "p1": p1_name,
                        "p2": p2_name,
                        "type": asp_name,
                        "angle": asp_angle,
                        "orb": orb_diff,
                        "weight": weight,
                        "score": ASPECT_SCORES[asp_name] * weight,
                    })
                    break

    # Sort by absolute weight (most important first)
    aspects.sort(key=lambda x: abs(x["score"]), reverse=True)
    return aspects


def calc_house_overlaps(pos_other, houses_self):
    """Determine which houses of self are activated by other's planets."""
    overlaps = {}
    for pname, plon in pos_other.items():
        for h in range(12):
            next_h = (h + 1) % 12
            h_start = houses_self[h]
            h_end = houses_self[next_h]
            if h_start < h_end:
                if h_start <= plon < h_end:
                    house_num = h + 1
                    if house_num not in overlaps:
                        overlaps[house_num] = []
                    overlaps[house_num].append(pname)
                    break
            else:
                if plon >= h_start or plon < h_end:
                    house_num = h + 1
                    if house_num not in overlaps:
                        overlaps[house_num] = []
                    overlaps[house_num].append(pname)
                    break
    return overlaps


def calculate_compatibility_score(aspects):
    """Calculate overall compatibility score (0-100)."""
    if not aspects:
        return 50  # Neutral

    total_score = 0
    max_possible = 0

    for asp in aspects:
        total_score += asp["score"]
        max_possible += abs(ASPECT_SCORES[asp["type"]]) * asp["weight"]

    if max_possible == 0:
        return 50

    # Normalize to 0-100 range
    raw = (total_score / max_possible) * 100
    # Scale: 50 is neutral, range roughly 20-80
    score = 50 + raw * 0.5
    score = max(10, min(95, score))
    return round(score)


def get_sphere_scores(aspects):
    """Calculate scores for different relationship spheres."""
    spheres = {
        "passion": {"planets": ["Mars", "Venus", "Pluto", "Sun"], "score": 0, "count": 0},
        "emotion": {"planets": ["Moon", "Venus", "Neptune", "Sun"], "score": 0, "count": 0},
        "communication": {"planets": ["Mercury", "Uranus", "Jupiter"], "score": 0, "count": 0},
        "values": {"planets": ["Jupiter", "Saturn", "Sun", "MC"], "score": 0, "count": 0},
        "family": {"planets": ["Moon", "Venus", "Saturn", "IC"], "score": 0, "count": 0},
    }

    for asp in aspects:
        p1, p2 = asp["p1"], asp["p2"]
        for sphere_name, sphere in spheres.items():
            if p1 in sphere["planets"] or p2 in sphere["planets"]:
                sphere["score"] += asp["score"]
                sphere["count"] += 1

    # Convert to 1-10 scale
    result = {}
    for name, sphere in spheres.items():
        if sphere["count"] > 0:
            raw = sphere["score"] / sphere["count"]
            # Map to 1-10
            score = 5 + raw * 1.5
            result[name] = max(1, min(10, round(score)))
        else:
            result[name] = 5  # Neutral

    return result


def get_aspect_description(asp):
    """Get human-readable description of a synastry aspect."""
    p1_info = PLANETS.get(asp["p1"], {"name_rus": asp["p1"]})
    p2_info = PLANETS.get(asp["p2"], {"name_rus": asp["p2"]})

    aspect_names = {
        "conjunction": "соединение",
        "opposition": "оппозиция",
        "trine": "трин",
        "square": "квадрат",
        "sextile": "секстиль",
        "semisextile": "полусекстиль",
        "semisextile": "полусекстиль",
        "semisquare": "полуквадрат",
        "quincunx": "квинконс",
    }

    symbols = {
        "conjunction": "☌",
        "opposition": "☍",
        "trine": "△",
        "square": "□",
        "sextile": "✶",
        "semisextile": "⚺",
        "semisquare": "∠",
        "quincunx": "⚹",
    }

    return {
        "text": f"{symbols.get(asp['type'], '?')} {p1_info['name_rus']}-{p2_info['name_rus']} ({aspect_names.get(asp['type'], asp['type'])}, орб {asp['orb']:.1f}°)",
        "positive": asp["score"] > 0,
        "weight": asp["weight"],
    }


def format_synastry(name1, name2, chart1, chart2, aspects, house_overlaps_1, house_overlaps_2):
    """Format complete synastry report."""
    lines = []

    # Header
    lines.append("💕 СИНАСТРИЯ — Совместимость")
    lines.append(f"👤 {name1}: {chart1['date']}, {chart1['city_full']}")
    lines.append(f"👤 {name2}: {chart2['date']}, {chart2['city_full']}")
    lines.append("")

    # Overall score
    score = calculate_compatibility_score(aspects)
    lines.append("═" * 50)
    lines.append(f"📊 ОБЩИЙ БАЛЛ СОВМЕСТИМОСТИ: {score}/100")
    lines.append("═" * 50)
    lines.append("")

    # Sphere scores
    spheres = get_sphere_scores(aspects)
    sphere_labels = {
        "passion": "🔥 СТРАСТЬ И ФИЗИЧЕСКОЕ ПРИТЯЖЕНИЕ",
        "emotion": "💞 ЭМОЦИОНАЛЬНАЯ СОВМЕСТИМОСТЬ",
        "communication": "🗣️ КОММУНИКАЦИЯ И ИНТЕЛЛЕКТ",
        "values": "🎯 ОБЩИЕ ЦЕЛИ И ЦЕННОСТИ",
        "family": "🏠 СЕМЬЯ И БЫТ",
    }

    for key, label in sphere_labels.items():
        s = spheres.get(key, 5)
        bar = "█" * s + "░" * (10 - s)
        lines.append(f"{label}")
        lines.append(f"   Балл: {s}/10  [{bar}]")
        lines.append("")

    # Key aspects
    lines.append("─" * 50)
    lines.append("🔑 КЛЮЧЕВЫЕ АСПЕКТЫ СИНАСТРИИ:")
    lines.append("─" * 50)

    # Show top aspects by weight
    shown = 0
    for asp in aspects[:20]:
        desc = get_aspect_description(asp)
        marker = "✅" if desc["positive"] else "⚠️"
        lines.append(f"  {marker} {desc['text']}")
        shown += 1

    lines.append("")

    # Strong aspects (positive)
    positive_asps = [a for a in aspects if a["score"] > 0 and a["weight"] >= 2.0]
    if positive_asps:
        lines.append("✨ СИЛЬНЫЕ СТОРОНЫ ПАРЫ:")
        lines.append("─" * 50)
        for asp in positive_asps[:8]:
            desc = get_aspect_description(asp)
            lines.append(f"  ✦ {desc['text']}")
            # Add interpretation
            lines.append(f"    {get_interpretation(asp, positive=True)}")
        lines.append("")

    # Conflict aspects (negative)
    negative_asps = [a for a in aspects if a["score"] < 0 and a["weight"] >= 1.5]
    if negative_asps:
        lines.append("⚡ КОНФЛИКТНЫЕ ТОЧКИ:")
        lines.append("─" * 50)
        for asp in negative_asps[:8]:
            desc = get_aspect_description(asp)
            lines.append(f"  ✦ {desc['text']}")
            lines.append(f"    {get_interpretation(asp, positive=False)}")
        lines.append("")

    # House overlaps
    lines.append("─" * 50)
    lines.append(f"🏠 ПЛАНЕТЫ {name1.upper()} В ДОМАХ {name2.upper()}:")
    lines.append("─" * 50)
    for house_num in sorted(house_overlaps_2.keys()):
        planets = ", ".join([PLANETS.get(p, {"name_rus": p})["name_rus"] for p in house_overlaps_2[house_num]])
        meaning = HOUSE_MEANINGS.get(house_num, "")
        lines.append(f"  {house_num} дом: {planets} — {meaning}")

    lines.append("")
    lines.append(f"🏠 ПЛАНЕТЫ {name2.upper()} В ДОМАХ {name1.upper()}:")
    lines.append("─" * 50)
    for house_num in sorted(house_overlaps_1.keys()):
        planets = ", ".join([PLANETS.get(p, {"name_rus": p})["name_rus"] for p in house_overlaps_1[house_num]])
        meaning = HOUSE_MEANINGS.get(house_num, "")
        lines.append(f"  {house_num} дом: {planets} — {meaning}")

    lines.append("")

    # Recommendations
    lines.append("─" * 50)
    lines.append("📋 РЕКОМЕНДАЦИИ:")
    lines.append("─" * 50)

    recs = generate_recommendations(spheres, positive_asps, negative_asps)
    for rec in recs:
        lines.append(f"  • {rec}")

    lines.append("")
    lines.append("─" * 50)
    lines.append("⚠️ Синастрия — инструмент самопознания, не приговор.")
    lines.append("Напряжённые аспекты указывают на зоны роста, а не несовместимость.")

    return "\n".join(lines)


def get_interpretation(asp, positive=True):
    """Get brief interpretation of a synastry aspect."""
    p1, p2, atype = asp["p1"], asp["p2"], asp["type"]

    # Key interpretations for important pairs
    interp_map = {
        ("Sun", "Moon", "conjunction"): "Глубинное узнавание, сильная связь на уровне сущности",
        ("Sun", "Moon", "trine"): "Естественная гармония, взаимопонимание без слов",
        ("Sun", "Moon", "opposition"): "Притяжение противоположностей, комплементарность",
        ("Sun", "Moon", "square"): "Эмоциональные трения, но и рост через конфликт",
        ("Sun", "Sun", "conjunction"): "Похожие базовые ценности, узнавание себя в другом",
        ("Sun", "Sun", "trine"): "Ладят на уровне личности, уважение и поддержка",
        ("Sun", "Sun", "square"): "Разные подходы к жизни, возможны столкновения эго",
        ("Moon", "Moon", "conjunction"): "Одинаковые эмоциональные потребности, комфорт",
        ("Moon", "Moon", "trine"): "Эмоциональная гармония, чувствуют друг друга",
        ("Moon", "Moon", "square"): "Разные эмоциональные ритмы, нужно притираться",
        ("Venus", "Mars", "conjunction"): "Мощная сексуальная химия, страстное притяжение",
        ("Venus", "Mars", "trine"): "Гармоничная романтическая и сексуальная связь",
        ("Venus", "Mars", "square"): "Страсть с конфликтом, но сильное притяжение",
        ("Venus", "Mars", "opposition"): "Интенсивное притяжение, борьба за доминирование",
        ("Saturn", "Sun", "conjunction"): "Серьёзные отношения, чувство долга и ответственности",
        ("Saturn", "Moon", "trine"): "Стабильность и надёжность, эмоциональная поддержка",
        ("Saturn", "Moon", "square"): "Эмоциональные ограничения, чувство тяжести",
        ("Pluto", "Sun", "conjunction"): "Интенсивная трансформативная связь, одержимость",
        ("Pluto", "Moon", "conjunction"): "Глубокая эмоциональная трансформация",
        ("Pluto", "Venus", "conjunction"): "Страстная, иногда болезненная привязанность",
        ("Mercury", "Mercury", "conjunction"): "Одинаковый стиль общения, лёгкий контакт",
        ("Mercury", "Mercury", "square"): "Разные стили мышления, недопонимания",
        ("Jupiter", "Sun", "trine"): "Поддержка и вдохновение, совместный рост",
        ("Jupiter", "Moon", "trine"): "Эмоциональная щедрость, оптимизм в паре",
        ("Uranus", "Venus", "conjunction"): "Неожиданная романтика, свобода в отношениях",
        ("Neptune", "Venus", "trine"): "Романтическая идеализация, духовная связь",
    }

    key = (p1, p2, atype)
    if key in interp_map:
        return interp_map[key]

    # Generic interpretations
    if positive:
        if atype == "trine":
            return "Гармоничное взаимодействие, лёгкость в этой сфере"
        elif atype == "sextile":
            return "Благоприятное влияние, потенциал для развития"
        elif atype == "conjunction":
            return "Слияние энергий, усиление темы этих планет"
        else:
            return "Положительное взаимодействие"
    else:
        if atype == "square":
            return "Напряжение и конфликт, но зона роста"
        elif atype == "opposition":
            return "Противоположные подходы, нужен компромисс"
        else:
            return "Требует осознанной работы"


def generate_recommendations(spheres, positive_asps, negative_asps):
    """Generate practical recommendations."""
    recs = []

    if spheres.get("passion", 5) >= 7:
        recs.append("Страсть и физическое притяжение — сильная сторона пары. Используйте это как фундамент.")
    elif spheres.get("passion", 5) <= 4:
        recs.append("Физическое притяжение может требовать внимания. Попробуйте новые совместные активности.")

    if spheres.get("emotion", 5) >= 7:
        recs.append("Эмоциональная совместимость высокая — вы чувствуете друг друга. Цените это.")
    elif spheres.get("emotion", 5) <= 4:
        recs.append("Эмоциональные потребности могут различаться. Важно проговаривать чувства.")

    if spheres.get("communication", 5) >= 7:
        recs.append("Общение — сильная сторона. Легко находите общий язык.")
    elif spheres.get("communication", 5) <= 4:
        recs.append("Стили общения могут различаться. Слушайте внимательнее друг друга.")

    if spheres.get("family", 5) >= 7:
        recs.append("Семейная жизнь и быт — зона гармонии. Комфортное совместное проживание.")
    elif spheres.get("family", 5) <= 4:
        recs.append("В бытовых вопросах возможны разногласия. Распределите роли заранее.")

    if spheres.get("values", 5) >= 7:
        recs.append("Общие ценности и цели — основа долгосрочных отношений.")
    elif spheres.get("values", 5) <= 4:
        recs.append("Жизненные цели могут различаться. Найдите точки соприкосновения.")

    if not recs:
        recs.append("Отношения сбалансированы. Работайте над взаимопониманием.")

    return recs


# ─── Main ───

def calc_synastry(chart1, chart2, name1="Партнёр 1", name2="Партнёр 2"):
    """Calculate complete synastry between two natal charts."""
    # Calculate cross-aspects
    aspects = calc_synastry_aspects(chart1["planets"], chart2["planets"])

    # Calculate house overlaps
    # Planets of partner 1 in houses of partner 2
    house_overlaps_1 = calc_house_overlaps(chart1["planets"], chart2["houses"])
    # Planets of partner 2 in houses of partner 1
    house_overlaps_2 = calc_house_overlaps(chart2["planets"], chart1["houses"])

    return {
        "name1": name1,
        "name2": name2,
        "chart1": chart1,
        "chart2": chart2,
        "aspects": aspects,
        "house_overlaps_1": house_overlaps_1,
        "house_overlaps_2": house_overlaps_2,
    }


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Использование: python synastry.py <дата1> <время1> <город1> <дата2> <время2> <город2>")
        print("Пример: python synastry.py 24.04.1983 06:00 Ижевск 25.10.1985 22:30 Можга")
        sys.exit(1)

    date1, time1, city1 = sys.argv[1], sys.argv[2], sys.argv[3]
    date2, time2, city2 = sys.argv[4], sys.argv[5], sys.argv[6]

    chart1 = nc.calc_natal_chart(date1, time1, city1)
    chart2 = nc.calc_natal_chart(date2, time2, city2)

    if "error" in chart1:
        print(f"❌ Ошибка для партнёра 1: {chart1['error']}")
        sys.exit(1)
    if "error" in chart2:
        print(f"❌ Ошибка для партнёра 2: {chart2['error']}")
        sys.exit(1)

    name1 = city1
    name2 = city2

    # Try to get names from args
    if len(sys.argv) >= 9:
        name1 = sys.argv[7]
        name2 = sys.argv[8]

    result = calc_synastry(chart1, chart2, name1, name2)
    print(format_synastry(name1, name2, chart1, chart2, result["aspects"],
                          result["house_overlaps_1"], result["house_overlaps_2"]))
