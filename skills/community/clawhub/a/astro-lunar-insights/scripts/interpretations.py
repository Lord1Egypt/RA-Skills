#!/usr/bin/env python3
"""
astro-lunar-insights: Autonomous Interpretations Module
Provides text interpretations for all 9 lunar metrics without AI.
Used when script is run directly (not through OpenClaw agent).

Each function takes metric data and returns a human-readable interpretation.
Bilingual: pass lang='ru' or lang='en' (default).
"""


# ============================================================
# 1. MOON PHASE INTERPRETATION
# ============================================================

def interpret_moon_phase(elongation, illumination, lang='en'):
    """Interpret the current Moon phase."""
    if lang == 'ru':
        phases = {
            (0, 22.5): (
                "Новолуние",
                "Луна не видна на небе. Энергия направлена внутрь. Время для планирования, "
                "медитации, работы с подсознанием. Хорошо начинать новые циклы на тонком уровне. "
                "Физическая энергия может быть снижена."
            ),
            (22.5, 67.5): (
                "Растущий серп",
                "Луна начинает проявляться. Энергия нарастает. Хорошее время для первых шагов "
                "в новых начинаниях. Мотивация растёт, но результаты ещё не видны. "
                "Важно заложить фундамент."
            ),
            (67.5, 112.5): (
                "Первая четверть",
                "Половина Луны освещена. Точка действия и решений. Возникают первые вызовы. "
                "Нужно проявить решительность. Энергия активна, но требует направления. "
                "Хорошо для преодоления препятствий."
            ),
            (112.5, 157.5): (
                "Растущая выпуклая Луна",
                "Большая часть Луны освещена. Энергия нарастает к кульминации. "
                "Время для уточнения и корректировки курса. Интуиция усиливается. "
                "Хорошо для развития проектов."
            ),
            (157.5, 202.5): (
                "Полнолуние",
                "Луна полностью освещена. Пик энергии и осознанности. Эмоции обострены. "
                "Всё скрытое проявляется. Время для откровений и завершений. "
                "Может быть бессонница, яркие сны. Избегайте конфликтов."
            ),
            (202.5, 247.5): (
                "Убывающая выпуклая Луна",
                "Свет начинает убывать. Время благодарности и деления опытом. "
                "Хорошо для обучения, передачи знаний. Энергия стабильна, но начинает снижаться. "
                "Подведение промежуточных итогов."
            ),
            (247.5, 292.5): (
                "Последняя четверть",
                "Снова половина Луны освещена, но убывает. Кризис сознания. "
                "Время отпускать то, что больше не служит. Нужно избавиться от старого. "
                "Хорошо для очищения и освобождения."
            ),
            (292.5, 337.5): (
                "Убывающий серп",
                "Луна почти исчезла. Энергия снижается. Время для отдыха, рефлексии, "
                "обработки опыта. Хорошо для завершения дел, прощения, отпускания. "
                "Подготовка к новому циклу."
            ),
            (337.5, 360): (
                "Бальзамическая Луна",
                "Тёмная Луна. Минимальная энергия. Глубокое погружение в подсознание. "
                "Время кармической обработки. Хорошо для молитвы, медитации, тишины. "
                "Не начинайте новых дел — завершайте старые."
            ),
        }
    else:
        phases = {
            (0, 22.5): (
                "New Moon",
                "The Moon is invisible. Energy turns inward. Time for planning, meditation, "
                "working with the subconscious. Good for starting new cycles on a subtle level. "
                "Physical energy may be low."
            ),
            (22.5, 67.5): (
                "Waxing Crescent",
                "The Moon begins to show. Energy builds. Good time for first steps in new ventures. "
                "Motivation grows but results aren't visible yet. Important to lay the foundation."
            ),
            (67.5, 112.5): (
                "First Quarter",
                "Half the Moon is lit. Point of action and decisions. First challenges arise. "
                "Need for determination. Energy is active but needs direction. Good for overcoming obstacles."
            ),
            (112.5, 157.5): (
                "Waxing Gibbous",
                "Most of the Moon is lit. Energy builds toward climax. Time for refinement "
                "and course correction. Intuition strengthens. Good for developing projects."
            ),
            (157.5, 202.5): (
                "Full Moon",
                "The Moon is fully lit. Peak energy and awareness. Emotions are heightened. "
                "Everything hidden comes to light. Time for revelations and completions. "
                "Insomnia and vivid dreams possible. Avoid conflicts."
            ),
            (202.5, 247.5): (
                "Waning Gibbous",
                "Light begins to wane. Time for gratitude and sharing experience. "
                "Good for teaching and knowledge transfer. Energy is stable but starting to decline. "
                "Interim results."
            ),
            (247.5, 292.5): (
                "Last Quarter",
                "Half the Moon is lit but waning. Crisis of consciousness. "
                "Time to release what no longer serves. Need to let go of the old. "
                "Good for cleansing and liberation."
            ),
            (292.5, 337.5): (
                "Waning Crescent",
                "The Moon has almost disappeared. Energy decreases. Time for rest, reflection, "
                "processing experience. Good for finishing things, forgiveness, release. "
                "Preparing for the new cycle."
            ),
            (337.5, 360): (
                "Balsamic Moon",
                "Dark Moon. Minimal energy. Deep dive into the subconscious. "
                "Time for karmic processing. Good for prayer, meditation, silence. "
                "Don't start new things — complete old ones."
            ),
        }

    for (lo, hi), (name, desc) in phases.items():
        if lo <= elongation < hi:
            return {'name': name, 'description': desc, 'illumination': illumination}

    return {'name': 'Unknown', 'description': '', 'illumination': illumination}


