#!/usr/bin/env python3
"""Собирает досье в Word строго по заданной структуре.

Почему скрипт, а не указания модели. Оформление, которое модель делает
каждый раз заново, каждый раз получается разным: то шрифт применён к
абзацам, но не к таблицам, то интервал сбился, то документ вырос на пять
страниц. Здесь оформление задано один раз и не зависит от прогона —
модель отвечает только за содержание.

Вход — JSON. Не свободный текст: свободный текст пришлось бы разбирать
обратно, а разбор — это ещё одно место, где всё ломается молча.

    python3 render_dossier.py dossier.json "Досье — Иванов Иван — 2026-08-27.docx"
    python3 render_dossier.py --check dossier.json     только проверить бюджет
    python3 render_dossier.py --schema                 показать формат входа
    python3 render_dossier.py --fit    <файл>          срезать под бюджет по правилу

Скрипт пишет ТОЛЬКО внутрь одного рабочего каталога — по порядку
`OUROBOROS_SKILL_STATE_DIR`, иначе `OUROBOROS_TASK_DRIVE`, иначе текущий
каталог: путь приходит аргументом, то есть в конечном счёте от модели, и без
ограничения досье можно было бы записать поверх настроек или другого навыка.
Читать JSON можно откуда угодно (только чтение). Сеть не трогается,
подпроцессы не запускаются.

Оформление фиксировано: Arial 12, интервал 1,5, поля 2 см, максимум две
страницы. Превышение бюджета — ошибка, а не предупреждение: документ на
три страницы никто не читает перед встречей.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import sys

sys.dont_write_bytecode = True  # каталог навыка может быть только для чтения

# --- Бюджет ------------------------------------------------------------------
# Arial 12 с интервалом 1,5 при полях 2 см даёт ~2700 знаков на странице A4.
# Две страницы — 5400. Держим небольшой запас на заголовки и таблицу.
CHARS_PER_PAGE = 2700
MAX_PAGES = 2
BUDGET = CHARS_PER_PAGE * MAX_PAGES

# Контекст встречи меняет назначение документа: «Темы на обсуждение»
# превращаются из списка зацепок в проработанную повестку. Под неё нужна
# отдельная страница, иначе разделу негде развернуться.
TOPICS_LIMIT_WITH_CONTEXT = 2800
BUDGET_WITH_CONTEXT = CHARS_PER_PAGE * 3

# --- Структура ---------------------------------------------------------------
# Порядок разделов фиксирован и одинаков в чате и в документе: читатель не
# должен переучиваться, переходя из одного в другое.
# Заголовки, зависящие от рода. Два варианта: (мужской, женский).
# «Кто он» над досье женщины бросается в глаза сильнее, чем кажется:
# документ сразу выглядит собранным без внимания.
SECTIONS = [
    ("completeness", ("Полнота данных", "Полнота данных"),     True,  250),
    ("summary",      ("Одним абзацем", "Одним абзацем"),       True,  500),
    ("who",          ("Кто он", "Кто она"),                    True,  600),
    ("known_for",    ("Чем известен", "Чем известна"),         True,  900),
    ("culture",      ("Культурный контекст", "Культурный контекст"), False, 400),
    ("avoid",        ("Чего не касаться", "Чего не касаться"), True,  300),
    # «О чём говорить» и «что обсуждать» — один раздел: читатель перед встречей
    # читает их подряд и не различает, а деление одного списка надвое даёт повторы.
    ("topics",       ("Темы на обсуждение", "Темы на обсуждение"), True, 1500),
    ("unconfirmed",  ("Не подтверждено", "Не подтверждено"),   True,  400),
    ("analysis",     ("Анализ", "Анализ"),                     False, 400),
]

# Полнота данных считается внутри — она нужна агенту, чтобы решить, хватает
# ли материала. Руководителю в документе служебная арифметика («8/10 якорей
# закрыты») не нужна и мешает: он открывает досье, чтобы узнать человека, а
# не оценивать работу над ним.
HIDDEN_IN_DOCX = {"completeness"}


def heading(spec, gender: str) -> str:
    """Заголовок раздела с учётом рода: gender = 'f' — женский, иначе мужской."""
    if isinstance(spec, (list, tuple)):
        return spec[1] if str(gender or "").lower().startswith("f") else spec[0]
    return str(spec)


# Месяцы на любом языке, встреченные в датах, приводим к русским. Досье
# читает русскоязычный руководитель: «по состоянию на agosto 2026» выглядит
# недоделкой, даже когда факт верен.
MONTHS = {
    "january": "январь", "february": "февраль", "march": "март", "april": "апрель",
    "may": "май", "june": "июнь", "july": "июль", "august": "август",
    "september": "сентябрь", "october": "октябрь", "november": "ноябрь",
    "december": "декабрь",
    "enero": "январь", "febrero": "февраль", "marzo": "март", "abril": "апрель",
    "mayo": "май", "junio": "июнь", "julio": "июль", "agosto": "август",
    "septiembre": "сентябрь", "octubre": "октябрь", "noviembre": "ноябрь",
    "diciembre": "декабрь",
    "janeiro": "январь", "fevereiro": "февраль", "março": "март", "abril": "апрель",
    "maio": "май", "junho": "июнь", "julho": "июль", "setembro": "сентябрь",
    "outubro": "октябрь", "novembro": "ноябрь", "dezembro": "декабрь",
}


def ru_dates(text: str) -> str:
    """Заменяет иноязычные месяцы на русские, не трогая остального текста."""

    def repl(m):
        word = m.group(0)
        ru = MONTHS.get(word.lower())
        return ru if ru else word

    text = re.sub(r"[A-Za-zÀ-ÿ]{3,12}", repl, text)
    # «2026-10-12» → «12 октября 2026», «2026-10» → «октябрь 2026»: в прогоне
    # строка роли вышла «(по состоянию на 2026-10-12)».
    def iso(m):
        y, mo, d = m.group(1), int(m.group(2)), m.group(3)
        if not 1 <= mo <= 12:
            return m.group(0)
        if d:
            return f"{int(d)} {_MONTHS_GEN[mo - 1]} {y}"
        return f"{_MONTHS_NOM[mo - 1]} {y}"
    return re.sub(r"(?<![\d-])((?:19|20)\d{2})-(\d{2})(?:-(\d{2}))?(?![\d-])", iso, text)


_MONTHS_GEN = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа",
               "сентября", "октября", "ноября", "декабря"]
_MONTHS_NOM = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август",
               "сентябрь", "октябрь", "ноябрь", "декабрь"]

SCHEMA = {
    "name": "Полное имя, как в источниках",
    "gender": "'m' или 'f' — от этого зависят заголовки «Кто он» / «Кто она»",
    "meeting_context": "Необязательно. ТОЛЬКО если владелец сам назвал контекст встречи в запросе — не придумывать. "
                       "При заполнении «Темы на обсуждение» расширяются до 2800 знаков, "
                       "а документ — до трёх страниц",
    "owner_context": "Необязательно. Для кого досье — организация, роль и интересы владельца, если они "
                     "названы в запросе или есть в памяти агента; не придумывать. В документ не выводится: "
                     "по нему строятся «Темы» — на стыке интересов владельца и опыта человека",
    "prepared": "Дата подготовки досье, ГГГГ-ММ-ДД — идёт в колонтитул",
    "last_known_role": "Последнее известное место работы и должность",
    "as_of": "Дата, на которую это известно (ГГГГ-ММ-ДД или «март 2025»)",
    "completeness": "Оценка полноты для чата. В документ НЕ выводится",
    "summary": "Один абзац, 3–4 предложения: кто сейчас, путь, чем примечателен, почему важен для разговора. "
               "Факты — с номером источника; связующий вывод можно без номера, но без «самый/крупнейший»",
    "who": "Последнее известное место работы и должность «по состоянию на <дата>», путь до этого, "
           "образование, возраст (выведенный — «около»). Номер источника у каждой фразы",
    "known_for": ["3–4 пункта: факт, год, номер источника [1]", "Ещё факт [2]"],
    "culture": "Необязательно. Только если разговор на стыке деловых культур",
    "avoid": "Конкретика или «специфических тем под запретом не выявлено». Семья, "
             "здоровье, утраты — только обобщённо («личная жизнь и семья»), без имён и дат",
    "topics": ["4–5 пунктов по 200–300 знаков: тема → почему уместна (зацепка из биографии [3]) → "
               "на что выйти в разговоре. С owner_context / meeting_context — на их стыке с опытом "
               "человека; при заданном meeting_context раздел становится проработанной повесткой"],
    "unconfirmed": ["Что не подтвердилось и чего не хватило"],
    "analysis": ["Необязательно. Вывод, а не факт — помечается отдельно"],
    "sources": [
        {"n": 1, "title": "Название", "date": "2025-03-15",
         "strength": "сильный | средний | слабый | первое лицо", "url": "https://example.com"}
    ],
    "figures": [
        {"value": "1 млн+", "source": 1,
         "quote": "ДОСЛОВНАЯ цитата из источника 1, содержащая это число"},
        {"value": "около 47 лет", "source": 3,
         "derived_from": "Вывод, а не цитата: из года окончания вуза (2001) [3]. "
                         "В тексте досье такое число обязано идти с «около» или «примерно»"},
    ],
}


# Запас, с которым просим сокращать. Ровно до лимита сокращать бесполезно:
# разделы считаются вместе, и сумма пересчитывается заново на каждом круге —
# срезав ровно превышение, автор промахивается снова. На GLM-5.2 это давало
# асимптоту 4760 -> 1246 -> 489 -> 327 -> 215 знаков превышения: пять кругов
# подряд, сходится, но раунды кончаются раньше. Цель с запасом превращает
# асимптоту в один-два шага.
TRIM_HEADROOM = 0.90


def target_for(limit: int) -> int:
    """До скольки просить сократить раздел с лимитом `limit`."""
    return int(limit * TRIM_HEADROOM)


def schema_with_limits() -> dict:
    """SCHEMA с проставленными лимитами разделов.

    Лимиты берутся из SECTIONS, а не переписываются руками: два списка
    разъедутся при первой же правке, и модель будет писать под вчерашнюю рамку.

    Без этого модель узнавала о бюджете только нарушив его: схема описывала,
    ЧТО писать, и молчала о том, СКОЛЬКО. Первое попадание в бюджет выходило
    случайным — у кого хватало запаса раундов, тот и доходил до файла.
    """
    out = dict(SCHEMA)
    for key, _spec, _req, limit in SECTIONS:
        if not limit or key not in out:
            continue
        note = f"ЛИМИТ {limit} знаков"
        if key == "topics":
            note += f" ({TOPICS_LIMIT_WITH_CONTEXT} при заданном meeting_context)"
        value = out[key]
        if isinstance(value, list):
            out[key] = list(value) + [f"<<{note} на весь раздел>>"]
        else:
            out[key] = f"{value}. {note}"
    out["_бюджет"] = (
        f"Весь документ — не более {BUDGET} знаков ({MAX_PAGES} страницы); "
        f"с заданным meeting_context — {BUDGET_WITH_CONTEXT} ({BUDGET_WITH_CONTEXT // CHARS_PER_PAGE} страницы). "
        f"Лимит каждого раздела — отказ, а не пожелание: превышение любого из них "
        f"не даст собрать документ. Пишите сразу под рамку."
    )
    # Всё, на что сборка отказывает, — одним списком и ДО первой записи JSON.
    # В живых прогонах агент узнавал эти правила по одному через отказы и
    # тратил на круги «записал — отказ — поправил» по 20–40 ходов.
    out["_сборка_откажет_если"] = [
        "число от двух цифр (кроме годов 1900–2099, дней в датах «13 марта» и раздела "
        "«Не подтверждено») есть в тексте, но нет записи в figures: "
        "{value, source: номер из sources, quote: дословная цитата источника на любом языке} "
        "или {value, derived_from: как выведено} — тогда в тексте «около»/«примерно»",
        "величина записана словами («восемьдесят шесть», «три миллиарда») — только цифрами",
        "в «who» или «known_for» есть фраза от 25 знаков без номера источника [n]",
        "в тексте есть ссылка [n], а источника с таким n нет в sources (лишние источники без "
        "ссылок не мешают — сборка уберёт их и перенумерует остальные сама)",
        "в любом разделе есть сведения о супругах, детях, родственниках, здоровье, болезнях, "
        "смерти близких — в «avoid» тема называется только обобщённо: «личная жизнь и семья»",
        "источник Википедия/энциклопедия помечен strength «сильный» — только «средний» или «слабый»",
        "превышен лимит раздела или общий бюджет (см. ЛИМИТ у каждого поля)",
        "поле talk_about вместо topics; номер источника — поле n в sources, в figures — поле source",
        "verify_facts.py не запускался без --dry-run или не подтвердил утверждение",
        "в журнале search.py меньше 6 успешных запросов Sonar с именем этого человека",
        "меньше половины источников досье (по сайтам) нашёл search.py — источники берите из "
        "его ответов, а не из встроенного поиска",
    ]
    return out


def as_text(value) -> str:
    """Разделы приходят строкой или списком — приводим к тексту одинаково."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "\n".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def budget_for(data: dict) -> int:
    """Общий бюджет знаков.

    Когда владелец дал контекст встречи, «Темы на обсуждение» становятся
    главным разделом документа: там сводится опыт человека с повесткой
    мероприятия. Ужимать его до 800 знаков — терять ровно то, ради чего
    досье и заказывали. Поэтому при заданном контексте бюджет раздела
    растёт до 2000, а весь документ — до трёх страниц.
    """
    return BUDGET_WITH_CONTEXT if as_text(data.get("meeting_context")) else BUDGET