# ============================================================
# 2. NEAREST PHASES INTERPRETATION
# ============================================================

def interpret_nearest_phases(nearest_phases, lang='en'):
    """Interpret the nearest Moon phases."""
    if lang == 'ru':
        parts = []
        for pname, pdata in nearest_phases.items():
            days = pdata['days_diff']
            if days > 0:
                parts.append(f"{pname} через {abs(days):.1f} дн.")
            else:
                parts.append(f"{pname} {abs(days):.1f} дн. назад")
        return " | ".join(parts)
    else:
        parts = []
        for pname, pdata in nearest_phases.items():
            days = pdata['days_diff']
            if days > 0:
                parts.append(f"{pname} in {abs(days):.1f}d")
            else:
                parts.append(f"{pname} {abs(days):.1f}d ago")
        return " | ".join(parts)


# ============================================================
# 3. LUNAR DAY (TITHI) INTERPRETATION
# ============================================================

def interpret_lunar_day(lunar_day, lang='en'):
    """Interpret the lunar day (tithi)."""
    meanings_ru = {
        1: "День 1 — Новое начало. Невидимая энергия. Планирование намерений.",
        2: "День 2 — Изобилие. Первые проявления. Энергия Лакшми.",
        3: "День 3 — Агрессия и действие. Хорошо для сложных задач.",
        4: "День 4 — Получение знаний. Обучение и преподавание.",
        5: "День 5 — Трансформация и перемены. Поток праны.",
        6: "День 6 — Восприимчивость и интуиция. Хорошо для партнёрства.",
        7: "День 7 — Слова и общение. Магия речи.",
        8: "День 8 — Пробуждение и перерождение. Кармическая работа.",
        9: "День 9 — Священный знак. Высокая интуиция и сны.",
        10: "День 10 — Высший успех. Лучший день для старта крупных проектов.",
        11: "День 11 — Поток энергии. Сильная личная сила.",
        12: "День 12 — Постепенный рост. Неожиданная помощь.",
        13: "День 13 — Переход между старым и новым. Баланс.",
        14: "День 14 — ЛУЧШИЙ день для любых начинаний. Пик энергии.",
        15: "День 15 — День искушений. Нужен самоконтроль.",
        16: "День 16 — Спокойствие и гармония. Отлично для отдыха.",
        17: "День 17 — Танец, радость, праздник. Художественная энергия.",
        18: "День 18 — Видение истины. Духовное пробуждение.",
        19: "День 19 — Опасный день. Избегайте конфликтов.",
        20: "День 20 — День орла. Видение общей картины свысока.",
        21: "День 21 — Мужество и победа. Очень активный день.",
        22: "День 22 — Мудрость и знание. Энергия Ганеши.",
        23: "День 23 — Змей мудрости. День хитрости.",
        24: "День 24 — Продвижение через препятствия. Преодоление.",
        25: "День 25 — Тишина и уединение. Внутренний учитель говорит.",
        26: "День 26 — День крокодила. Потенциальная опасность.",
        27: "День 27 — Различение и распознавание. Ясное видение.",
        28: "День 28 — Процветание и мягкий свет. Благословения.",
        29: "День 29 — Трудный день. Осторожность. Тёмная луна.",
        30: "День 30 — День благословения. Конец цикла. Благодарность.",
    }
    meanings_en = {
        1: "Day 1 — New beginning. Invisible energy. Planning intentions.",
        2: "Day 2 — Abundance. First manifestations. Lakshmi energy.",
        3: "Day 3 — Aggression and action. Good for difficult tasks.",
        4: "Day 4 — Knowledge acquisition. Learning and teaching.",
        5: "Day 5 — Transformation and change. Prana flow.",
        6: "Day 6 — Receptivity and intuition. Good for partnerships.",
        7: "Day 7 — Words and communication. Magic of speech.",
        8: "Day 8 — Awakening and rebirth. Karmic work.",
        9: "Day 9 — Sacred sign. High intuition and dreams.",
        10: "Day 10 — Supreme success. Best day for starting major projects.",
        11: "Day 11 — Energy flow. Strong personal power.",
        12: "Day 12 — Gradual increase. Unexpected help.",
        13: "Day 13 — Transition between old and new. Balance.",
        14: "Day 14 — BEST day for starting anything new. Peak energy.",
        15: "Day 15 — Temptation day. Self-control needed.",
        16: "Day 16 — Calm and harmony. Excellent for rest.",
        17: "Day 17 — Dance, joy, celebration. Artistic energy.",
        18: "Day 18 — Seeing the truth. Spiritual awakening.",
        19: "Day 19 — Dangerous day. Avoid conflicts.",
        20: "Day 20 — Eagle day. Seeing the big picture from above.",
        21: "Day 21 — Courage and victory. Very active day.",
        22: "Day 22 — Wisdom and knowledge. Ganesha energy.",
        23: "Day 23 — Serpent of wisdom. Day of cunning.",
        24: "Day 24 — Advance through obstacles. Overcoming.",
        25: "Day 25 — Silence and solitude. The teacher within speaks.",
        26: "Day 26 — Crocodile day. Potential danger.",
        27: "Day 27 — Discernment and discrimination. Clear vision.",
        28: "Day 28 — Prosperity and soft light. Blessings.",
        29: "Day 29 — Difficult day. Caution. Dark moon.",
        30: "Day 30 — Blessing day. End of cycle. Gratitude.",
    }
    meanings = meanings_ru if lang == 'ru' else meanings_en
    return meanings.get(lunar_day, f"Day {lunar_day}")


# ============================================================
# 4. TRANSIT MOON TO NATAL MOON INTERPRETATION
# ============================================================

def interpret_transit_moon_to_natal_moon(aspect_name, orb, natal_moon_sign, transit_moon_sign, lang='en'):
    """Interpret the transit Moon -> natal Moon aspect."""
    if lang == 'ru':
        base_interp = {
            'Conjunction': (
                "Персональное новолуние. Начинается новый ~28-дневный эмоциональный цикл. "
                "Эмоциональный сброс и обновление. Высокая чувствительность. "
                "Хорошо для интроспекции, постановки намерений, работы с эмоциональными паттернами."
            ),
            'Semisextile': (
                "Тонкое напряжение в эмоциональной жизни. Небольшие корректировки в привычных "
                "эмоциональных реакциях. Едва заметное беспокойство."
            ),
            'Semisquare': (
                "Незначительное раздражение. Фрустрация от повторяющихся эмоциональных паттернов. "
                "Нужно проявить терпение."
            ),
            'Sextile': (
                "Эмоциональная лёгкость. Хороший день для отношений и творчества. "
                "Естественный поток эмоций. Легко находить общий язык с людьми."
            ),
            'Square': (
                "Кризисная точка в эмоциональной жизни. Нужны действия и решения. "
                "Внутреннее напряжение между привычным и необходимым. "
                "Избегайте импульсивных решений, но не откладывайте."
            ),
            'Sesquiquadrate': (
                "Беспокойство и неудовлетворённость. Нужно сломать эмоциональные паттерны. "
                "Ощущение, что что-то не так, но трудно сформулировать что именно."
            ),
            'Trine': (
                "Эмоциональная гармония. Сильная интуиция. Хороший день для планирования. "
                "Эмоции текут свободно и естественно. Легко понять свои чувства."
            ),
            'Quincunx': (
                "Нужна корректировка эмоциональных приоритетов. Что-то не сходится. "
                "Ощущение дискомфорта без явной причины. Перестройка эмоциональных реакций."
            ),
            'Opposition': (
                "Персональное полнолуние. Эмоциональная кульминация. Осознание через контраст. "
                "Завершение 28-дневной эмоциональной темы. Всё скрытое выходит на поверхность. "
                "Мощный день для эмоциональных откровений."
            ),
        }
    else:
        base_interp = {
            'Conjunction': (
                "Personal New Moon. A new ~28-day emotional cycle begins. "
                "Emotional reset and renewal. High sensitivity. "
                "Good for introspection, setting intentions, working with emotional patterns."
            ),
            'Semisextile': (
                "Subtle tension in emotional life. Small adjustments in habitual "
                "emotional reactions. Barely noticeable restlessness."
            ),
            'Semisquare': (
                "Minor irritation. Frustration with repeating emotional patterns. "
                "Patience needed."
            ),
            'Sextile': (
                "Emotional ease. Good day for relationships and creativity. "
                "Natural flow of emotions. Easy to connect with people."
            ),
            'Square': (
                "Crisis point in emotional life. Need for action and decisions. "
                "Inner tension between habitual and necessary. "
                "Avoid impulsive decisions but don't postpone."
            ),
            'Sesquiquadrate': (
                "Restlessness and dissatisfaction. Need to break emotional patterns. "
                "Feeling something is off but hard to articulate what."
            ),
            'Trine': (
                "Emotional harmony. Strong intuition. Good day for planning. "
                "Emotions flow freely and naturally. Easy to understand your feelings."
            ),
            'Quincunx': (
                "Adjustment needed in emotional priorities. Something doesn't fit. "
                "Feeling of discomfort without clear cause. Restructuring emotional responses."
            ),
            'Opposition': (
                "Personal Full Moon. Emotional climax. Awareness through contrast. "
                "Culmination of a 28-day emotional theme. Everything hidden comes to surface. "
                "Powerful day for emotional revelations."
            ),
        }

    interp = base_interp.get(aspect_name, f"Active {aspect_name} aspect.")
    orb_text = f" (орб {orb:.1f}°)" if lang == 'ru' else f" (orb {orb:.1f}°)"
    return interp + orb_text