def limits_for(data: dict) -> dict:
    """Лимиты разделов; при заданном контексте «Темы» расширяются."""
    limits = {key: limit for key, _t, _r, limit in SECTIONS}
    if as_text(data.get("meeting_context")):
        limits["topics"] = TOPICS_LIMIT_WITH_CONTEXT
    return limits


def measure(data: dict) -> tuple[int, list[tuple[str, int, int]]]:
    """Считает знаки по разделам. Возвращает (всего, [(раздел, факт, бюджет)])."""
    rows = []
    gender = data.get("gender") or "m"
    limits = limits_for(data)
    total = len(as_text(data.get("name"))) + len(as_text(data.get("last_known_role"))) + 60
    for key, spec, _required, _limit in SECTIONS:
        title = heading(spec, gender)
        limit = limits[key]
        n = len(as_text(data.get(key)))
        if n:
            n += len(title) + 2
        # Полнота данных в документ не идёт — и место не занимает.
        if key in HIDDEN_IN_DOCX:
            n = 0
        total += n
        rows.append((title, n, limit))
    # Таблица источников: строка занимает примерно 90 знаков полезной ширины.
    # Отдельной строкой в отчёте: 30 источников — это половина бюджета, и без
    # неё «превышен бюджет» при скромных разделах выглядел загадкой.
    # Считаются только источники, на которые есть ссылки: остальные сборка
    # уберёт сама. Раньше лишние строки съедали бюджет, агент удалял их
    # руками — и вместе с ними источники, на которые ссылался текст.
    srcs = [s for s in (data.get("sources") or []) if isinstance(s, dict)]
    cited = set(cited_numbers(data))
    used = [s for s in srcs if str(s.get("n")) in cited] if cited else srcs
    total += 90 * len(used)
    rows.append((f"Источники ({len(used)} × 90)", 90 * len(used), 0))
    return total, rows


# Поля с текстом, где стоят ссылки [n], — в порядке документа.
TEXT_FIELDS = ["last_known_role"] + [k for k, _s, _r, _l in SECTIONS]


def cited_numbers(data: dict) -> list:
    """Номера источников в порядке первого упоминания (текст, затем figures)."""
    out = []
    for key in TEXT_FIELDS:
        for n in _vf().cite_numbers(as_text(data.get(key))):
            if str(n) not in out:
                out.append(str(n))
    for f in data.get("figures") or []:
        if isinstance(f, dict) and f.get("source") not in (None, ""):
            if str(f.get("source")) not in out:
                out.append(str(f.get("source")))
    return out


def dangling_citations(data: dict) -> list:
    """Номера, на которые ссылается текст, но которых нет в sources."""
    have = {str(s.get("n")) for s in (data.get("sources") or []) if isinstance(s, dict)}
    out = []
    for key in TEXT_FIELDS:
        for n in _vf().cite_numbers(as_text(data.get(key))):
            if str(n) not in have and (key, str(n)) not in out:
                out.append((key, str(n)))
    return out


_CITE_GROUP_RE = re.compile(r"\[(\d+(?:\s*[,;–—-]\s*\d+)*)\]")


def prepare_sources(data: dict) -> dict:
    """Копия досье для документа и чата: источники без ссылок убраны, остальные
    перенумерованы 1, 2, 3… в порядке первого упоминания, ссылки в тексте и в
    figures переписаны. Номера из брифа можно ставить как есть — порядок
    наведёт сборка. Исходный dossier.json не меняется."""
    import copy
    out = copy.deepcopy(data)
    order = cited_numbers(out)
    srcs = [s for s in (out.get("sources") or []) if isinstance(s, dict)]
    by_n = {str(s.get("n")): s for s in srcs}
    order = [n for n in order if n in by_n]
    if not order:
        return out
    mapping = {old: str(i) for i, old in enumerate(order, 1)}

    def expand(group: str) -> list:
        nums = []
        for part in re.split(r"\s*[,;]\s*", group):
            m = re.match(r"^(\d+)\s*[–—-]\s*(\d+)$", part.strip())
            if m and int(m.group(2)) - int(m.group(1)) <= 20:
                nums += [str(x) for x in range(int(m.group(1)), int(m.group(2)) + 1)]
            elif part.strip().isdigit():
                nums.append(part.strip())
        return nums

    def repl(m):
        new = []
        for n in expand(m.group(1)):
            k = mapping.get(n)
            if k and k not in new:
                new.append(k)
        new.sort(key=int)
        return "[" + ", ".join(new) + "]" if new else ""

    def rewrite(value):
        if isinstance(value, str):
            return _CITE_GROUP_RE.sub(repl, value)
        if isinstance(value, list):
            return [rewrite(v) for v in value]
        return value

    for key in TEXT_FIELDS:
        if key in out:
            out[key] = rewrite(out[key])
    for f in out.get("figures") or []:
        if isinstance(f, dict) and str(f.get("source")) in mapping:
            f["source"] = int(mapping[str(f.get("source"))])
    new_srcs = []
    for old in order:
        s = dict(by_n[old])
        s["n"] = int(mapping[old])
        new_srcs.append(s)
    out["sources"] = new_srcs
    return out


# --- Проверка цифр -----------------------------------------------------------
# Одно из досье утверждало «аналитика для 1 млн+
# частных инвесторов [1]». Источник [1] — собственная анкета человека в отраслевом реестре —
# говорит про частных инвесторов и оба канала, но НИКАКОГО числа не содержит.
# Сплошной поиск по 194 333 знакам всей доказательной базы прогона дал ноль
# совпадений «число + инвестор». Модель взяла верное утверждение и дописала к
# нему порядок величины, оставив ссылку на источник, в котором его нет.
#
# Опаснее всего то, что число правдоподобное: проверить его на глаз нельзя.
# Поэтому проверка машинная, а не инструкцией. Правило простое: каждое
# числовое утверждение в тексте обязано иметь запись в `figures` — либо с
# ДОСЛОВНОЙ цитатой источника, где это число стоит, либо с пометкой, что оно
# выведено. Процитировать то, чего в источнике нет, невозможно.

_CITE_RE = re.compile(r"\[\d+(?:\s*[,;–—-]\s*\d+)*\]")
_SCALE = (r"трлн|триллион\w*|млн|млрд|тыс(?:яч[аи]?|\.)?|миллион\w*|миллиард\w*|%|руб\w*|₽|"
          r"долл\w*|\$|€|bn\b|B(?![A-Za-z])")
_FIGURE_PATTERNS = [
    # Число со шкалой: «1 млн+», «250 млн», «15 %», «$3 млрд», «₽1,2 трлн», «$1.5B».
    # Не внутри обозначения: «B2B», «A100 млн» — не величины.
    re.compile(r"(?:[$€₽]\s*|(?<![\w.,/-]))\d[\d\s.,]*\+?\s*(?:%s)" % _SCALE, re.I),
    # Голое целое от двух знаков: «47 лет», «15 отраслей», «950 советов» — но НЕ
    # год. Порог именно двузначный: возраст и счётные утверждения («14+
    # инвестбанков») — самые частые места, где к верному факту дописывают
    # неверную величину. Однозначные числа пропускаем: шума от них больше, чем
    # риска.
    # Разряды через пробел («10 738», «10 000») — одно число, а не «10» и «000».
    # Не величины: цифры в обозначениях («x86», «H100», «COVID-19», «МС-21»,
    # «топ-10»), десятилетия и порядковые («90-х», «10-й»), законы («152-ФЗ»),
    # дроби и режимы («24/7», «50/50»).
    re.compile(r"(?<![\w.,/-])(?:\d{1,3}(?:[   ]\d{3})+|\d{2,})"
               r"(?!\d|[.,]\d|[A-Za-zА-Яа-я]|\s*-\s*(?:х|е|й|я|го|му|м|ФЗ)(?![А-Яа-я])|\s*-\s*[А-ЯA-Z]|/)"),
]
# Названия, в которые входит число, но которые не величина: «Fortune 500»,
# «РБК 500», «ISO 9001», «iPhone 15», «ВТБ 24», «Forbes Global 2000».
_NAMED_NUMBER_RE = re.compile(
    r"(?i)(?<!\w)(?:fortune(?:\s+global)?|forbes(?:\s+global)?|global|iso|iphone|galaxy|pixel|windows|"
    r"рбк|втб|covid|sars-cov|top|топ|рейтинг[а-я]*|список[а-я]*|inc\.?|series|серии|серия)"
    r"\s*-?\s*\d+")
_YEAR_RE = re.compile(r"^(?:1[89]|20)\d{2}$")
_HEDGES = ("около", "примерно", "порядка", "ориентировочно", "оценк", "приблизительно", "~")


def _norm_figure(text: str) -> str:
    """Сводим написание к сравнимому виду: регистр, пробелы, плюс, неразрывные."""
    s = str(text or "").lower().replace(" ", " ").replace("+", " ")
    s = re.sub(r"[\s,]+", " ", s)
    return s.strip(" .")


def _vf():
    """verify_facts как модуль: общие функции без дублирования кода."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import verify_facts  # noqa: E402
    return verify_facts


def _figure_in_text(value: str, text: str) -> bool:
    """«$10 млрд» в досье и «$10 billion» в цитате — одно число."""
    try:
        return _vf().figure_in_text(value, text)
    except Exception:  # noqa: BLE001 — сравнение строк выше остаётся в силе
        return False


_DAY_OF_MONTH_RE = re.compile(
    r"(?i)(?<![\d.,])\d{1,2}(?:-?(?:го|е|й))?\s+(?:января|февраля|марта|апреля|мая|июня|июля|августа|"
    r"сентября|октября|ноября|декабря|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|"
    r"july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b|"
    r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|"
    r"sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?\s+\d{1,2}(?:st|nd|rd|th)?\b(?!\s*%)")


def _numeric_claims(data: dict) -> list[tuple[str, str]]:
    """Находит числовые утверждения в теле досье. Возвращает [(раздел, фрагмент)]."""
    found: list[tuple[str, str]] = []
    fields = [k for k, _s, _r, _l in SECTIONS if k != "completeness"]
    fields.append("last_known_role")
    for key in fields:
        text = _NAMED_NUMBER_RE.sub(" ", _CITE_RE.sub(" ", as_text(data.get(key))))
        # День месяца — часть даты, а не величина: «13 марта 1956», «March 13».
        # В прогоне каждая дата рождения и назначения требовала записи в figures.
        text = _DAY_OF_MONTH_RE.sub(" ", text)
        for pat in _FIGURE_PATTERNS:
            for m in pat.finditer(text):
                frag = m.group(0).strip()
                # Год — не величина: «с 2022 года» проверять нечего.
                if _YEAR_RE.match(frag.replace(" ", "")):
                    continue
                found.append((key, frag))
    return found


def check_figures(data: dict) -> list[str]:
    """Каждое число в тексте должно быть подтверждено записью в `figures`."""
    problems: list[str] = []
    raw = data.get("figures")
    figures = [f for f in (raw or []) if isinstance(f, dict)]
    known_sources = {str(s.get("n")) for s in (data.get("sources") or []) if isinstance(s, dict)}

    for fig in figures:
        value = str(fig.get("value") or "").strip()
        if not value:
            problems.append("в figures есть запись без поля «value»")
            continue
        src = str(fig.get("source") or "").strip()
        if src and src not in known_sources:
            problems.append(f"figures «{value}»: источник [{src}] отсутствует в списке источников")
        quote = str(fig.get("quote") or "").strip()
        derived = str(fig.get("derived_from") or "").strip()
        if not quote and not derived:
            problems.append(
                f"figures «{value}»: нужна либо дословная цитата источника (quote), "
                f"либо пояснение вывода (derived_from)")
            continue
        if quote and _norm_figure(value) not in _norm_figure(quote) and not _figure_in_text(value, quote):
            # В прогоне агент трижды менял запись числа («12 930 300 000» →
            # «$12,93 млрд» → «12,9»), не видя, какое число в цитате стоит:
            # показываем его — и правка выходит с первого раза.
            in_quote = re.findall(r"\d+(?:[   ]\d{3})*(?:[.,]\d+)?", quote)
            seen_q = list(dict.fromkeys(n.strip() for n in in_quote))[:4]
            tail = (f" В цитате стоит: {', '.join(seen_q)} — запишите число в value и в "
                    f"тексте так же (то же округление)" if seen_q
                    else " В цитате нет ни одной цифры")
            problems.append(
                f"figures «{value}»: этого числа в quote нет.{tail}. Иначе — процитируйте "
                f"источник ДОСЛОВНО (язык цитаты любой: «$10 млрд» = «$10 billion») или "
                f"пометьте число как выведенное (derived_from + «около» в тексте)")
        if quote and not src:
            problems.append(f"figures «{value}»: цитата есть, а номер источника не указан")

    covered = [_norm_figure(f.get("value")) for f in figures if f.get("value")]
    hedged = {
        _norm_figure(f.get("value"))
        for f in figures
        if f.get("derived_from") and not f.get("quote")
    }
    for key, frag in _numeric_claims(data):
        if key == "unconfirmed":
            # «Не подтверждено» и есть место для спорного числа («200 [1] или
            # 350 [2]»): досье его не утверждает. Требование цитаты здесь
            # противоречило инструкции и в прогоне дало четыре лишних круга.
            continue
        norm = _norm_figure(frag)
        match = next((c for c in covered if c and (c in norm or norm in c)), None)
        if match is None:
            problems.append(
                f"раздел «{key}»: число «{frag}» ничем не подтверждено — "
                f"добавьте запись в figures с дословной цитатой источника "
                f"или уберите число из текста")
            continue
        if match in hedged:
            context = _CITE_RE.sub(" ", as_text(data.get(key))).lower()
            if not any(h in context for h in _HEDGES):
                problems.append(
                    f"раздел «{key}»: «{frag}» выведено, а не взято из источника — "
                    f"такое число подаётся с «около» или «примерно»")
    return problems


# --- Числа словами ------------------------------------------------------------
# Проверку цифр можно обойти, записав величину словами: «около восьмидесяти
# шести подчинённых», «свыше четырёх триллионов». Так и случилось в живом
# прогоне — скрипт искал цифры и не видел слов. Поэтому числительные от
# одиннадцати и выше, а также шкалы («тысяч», «миллионов», «триллионов») без
# цифры перед ними считаются обходом: величина пишется цифрами и идёт в figures.
_NUMWORD_RE = re.compile(
    r"(?<![\w-])(одиннадцат|двенадцат|тринадцат|четырнадцат|пятнадцат|шестнадцат|"
    r"семнадцат|восемнадцат|девятнадцат|двадцат|тридцат|сорок[аеу]?(?![\w-])|пятьдесят|"
    r"пятидесят|шестьдесят|шестидесят|семьдесят|семидесят|восемьдесят|восьмидесят|"
    r"девяност|двухсот|двести|тр[её]хсот|триста|четыр[её]хсот|четыреста|пятьсот|"
    r"пятисот|шестьсот|шестисот|семьсот|семисот|восемьсот|восьмисот|девятьсот|девятисот)\w*",
    re.I)
_SCALEWORD_RE = re.compile(
    r"(?<![\w-])(тысяч\w*|миллион\w*|миллиард\w*|триллион\w*|thousand|million|billion|trillion)",
    re.I)


def check_number_words(data: dict) -> list[str]:
    problems = []
    fields = [k for k, _s, _r, _l in SECTIONS
              if k not in ("completeness", "unconfirmed")] + ["last_known_role"]
    for key in fields:
        text = _CITE_RE.sub(" ", as_text(data.get(key)))
        for m in _NUMWORD_RE.finditer(text):
            problems.append(
                f"раздел «{key}»: число записано словами («{m.group(0)}») — так оно обходит "
                f"проверку. Запишите цифрами и добавьте в figures с цитатой, либо уберите")
        for m in _SCALEWORD_RE.finditer(text):
            before = text[:m.start()].rstrip()
            if before and (before[-1].isdigit() or before[-1] in "+$€₽"):
                continue  # «4 триллиона», «$3 млрд» — обычная величина, её ловит проверка цифр
            problems.append(
                f"раздел «{key}»: величина без цифры («…{text[max(0, m.start() - 25):m.end()]}») — "
                f"запишите число цифрами с записью в figures или уберите величину")
    return problems


# --- Запретные сведения ---------------------------------------------------------
# Инструкция: не собираем данные членов семьи, здоровье, частную жизнь. В живом
# прогоне в «Кто он» попали жена, дети и двоюродная сестра. Проверка грубая
# намеренно: лучше убрать лишнее, чем унести на встречу семейную справку.
_PRIVATE_RE = re.compile(
    r"(?<!\w)(жена|жены|жене|женой|женат\w*|замуж\w*|супруг\w*|муж|мужа|мужу|мужем|"
    r"сын|сына|сыну|сыном|сыновья\w*|сыновей|доч(ь|ери|ерью|ерей|ерям)|ребён\w*|ребен\w*|"
    r"двоюродн\w*|кузен\w*|кузин\w*|племянни\w*|внук(?!ов[оа])\w*|внучк\w*|"
    r"от(ец|ца|цу|цом)(?!\s*-|\s+[А-ЯA-Z])|мать|матери|матерью|"
    r"брат(а|у|ом|е|ья|ьев|ьям)?|сестр(а|ы|е|у|ой|ёй|ами)?|родител(и|ей|ям|ями|ях)|"
    r"вдов(а|ы|ой|ец|ца)|развел(ся|ась|ись)|развёл(ся)?|"
    r"диагноз\w*|госпитализ\w*|сексуальн\w* ориентаци\w*|домашн\w* адрес\w*|"
    r"скончал\w*|умер(?:ла|ли|ший|шая|шего|шей|шему)?|похорон\w*|"
    r"инсульт\w*|инфаркт\w*|"
    r"wife|husband|daughters?|divorc\w*|widow\w*|passed away)(?!\w)",
    re.I)
# Слова, частные ТОЛЬКО рядом с человеком: «болезни роста», «смерть рынка»,
# «программа для детей», «онкологические препараты» — деловой текст. Отказ,
# лишь если во фразе есть «он/она/его/её/у него».
_PRIVATE_IF_PERSONAL_RE = re.compile(
    r"(?<!\w)(болезн\w*|смерт(?!ност)\w*|гибел\w*|погиб\w*|инвалид\w*|паралич\w*|"
    r"церебральн\w*|онколог\w*|рак(ом|а|е)?|дет(и|ей|ям|ьми)|похищ\w*|здоровь\w*|"
    r"развод\w*|в браке)(?!\w)", re.I)
_PERSONAL_RE = re.compile(r"(?<!\w)(он|она|его|её|ее|ему|ей|у него|у неё|у нее|сам|сама)(?!\w)", re.I)


def check_private(data: dict) -> list[str]:
    """Семья, здоровье, частная жизнь — ни в одном разделе.

    «Чего не касаться» раньше не проверялся, и в живом прогоне туда попала
    история о болезни и смерти сына героя досье — с именем и годом. Раздел
    называет тему, а не пересказывает её: «личная жизнь и семья» — достаточно.
    """
    problems = []
    fields = [k for k, _s, _r, _l in SECTIONS if k != "completeness"] + ["last_known_role"]
    for key in fields:
        text = as_text(data.get(key))
        hits = [m.group(0) for m in _PRIVATE_RE.finditer(text)]
        for sent in split_sentences(text):
            if _PERSONAL_RE.search(sent):
                hits += [m.group(0) for m in _PRIVATE_IF_PERSONAL_RE.finditer(sent)]
        for word in dict.fromkeys(hits):
            hint = (" В «Чего не касаться» назовите тему обобщённо («личная жизнь и семья»), "
                    "без имён, дат и подробностей" if key == "avoid" else " Уберите")
            problems.append(
                f"раздел «{key}»: запретные сведения («{word}») — семья, здоровье и "
                f"частная жизнь в досье и в ответе не упоминаются.{hint}")
    return problems


# --- Ссылки на источники --------------------------------------------------------
_REFERENCE_DOMAINS = ("wikipedia.org", "wikiwand.com", "ruwiki.ru", "britannica.com")


def split_sentences(text: str) -> list[str]:
    """Фразы текста без разрывов на сокращениях («1969 г. в Тайнане», «Л. Су»).
    Тот же разбор, что в verify_facts.py: проверка ссылок и триангуляция
    должны видеть одни и те же фразы."""
    return _vf().split_sentences(text)


def check_citations(data: dict) -> list[str]:
    """Каждая фраза в «Кто он» и «Чем известен» несёт номер источника."""
    problems = []
    for key in ("who", "known_for"):
        for sent in split_sentences(as_text(data.get(key))):
            sent = sent.strip(" -•\t")
            if len(sent) >= 25 and not _CITE_RE.search(sent) and "[Анализ]" not in sent:
                # В прогоне агент дважды не понял отказ: номер стоял в конце
                # строки, а «;» внутри делит её на две фразы, и первой номер
                # тоже нужен — иначе её утверждение уходит без проверки.
                semi = (" Внутри строки стоит «;» — это граница фразы: поставьте номер источника "
                        "перед «;» или замените «;» точкой с номером."
                        if sent.rstrip().endswith(";") else "")
                problems.append(f"раздел «{key}»: фраза без номера источника — «{sent[:70]}…».{semi}")
    for src in data.get("sources") or []:
        if not isinstance(src, dict):
            continue
        url = str(src.get("url") or "").lower()
        if any(d in url for d in _REFERENCE_DOMAINS) and "сильн" in str(src.get("strength") or "").lower():
            problems.append(
                f"источник [{src.get('n')}]: справочник/энциклопедия — это средний или слабый "
                f"источник, не «сильный»")
    return problems


# --- Триангуляция: сборка без неё невозможна -------------------------------------
def triangulation_gaps(data: dict) -> list[str]:
    """Утверждения, которые verify_facts.py НЕ подтвердил (по его кэшу)."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import verify_facts as vf  # noqa: E402

    srcmap = vf.sources_by_number(data)
    cache = vf.load_cache()
    good = vf.GOOD_STATUSES
    gaps = []
    for claim in vf.collect_claims(data):
        if vf.primary_only(claim, srcmap):
            continue
        hit = cache.get(vf.claim_key(claim, srcmap))
        if not (isinstance(hit, dict) and hit.get("status") in good):
            gaps.append(claim["text"][:90])
    return gaps