# ============================================================
# 5. PERSONAL SOLAR-LUNAR PHASE INTERPRETATION
# ============================================================

def interpret_personal_phase(phase_key, personal_elong, lang='en'):
    """Interpret the personal solar-lunar phase."""
    if lang == 'ru':
        phases = {
            'new_moon': (
                "Персональное новолуние",
                "Начало ~29.5-дневного личного цикла. Высокая внутренняя энергия. "
                "Хорошо для старта личных проекктов, постановки целей, работы над собой. "
                "Энергия направлена внутрь. Внешние результаты пока невидимы."
            ),
            'crescent': (
                "Персональный серп",
                "Проявление. Энергия нарастает. Первые шаги в новых начинаниях. "
                "Начинайте действовать — энергия поддерживает. Но не ожидайте быстрых результатов."
            ),
            'first_quarter': (
                "Персональная первая четверть",
                "Точка действия и решений. Возникают вызовы. Нужно проявить решительность. "
                "Прорывайтесь через препятствия. Не отступайте — энергия на вашей стороне."
            ),
            'gibbous': (
                "Персональная выпуклая луна",
                "Уточнение и корректировка. Доводите подход до совершенства. "
                "Интуиция усиливается. Хорошо для развития и углубления проектов."
            ),
            'full_moon': (
                "Персональное полнолуние",
                "КУЛЬМИНАЦИЯ. Максимальное осознание. Эмоциональное откровение. "
                "Завершение личного цикла. Всё скрытое проявляется. "
                "Мощный день для самопознания и трансформации."
            ),
            'disseminating': (
                "Персональная распространяющая",
                "Делиться и благодарность. Учите тому, что узнали. "
                "Передача опыта другим. Хорошо для наставничества и обучения."
            ),
            'last_quarter': (
                "Персональная последняя четверть",
                "Кризис сознания. Отпустите то, что не служит. "
                "Нужно избавиться от старого, чтобы освободить место для нового. "
                "Хорошо для очищения и освобождения."
            ),
            'balsamic': (
                "Персональная бальзамическая",
                "Отдых и рефлексия. Подготовка к следующему циклу. "
                "Кармическая обработка. Время молчания и внутренней работы. "
                "Не начинайте нового — завершайте старое."
            ),
        }
    else:
        phases = {
            'new_moon': (
                "Personal New Moon",
                "Beginning of a ~29.5-day personal cycle. High inward energy. "
                "Good for starting personal projects, goal setting, self-work. "
                "Energy turns inward. External results not yet visible."
            ),
            'crescent': (
                "Personal Crescent",
                "Emerging. Energy builds. First steps in new ventures. "
                "Start acting — energy supports. But don't expect quick results."
            ),
            'first_quarter': (
                "Personal First Quarter",
                "Action and decision point. Challenges arise. Need for determination. "
                "Push through obstacles. Don't retreat — energy is on your side."
            ),
            'gibbous': (
                "Personal Gibbous",
                "Refinement and adjustment. Fine-tune your approach. "
                "Intuition strengthens. Good for developing and deepening projects."
            ),
            'full_moon': (
                "Personal Full Moon",
                "CLIMAX. Maximum awareness. Emotional revelation. "
                "Culmination of the personal cycle. Everything hidden comes to light. "
                "Powerful day for self-discovery and transformation."
            ),
            'disseminating': (
                "Personal Disseminating",
                "Sharing and gratitude. Teach what you've learned. "
                "Transferring experience to others. Good for mentoring and teaching."
            ),
            'last_quarter': (
                "Personal Last Quarter",
                "Crisis of consciousness. Let go of what doesn't serve. "
                "Need to release the old to make room for the new. "
                "Good for cleansing and liberation."
            ),
            'balsamic': (
                "Personal Balsamic",
                "Rest and reflection. Prepare for the next cycle. "
                "Karmic processing. Time for silence and inner work. "
                "Don't start new things — complete old ones."
            ),
        }

    return phases.get(phase_key, ("Unknown", ""))