def unverified_allowed():
    """Причина сбоя триангуляции, если verify_facts.py недавно упал из-за ключа
    или сети; иначе None — тогда --unverified не принимается."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import time as _time
    import verify_facts as vf  # noqa: E402
    try:
        st = json.loads((vf.work_dir() / vf.STATUS_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if st.get("status") not in ("no_key", "auth", "network"):
        return None
    if _time.time() - float(st.get("ts") or 0) > 6 * 3600:
        return None
    return str(st.get("detail") or st.get("status"))


# --- Поиск шёл через Sonar -------------------------------------------------------
# В живом прогоне агент прочитал «ищите через search.py», сам написал «вижу
# новый шаг — search.py» и всё равно собрал материал встроенным поиском:
# восемь запросов, ни одного через Sonar. Инструкция этого не удерживает,
# поэтому сборка сверяется с журналом search.py: был ли хотя бы один
# успешный запрос про этого человека за последние часы.
SEARCH_WINDOW_HOURS = 12
# Порог — одна полная волна. В прогоне 1.0.6 при пороге «хотя бы один запрос»
# агент собрал всё встроенным поиском, а в Sonar отправил два запроса в самом
# конце — ровно чтобы сборка пропустила. Шесть — это первая волна методики
# (личность, работодатель, латиница, LinkedIn, соцсети, тёзки), не норма в 40.
MIN_SONAR_QUERIES = 6
_TRANSLIT = dict(zip(
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o",
     "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya"]))


def _latin(text: str) -> str:
    s = "".join(_TRANSLIT.get(ch, ch) for ch in str(text or "").lower())
    s = s.replace("dzh", "j").replace("kh", "h").replace("ё", "e")
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def _skel(token: str) -> str:
    """Согласный скелет слова в латинице: «Kaspersky»/«Касперской» → «kspr»,
    «Musk»/«Маск» → «msk». Ловит падежи и разные транслитерации."""
    t = _latin(token).strip()
    t = t.replace("shch", "s").replace("sch", "s").replace("sh", "s").replace("ch", "c")
    t = t.replace("zh", "s").replace("ts", "s").replace("ck", "k").replace("x", "ks")
    t = t.replace("ph", "f").replace("z", "s").replace("c", "k").replace("q", "k")
    sk = re.sub(r"[aeiouyhjw ]+", "", t)
    sk = re.sub(r"(.)\1+", r"\1", sk)
    return sk[:4] if len(sk) >= 3 else "=" + re.sub(r"[^a-z]", "", t)


def _name_variants(data: dict) -> list[list[str]]:
    """Варианты имени: основное, в скобках, name_en/name_latin — списками слов."""
    raw = [as_text(data.get(k)) for k in ("name", "name_en", "name_latin")]
    out = []
    for r in raw:
        for part in re.split(r"[()\[\]/]", r):
            toks = [t for t in re.findall(r"[A-Za-zА-Яа-яЁё]+", part) if len(t) >= 2]
            if toks:
                out.append(toks)
    return out


def _surname(tokens: list[str]) -> str:
    """Фамилия: последняя часть, а при отчестве («Иванов Пётр Сергеевич») — первая."""
    if len(tokens) >= 3 and re.search(r"(вич|вна|ична|чна|ogly|ovich|ovna)$", tokens[-1], re.I):
        return tokens[0]
    return tokens[-1]


def _name_keys(data: dict) -> list[str]:
    """Ключи фамилии по всем вариантам имени (для совместимости и подсказок)."""
    return sorted({_skel(_surname(v)) for v in _name_variants(data)})


def _about_person(text: str, data: dict) -> bool:
    """Запрос про этого человека: есть фамилия (в любом падеже и написании)
    или все части имени. Совпадение по одному имени («Наталья») не считается."""
    qkeys = {_skel(t) for t in re.findall(r"[A-Za-zА-Яа-яЁё]+", str(text or "")) if len(t) >= 2}
    for v in _name_variants(data):
        if _skel(_surname(v)) in qkeys:
            return True
        if len(v) >= 2 and all(_skel(t) in qkeys for t in v):
            return True
    return False


def search_evidence(data: dict) -> tuple[int, int]:
    """(успешных запросов Sonar про этого человека, всего успешных) за окно."""
    import time as _time
    path = _vf().work_dir() / "search_log.jsonl"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return 0, 0
    now = _time.time()
    about, total = 0, 0
    for line in lines:
        try:
            rec = json.loads(line)
            ts = _time.mktime(_time.strptime(str(rec.get("ts")), "%Y-%m-%dT%H:%M:%S"))
        except (ValueError, TypeError, json.JSONDecodeError, OverflowError):
            continue
        if not rec.get("ok") or now - ts > SEARCH_WINDOW_HOURS * 3600:
            continue
        total += 1
        if _about_person(rec.get("person") or "", data) or _about_person(rec.get("query"), data):
            about += 1
    return about, total


def _reg_domain(url: str) -> str:
    """ru.wikipedia.org → wikipedia.org, news.bbc.co.uk → bbc.co.uk."""
    host = re.sub(r"^(?:[a-z]+://)?(?:www\.)?", "", str(url or "").strip().lower()).split("/")[0].split(":")[0]
    parts = [x for x in host.split(".") if x]
    if len(parts) <= 2:
        return ".".join(parts)
    if len(parts[-1]) == 2 and parts[-2] in ("co", "com", "org", "net", "gov", "ac", "edu"):
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def sonar_domains():
    """Сайты из ответов search.py за окно поиска. None — журнал старый, без адресов."""
    import time as _time
    path = _vf().work_dir() / "search_log.jsonl"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    seen_urls, out = False, set()
    now = _time.time()
    for line in lines:
        try:
            rec = json.loads(line)
            ts = _time.mktime(_time.strptime(str(rec.get("ts")), "%Y-%m-%dT%H:%M:%S"))
        except (ValueError, TypeError, json.JSONDecodeError, OverflowError):
            continue
        if not rec.get("ok") or now - ts > SEARCH_WINDOW_HOURS * 3600 or "urls" not in rec:
            continue
        seen_urls = True
        out.update(_reg_domain(u) for u in rec.get("urls") or [] if u)
    return out if seen_urls else None


def sonar_share(data: dict):
    """(из Sonar, всего, [источники не из Sonar]) или None, если сверять не с чем."""
    domains = sonar_domains()
    if domains is None:
        return None
    srcs = [s for s in (data.get("sources") or []) if isinstance(s, dict) and s.get("url")]
    outside = [s for s in srcs if _reg_domain(s.get("url")) not in domains]
    return len(srcs) - len(outside), len(srcs), outside


_EVALUATIVE_RE = re.compile(
    r"(?<![\w-])(крупнейш\w*|одн(?:им|ой|ого|а|у) из (?:сам|крупн|ведущ|лучш|наиболее|влиятельн|ключев|главн|известн)\w*|"
    r"один из (?:сам|крупн|ведущ|лучш|наиболее|влиятельн|ключев|главн|известн)\w*|самы[йхем]\w*|наиболее|легендарн\w*|"
    r"выдающ\w*|уникальн\w*|беспрецедентн\w*|культов\w*)", re.I)


def evaluative_phrases(data: dict) -> list[tuple[str, str]]:
    """Оценки, которые Sonar при проверке почти всегда помечает «ЧАСТИЧНО»."""
    found = []
    for key in ("summary", "who", "known_for"):
        text = as_text(data.get(key))
        for m in _EVALUATIVE_RE.finditer(text):
            found.append((key, text[max(0, m.start() - 20):m.end() + 25].strip()))
    return found


def source_notes(data: dict) -> list[str]:
    """Повторы адресов и источники без ссылок: место в бюджете (90 знаков на
    строку) и путаница в списке. В досье прогона [2]=[6] и [5]=[7], а [9]
    остался от убранного факта. Подсказка, не отказ: после проверки фактов
    отказ по такой мелочи стоил бы лишнего круга."""
    notes = []
    srcs = [s for s in (data.get("sources") or []) if isinstance(s, dict)]
    seen: dict[str, str] = {}
    for s in srcs:
        url = re.sub(r"[#?].*$", "", str(s.get("url") or "").strip().lower()).rstrip("/")
        url = re.sub(r"^https?://(www\.)?", "", url)
        if not url:
            continue
        if url in seen:
            notes.append(f"источники [{seen[url]}] и [{s.get('n')}] — один адрес: оставьте один номер "
                         f"и поправьте ссылки в тексте")
        else:
            seen[url] = str(s.get("n"))
    body = " ".join(as_text(data.get(k)) for k, _s, _r, _l in SECTIONS) + " " + \
        as_text(data.get("last_known_role")) + " " + \
        " ".join(str(f.get("source") or "") and f"[{f.get('source')}]"
                 for f in (data.get("figures") or []) if isinstance(f, dict))
    cited = set(_vf().cite_numbers(body))
    unused = [str(s.get("n")) for s in srcs if str(s.get("n")) not in cited]
    if unused:
        notes.append("источники без ссылок в тексте: " + ", ".join(f"[{n}]" for n in unused)
                     + " — в документ не попадут, сборка уберёт их сама; править не нужно")
    return notes


def _short_source(s: dict) -> str:
    """«[3] Nandan Nilekani — Britannica (britannica.com)» — без длинного URL."""
    title = re.sub(r"\s+", " ", str(s.get("title") or "")).strip()
    if len(title) > 60:
        title = title[:57].rstrip(" ,.;:—-") + "…"
    host = re.sub(r"^(?:https?://)?(?:www\.)?", "", str(s.get("url") or "")).split("/")[0]
    body = f"{title} ({host})" if title and host and host.lower() not in title.lower() else (title or host)
    return f"[{s.get('n')}] {body}".strip()


_USD_RE = re.compile(
    r"(?<![\w$])(?:US)?\$\s?((?:\d[\d\s.,]*\d|\d)(?:\s*[–—-]\s*\$?\s?(?:\d[\d\s.,]*\d|\d))?)"
    r"(?:\s*(трлн|млрд|млн|тыс\.?|trillion|billion|million|thousand|bn|B|M|K)(?![A-Za-zА-Яа-я]))?")
_USD_SCALE = {"trillion": "трлн", "billion": "млрд", "bn": "млрд", "b": "млрд",
              "million": "млн", "m": "млн", "thousand": "тыс.", "k": "тыс."}


def chat_safe_money(text: str) -> str:
    """«$10 млрд» → «10 млрд долл.» — только для текста в чат.

    Чат ГигаАгента рисует текст между двумя знаками «$» как формулу: в одном
    абзаце «с $2 млрд до $5 млрд» превращалось в курсив без пробелов. В
    документе Word знак доллара остаётся как есть."""
    def repl(m):
        num = re.sub(r"\s*[–—-]\s*\$?\s?", "–", m.group(1).strip())  # «$10–$20» → «10–20»
        scale = m.group(2) or ""
        scale = _USD_SCALE.get(scale.lower(), scale)
        return f"{num} {scale} долл." if scale else f"{num} долл."
    text = _USD_RE.sub(repl, str(text or ""))
    return text.replace("$", "＄")  # одиночный знак не по шаблону — без формулы


def chat_text(data: dict, ver: str, why_unverified: str = "") -> str:
    """Готовый текст ответа в чат — тот же, что в документе, в том же порядке.

    Агент раз за разом начинал ответ с «Готово. Файл отправлен.» вместо оценки
    полноты и пересказывал досье своими словами, добавляя то, что проверка
    отсекла. Поэтому текст собирает скрипт — из того же JSON, что и документ.
    """
    gender = data.get("gender") or "m"
    out = []
    if why_unverified:
        out.append(f"⚠️ Триангуляция НЕ отработала: {why_unverified}. "
                   f"Досье через внешние источники НЕ проверено.")
    out.append(f"**Полнота данных:** {as_text(data.get('completeness'))}")
    out.append("")
    out.append(f"## Досье — {as_text(data.get('name'))}")
    role = as_text(data.get("last_known_role"))
    as_of = ru_dates(as_text(data.get("as_of")))
    if role:
        out.append(role + (f" (по состоянию на {as_of})" if as_of else ""))
    for key, spec, _req, _lim in SECTIONS:
        if key == "completeness":
            continue
        value = data.get(key)
        if not as_text(value):
            continue
        out.append("")
        out.append(f"**{heading(spec, gender)}**")
        if isinstance(value, (list, tuple)):
            out.extend(f"- {str(v).strip()}" for v in value if str(v).strip())
        else:
            out.append(as_text(value))
    srcs = [s for s in (data.get("sources") or []) if isinstance(s, dict)]
    if srcs:
        out.append("")
        out.append("**Источники**")
        # Одной строкой и коротко: полный список с адресами — в документе.
        # 26 строк с URL агент из ответа вырезал целиком, а короткую строку
        # оставлял (прогоны 1.0.6 и 1.1.0).
        out.append(" · ".join(_short_source(s) for s in srcs))
    out.append("")
    check = "БЕЗ ТРИАНГУЛЯЦИИ" if why_unverified else "проверка verify_facts"
    # Модели в строке нет намеренно: агент в этой установке её не знает и во
    # всех прогонах подписывал не ту (opus вместо sonnet по журналу задачи).
    # Неверная подпись хуже никакой; модель видна в настройках и журнале.
    out.append(f"Собрано: dossier v{ver} · {check} · вёрстка render_dossier")
    return chat_safe_money("\n".join(out))


def skill_version() -> str:
    try:
        head = (pathlib.Path(__file__).resolve().parent.parent / "SKILL.md").read_text(encoding="utf-8")[:3000]
        m = re.search(r"^version:\s*([\w.]+)", head, re.M)
        return m.group(1) if m else "?"
    except OSError:
        return "?"


def validate(data: dict) -> list[str]:
    problems = []
    for key in ("name", "last_known_role", "summary", "sources"):
        if not as_text(data.get(key)) and not data.get(key):
            problems.append(f"нет обязательного поля «{key}»")
    gender = data.get("gender") or "m"
    for key, spec, required, _limit in SECTIONS:
        if required and not as_text(data.get(key)):
            if key in HIDDEN_IN_DOCX:
                # В документ не выводится, но нужна для первой строки ответа в чате.
                problems.append(f"поле «{key}» обязательно: оценка полноты идёт первой строкой "
                                f"в чат (в документ не выводится)")
                continue
            problems.append(f"раздел «{heading(spec, gender)}» обязателен — напишите "
                            f"«сведений нет», если наполнить нечем")
    srcs = data.get("sources") or []
    if not isinstance(srcs, list):
        problems.append("sources — это список объектов {n, title, url, strength}")
        srcs = []
    if not srcs:
        problems.append("список источников пуст — досье без источников не сдаётся")
    seen_n = set()
    for s in srcs:
        if not isinstance(s, dict):
            problems.append(f"источник «{str(s)[:40]}» должен быть объектом {{n, title, url, strength}}")
            continue
        if not str(s.get("url") or "").startswith("http"):
            problems.append(f"источник {s.get('n')}: нет адреса")
        if str(s.get("n")) in seen_n:
            problems.append(f"номер источника [{s.get('n')}] повторяется — у каждого свой номер")
        seen_n.add(str(s.get("n")))
    if data.get("gender") in (None, ""):
        problems.append("нет поля gender: 'm' или 'f' — от него зависят заголовки («Кто он/она»)")
    total, rows = measure(data)
    budget = budget_for(data)
    pages = budget // CHARS_PER_PAGE
    if total > budget:
        target = target_for(budget)
        problems.append(
            f"превышен бюджет: {total} знаков против {budget} "
            f"(≈{total / CHARS_PER_PAGE:.1f} страницы вместо {pages}) — "
            f"СОКРАТИТЕ ДО {target} (убрать {total - target}). "
            f"Либо запустите «--fit <файл>»: скрипт срежет сам, по правилу и вслух")
    # Лимит раздела — тоже отказ, а не пометка. Раньше он только печатался:
    # «Кто она 1026 / 600 превышен», и тут же «ГОДНО». Раздел раздувался вдвое,
    # съедал место у остальных, и ловил это лишь общий бюджет — то есть уже
    # тогда, когда документ поехал за два листа.
    for title, actual, limit in rows:
        if limit and actual > limit:
            target = target_for(limit)
            problems.append(
                f"раздел «{title}»: {actual} знаков из {limit} — "
                f"СОКРАТИТЕ ДО {target} (убрать {actual - target}). "
                f"Цель ниже лимита намеренно: разделы считаются вместе, и "
                f"срезав ровно превышение, вы промахнётесь снова")
    if data.get("gender") not in ("m", "f", None, ""):
        problems.append("поле gender принимает только 'm' или 'f'")
    # Отдельного раздела «О чём говорить» нет — всё про разговор идёт в topics.
    # Молча игнорировать лишнее поле нельзя: автор решил бы, что раздел на месте.
    if data.get("talk_about"):
        problems.append(
            "поле «talk_about» не поддерживается: «о чём говорить» и «что обсуждать» — "
            "один раздел «topics». Перенесите содержимое туда")
    # Ссылка на источник, которого нет в списке, — битая: в документе [13]
    # ведёт в никуда. В прогоне агент удалил «лишние» строки источников, чтобы
    # уложиться в объём, а ссылки [13], [17], [18], [22] в тексте остались.
    dang = dangling_citations(data)
    if dang:
        nums = sorted({n for _k, n in dang}, key=lambda x: int(x) if x.isdigit() else 0)
        where = sorted({k for k, _n in dang})
        problems.append(
            f"ссылки на несуществующие источники: {', '.join('[' + n + ']' for n in nums)} "
            f"(разделы: {', '.join(where)}) — верните эти источники в sources (n, url, title из "
            f"брифа) или уберите ссылки. Лишние источники удалять не нужно: сборка уберёт сама")
    problems.extend(check_figures(data))
    problems.extend(check_number_words(data))
    problems.extend(check_private(data))
    problems.extend(check_citations(data))
    return problems


# Ориентиры полноты: ниже них досье при богатом материале выходит тонким.
# Это подсказка (verify_facts показывает её один раз до платной проверки),
# а не условие сборки: у малоизвестного человека писать может быть нечего.
UNDERFILL_MIN = {"summary": 300, "who": 280, "known_for": 380, "topics": 700}
UNDERFILL_ITEMS = {"known_for": 3, "topics": 4}
RICH_MATERIAL = (20, 12)   # ответов Sonar про человека, разных адресов в них


def underfill(data: dict) -> list:
    if re.match(r"\s*данных\s+мало", as_text(data.get("completeness")), re.I):
        return []
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import search  # noqa: E402
        answers, urls = search.person_material(as_text(data.get("name")))
    except Exception:  # noqa: BLE001
        return []
    if answers < RICH_MATERIAL[0] or urls < RICH_MATERIAL[1]:
        return []
    gender = data.get("gender") or "m"
    titles = {k: heading(spec, gender) for k, spec, _r, _l in SECTIONS}
    targets = {"summary": "3–4 предложения, 350–500 знаков", "who": "450–600 знаков",
               "known_for": "3–4 пункта, 500–900 знаков", "topics": "4–5 пунктов, 800–1400 знаков"}
    out = []
    for key, minimum in UNDERFILL_MIN.items():
        value = data.get(key)
        n = len(as_text(value))
        items = len([v for v in value if str(v).strip()]) if isinstance(value, list) else None
        need = UNDERFILL_ITEMS.get(key)
        if n < minimum or (need and items is not None and items < need):
            have = f"{items} пункт(а), {n} знаков" if items is not None else f"{n} знаков"
            out.append(f"«{titles[key]}»: {have} — ориентир {targets[key]}")
    if out:
        out.append(f"материал: {answers} ответов Sonar, {urls} адресов — на полное досье его хватает")
    return out


def require_docx():
    """python-docx — сторонняя библиотека, и без неё скрипт бесполезен.

    Проверяем ДО сбора данных и до записи файла: сообщение «нет python-docx»
    полезнее, чем ImportError из середины сборки.
    """
    try:
        # Всё, что нужно сборке, а не только корень пакета: неполная установка
        # иначе падала бы посреди сборки, когда данные уже собраны.
        from docx import Document  # noqa: F401
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING  # noqa: F401
        from docx.oxml import OxmlElement  # noqa: F401
        from docx.oxml.ns import qn  # noqa: F401
        from docx.shared import Cm, Pt, RGBColor  # noqa: F401
    except ImportError:
        raise SystemExit(
            "[!] Не установлена библиотека python-docx — собрать документ нечем.\n"
            "    Навык объявляет её зависимостью (python-docx>=1.1): проверьте, что\n"
            "    окружение навыка собрано после установки/ревью. Вручную: pip install python-docx")


def default_base() -> pathlib.Path:
    """Каталог, куда разрешено писать.

    По умолчанию — собственный каталог состояния навыка: скрипт не должен
    иметь возможности писать за пределы своей песочницы. Рабочий каталог
    задачи используется, только если он задан явно через OUROBOROS_TASK_DRIVE.
    Готовый файл агент отдаёт владельцу через send_file — тому всё равно,
    из какого каталога читать.
    """
    state = os.environ.get("OUROBOROS_SKILL_STATE_DIR")
    if state:
        return pathlib.Path(state)
    drive = os.environ.get("OUROBOROS_TASK_DRIVE")
    if drive:
        return pathlib.Path(drive)
    return pathlib.Path.cwd()


def safe_out_path(raw: str, base: pathlib.Path) -> pathlib.Path:
    """Не даём записать файл куда угодно.

    Путь приходит аргументом командной строки, а значит в конечном счёте от
    модели. Без ограничения досье можно было бы записать поверх настроек или
    другого навыка. Разрешаем только внутрь base — см. default_base().
    """
    candidate = pathlib.Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = base / candidate
    candidate = candidate.resolve()
    base = base.resolve()
    # Строго ВНУТРЬ base. Оговорки «или сам base» здесь быть не должно: base —
    # это каталог, писать в него как в файл незачем, а лазейку закрывала только
    # проверка расширения ниже.
    if base not in candidate.parents:
        # В прогоне агент передал путь вместо имени, получил отказ и потратил
        # ход. Безопасно и без отказа: берём только имя файла — внутри base.
        name = pathlib.Path(str(raw).replace("\\", "/")).name
        if name and name not in (".", "..") and name.lower().endswith(".docx"):
            fallback = (base / name).resolve()
            if base in fallback.parents:
                print(f"[i] Путь «{raw}» вне рабочего каталога — сохраняю под именем {name}")
                return fallback
        raise SystemExit(
            f"[!] Путь вне рабочего каталога: {candidate}\n"
            f"    Разрешено писать только внутрь {base}\n"
            f"    Уберите ../ и абсолютные пути из имени файла.")
    if candidate.suffix.lower() != ".docx":
        # «Досье — Хаас Рене — Arm» без расширения: в прогоне это стоило хода.
        if candidate.suffix.lower() not in (".pdf", ".doc", ".txt", ".md", ".json", ".html", ".htm",
                                            ".rtf", ".odt", ".xlsx", ".pptx", ".py", ".sh"):
            candidate = candidate.with_name(candidate.name.rstrip(".") + ".docx")
            if base in candidate.parents:
                return candidate
        raise SystemExit(f"[!] Ожидается имя файла .docx, получено: {candidate.name}")
    return candidate


def allowed_roots() -> list[pathlib.Path]:
    """Каталоги, внутри которых скрипту разрешено что-либо ПЕРЕЗАПИСЫВАТЬ."""
    roots = []
    for env in ("OUROBOROS_SKILL_STATE_DIR", "OUROBOROS_TASK_DRIVE"):
        v = os.environ.get(env)
        if v:
            roots.append(pathlib.Path(v).resolve())
    # Каталоги задач: --fit переписывает dossier.json агента на месте. Раньше
    # он писал копию в каталог навыка, агент правил оригинал, а проверка
    # находила копию — и повторяла те же отказы по кругу.
    for root in _vf().task_drive_roots():
        roots.append(root.resolve())
    if not roots:
        roots.append(pathlib.Path.cwd().resolve())
    return roots


def resolve_input(raw: str) -> tuple[pathlib.Path | None, list[str]]:
    """Найти JSON досье. Возвращает (путь или None, где искали).

    Агент часто передаёт голое имя «dossier.json», а текущий каталог скрипта —
    не каталог задачи. Вместо отказа ищем по тем же местам, куда агент мог
    сохранить файл, и при неудаче честно перечисляем, где искали: угадывание
    пути в прошлых прогонах стоило по пятнадцать минут.
    """
    # Один поиск на оба скрипта (verify_facts.resolve_input): каталог задачи
    # раньше каталога навыка. Свой порядок здесь подхватывал устаревшую копию
    # из каталога навыка раньше свежего файла задачи.
    return _vf().resolve_input(raw)


def build(data: dict, out_path: pathlib.Path) -> None:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    doc = Document()

    # Оформление задаётся СТИЛЮ, а не абзацам: иначе таблицы и списки
    # останутся на шрифте по умолчанию, и документ поедет.
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(12)
    # Для кириллицы одного font.name мало — Word берёт шрифт из отдельного
    # поля, и без этой строки текст выйдет другим шрифтом.
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    normal.element.rPr.rFonts.set(qn("w:cs"), "Arial")
    pf = normal.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(6)
    pf.space_before = Pt(0)

    for section in doc.sections:
        section.top_margin = section.bottom_margin = Cm(2)
        section.left_margin = section.right_margin = Cm(2)

    def style_heading(par, size, color=(0x1F, 0x3B, 0x4D)):
        for run in par.runs:
            run.font.name = "Arial"
            run.font.size = Pt(size)
            run.font.bold = True
            run.font.color.rgb = RGBColor(*color)
            run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        par.paragraph_format.space_before = Pt(8)
        par.paragraph_format.space_after = Pt(2)

    # --- Пометка о непроверенном досье ----------------------------------------
    # Непроверенное досье внешне неотличимо от проверенного, поэтому отличать
    # его должна первая строка самого документа, а не примечание в чате.
    if data.get("_unverified"):
        warn = doc.add_paragraph()
        r = warn.add_run("⚠️ Внешняя проверка фактов (триангуляция) НЕ проводилась. "
                         "Сведения не подтверждены независимыми источниками.")
        r.bold = True
        r.font.color.rgb = RGBColor(0xB0, 0x00, 0x20)

    # --- Шапка ---------------------------------------------------------------
    title = doc.add_paragraph(as_text(data.get("name")), style="Heading 1")
    style_heading(title, 16)

    role = doc.add_paragraph()
    run = role.add_run(as_text(data.get("last_known_role")))
    run.font.size = Pt(12)
    run.font.bold = True
    as_of = as_text(data.get("as_of"))
    if as_of:
        tail = role.add_run(f"  ·  по состоянию на {ru_dates(as_of)}")
        tail.font.size = Pt(11)
        tail.font.color.rgb = RGBColor(0x55, 0x5F, 0x6B)
    role.paragraph_format.space_after = Pt(8)

    # Блок полноты данных в документ НЕ идёт: агент считает якоря для себя,
    # чтобы решить, хватает ли материала, но руководителю служебная
    # арифметика не нужна — он открывает досье, чтобы узнать человека.

    # --- Разделы -------------------------------------------------------------
    gender = data.get("gender") or "m"
    for key, spec, _required, _limit in SECTIONS:
        if key in HIDDEN_IN_DOCX:
            continue
        section_title = heading(spec, gender)
        body = data.get(key)
        text = as_text(body)
        if not text:
            continue
        head = doc.add_paragraph(section_title, style="Heading 2")
        style_heading(head, 12)
        if isinstance(body, (list, tuple)):
            for item in body:
                item = str(item).strip()
                if not item:
                    continue
                par = doc.add_paragraph(style="List Bullet")
                add_rich_text(par, item)
                par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
                par.paragraph_format.space_after = Pt(2)
                for run in par.runs:
                    run.font.name = "Arial"
                    run.font.size = Pt(12)
                    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Arial")
        else:
            for chunk in text.split("\n"):
                if chunk.strip():
                    add_rich_text(doc.add_paragraph(), chunk.strip())

    # --- Источники таблицей --------------------------------------------------
    srcs = data.get("sources") or []
    if srcs:
        head = doc.add_paragraph("Источники", style="Heading 2")
        style_heading(head, 12)
        tbl = doc.add_table(rows=1, cols=4)
        tbl.style = "Table Grid"
        for i, name in enumerate(("№", "Источник", "Дата", "Сила")):
            cell = tbl.rows[0].cells[i]
            cell.text = ""
            run = cell.paragraphs[0].add_run(name)
            run.font.name = "Arial"
            run.font.size = Pt(10)
            run.font.bold = True
            run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        for s in srcs:
            cells = tbl.add_row().cells
            values = (str(s.get("n") or ""), str(s.get("title") or ""),
                      str(s.get("date") or ""), str(s.get("strength") or ""))
            for i, value in enumerate(values):
                cells[i].text = ""
                par = cells[i].paragraphs[0]
                par.paragraph_format.space_after = Pt(0)
                if i == 1 and str(s.get("url") or "").startswith("http"):
                    add_hyperlink(par, value or s["url"], s["url"])
                else:
                    run = par.add_run(value)
                    run.font.name = "Arial"
                    run.font.size = Pt(10)
                    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")

    # --- Колонтитул ----------------------------------------------------------
    footer = doc.sections[0].footer.paragraphs[0]
    footer.text = (f"Досье: {as_text(data.get('name'))}  ·  подготовлено {as_text(data.get('prepared'))}"
                   + ("  ·  БЕЗ ТРИАНГУЛЯЦИИ" if data.get("_unverified") else ""))
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in footer.runs:
        run.font.name = "Arial"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x77, 0x7F, 0x88)
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")

    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(out_path))
    except OSError as exc:
        raise SystemExit(
            f"[!] Не удалось записать файл {out_path}: {type(exc).__name__}: {exc}\n"
            f"    Проверьте, что рабочий каталог навыка доступен на запись и есть место на диске.")


_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def add_rich_text(paragraph, text: str) -> None:
    """Текст с разметкой **жирного**: пометка **[Анализ]** в Word должна быть
    жирной, а не звёздочками — звёздочки в документе выглядят как недоделка."""
    pos = 0
    for m in _BOLD_RE.finditer(text):
        if m.start() > pos:
            paragraph.add_run(text[pos:m.start()])
        paragraph.add_run(m.group(1)).bold = True
        pos = m.end()
    if pos < len(text):
        paragraph.add_run(text[pos:])


def add_hyperlink(paragraph, text, url):
    """Кликаемая ссылка. python-docx этого не умеет — собираем через XML."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    for tag, attrs in (("w:rFonts", {qn("w:ascii"): "Arial", qn("w:hAnsi"): "Arial",
                                     qn("w:eastAsia"): "Arial"}),
                       ("w:sz", {qn("w:val"): "20"}),
                       ("w:color", {qn("w:val"): "1155CC"}),
                       ("w:u", {qn("w:val"): "single"})):
        el = OxmlElement(tag)
        for k, v in attrs.items():
            el.set(k, v)
        rPr.append(el)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