# ============================================================
# 6. TRANSIT MOON IN NATAL HOUSE INTERPRETATION
# ============================================================

def interpret_moon_house(house, natal_planets_in_house, lang='en'):
    """Interpret transit Moon in natal house."""
    if lang == 'ru':
        house_interp = {
            1: "Активируется сфера личности и самовыражения. Эмоциональная вовлечённость в собственную идентичность. Хорошо для заботы о себе, внешности, личных целях.",
            2: "Активируются деньги и ценности. Финансовые вопросы на повестке дня. Эмоциональная реакция на материальные дела. Хорошо для оценки ресурсов.",
            3: "Активируется общение и обучение. Встречи, поездки, разговоры. Эмоциональный интерес к новым знаниям. Хорошо для переговоров.",
            4: "Активируется дом и семья. Эмоциональная вовлечённость в семейные дела. Хорошо для домашних дел, работы с корнями, родителями.",
            5: "Активируется творчество и романтика. Эмоциональный подъём в любви и творчестве. Хорошо для хобби, детей, романтических встреч.",
            6: "Активируется здоровье и работа. Эмоциональная реакция на повседневные дела. Хорошо для заботы о здоровье, рабочих рутин.",
            7: "Активируется партнёрство. Эмоциональная вовлечённость в отношения. Хорошо для встреч с партнёром, переговоров, сотрудничества.",
            8: "Активируется трансформация. Глубокие эмоциональные процессы. Хорошо для работы с кризисами, общими ресурсами, психологией.",
            9: "Активируются путешествия и философия. Эмоциональный интерес к обучению, духовности, дальним дорогам. Хорошо для планирования поездок.",
            10: "Активируется карьера и статус. Эмоциональная вовлечённость в профессиональные вопросы. Хорошо для публичных выступлений, карьерных решений.",
            11: "Активируются друзья и надежды. Эмоциональная вовлечённость в социальные связи. Хорошо для встреч с друзьями, групповых проектов.",
            12: "Активируется подсознание. Глубокие внутренние процессы. Хорошо для медитации, работы с психикой, отдыха, уединения.",
        }
    else:
        house_interp = {
            1: "Self and identity activated. Emotional involvement in personal identity. Good for self-care, appearance, personal goals.",
            2: "Money and values activated. Financial matters on the agenda. Emotional response to material affairs. Good for resource assessment.",
            3: "Communication and learning activated. Meetings, trips, conversations. Emotional interest in new knowledge. Good for negotiations.",
            4: "Home and family activated. Emotional involvement in family matters. Good for home affairs, working with roots, parents.",
            5: "Creativity and romance activated. Emotional uplift in love and creativity. Good for hobbies, children, romantic dates.",
            6: "Health and work activated. Emotional response to daily affairs. Good for health care, work routines.",
            7: "Partnership activated. Emotional involvement in relationships. Good for meetings with partner, negotiations, cooperation.",
            8: "Transformation activated. Deep emotional processes. Good for working with crises, shared resources, psychology.",
            9: "Travel and philosophy activated. Emotional interest in learning, spirituality, distant roads. Good for trip planning.",
            10: "Career and status activated. Emotional involvement in professional matters. Good for public speaking, career decisions.",
            11: "Friends and hopes activated. Emotional involvement in social connections. Good for meeting friends, group projects.",
            12: "Subconscious activated. Deep internal processes. Good for meditation, psychological work, rest, solitude.",
        }

    result = house_interp.get(house, "")
    if natal_planets_in_house:
        planet_names = ", ".join([p['name'] for p in natal_planets_in_house])
        if lang == 'ru':
            result += f" Натальные планеты в этом доме ({planet_names}) усиливают активацию."
        else:
            result += f" Natal planets in this house ({planet_names}) amplify the activation."
    return result


# ============================================================
# 7. MOON SPEED INTERPRETATION
# ============================================================

def interpret_moon_speed(speed, approaching, lang='en'):
    """Interpret Moon speed."""
    if lang == 'ru':
        if speed > 15:
            desc = "Очень быстрая Луна (рядом с перигеем). События развиваются быстро. Эмоции поверхностные, но интенсивные. Хорошо для быстрых решений."
        elif speed > 13.5:
            desc = "Быстрая Луна. Быстрые эмоциональные перемены. Дела продвигаются. Хорошо для активной деятельности."
        elif speed > 11.5:
            desc = "Нормальная скорость Луны. Сбалансированная эмоциональная обработка. Стандартный ритм жизни."
        elif speed > 10:
            desc = "Медленная Луна. Затяжные чувства, глубокое влияние. Эмоции переживаются глубже и дольше. Хорошо для глубокой работы."
        else:
            desc = "Очень медленная Луна (рядом с апогеем). Затяжная эмоциональная интенсивность. Ощущение застревания. Терпение необходимо."
    else:
        if speed > 15:
            desc = "Very fast Moon (near perigee). Events move quickly. Emotions are surface-level but intense. Good for quick decisions."
        elif speed > 13.5:
            desc = "Fast Moon. Rapid emotional shifts. Matters progress. Good for active work."
        elif speed > 11.5:
            desc = "Normal Moon speed. Balanced emotional processing. Standard life rhythm."
        elif speed > 10:
            desc = "Slow Moon. Lingering feelings, deeper impact. Emotions are experienced more deeply and longer. Good for deep work."
        else:
            desc = "Very slow Moon (near apogee). Prolonged emotional intensity. Feeling of being stuck. Patience needed."

    if lang == 'ru':
        desc += f" Луна приближается к {approaching}."
    else:
        desc += f" Moon approaching {approaching}."
    return desc