# Порядок сокращения не выдуман здесь — он опубликован в SKILL.md как правило:
# «Анализ» -> «Культурный контекст» -> примеры в «Чем известен». Раз это
# правило, его можно исполнять детерминированно, а не просить модель следовать
# ему прозой. Одинаковый вход даёт одинаковый выход на любой модели.
#
# Три раздела не трогаются никогда: полнота данных, «Не подтверждено» и
# «Источники». Это то, ради чего досье вообще читают, и именно там живёт
# граница между проверенным и непроверенным.
TRIM_ORDER = [
    ("analysis", 0),      # вывод, а не факт — уходит первым, можно до нуля
    ("culture", 0),       # необязательный раздел
    ("known_for", 3),     # примеры; меньше трёх не оставляем
    ("topics", 3),
]
TRIM_PROTECTED = ("completeness", "unconfirmed", "sources")


def _section_limit(key: str, data: dict) -> int:
    """Лимит раздела с учётом расширения «Тем» при заданном контексте встречи."""
    return limits_for(data).get(key, 0)


def _measure_section(key: str, data: dict) -> int:
    return len(as_text(data.get(key)))


def fit_to_budget(data: dict) -> tuple[bool, list[str]]:
    """Срезать документ под бюджет по правилу. Возвращает (влезло, что убрано).

    Режем только целыми элементами списков и только необязательные разделы:
    обрывать биографию на полуслове хуже, чем отказать. Прозаические разделы
    сверх лимита остаются на совести автора — им скрипт называет цель.

    Два условия остановки, и оба нужны: общий бюджет и собственный лимит
    раздела. Без второго --fit укладывался в сумму, оставляя «Чем известен»
    вдвое сверх нормы, и следующий же --check отказывал по нему — то есть
    круг сокращения не заканчивался, а только менял повод.
    """
    removed: list[str] = []
    budget = budget_for(data)
    target = target_for(budget)

    def total() -> int:
        return measure(data)[0]

    def over(key: str) -> bool:
        limit = _section_limit(key, data)
        return bool(limit) and _measure_section(key, data) > target_for(limit)

    for key, floor in TRIM_ORDER:
        while total() > target or over(key):
            value = data.get(key)
            if isinstance(value, list):
                if len(value) <= floor:
                    break
                dropped = value.pop()
                removed.append(f"{key}\u0000убран пункт — {str(dropped)[:70]}…")
            elif isinstance(value, str) and value.strip():
                if floor:
                    break
                removed.append(f"{key}\u0000раздел убран целиком ({len(value)} знаков)")
                data[key] = ""
            else:
                break
    return total() <= budget, removed