# ============================================================
# 8. TRANSIT MOON ASPECTS TO ALL NATAL PLANETS INTERPRETATION
# ============================================================

def interpret_moon_aspects_to_planets(aspects, lang='en'):
    """Interpret transit Moon aspects to all natal planets."""
    if not aspects:
        return "Нет точных аспектов транзитной Луны к натальным планетам." if lang == 'ru' else "No exact transit Moon aspects to natal planets."

    if lang == 'ru':
        planet_meanings = {
            'Sun': "эго и жизненная сила",
            'Moon': "эмоции и подсознание",
            'Mercury': "мышление и общение",
            'Venus': "любовь и ценности",
            'Mars': "энергия и действие",
            'Jupiter': "расширение и удача",
            'Saturn': "дисциплина и ограничения",
            'Uranus': "перемены и свобода",
            'Neptune': "интуиция и духовность",
            'Pluto': "трансформация и власть",
        }
        aspect_nature = {
            'Conjunction': "слияние энергий",
            'Sextile': "гармоничная возможность",
            'Square': "напряжение и вызов",
            'Trine': "естественный поток",
            'Opposition': "осознание через контраст",
            'Semisextile': "тонкое влияние",
            'Semisquare': "лёгкое раздражение",
            'Sesquiquadrate': "внутреннее беспокойство",
            'Quincunx': "необходимость корректировки",
        }
    else:
        planet_meanings = {
            'Sun': "ego and life force",
            'Moon': "emotions and subconscious",
            'Mercury': "thinking and communication",
            'Venus': "love and values",
            'Mars': "energy and action",
            'Jupiter': "expansion and luck",
            'Saturn': "discipline and limitations",
            'Uranus': "change and freedom",
            'Neptune': "intuition and spirituality",
            'Pluto': "transformation and power",
        }
        aspect_nature = {
            'Conjunction': "fusion of energies",
            'Sextile': "harmonious opportunity",
            'Square': "tension and challenge",
            'Trine': "natural flow",
            'Opposition': "awareness through contrast",
            'Semisextile': "subtle influence",
            'Semisquare': "mild irritation",
            'Sesquiquadrate': "inner restlessness",
            'Quincunx': "need for adjustment",
        }

    parts = []
    for a in aspects:
        if not a['major']:
            continue
        planet = a['natal']
        aspect = a['aspect']
        meaning = planet_meanings.get(planet, planet)
        nature = aspect_nature.get(aspect, aspect)
        if lang == 'ru':
            parts.append(f"Луна {aspect} {planet}: {meaning} — {nature}")
        else:
            parts.append(f"Moon {aspect} {planet}: {meaning} — {nature}")

    return "; ".join(parts) if parts else ""


# ============================================================
# 9. OVERALL CONCLUSION (for AI use)
# ============================================================