def run_fit(src: pathlib.Path, data: dict) -> int:
    """Режим --fit: сократить под бюджет, переписать файл, отчитаться вслух."""
    before = measure(data)[0]
    budget = budget_for(data)
    # Сокращать нужно не только при превышении общего бюджета, но и когда
    # сокращаемый раздел вышел за свой лимит: иначе --check отказывает по
    # разделу, а --fit отвечает «сокращать нечего», и круг не размыкается.
    over_sections = [key for key, _floor in TRIM_ORDER
                     if _section_limit(key, data)
                     and _measure_section(key, data) > _section_limit(key, data)]
    if before <= budget and not over_sections:
        print(f"Сокращать нечего: {before} знаков из {budget}, лимиты разделов соблюдены.")
        return 0

    # Режем копию: исходные данные не меняются, пока сокращённая версия не
    # записана на диск.
    import copy
    data = copy.deepcopy(data)
    ok, removed = fit_to_budget(data)
    after = measure(data)[0]

    print(f"Было {before} знаков, стало {after} (бюджет {budget}).")
    if removed:
        print("\nУбрано — по правилу «Анализ» -> «Культурный контекст» -> примеры:")
        for line in removed:
            key, _, what = line.partition("\u0000")
            print(f"  − «{key}»: {what}")
    else:
        print("\nУбирать оказалось нечего: необязательные разделы уже пусты.")

    # Молчаливое усечение здесь недопустимо. Владелец должен увидеть, что из
    # досье что-то вынули, — иначе документ выглядит полным, каким не является.
    touched: list[str] = []
    for line in removed:
        key = line.partition("\u0000")[0]
        if key not in touched:
            touched.append(key)
    note = ("Часть необязательных разделов сокращена, чтобы уложиться в объём: "
            + ", ".join(touched) + ".")
    if removed:
        unconf = data.get("unconfirmed")
        if isinstance(unconf, list):
            unconf.append(note)
        elif isinstance(unconf, str):
            data["unconfirmed"] = (unconf + " " + note).strip()

    # Переписываем исходный файл, только если он лежит в разрешённом каталоге
    # (каталог навыка или задачи). Иначе — пишем копию в рабочий каталог:
    # путь пришёл от модели, и перезаписывать произвольный файл нельзя.
    resolved = src.resolve()
    body = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    dest = None
    if any(root == resolved.parent or root in resolved.parents for root in allowed_roots()):
        try:
            resolved.write_text(body, encoding="utf-8")
            dest = resolved
        except OSError:
            dest = None
    if dest is None:
        # Копия под ДРУГИМ именем: файл «dossier.json» в каталоге навыка
        # подменял бы оригинал агента при поиске по голому имени.
        dest = default_base().resolve() / (resolved.stem + ".fit" + resolved.suffix)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8")
    if dest == resolved:
        print(f"\nФайл переписан: {dest}")
    else:
        print(f"\nИсходный файл переписать не удалось — сокращённая версия записана сюда:\n  {dest}")
        print("  Перенесите её в свой dossier.json (write_file целиком) или дальше передавайте")
        print("  скриптам этот АБСОЛЮТНЫЙ путь.")

    still_over = [key for key, _floor in TRIM_ORDER
                  if _section_limit(key, data)
                  and _measure_section(key, data) > _section_limit(key, data)]
    if still_over:
        print("\nВнимание: разделы всё ещё сверх лимита (дальше резать нельзя — "
              "дошли до минимума пунктов): " + ", ".join(still_over)
              + ". Сократите формулировки сами; цель назовёт --check.")
        ok = False
    if not ok:
        print("\nНЕ ГОДИТСЯ: под бюджет не уложились даже после сокращения.")
        print("Дальше резать нельзя — остались только защищённые разделы")
        print("(полнота данных, «Не подтверждено», «Источники»).")
        print("Сократите прозу обязательных разделов: скрипт назовёт цель в --check.")
        return 1
    # После сокращения — полная проверка того, что получилось: объём сошёлся,
    # но числа, обязательные поля и лимиты прозы проверяются заново, чтобы
    # «ГОДНО по объёму» не выдавалось за готовность к сборке.
    rest = validate(data)
    if rest:
        print("\nОбъём сошёлся, но досье ещё НЕ ГОДИТСЯ:")
        for p in rest:
            print(f"  [!] {p}")
        return 1
    print("\nГОДНО: объём сошёлся, остальные проверки пройдены. Можно рендерить.")
    return 0


_CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _clean_controls(value):
    """Управляющие символы ломают Word («All strings must be XML compatible»)."""
    if isinstance(value, str):
        return _CTRL_RE.sub("", value).replace("\r\n", "\n").replace("\r", "\n")
    if isinstance(value, list):
        return [_clean_controls(v) for v in value]
    if isinstance(value, dict):
        return {k: _clean_controls(v) for k, v in value.items()}
    return value


def main() -> int:
    args = [a for a in sys.argv[1:]]
    if "--schema" in args:
        print(json.dumps(schema_with_limits(), ensure_ascii=False, indent=2))
        return 0

    # Зависимость проверяется ДО всего остального: сообщение «нет python-docx»
    # полезнее, чем ImportError из середины сборки, когда данные уже собраны.
    if "--check" not in args and "--fit" not in args:
        require_docx()

    check_only = "--check" in args
    fit_only = "--fit" in args
    unverified = "--unverified" in args
    args = [a for a in args if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 64

    src, tried = resolve_input(args[0])
    if src is None:
        print(f"[!] нет файла {args[0]}. Искал:")
        for t in tried:
            print(f"    {t}")
        print("    Передайте АБСОЛЮТНЫЙ путь к dossier.json в каталоге задачи.")
        return 1
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[!] JSON не разбирается: {exc}")
        return 1
    if str(src) != args[0]:
        who = as_text(data.get("name")) if isinstance(data, dict) else ""
        print(f"[i] Файл: {src}" + (f" — досье на «{who}»" if who else ""))
    if not isinstance(data, dict):
        print("[!] ожидается JSON-объект досье (см. --schema)")
        return 1
    _vf().normalize_aliases(data)
    data = _clean_controls(data)

    if fit_only:
        return run_fit(src, data)

    total, rows = measure(data)
    problems = validate(data)

    budget = budget_for(data)
    pages = budget // CHARS_PER_PAGE
    ctx = " (задан контекст встречи — «Темы» расширены)" if as_text(data.get("meeting_context")) else ""
    print(f"Объём: {total} знаков из {budget} "
          f"(≈{total / CHARS_PER_PAGE:.1f} страницы из {pages}){ctx}")
    for title, n, limit in rows:
        if n and not limit:
            print(f"  {title:<24} {n:>5}")
        elif n:
            mark = "  превышен" if n > limit else ""
            print(f"  {title:<24} {n:>5} / {limit}{mark}")

    if problems:
        print()
        print(f"НЕ ГОДИТСЯ — замечаний: {len(problems)}. Это ПОЛНЫЙ список: исправьте ВСЕ")
        print("сразу, перезаписав dossier.json одним write_file, и вызовите verify_facts.py снова.")
        for p in problems:
            print(f"  [!] {p}")
        print()
        print("Сокращать в порядке: «Анализ» → «Культурный контекст» → примеры")
        print("в «Чем известен». НЕ сокращать: полноту данных, «Не подтверждено»,")
        print("«Источники».")
        return 1

    if check_only:
        print("\nГОДНО по форме. Дальше — verify_facts.py <этот файл> (проверка фактов).")
        for item in underfill(data):
            print(f"[i] Недобор: {item}")
        evals = evaluative_phrases(data)
        if evals:
            print(f"[i] Оценочные слова ({len(evals)}) — verify_facts.py почти всегда ставит им "
                  f"«ЧАСТИЧНО». Уберите их сейчас, ДО проверки фактов, одним write_file:")
            for key, frag in evals[:8]:
                print(f"    «{key}»: …{frag}…")
        share = sonar_share(data)
        if share and share[1] and share[0] * 2 < share[1]:
            print(f"[i] Источников из ответов search.py: {share[0]} из {share[1]} — сборка откажет "
                  f"(нужно не меньше половины).")
        for note in source_notes(data):
            print(f"[i] {note}")
        about, _total = search_evidence(data)
        if about < MIN_SONAR_QUERIES:
            print(f"[i] В журнале search.py {about} запрос(ов) Sonar про этого человека из "
                  f"{MIN_SONAR_QUERIES} нужных — сборка откажет. Ищите через search.py.")
        return 0

    base = default_base()
    raw_out = args[1] if len(args) > 1 else ""
    if not pathlib.Path(raw_out.replace("\\", "/")).name.lower().startswith("досье"):
        # Имя по шаблону, если агент дал своё («son_dossier.docx») или не дал никакого.
        parts = re.sub(r"\(.*?\)", " ", as_text(data.get("name"))).split()
        who = f"{parts[-1]} {parts[0]}" if len(parts) >= 2 else (parts[0] if parts else "без имени")
        when = as_text(data.get("prepared"))[:10] or __import__("time").strftime("%Y-%m-%d")
        std = re.sub(r'[\\/:*?"<>|]', "", f"Досье — {who} — {when}.docx")
        if raw_out:
            print(f"[i] Имя файла «{raw_out}» не по шаблону — сохраняю как «{std}»")
        raw_out = std
    out = safe_out_path(raw_out, base)
    # Предварительная проверка: каталог доступен на запись — до того, как
    # собирать документ, а не после.
    try:
        base.mkdir(parents=True, exist_ok=True)
        probe = base / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        print(f"[!] Рабочий каталог {base} недоступен на запись: {type(exc).__name__}: {exc}")
        return 1
    # Сборка без триангуляции невозможна: скрипт сам сверяется с тем, что
    # подтвердил verify_facts.py. В живом прогоне ключа не было, проверка шла
    # только в --dry-run, а досье ушло владельцу как обычное — с пометкой в
    # самом конце ответа. Теперь такой путь только явный и с пометкой в файле.
    gaps = triangulation_gaps(data)
    if gaps and not unverified:
        print("\nНЕ ГОДИТСЯ: триангуляция не пройдена — verify_facts.py не подтвердил:")
        for g in gaps[:15]:
            print(f"  [!] {g}")
        if len(gaps) > 15:
            print(f"  … и ещё {len(gaps) - 15}")
        print("\nЗапустите verify_facts.py БЕЗ --dry-run и добейтесь «ГОДНО».")
        print("Если триангуляция невозможна (нет ключа, сбой сети) — собирайте с флагом")
        print("--unverified: документ получит пометку, а ответ в чат ОБЯЗАН начинаться строкой")
        print("«⚠️ Триангуляция НЕ отработала: <причина>. Досье через внешние источники НЕ проверено.»")
        return 1
    if gaps and unverified:
        # --unverified — только после НАСТОЯЩЕГО сбоя триангуляции. В прогоне
        # агент сам решил «ключа нет», не запустив verify_facts.py ни разу, хотя
        # ключ был и Sonar работал. Теперь флаг требует свежую запись о сбое.
        why = unverified_allowed()
        if why is None:
            print("\nНЕ ГОДИТСЯ: --unverified разрешён только после реального сбоя триангуляции.")
            print("Сначала запустите verify_facts.py БЕЗ --dry-run. Если он подтвердит факты —")
            print("соберите без флага. Если откажет из-за неподтверждённых утверждений —")
            print("исправьте досье. Флаг допустим, только если скрипт упал из-за ключа или сети.")
            return 1
        print(f"\nТриангуляция невозможна: {why}. Собираю с пометкой «БЕЗ ТРИАНГУЛЯЦИИ».")
        data["_unverified"] = True
        data["_unverified_why"] = why

    # Дальше — на копии с наведённым порядком источников: только те, на которые
    # есть ссылки, нумерация 1, 2, 3… по первому упоминанию.
    data = prepare_sources(data)

    # Поиск через Sonar — обязателен, если Sonar вообще доступен.
    about, total = search_evidence(data)
    if about < MIN_SONAR_QUERIES:
        if data.get("_unverified"):
            print(f"[i] Запросов search.py про этого человека: {about} — Sonar недоступен по той же причине.")
        else:
            print("\nНЕ ГОДИТСЯ: материал собран не через search.py (Perplexity Sonar).")
            print(f"  В журнале поиска за {SEARCH_WINDOW_HOURS} ч успешных запросов про "
                  f"«{as_text(data.get('name'))}»: {about}, нужно не меньше {MIN_SONAR_QUERIES} — "
                  f"одна полная волна (всего успешных запросов в журнале: {total}).")
            print("  Встроенный поиск агента — только добор. Ищите волнами через Sonar —")
            print("  с первого шага, а не для галочки перед сборкой:")
            print('  skill_exec(skill="dossier", script="search.py", args=["<Имя Фамилия> биография", ...])')
            print("  и дополните досье найденным. В запросах пишите имя человека — по нему")
            print("  сборка узнаёт, что поиск был про него (кириллица и латиница равноценны).")
            return 1
    else:
        print(f"Поиск через Sonar: {about} запрос(ов) про этого человека в журнале.")

    # Источники — из Sonar. В прогоне агент после сбоя одного вызова search.py
    # ушёл во встроенный поиск, и в досье попали блог и сайт цитат.
    share = None if data.get("_unverified") else sonar_share(data)
    if share and share[1] >= 2 and share[0] * 2 < share[1]:
        print(f"\nНЕ ГОДИТСЯ: источников из ответов search.py (Sonar) — {share[0]} из {share[1]}, "
              f"нужно не меньше половины. Не из Sonar:")
        for s in share[2][:12]:
            print(f"  [!] [{s.get('n')}] {s.get('title') or ''} — {s.get('url')}")
        print("  Найдите эти факты через search.py и сошлитесь на источники из его ответа —")
        print("  или уберите факты. Встроенный поиск агента — не источник досье.")
        return 1
    if share:
        print(f"Источники из Sonar: {share[0]} из {share[1]}.")

    build(data, out)
    size = out.stat().st_size
    print(f"\nГотово: {out}  ({size:,} байт)")
    ver = skill_version()
    print("\nДальше, обязательно, одним ходом:")
    print("  1. send_file этого файла.")
    print("  2. В чат — ТЕКСТ НИЖЕ КАК ЕСТЬ, от первой до последней строки, без единой правки")
    print("     (суммы в нём уже записаны так, чтобы чат не превратил их в формулу; модель")
    print("     в строку «Собрано» не дописывайте). Ничего не добавляйте и не пересказывайте:")
    print("     в чате не должно быть сведений, которых нет в документе.")
    print("     Ответ начинается строкой «Полнота данных» — без «Готово», «Файл отправлен»")
    print("     и прочих вступлений; блок «Источники» не вырезать.")
    print("\n===== ТЕКСТ ДЛЯ ЧАТА =====")
    print(chat_text(data, ver, str(data.get("_unverified_why") or "") if data.get("_unverified") else ""))
    print("===== КОНЕЦ ТЕКСТА =====")
    return 0


if __name__ == "__main__":
    sys.exit(main())