def generate_metric_summaries(data, lang='en'):
    """
    Generate structured summaries for each of the 9 metrics.
    This is used by the AI to build a comprehensive conclusion.
    Returns a dict with all metric data ready for AI interpretation.
    """
    elongation = data['moon_phase']['elongation']
    illumination = data['moon_phase']['illumination']
    lunar_day = data['lunar_day']['number']
    personal_elong = data['personal_phase']['elongation']
    personal_key = data['personal_phase']['key']
    moon_house = data['transit_moon_house']['house']
    moon_speed = data['moon_speed']['speed']
    approaching = data['transit_moon']['approaching']
    tm_aspect = data['transit_moon_to_natal_moon']['aspect']
    tm_orb = data['transit_moon_to_natal_moon']['orb']
    all_aspects = data['transit_moon_aspects']

    # Count major aspects
    major_aspects = [a for a in all_aspects if a['major']]

    # Determine dominant energy
    if lang == 'ru':
        if personal_key in ('new_moon', 'crescent'):
            cycle_energy = "нарастающая энергия нового цикла"
        elif personal_key in ('first_quarter', 'gibbous'):
            cycle_energy = "активная энергия развития"
        elif personal_key in ('full_moon',):
            cycle_energy = "пиковая энергия кульминации"
        else:
            cycle_energy = "убывающая энергия завершения"

        if len(major_aspects) >= 3:
            intensity = "высокая интенсивность — множество аспектов активируют натальную карту"
        elif len(major_aspects) >= 1:
            intensity = "умеренная интенсивность — несколько значимых аспектов"
        else:
            intensity = "спокойный день — точных мажорных аспектов нет"
    else:
        if personal_key in ('new_moon', 'crescent'):
            cycle_energy = "building energy of a new cycle"
        elif personal_key in ('first_quarter', 'gibbous'):
            cycle_energy = "active energy of development"
        elif personal_key in ('full_moon',):
            cycle_energy = "peak energy of culmination"
        else:
            cycle_energy = "waning energy of completion"

        if len(major_aspects) >= 3:
            intensity = "high intensity — multiple aspects activate the natal chart"
        elif len(major_aspects) >= 1:
            intensity = "moderate intensity — several significant aspects"
        else:
            intensity = "calm day — no exact major aspects"

    return {
        'moon_phase': {
            'name': data['moon_phase']['name'],
            'elongation': elongation,
            'illumination': illumination,
            'interpretation': interpret_moon_phase(elongation, illumination, lang),
        },
        'nearest_phases': data['nearest_phases'],
        'lunar_day': {
            'number': lunar_day,
            'interpretation': interpret_lunar_day(lunar_day, lang),
        },
        'transit_moon_to_natal_moon': {
            'aspect': tm_aspect,
            'orb': tm_orb,
            'interpretation': interpret_transit_moon_to_natal_moon(
                tm_aspect, tm_orb,
                data['_natal']['Moon']['lon'],
                data['transit_moon']['lon'],
                lang
            ) if tm_aspect else None,
        },
        'personal_phase': {
            'key': personal_key,
            'elongation': personal_elong,
            'interpretation': interpret_personal_phase(personal_key, personal_elong, lang),
        },
        'transit_moon_house': {
            'house': moon_house,
            'interpretation': interpret_moon_house(
                moon_house,
                data['transit_moon_house']['natal_planets_in_house'],
                lang
            ),
        },
        'moon_speed': {
            'speed': moon_speed,
            'approaching': approaching,
            'interpretation': interpret_moon_speed(moon_speed, approaching, lang),
        },
        'transit_moon_aspects': {
            'all': all_aspects,
            'major': major_aspects,
            'interpretation': interpret_moon_aspects_to_planets(all_aspects, lang),
        },
        'summary': {
            'cycle_energy': cycle_energy,
            'intensity': intensity,
            'total_aspects': len(all_aspects),
            'major_aspects': len(major_aspects),
        },
    }
