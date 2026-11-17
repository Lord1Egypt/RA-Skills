# -*- coding: utf-8 -*-
"""summary.py — сборка одностраничного резюме для руководителя (A4, PDF + HTML).

Команды:
  schema                                   напечатать формат summary.json и бюджет знаков
  check <job> --json '<JSON-строка>' | --file <путь> [--natural]
                                           проверка текста без вёрстки: канон, числа, семь правил.
                                           Естественность здесь НЕ проверяется (она — один раз, на этапе humanize);
                                           --natural — только для диагностики вручную
  build <job> --json '<JSON-строка>' | --file <путь внутри папки состояния>  [--density standard|compact] [--reset]
  factcheck <job> --json '<отчёт>' | --file <путь>   отчёт модели о сверке утверждений резюме с документом

build делает всё детерминированно, без участия модели:
  1) проверяет структуру и редакторский канон (длины, стоп-слова, кальки, «морали», описательность);
     семь правил содержания — по реестру фактов;
  2) сверяет каждое число резюме с текстом исходного PDF;
  3) расставляет русскую типографику;
  4) верстает страницу A4 (12 pt, интервал 1,5), считает страницы и заполнение листа;
  5) сохраняет <название>_summary.pdf (результат), <название>_summary.html и summary.json.

Порядок (версия 2.2), состояние — out/fit_state.json:
  ЭТАП fit
  • страниц больше одной → "shorten_required": модель сокращает текст и собирает снова.
    Естественность на этом этапе не проверяется. Попыток сокращения не больше MAX_SHORTEN (5);
  • одна страница (сразу или после сокращений) → "humanize_required";
  • после 5 сокращений всё ещё больше страницы → тоже "humanize_required" (проверка выполняется всё равно).
  ЭТАП humanize (один раз)
  • ответ содержит humanize: инструкцию (references/humanize_guide.md), найденные скриптом признаки
    машинного текста, памятку читателя, весь текст и предел длины. Модель переписывает summary.json целиком
    и вызывает build — это финальная сборка, естественность повторно не проверяется;
  • если редактура вывела помещавшийся текст за страницу — "trim_required" (до MAX_TRIMS подрезок).
  ЭТАП factcheck (сверка фактов с документом, _factcheck.py)
  • "factcheck_required": утверждения резюме (заголовок, преамбула, тезисы, каждое предложение выводов и
    обоснований вопросов) с фрагментами страниц и фактами реестра + инструкция references/factcheck_guide.md;
  • модель отправляет отчёт summary.py factcheck: ok | fix | unsupported с дословными цитатами; скрипт проверяет,
    что цитаты есть на страницах, а числа — в цитатах; ошибки модель исправляет в summary.json и вызывает build;
  • на следующих раундах (до MAX_FACTCHECK_ROUNDS) сверяются только изменённые предложения;
  • всё подтверждено → "ready" (одна страница) или "ready_as_is" (больше).
"fix_required" — ошибки канона, сверки чисел и семи правил на любом этапе (этап не меняется);
тогда на диске только черновики <название>_summary_ЧЕРНОВИК.pdf и .html. --reset начинает этапы заново.
Преамбула («Резюме для руководства. …») — одно предложение, 10 pt, интервал 1.
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _core as core  # noqa: E402
import facts_rules as rules  # noqa: E402
import _natural as natural  # noqa: E402
import _factcheck as fc  # noqa: E402
import context as ctxreg  # noqa: E402

INK, INK_SOFT, BRAND, ACCENT = "#15191E", "#4A5560", "#1F4E79", "#2E75B6"
RULE, TINT, TINT_RULE = "#C9D4DF", "#F4F7FA", "#D3DEE8"
MM = 72 / 25.4
A4_W, A4_H = 595.28, 841.89

DENSITY = {
    "standard": dict(base=12.0, lh=1.5, h1=14.0, h2=14.0, mast=10.0, foot=9.0, idx=21.0, gap=4.6),
    "compact": dict(base=10.0, lh=1.38, h1=13.0, h2=11.5, mast=8.5, foot=8.0, idx=17.0, gap=3.6),
}
LEDE_PT, LEDE_LH = 10.0, 1.0      # преамбула: кегль и интервал
LEDE_SOFT, LEDE_MAX = 160, 200     # преамбула: ориентир и предел знаков; всегда одно предложение
MAX_SHORTEN = 5                    # попыток сокращения, если резюме не уместилось на страницу
MAX_TRIMS = 2                      # подрезок после редактуры, если она вывела текст за страницу
HUMANIZE_GUIDE = Path(__file__).resolve().parent.parent / "references" / "humanize_guide.md"
FACTCHECK_GUIDE = Path(__file__).resolve().parent.parent / "references" / "factcheck_guide.md"
MAX_FACTCHECK_ROUNDS = 3           # раундов сверки фактов: первый — всё резюме, дальше — только изменённые предложения
FC_EXTRA_ROUNDS = 2                # доп. раунды, если не подтверждены только обязательные строки (заголовок, преамбула, тезис, вопрос)
FC_REQUIRED_KINDS = ("заголовок", "преамбула", "тезис", "факт в вопросе")
MAX_BUILDS = 18                    # 1 + до 5 сокращений + humanize + до 3 раундов сверки + до 2 подрезок + правки; потом черновик
DELIVERABLE = ("ready", "ready_as_is")
BUDGET = {
    "standard": dict(total=1850, finding=(140, 240), question=(170, 270), findings=(5, 7), questions=(3, 4)),
    "compact": dict(total=3100, finding=(240, 380), question=(260, 400), findings=(6, 8), questions=(3, 4)),
}

SCHEMA = {
    "masthead_left": "издание/серия · месяц и год (например: McKinsey Global Survey · ноябрь 2025)",
    "masthead_right": "организация-издатель",
    "title": "суть отчёта одной фразой, до 110 знаков, без слов «отчёт о»",
    "lede": "ОДНО предложение, как можно короче (ориентир до 160 знаков, предел 200): кто, когда и о чём; "
            "без должностей, объёма и оглавления. Слова «Резюме для руководства.» скрипт добавит сам; "
            "набирается 10 pt с интервалом 1",
    "findings": [{"lead": "Тезис-утверждение до 60 знаков, с точкой, без цифр и двоеточий.",
                  "body": "Тело: факты с числами из документа.", "source_pages": [3, 4],
                  "fact_ids": ["f003", "f007"]}],
    "questions": [{"q": "Открытый вопрос без вариантов на выбор, о нашей стороне: «Какие…», «Как…», «Где…», «Сколько…»?",
                   "body": "Не печатается: факт из выводов (по документу, с числом), из которого вытекает вопрос.",
                   "ask": "Необязательно и не печатается: что нужно знать, чтобы ответить.",
                   "source_pages": [5], "fact_ids": ["f010"],
                   "scope": "company — вопрос о нашей компании (контекст по Сбербанку) | country — о стране (контекст по России)",
                   "context_ids": ["c001", "c002"],
                   "known": "Не печатается. Что уже известно по контексту (1–3 фразы со ссылками на id): что Сбер "
                            "уже делает по теме, какие компании отрасли с ним связаны, что решено в стране — и почему "
                            "ответа на вопрос пока нет.",
                   "players": [{"name": "Компания отрасли в России", "relation": "own | related | competitor | neutral",
                                "source": "kb:co/… или id записи контекста (c001)"}]}],
    "source_footer": "полное библиографическое описание источника",
}

PARASITES = [
    (r"\bдрайвер", "причина / двигатель роста"), (r"\bчеллендж", "сложность / задача"),
    (r"\bимплементац", "внедрение"), (r"\bландшафт", "рынок / расстановка сил / набор угроз"),
    (r"\bв разрезе\b", "по / в разбивке по"), (r"\bна текущий момент\b", "сейчас"),
    (r"ключевым фактором является", "назвать фактор прямо"), (r"\bв рамках\b", "в / при / убрать"),
    (r"по итогам проведённого анализа", "убрать"), (r"\bстоит отметить\b", "убрать"),
    (r"\bважно понимать\b", "убрать"), (r"\bтаким образом\b", "убрать"),
    (r"\bна (ежегодной|ежемесячной|ежеквартальной|ежедневной|постоянной|регулярной) основе\b", "ежегодно / постоянно / регулярно"),
    (r"\bвалидир", "проверить / подтвердить"),
    (r"\bигра\w*\s+(\w+\s+){0,2}рол[ьи]", "калька «plays a role»: скажите, что именно происходит — «определяет», «от него зависит»"),
    (r"\bв терминах\b", "калька «in terms of»: «по», «в пересчёте на»"), (r"\bимеет место\b|\bимели место\b", "происходит / есть"),
    (r"\bфокусир\w*|\bсфокусирова\w*", "калька «focus on»: «сосредоточен», «занимается в первую очередь»"),
    (r"\bадресова\w*", "калька «address»: «решать», «заниматься»"), (r"\bгайд[еа]нс\w*", "прогноз компании (план руководства на год)"),
    (r"\bкапекс\w*", "капитальные вложения (капзатраты)"), (r"\bболее того\b", "уберите связку: новое предложение или смысловая связь («поэтому», «при этом»)"),
    (r"\bв эпоху\b", "шаблон нейросети: убрать"), (r"открыва\w*\s+(\w+\s+)?возможност", "шаблон нейросети: скажите, что именно станет возможным"),
    (r"\bне просто\b[^.?!]{1,60}?\s+а\b", "шаблон «не просто X, а Y»: скажите прямо, что это"),
    (r"\bисторически,", "калька «historically»: «раньше», «обычно»"), (r"\bкак результат\b", "калька «as a result»: «поэтому», «в результате»"),
    (r"\bна сегодняшний день\b", "сейчас"), (r"\bпредставля\w+ собой\b", "тире или «это»"),
    (r"\bдраматическ\w*", "калька «dramatically»: числом — «в 3 раза», «на 40%»"),
    (r"\bявляется\b", "тире или глагол действия"), (r"\bосуществля", "глагол действия"),
    (r"\bданн(ый|ая|ое|ого|ой|ому|ую|ом)\b", "этот"),
]
JARGON = [
    (r"развёртывани|раскатк", "установка; «обновление дошло до всех устройств»"),
    (r"конечн\w+ устройств", "устройства сети / компьютеры сотрудников"),
    (r"\bпаритет", "тот же уровень"), (r"\bинцидент", "взлом / успешная атака / сбой"),
    (r"недофинансирован", "денег почти нет / держится на добровольцах"),
    (r"риск-профил|операционн\w+ риск", "убрать или сказать простыми словами"),
    (r"\bмедианн", "типичный (медианный) — с пояснением"),
    (r"\bкейс", "пример / случай"), (r"\bинсайт", "вывод / наблюдение"),
    (r"\bрельс\w*", "платёжная инфраструктура / системы расчётов"), (r"\bстек\w*", "набор технологий / цепочка сервисов"),
    (r"\bинференс\w*", "при первом упоминании пояснить: «работа уже обученной модели (инференс)»"),
    (r"\bсофт\w*", "программы"), (r"\bкодинг\w*", "программирование"), (r"\bредизайн\w*", "перестройка"),
]
STYLE_WARN = [
    (r"\bключев\w+ игрок|\bигрок\w* (рынка|отрасли)", "калька «key player»: назовите, кто именно — «крупнейшие банки», «три производителя»"),
    (r"\bлидирующ\w*", "«крупнейший», «первый»"), (r"\bкритически важн\w*", "пустой усилитель: назовите, что от этого зависит"),
    (r"\bбеспрецедентн\w*", "пустой усилитель: «впервые» и в чём именно"), (r"\bстремительн\w*", "пустой усилитель: число вместо эпитета"),
    (r"\bэкосистем\w*", "«набор сервисов», «партнёры и поставщики»"), (r"\bвызов(ы|ов|ами|ам|ах)\b", "калька «challenges»: «сложности», «угрозы», «задачи»"),
    (r"\bг/г\b|\bгод к году\b", "калька «YoY»: «за год», «к прошлому году»"), (r"\bв свою очередь\b", "убрать"),
    (r"\bс точки зрения\b", "«для», «по» — или переформулировать"), (r"\bв то время как\b", "«а», «тогда как» — или два предложения"),
    (r"\bамбициозн\w*", "цель — числом"), (r"\bтрансформаци\w*", "скажите, что именно меняется"), (r"\bв настоящее время\b", "сейчас"),
]
DOC_ACTOR = (r"\b(записк|документ|отч[её]т|доклад|исследовани|обзор|стать|материал|публикаци)\w*\s+"
             r"(предлага|рекоменду|призыва|настаива|счита|утвержда|требу|предусматрива)\w*")
HEDGE = (r"предлага|рассматрива|изуча|прорабатыва|исследу|намерен|планиру|собира|\bмож(ет|ут)\b|могл?[аио]?\b|возможн|ожида|допуска|"
         r"обсужда|объяв|договорил|меморандум|соглашени|пилот|тестир|испыт|не исключ|вероятн|рассчитыва|\bцел(ь|ью|и)\b|прогноз|оцен|"
         r"по мнению|по данным|предполага|потенциальн|пока не|ещё не|еще не|не назван|не определ|не раскры|в перспективе|намечен|готов\w* к|"
         r"должн\w*|по замыслу|по проекту|по плану|\bбуд(ет|ут)\b|\bстан(ет|ут)\b")
DONE = (r"\b(работает|работают|действует|действуют|запущен\w*|внедрен\w*|внедрил\w*|ввел\w*|ввёл\w*|заработал\w*|применя\w+|"
        r"проводят|проводит|делают|делает|используют|использует|сделал\w*|стал\w* совместим\w*|совместим\w*|перешл?\w*|перевел\w*|перевёл\w*|"
        r"завершил\w*|завершен\w*|завершён\w*|запустил\w*|купил\w*|приобрел\w*|приобрёл\w*|поглотил\w*|подключил\w*|обязан\w*)\b")
MONTHS = r"(январ|феврал|март|апрел|ма[йя]|июн|июл|август|сентябр|октябр|ноябр|декабр)\w*"
START_DATE = r"\bс\s+(\d{1,2}\s+%s|%s\s+\d{4}|\d{4}\s+г)" % (MONTHS, MONTHS)
PRECEDENT_RX = r"впервые|перв(ый|ая|ое|ые|ого|ой|ую)\b[^.]{0,40}\b(так|в истории|в мире|в своём роде|случа|раз)|прецедент|раньше (такого )?не было|до сих пор не|рекорд"
GAP_RX = (r"не (назначен|определ|указан|описан|установлен|создан|утвержд|раскры|решен|решён|прописан|согласован|ясн|названы?)\w*|"
          r"\bнет\b|отсутству|пока не|ещё не|еще не|неясно|не ясно|без (ответственн|сроков|спецификац|стандарт|органа|финансирован)")
BENEF_RX = r"получа|выигрыва|выгод|достаётся|достается|теряет|теряют|платит|платят|экономит|экономят|отда[её]т"
FORK_RX = r"\bили\b|\bлибо\b"
YESNO_RX = r"(?:^|[\s,(«])(?:[а-яё]+)\s+ли\b"
OPEN_Q_RX = (r"\b(как\w*|каков\w*|что|чего|чем|чему|где|куда|откуда|сколько|когда|кто|кого|кому|кем|почему|зачем|"
             r"насколько|чей|чья|чьи)\b")
Q_STOP = {"нашего", "нашей", "наших", "нашим", "нашими", "можно", "нужно", "будет", "будут", "сейчас", "этого", "этому",
          "какие", "каких", "какой", "какая", "какую", "каким", "сколько", "когда", "через", "после", "сбера", "сбер",
          "сбербанк", "сбербанка", "банка", "банку", "россии", "российских", "российского", "который", "которые", "чтобы",
          "также", "более", "менее", "если", "уже", "этот", "этих", "наши", "нашу", "нашем"}


def _key_stems(text: str) -> set[str]:
    out = set()
    for w in re.findall(r"[а-яёa-z]+", (text or "").lower().replace("ё", "е")):
        if len(w) < 5 or w in Q_STOP:
            continue
        out.add(w[:max(5, len(w) - 3)])
    return out


def _repeated_stem(text: str) -> str:
    seen = set()
    for w in re.findall(r"[а-яё]+", (text or "").lower()):
        if len(w) < 6 or w in Q_STOP:
            continue
        st = w[:max(5, len(w) - 3)]
        if st in seen:
            return st
        seen.add(st)
    return ""
RESPONSIBLE_RX = r"\bкто\b[^?]{0,40}\b(отвеча|возглав|курир|будет отвечать|займ[её]тся)|назнач\w*|ответственн\w*"

DESCRIPTIVE = r"(записк|документ|отч[её]т|доклад|обзор|исследовани)\w*\s+(описыва|рассматрива|анализиру|посвящ|освеща)\w*|в отч[её]те (рассматрива|описыва|анализиру|говорится)|автор\w* (описыва|рассматрива)|речь ид[её]т о|отч[её]т посвящ|в (первой|второй|третьей) части"
MORAL = (r"^это (превращает|указывает|означает|делает|подч[её]ркивает|говорит о|свидетельствует|показывает важность)"
         r"|^это не (вопрос|про|просто)\b|^бизнес опирается|^вс[её] это|^без [^.]{3,80} оста[её]?[тю]тся"
         r"|оста[её]тся декларацией|остаются декларацией")

SPELLED_RATIOS = [
    (r"в\s+два\s+раза|вдвое|двукратн\w*|удво\w+", r"twice|two times|two-?fold|doubl\w*|\b2x\b|\b2(\.0)? times|в два раза|вдвое|двукратн|удво", "в два раза"),
    (r"в\s+три\s+раза|втрое|тр[её]хкратн\w*|утро\w+", r"three times|three-?fold|tripl\w*|\b3x\b|\b3(\.0)? times|в три раза|втрое|тр[её]хкратн|утро", "в три раза"),
    (r"дв(е|ух|ум) трет\w+", r"two[- ]thirds|две трети|двух третей", "две трети"),
    (r"тр(и|[её]х|[её]м) четверт\w+", r"three[- ]quarters|три четверти|тр[её]х четвертей", "три четверти"),
    (r"(?<!дв[еу] )(?<!двух )(?<!двум )\bтрет(ь|и|ью)\b", r"\bthirds?\b|one[- ]third|\bтрет(ь|и|ью)\b", "треть"),
    (r"(?<!три )(?<!тр[её]х )(?<!тр[её]м )\bчетверт(ь|и|ью)\b", r"quarter|четверт", "четверть"),
    (r"\bполовин\w+", r"\bhalf\b|\bhalve|половин", "половина"),
    (r"\bкажд\w+ (втор|трет|четв[её]рт|пят|десят)\w+", r"(one|1) in (two|three|four|five|ten|2|3|4|5|10)\b|\bhalf\b|third|quarter|fifth|tenth|кажд\w+ (втор|трет|четв|пят|десят)", "каждый N-й"),
    (r"\b(один|одна|двое|два|две|трое|три|четверо|четыре|пять|шесть|семь|восемь|девять) из (тр[её]х|четыр[её]х|пяти|десяти)\b",
     r"\b(one|two|three|four|five|six|seven|eight|nine|\d) (in|out of) (three|four|five|ten|\d+)\b|\bиз (тр[её]х|четыр[её]х|пяти|десяти)\b", "N из M"),
]
ABBR_RE = re.compile(r"(?<![\w\u2011-])(?:[A-ZА-ЯЁ]{2,6}\d*|[a-z]\d{2,4}|[A-Z]{1,4}\d[A-Z\d]*)(?![\w\u2011-])")
KNOWN_ABBR = {"ИИ", "США", "ЕС", "ВВП", "РФ", "ЦБ", "ФРС", "ООН", "СНГ", "КНР", "ИТ", "IT", "ОАЭ", "НДС", "МВФ", "ОПЕК"}
FORECAST = (r"прогноз|оцен|ожида|консенсус|по модели|по расч[её]т|может|могут|мог(ла|ли)?\b|вероятн|предполага|планиру|"
            r"по мнению|по данным|сценари|цел(ь|евой|и)\b|оценк|аналитик")
ADVICE = r"нужно усилить|следует уделить|необходимо обратить|рекомендуется|важно обеспечить"


def _sentences(text: str) -> list[str]:
    keep = "\x01"   # временная склейка: инициалы и сокращения не делят предложение
    t = re.sub(r"(?<![\w-])([А-ЯЁA-Z]\.)[\s\u00a0]+(?=[А-ЯЁA-Z])", r"\1" + keep, text)
    t = re.sub(r"\b(г|гг|млн|млрд|трлн|тыс|долл|руб|см|илл|т\.\s?е|т\.\s?д)\.[\s\u00a0]+(?=[а-яёa-z0-9(«])", r"\1." + keep, t)
    parts = re.split(r"(?<=[.!?…])\s+(?=[«\"(]?[А-ЯЁA-Z0-9])", t.strip())
    return [p.replace(keep, " ") for p in parts if p.strip()]


def _words(s: str) -> int:
    return len(re.findall(r"[\w%$€₽]+(?:[-–][\w%]+)*", s))


def lint(data: dict, density: str) -> tuple[list[dict], list[dict]]:
    errors, warnings = [], []
    bud = BUDGET[density]

    def err(where, msg, fix=""):
        errors.append({"where": where, "problem": msg, **({"fix": fix} if fix else {})})

    def warn(where, msg, fix=""):
        warnings.append({"where": where, "problem": msg, **({"fix": fix} if fix else {})})

    for key in ("masthead_left", "masthead_right", "title", "lede", "source_footer"):
        if not core.as_text(data.get(key)):
            err(key, "поле пустое")
    findings = data.get("findings") or []
    questions = data.get("questions") or []
    if not isinstance(findings, list) or not isinstance(questions, list):
        err("findings/questions", "должны быть списками")
        return errors, warnings

    lo, hi = bud["findings"]
    if not (lo <= len(findings) <= hi):
        err("findings", "выводов %d, нужно %d–%d при плотности %s" % (len(findings), lo, hi, density))
    lo, hi = bud["questions"]
    if not (lo <= len(questions) <= hi):
        err("questions", "вопросов %d, нужно %d–%d при плотности %s" % (len(questions), lo, hi, density))

    title = core.as_text(data.get("title"))
    if len(title) > 110:
        err("title", "заголовок %d знаков, предел 110" % len(title))
    if re.match(r"(?i)^\s*отч[её]т о", title):
        err("title", "заголовок начинается с «отчёт о» — нужна суть, а не жанр")
    lede = re.sub(r"^\s*Резюме для руководства\.?\s*", "", core.as_text(data.get("lede")))
    if len(lede) > LEDE_MAX:
        err("lede", "преамбула %d знаков, предел %d" % (len(lede), LEDE_MAX),
            "одна фраза: кто, когда и о чём; уберите должности, объём документа и пересказ разделов")
    elif len(lede) > LEDE_SOFT:
        warn("lede", "преамбула %d знаков при ориентире до %d — можно короче" % (len(lede), LEDE_SOFT))
    if len(_sentences(lede)) > 1:
        err("lede", "преамбула из %d предложений — нужно одно" % len(_sentences(lede)),
            "одна короткая фраза: кто, когда и о чём — «Аналитики Morgan Stanley, март 2026 г.: как облачные гиганты финансируют стройку ЦОД.»")

    def common(where: str, text: str) -> None:
        low = text.lower()
        for rx, fix in PARASITES:
            m = re.search(rx, low)
            if m:
                err(where, "стоп-слово «%s»" % m.group(0), fix)
        for rx, fix in JARGON:
            m = re.search(rx, low)
            if m and not re.match(r"\w*\s?\(", low[m.end():m.end() + 25]) and "(" not in low[max(0, m.start() - 2):m.start()]:
                warn(where, "жаргон «%s»" % m.group(0), fix)
        for rx, fix in STYLE_WARN:
            m = re.search(rx, low)
            if m:
                warn(where, "оборот «%s» звучит как перевод или текст нейросети" % m.group(0), fix)
        m = re.search(DOC_ACTOR, low)
        if m:
            err(where, "документ подан как действующее лицо: «%s» (правило модальности)" % m.group(0),
                "передайте модальность источника: «предлагается рассмотреть», «авторы предлагают», «по оценке авторов»")
        m = re.search(DESCRIPTIVE, low)
        if m:
            err(where, "пересказ структуры («%s») вместо вывода" % m.group(0), "скажите, что это меняет для нас")
        if "!" in text:
            err(where, "восклицательный знак")
        if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text):
            err(where, "эмодзи")
        for s in (_sentences(text) if where.startswith(("вывод", "вопрос")) else []):
            n = _words(s)
            if n > 25:
                err(where, "предложение из %d слов (предел 25): «%s…»" % (n, s[:60]), "разбейте на два")
        caps = [w for w in re.findall(r"\b[А-ЯЁ]{4,}\b", text)]
        if len(caps) >= 2 or any(len(w) >= 6 for w in caps):
            err(where, "слова капсом: %s" % ", ".join(caps[:3]), "обычный регистр; капитель в заголовках секций задаёт оформление")
        m = None
        if where.startswith(("вывод", "вопрос", "title", "lede")):
            m = re.search(r"(?<![A-Za-z0-9_./\-\u2011])[a-z]{2,}[-\u2011][a-z]{2,}(?:[-\u2011][a-z]{2,})*", text) or \
                re.search(r"(?<![A-Za-z0-9_./\-\u2011])[a-z]{4,}(?![A-Za-z0-9_./\-\u2011])(?:\s+[a-z]{3,})*", text)
        if m:
            err(where, "непереведённый английский текст: «%s»" % m.group(0).strip()[:50],
                "переведите на русский; латиницей остаются только названия и аббревиатуры (McKinsey, EBIT)")

    for i, f in enumerate(findings, 1):
        where = "вывод %d" % i
        if not isinstance(f, dict):
            err(where, "пункт должен быть объектом с lead и body")
            continue
        lead, body = core.as_text(f.get("lead")), core.as_text(f.get("body"))
        if not lead or not body:
            err(where, "нужны и lead, и body")
            continue
        if len(lead) > 60:
            err(where + ".lead", "тезис %d знаков, предел 60" % len(lead))
        if not lead.endswith("."):
            err(where + ".lead", "тезис — законченное утверждение с точкой")
        if re.search(r"\d", lead):
            err(where + ".lead", "в тезисе цифры — числа живут только в теле пункта")
        if ":" in lead:
            err(where + ".lead", "в тезисе двоеточие")
        if _words(lead) < 3:
            err(where + ".lead", "тезис — утверждение, а не тема из одного-двух слов")
        if re.match(r"(?i)^(вопрос|ситуация|проблема|тема|роль|влияние|состояние|анализ|обзор|о|об)\s", lead):
            err(where + ".lead", "тезис начинается с существительного-темы («%s…»)" % lead.split()[0],
                "начните с утверждения: «Времени на реакцию почти не осталось.»")
        if not re.search(r"\d", body):
            warn(where + ".body", "в теле нет ни одного числа", "добавьте число из реестра фактов, если оно там есть")
        sents = _sentences(body)
        if sents and re.search(MORAL, sents[-1].strip().lower()):
            err(where + ".body", "пункт заканчивается обобщающей моралью: «%s»" % sents[-1][:70],
                "последнее предложение — факт, причина или следствие с числом")
        total = len(lead) + 1 + len(body)
        lo, hi = bud["finding"]
        if total > hi * 1.25:
            err(where, "пункт %d знаков при ориентире %d–%d" % (total, lo, hi), "сократите: один контраст чисел, без вводных")
        elif total > hi or total < lo * 0.7:
            warn(where, "пункт %d знаков при ориентире %d–%d" % (total, lo, hi))
        common(where, lead + " " + body)

    for i, q in enumerate(questions, 1):
        where = "вопрос %d" % i
        if not isinstance(q, dict):
            err(where, "вопрос должен быть объектом с q и body (ask — по желанию)")
            continue
        qq, body, ask = (core.as_text(q.get(k)) for k in ("q", "body", "ask"))
        if not (qq and body):
            err(where, "нужны q и body")
            continue
        if not qq.endswith("?"):
            err(where + ".q", "вопрос-заголовок должен заканчиваться знаком «?»")
        low_q = qq.lower()
        m = re.search(FORK_RX, low_q)
        if m:
            err(where + ".q", "вопрос с выбором «%s»: вопросы — открытые, без вариантов на выбор" % m.group(0),
                "спросите, как, где, сколько, на каких условиях: «Какие процессы СберЛогистики можно перевести на "
                "складских роботов при окупаемости меньше трёх лет?»")
        m = re.search(YESNO_RX, low_q)
        if m:
            err(where + ".q", "вопрос «да или нет» («%s»): это тот же выбор из двух вариантов" % m.group(0).strip(),
                "откройте вопрос: не «Стоит ли нам…», а «Что нам даст…», «Где у нас…», «Сколько…»")
        elif not re.search(OPEN_Q_RX, " ".join(re.findall(r"[а-яё]+", low_q)[:4])):
            err(where + ".q", "вопрос не открытый: в начале нет вопросительного слова",
                "начните с «Как», «Какие», «Что», «Где», «Сколько», «Когда», «Кто», «За счёт чего», «На каких условиях»")
        rep_stem = _repeated_stem(qq)
        if rep_stem:
            warn(where + ".q", "в вопросе дважды одно и то же слово («%s…»)" % rep_stem, "уберите повтор")
        m = re.search(RESPONSIBLE_RX, (qq + " " + ask).lower())
        if m:
            err(where, "вопрос о назначении ответственного («%s»)" % m.group(0),
                "спросите о сути дела, а не о том, кто будет отвечать")
        if re.search(ADVICE, (qq + " " + body + " " + ask).lower()):
            err(where, "рекомендация вместо вопроса", "вопрос должен быть проверяемым: срок, ответственный, наличие перечня")
        if not re.search(r"\b(мы|нас|нам|нами|наш\w*|сбер\w*)\b", qq.lower()):
            warn(where, "нет «мы / у нас» — вопрос звучит не как реплика на правлении")
        if not re.search(r"\d", body):
            warn(where + ".body", "в обосновании нет числа из документа")
        for sent in _sentences(body):
            if re.search(MORAL, sent.strip().lower()):
                err(where + ".body", "оценочная фраза, которой нет в документе: «%s»" % sent.strip()[:70],
                    "обоснование вопроса — 1–2 предложения строго из документа, с числом; рассуждения уберите")
        total = len(qq) + len(body) + len(ask) + 2
        lo, hi = bud["question"]
        if total > hi * 1.25:
            err(where, "вопрос %d знаков при ориентире %d–%d" % (total, lo, hi))
        elif total > hi or total < lo * 0.7:
            warn(where, "вопрос %d знаков при ориентире %d–%d" % (total, lo, hi))
        common(where, qq + " " + body + " " + ask)

    # тавтология между вопросами и с выводами
    qlist = [(i, q) for i, q in enumerate(questions, 1) if isinstance(q, dict) and core.as_text(q.get("q"))]
    qstems = {i: _key_stems(core.as_text(q.get("q"))) for i, q in qlist}
    for a in range(len(qlist)):
        for b in range(a + 1, len(qlist)):
            i, j = qlist[a][0], qlist[b][0]
            common_st = qstems[i] & qstems[j]
            small = min(len(qstems[i]), len(qstems[j])) or 1
            if len(common_st) >= 3 or (len(common_st) >= 2 and len(common_st) / small >= 0.4):
                err("вопросы %d и %d" % (i, j), "вопросы повторяют друг друга (общие слова: %s)" % ", ".join(sorted(common_st)),
                    "у каждого вопроса — свой предмет и своя сторона дела: деньги и риск, клиенты, технологии и продукты, "
                    "рынок и конкуренты; одну тему — одним вопросом")
            ids_i, ids_j = set(_ids(qlist[a][1])), set(_ids(qlist[b][1]))
            if ids_i and ids_i == ids_j:
                err("вопросы %d и %d" % (i, j), "у вопросов одна и та же опора (fact_ids)", "возьмите для второго вопроса другой вывод")
    firsts = [re.findall(r"[а-яё]+", core.as_text(q.get("q")).lower())[:1] for _, q in qlist]
    if len(qlist) >= 3 and len({tuple(x) for x in firsts}) == 1:
        warn("questions", "все вопросы начинаются одним словом («%s»)" % (firsts[0][0] if firsts[0] else ""),
             "начните вопросы по-разному: однотипный зачин читается как шаблон")
    for i, q in qlist:
        for k, f in enumerate(findings, 1):
            fl = _key_stems(core.as_text(f.get("lead")))
            if fl and len(qstems[i] & fl) >= max(2, int(0.6 * len(fl))):
                warn("вопрос %d" % i, "вопрос пересказывает тезис вывода %d" % k,
                     "вопрос не повторяет вывод, а спрашивает, что из него следует для нас")

    common("title", title)
    common("lede", core.as_text(data.get("lede")))
    leads = [core.as_text(f.get("lead")).lower() for f in findings if isinstance(f, dict)]
    if len(set(leads)) < len(leads):
        err("findings", "повторяющиеся тезисы")

    parts = [("title", title), ("lede", core.as_text(data.get("lede")))]
    parts += [("вывод %d" % i, "%s %s" % (core.as_text(f.get("lead")), core.as_text(f.get("body"))))
              for i, f in enumerate(findings, 1) if isinstance(f, dict)]
    parts += [("вопрос %d" % i, " ".join(core.as_text(q.get(k)) for k in ("q", "body", "ask")))
              for i, q in enumerate(questions, 1) if isinstance(q, dict)]
    seen_abbr, bare = set(), []
    for where, text in parts:
        for m in ABBR_RE.finditer(text):
            a = m.group(0)
            if a in seen_abbr or a in KNOWN_ABBR:
                continue
            seen_abbr.add(a)
            around = text[max(0, m.start() - 2):m.end() + 2]
            if "(" not in around and ")" not in around:
                bare.append("%s (%s)" % (a, where))
    if bare:
        warn("аббревиатуры", "не раскрыты при первом появлении: %s" % ", ".join(bare[:8]),
             "раскройте в скобках: «CAGR (среднегодовой темп роста)», «ЦОД (центры обработки данных)»; "
             "названия компаний и продуктов оставьте как есть")
    year_now = datetime.date.today().year
    for where, text in parts:
        if not where.startswith(("вывод", "вопрос", "lede")):
            continue
        for sent in _sentences(text):
            yrs = [int(y) for y in re.findall(r"(?<!\d)(20[2-9]\d)(?!\d)", sent)]
            if yrs and max(yrs) > year_now and not re.search(FORECAST, sent.lower()):
                warn(where, "прогноз подан как факт: «%s»" % sent.strip()[:80],
                     "назовите, чей это прогноз или оценка: «по прогнозу…», «по консенсусу аналитиков…», «по модели…»")
                break
    return errors, warnings


def verify_numbers(data: dict, jdir: Path) -> tuple[list[dict], list[dict]]:
    meta = core.read_json(jdir / "meta.json", {})
    total = int(meta.get("pages_extracted", 0))
    page_idx = {n: core.number_index(core.page_text_for_numbers(jdir, n)) for n in range(1, total + 1)}
    doc_idx: set[str] = set()
    for s in page_idx.values():
        doc_idx |= s
    facts = core.read_json(jdir / "facts.json", {"facts": []})
    for f in facts.get("facts", []):
        if f.get("from_image"):
            doc_idx |= core.number_index(" ; ".join(f.get("numbers", [])))
    soft_idx = set(doc_idx) | {str(meta.get("pages_total", ""))}
    errors, warnings = [], []

    def scan(where: str, text: str, pages, strict: bool) -> None:
        missing, minor = core.check_numbers(text, doc_idx if strict else soft_idx)
        if missing:
            (errors if strict else warnings).append(
                {"where": where, "problem": "чисел нет в исходном документе: %s" % ", ".join(missing),
                 "fix": "перенесите число ровно как в источнике; нельзя округлять, складывать и пересчитывать"})
        if minor:
            warnings.append({"where": where, "problem": "одиночные цифры без опоры в тексте: %s" % ", ".join(minor),
                             "fix": "проверьте, что это не пересчёт (например, «в 2 раза» при «doubled» допустимо)"})
        if not isinstance(pages, (list, tuple)):
            pages = [pages] if pages is not None else []
        pages = [int(p) for p in pages if str(p).isdigit()]
        if strict and not pages and re.search(r"\d", text):
            warnings.append({"where": where, "problem": "не указаны source_pages — числа сверены только со всем документом",
                             "fix": "укажите страницы, откуда взяты числа: сверка станет точной"})
        if strict and pages and not missing:
            near: set[str] = set()
            for p in pages:                              # только указанные страницы, без соседних
                near |= page_idx.get(p, set())
            off, _ = core.check_numbers(text, near)
            if off:
                errors.append({"where": where, "problem": "чисел %s нет на указанных страницах %s" % (", ".join(off), pages),
                               "fix": "исправьте source_pages либо уберите число: оно может быть из другой таблицы или совпадать случайно"})

    page_txt = {n: core.page_text_for_numbers(jdir, n).lower() for n in range(1, total + 1)}
    image_txt = " ; ".join("%s %s" % (f.get("claim", ""), f.get("quote", "")) for f in facts.get("facts", []) if f.get("from_image")).lower()

    def scan_spelled(where: str, text: str, pages) -> None:
        if not isinstance(pages, (list, tuple)):
            pages = [pages] if pages is not None else []
        pages = [int(p) for p in pages if str(p).isdigit()]
        low = text.lower().replace(core.NBSP, " ")
        for ru, src, label in SPELLED_RATIOS:
            m = re.search(ru, low)
            if not m:
                continue
            near = " ".join(page_txt.get(p, "") for p in pages) if pages else ""
            if pages and re.search(src, near + " " + image_txt):
                if label.startswith("в "):
                    warnings.append({"where": where, "problem": "кратность прописью «%s» сверена только по слову в тексте страниц" % m.group(0),
                                     "fix": "убедитесь, что в источнике кратность относится именно к этому показателю; "
                                            "если там две доли («nearly half против 31 percent») — приведите их, а не кратность"})
                continue
            anywhere = [n for n, tx in page_txt.items() if re.search(src, tx)]
            if not pages and anywhere:
                continue
            where_hint = ("в документе такая величина встречается на с. %s — проверьте, что она про тот же показатель, и поправьте source_pages"
                          % ", ".join(map(str, anywhere[:8]))) if anywhere else "в документе такой величины нет"
            errors.append({"where": where, "problem": "«%s» (%s) не подтверждается указанными страницами %s" % (m.group(0), label, pages or "—"),
                           "fix": "%s. Доли и кратности переносятся как в источнике: «nearly half против 31 percent» — это «почти половина против 31%%», "
                                  "а не «в два раза»; не выводите кратность сами." % where_hint})

    t = core.as_text
    for i, f in enumerate(data.get("findings") or [], 1):
        if isinstance(f, dict):
            scan_spelled("вывод %d" % i, "%s %s" % (t(f.get("lead")), t(f.get("body"))), f.get("source_pages"))
    for i, q in enumerate(data.get("questions") or [], 1):
        if isinstance(q, dict):
            scan_spelled("вопрос %d" % i, "%s %s" % (t(q.get("q")), t(q.get("body"))), q.get("source_pages"))
    for i, f in enumerate(data.get("findings") or [], 1):
        if isinstance(f, dict):
            scan("вывод %d" % i, "%s %s" % (t(f.get("lead")), t(f.get("body"))), f.get("source_pages"), True)
    for i, q in enumerate(data.get("questions") or [], 1):
        if isinstance(q, dict):
            scan("вопрос %d" % i, "%s %s %s" % (t(q.get("q")), t(q.get("body")), t(q.get("ask"))), q.get("source_pages"), True)
    missing, _m = core.check_numbers(t(data.get("title")), doc_idx)
    if missing:
        errors.append({"where": "title", "problem": "чисел нет в исходном документе: %s" % ", ".join(missing)})
    scan("lede", t(data.get("lede")), None, False)
    return errors, warnings



def _ids(item) -> list[str]:
    ids = item.get("fact_ids") or []
    if isinstance(ids, str):
        ids = re.split(r"[,; ]+", ids)
    return [core.as_text(x).lower() for x in ids if core.as_text(x)]


def rules_check(data: dict, jdir: Path) -> tuple[list[dict], list[dict]]:
    """Семь правил содержания по реестру фактов: статус, модальность, механизм, недостающее, прецедент, бенефициары."""
    errors, warnings = [], []
    store = core.read_json(jdir / "facts.json", {"facts": []})
    facts = {f["id"]: f for f in store.get("facts", [])}
    if not rules.load(jdir):
        warnings.append({"where": "сектор", "problem": "сектор документа не выбран — факты извлекались без отраслевых правил",
                         "fix": "facts_rules.py detect / set"})
    t = core.as_text
    findings = [f for f in (data.get("findings") or []) if isinstance(f, dict)]
    questions = [q for q in (data.get("questions") or []) if isinstance(q, dict)]
    ftexts = ["%s %s" % (t(f.get("lead")), t(f.get("body"))) for f in findings]
    linked: set[str] = set()
    no_ids = []

    for i, (f, text) in enumerate(zip(findings, ftexts), 1):
        where = "вывод %d" % i
        ids = _ids(f)
        if not ids:
            no_ids.append(i)
        unknown = [x for x in ids if x not in facts]
        if unknown:
            warnings.append({"where": where, "problem": "fact_ids нет в реестре: %s" % ", ".join(unknown[:6]),
                             "fix": "возьмите номера из facts.py list"})
        linked_facts = [facts[x] for x in ids if x in facts]
        linked |= {x for x in ids if x in facts}
        not_done = [lf for lf in linked_facts if lf.get("status") in rules.NOT_DONE]
        for sent in _sentences(text):
            low = sent.lower()
            d = re.search(DONE, low)
            if not_done and d and not re.search(HEDGE, low):
                st = ", ".join(sorted({lf["status"] for lf in not_done}))
                errors.append({"where": where, "problem": "правило статуса: «%s» читается как действующий механизм, а в "
                                                          "источнике статус %s (%s)" % (d.group(0), st, ", ".join(lf["id"] for lf in not_done)[:40]),
                               "fix": "передайте стадию как в документе: «объявили о начале совместной работы», «предлагается», "
                                      "«изучают», «планируют запустить»; сроки — только если они названы"})
                break
            if re.search(START_DATE, low) and d and not re.search(HEDGE, low):
                (errors if not_done else warnings).append(
                    {"where": where, "problem": "правило статуса: конструкция «с <даты> … %s» читается как начало работы" % d.group(0),
                     "fix": "дата объявления — не дата запуска: «12 марта объявили о…»; если запуск датирован в документе — "
                            "проверьте, что это именно дата запуска"})
                break
        soft = [lf for lf in linked_facts if lf.get("status") in ("proposed", "studied")]
        if soft and not re.search(HEDGE, text.lower()):
            errors.append({"where": where, "problem": "правило модальности: в источнике это предложение или изучение (%s), а в "
                                                      "резюме звучит как решённое" % ", ".join(lf["id"] for lf in soft),
                           "fix": "сохраните модальность: «предлагается рассмотреть», «изучают возможность»"})
        else:
            modal = [lf for lf in linked_facts if lf.get("modality")]
            soft_modal = [lf for lf in linked_facts if not lf.get("modality") and lf.get("kind") in ("forecast", "estimate", "opinion", "recommendation")]
            if modal and not re.search(HEDGE, text.lower()):
                mods = "; ".join("%s: «%s»" % (lf["id"], lf["modality"]) for lf in modal[:3])
                errors.append({"where": where, "problem": "правило модальности: в источнике %s, а в резюме звучит как факт" % mods,
                               "fix": "перенесите модальную формулу источника: «по оценке участников… может», «ожидается», «предлагается»"})
            elif soft_modal and not re.search(HEDGE, text.lower()):
                warnings.append({"where": where, "problem": "модальность источника не видна в тексте (%s)" %
                                 ", ".join("%s: %s" % (lf["id"], lf["kind"]) for lf in soft_modal[:3]),
                                 "fix": "прогноз и оценку — с атрибуцией: «по оценке…», «ожидается»"})
    if no_ids:
        warnings.append({"where": "выводы %s" % ", ".join(map(str, no_ids)), "problem": "не указаны fact_ids",
                         "fix": "укажите номера фактов реестра: по ним проверяются статус, модальность и семь правил"})

    def covered(kind_facts: list[dict], rx: str) -> bool:
        if any(f["id"] in linked for f in kind_facts):
            return True
        return any(re.search(rx, tx.lower()) for tx in ftexts)

    by_kind: dict[str, list[dict]] = {}
    for f in facts.values():
        by_kind.setdefault(f.get("kind"), []).append(f)

    prec = [f for f in by_kind.get("precedent", []) if f.get("relevance") == "high"]
    if prec and not covered(prec, PRECEDENT_RX):
        errors.append({"where": "выводы", "problem": "правило прецедента: в реестре есть «впервые» (%s), в выводах его нет" %
                       ", ".join(f["id"] for f in prec[:4]),
                       "fix": "вынесите прецедент в выводы — первым или вторым пунктом: «Сделка первая такого рода.»"})
    gaps = [f for f in by_kind.get("gap", []) if f.get("relevance") == "high"]
    if gaps and not covered(gaps, GAP_RX):
        errors.append({"where": "выводы", "problem": "правило недостающего: в реестре есть пробелы для внедрения (%s), в выводах их нет" %
                       ", ".join(f["id"] for f in gaps[:4]),
                       "fix": "отдельный вывод о том, чего нет: ответственного, спецификаций, органа управления, сроков; "
                              "в вопросах это не заменяет вывод"})
    mech = [f for f in by_kind.get("mechanism", []) if f.get("relevance") == "high"]
    if mech and not any(f["id"] in linked for f in mech):
        warnings.append({"where": "выводы", "problem": "правило механизма: факты о новом порядке работы (%s) не привязаны ни к одному выводу" %
                         ", ".join(f["id"] for f in mech[:4]),
                         "fix": "изложите, что меняется в процессе — кто что делает и в каком порядке, — а не только эффект"})
    ben = [f for f in by_kind.get("beneficiary", []) if f.get("relevance") in ("high", "medium")]
    parties = sorted({t(f.get("party")).lower() for f in ben if t(f.get("party"))})
    if len(parties) >= 2:
        need = min(len(parties), 3)
        got = {t(f.get("party")).lower() for f in ben if f["id"] in linked and t(f.get("party"))}
        benef_texts = [tx.lower() for tx in ftexts if re.search(BENEF_RX, tx.lower())]
        for party in parties:
            stem = re.sub(r"[^\w-]", "", party.split()[0])[:6]
            if stem and any(stem in tx for tx in benef_texts):
                got.add(party)
        if len(got) < need:
            errors.append({"where": "выводы", "problem": "правило бенефициаров: в реестре стороны %s; в выводах разобрано %d из %d" %
                           ("; ".join(parties)[:140], len(got), need),
                           "fix": "один вывод: что получает и что отдаёт каждая сторона механизма (fact_ids — факты kind=beneficiary)"})
    for i, q in enumerate(questions, 1):
        ids = _ids(q)
        if ids and any(x not in facts for x in ids):
            warnings.append({"where": "вопрос %d" % i, "problem": "fact_ids нет в реестре: %s" % ", ".join(x for x in ids if x not in facts)})
    return errors, warnings


def _rgb(hex_color: str):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _h(text: str) -> str:
    return core.esc_html(text).replace(core.NBSP, "&#160;")


class Layout:

    def __init__(self, pymupdf, density: str):
        self.mu = pymupdf
        self.d = DENSITY[density]
        self.doc = pymupdf.open()
        self.left, self.right = 14 * MM, A4_W - 14 * MM
        self.top, self.bottom = 12 * MM, A4_H - 9 * MM
        self.width = self.right - self.left
        self.items = []
        self.page_i = 0
        self.y = self.top
        self.font_b = pymupdf.Font("hebo")
        self.font_r = pymupdf.Font("helv")
        self.limit = self.bottom
        self.flow_height = 0.0

    def css(self, size: float, color: str, extra: str = "") -> str:
        return (
            "body{margin:0;padding:0} p{margin:0;padding:0;font-family:sans-serif;font-size:%spt;"
            "line-height:%s;color:%s;text-align:left} b{font-weight:bold} %s" % (size, self.d["lh"], color, extra)
        )

    def measure(self, html: str, css: str, width: float) -> float:
        story = self.mu.Story(html=html, user_css=css)
        _more, filled = story.place(self.mu.Rect(0, 0, width, 50_000))
        return float(filled[3])

    def need(self, h: float) -> None:
        if self.y + h > self.limit + 0.5 and self.y > self.top + 1:
            self.page_i += 1
            self.y = self.top
            self.limit = self.bottom

    def text(self, html: str, css: str, x: float = 0.0, width: float | None = None, after: float = 0.0, tag=None) -> tuple:
        w = (self.width - x) if width is None else width
        h = self.measure(html, css, w)
        self.need(h)
        rect = (self.left + x, self.y, self.left + x + w, self.y + h + 2)
        pi, y0 = self.page_i, self.y
        self.items.append((pi, "html", rect, html, css, tag))
        self.y += h + after
        self.flow_height += h + after
        return pi, y0, y0 + h

    def space(self, h: float) -> None:
        self.y += h
        self.flow_height += h

    def deco(self, kind: str, *payload, page=None) -> None:
        self.items.append((self.page_i if page is None else page, kind, payload))

    def spaced(self, x: float, baseline: float, text: str, bold: bool, size: float, color: str, tracking: float, right: bool = False) -> float:
        font = self.font_b if bold else self.font_r
        widths = [font.text_length(ch, size) + tracking * size for ch in text]
        total = sum(widths) - tracking * size
        x0 = x - total if right else x
        self.deco("spaced", x0, baseline, text, bold, size, color, widths)
        return total

    def paint(self, out_pdf: Path) -> int:
        mu = self.mu
        n_pages = max(i[0] for i in self.items) + 1 if self.items else 1
        for _ in range(n_pages):
            self.doc.new_page(width=A4_W, height=A4_H)
        pages = [self.doc[i] for i in range(n_pages)]
        order = {"bg": 0, "line": 1, "circle": 1, "spaced": 2, "html": 3}
        for item in sorted(self.items, key=lambda it: order.get(it[1], 9)):
            page = pages[item[0]]
            kind = item[1]
            if kind == "html":
                _pi, _k, rect, html, css, _tag = item
                spare, _scale = page.insert_htmlbox(mu.Rect(*rect), html, css=css, scale_low=1)
                if spare < 0:
                    page.insert_htmlbox(mu.Rect(rect[0], rect[1], rect[2], rect[3] + 40), html, css=css, scale_low=1)
            else:
                p = item[2]
                if kind == "bg":
                    rect, fill, edge = p
                    page.draw_rect(mu.Rect(*rect), color=None, fill=_rgb(fill))
                    if edge:
                        page.draw_rect(mu.Rect(rect[0], rect[1], rect[0] + 2, rect[3]), color=None, fill=_rgb(edge))
                elif kind == "line":
                    x0, y0, x1, y1, color, width = p
                    page.draw_line((x0, y0), (x1, y1), color=_rgb(color), width=width)
                elif kind == "circle":
                    cx, cy, r, fill = p
                    page.draw_circle((cx, cy), r, color=None, fill=_rgb(fill))
                elif kind == "spaced":
                    x0, baseline, text, bold, size, color, widths = p
                    tw = mu.TextWriter(page.rect)
                    x = x0
                    font = self.font_b if bold else self.font_r
                    for ch, w in zip(text, widths):
                        tw.append((x, baseline), ch, font=font, fontsize=size)
                        x += w
                    tw.write_text(page, color=_rgb(color))
        self.doc.set_metadata({"producer": core.SKILL_NAME, "creator": core.SKILL_NAME})
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.doc.subset_fonts()
        except Exception:
            pass
        self.doc.save(out_pdf, garbage=4, deflate=True)
        return n_pages


PROVENANCE = {   # строка о происхождении данных в подвале: честно говорит, что кроме отчёта повлияло на вопросы
    (): "Выводы, числа и вопросы основаны только на указанном отчёте.",
    ("kb",): "Выводы и числа — только из отчёта; при постановке вопросов учтена база знаний о Сбере.",
    ("web",): "Выводы и числа — только из отчёта; при постановке вопросов учтены результаты поиска в интернете.",
    ("kb", "web"): "Выводы и числа — только из отчёта; при постановке вопросов учтены база знаний о Сбере и поиск в интернете.",
}


def provenance(data: dict, jdir: Path) -> str:
    reg = ctxreg.load(jdir)
    kinds = {reg[c]["kind"] for q in (data.get("questions") or []) if isinstance(q, dict)
             for c in (q.get("context_ids") or []) if isinstance(c, str) and c in reg}
    return PROVENANCE[tuple(sorted(kinds & {"kb", "web"}))]


def render_pdf(pymupdf, data: dict, density: str, out_pdf: Path) -> dict:
    L = Layout(pymupdf, density)
    d = L.d
    lh = d["lh"]

    foot_html = '<p><b style="color:%s">ИСТОЧНИК</b> · %s. %s</p>' % (
        ACCENT, _h(data["source_footer"].rstrip(". ")), _h(data.get("_provenance") or PROVENANCE[()]))
    foot_css = L.css(d["foot"], INK_SOFT)
    foot_h = L.measure(foot_html, foot_css, L.width) + 6 + 1
    L.limit = L.bottom - foot_h - 4

    size = d["mast"]
    base_y = L.y + size
    left_text = data["masthead_left"].upper()
    L.spaced(L.left, base_y, left_text, True, size, BRAND, 0.06)
    # L.spaced(L.right, base_y, data["masthead_right"].upper(), False, size, INK_SOFT, 0.06, right=True)
    L.space(size * lh + 3)
    L.deco("line", L.left, L.y, L.right, L.y, BRAND, 1.6)
    L.space(7)

    L.text("<p><b>%s</b></p>" % _h(data["title"]), L.css(d["h1"], BRAND), after=3.5)
    lede_css = L.css(LEDE_PT, INK_SOFT, "b{color:%s}" % INK).replace("line-height:%s;" % d["lh"], "line-height:%s;" % LEDE_LH)
    L.text("<p><b>Резюме для руководства.</b> %s</p>" % _h(data["lede"]), lede_css, after=6.0)
    L.deco("line", L.left, L.y, L.right, L.y, RULE, 0.5)
    content_top = L.y

    def heading(idx: str, title: str, inset: float = 0.0, rule_color: str = RULE) -> None:
        r = d["idx"] / 2
        h = d["idx"] + 1
        L.need(h + d["base"] * lh * 2)
        cy = L.y + r
        x = L.left + inset
        L.deco("circle", x + r, cy, r, ACCENT)
        nw = L.font_b.text_length(idx, d["h2"])
        L.deco("spaced", x + r - nw / 2, cy + d["h2"] * 0.35, idx, True, d["h2"], "#FFFFFF", [nw])
        tx = x + d["idx"] + 6
        tw = L.spaced(tx, cy + d["h2"] * 0.35, title.upper(), True, d["h2"], ACCENT, 0.09)
        L.deco("line", tx + tw + 6, cy, L.right - inset, cy, rule_color, 0.5)
        L.space(h + 4.5)

    L.space(7.5)
    heading("1", "Ключевые выводы")
    body_css = L.css(d["base"], INK, "b{color:%s}" % BRAND)
    findings = data["findings"]
    for i, f in enumerate(findings):
        html = "<p><b>%s</b> %s</p>" % (_h(f["lead"]), _h(f["body"]))
        pi, y0, _y1 = L.text(html, body_css, x=9, after=(d["gap"] if i < len(findings) - 1 else 0), tag="вывод %d" % (i + 1))
        L.deco("circle", L.left + 1.5, y0 + d["base"] * lh / 2, 1.5, ACCENT, page=pi)

    L.space(8.5)
    pad_x, pad_top, pad_bot = 8.0, 6.0, 5.0
    seg_start = {}

    def mark(pi: int, y0: float, y1: float) -> None:
        a, b = seg_start.get(pi, (y0, y1))
        seg_start[pi] = (min(a, y0), max(b, y1))

    L.need(d["idx"] + d["base"] * lh * 3)
    block_top = L.y
    L.space(pad_top)
    pi0 = L.page_i
    heading("2", "Вопросы для обсуждения", inset=pad_x, rule_color=TINT_RULE)
    mark(pi0, block_top, L.y)
    q_css = L.css(d["base"], INK, "p.q{color:%s;font-weight:bold} b{color:%s}" % (BRAND, INK))
    num_css = L.css(d["base"], ACCENT)
    questions = data["questions"]
    for i, q in enumerate(questions, 1):
        html = '<p class="q">%s</p>' % (_h(q["q"]),)
        w = L.width - 2 * pad_x - 17
        pi, y0, y1 = L.text(html, q_css, x=pad_x + 17, width=w, after=(5 if i < len(questions) else 0), tag="вопрос %d" % i)
        L.items.append((pi, "html", (L.left + pad_x, y0, L.left + pad_x + 17, y0 + d["base"] * lh + 2),
                        "<p><b>%02d</b></p>" % i, num_css, None))
        mark(pi, y0 - (pad_top if pi != pi0 and y0 <= L.top + 1 else 0), y1)
    L.space(pad_bot)
    for pi, (a, b) in seg_start.items():
        L.deco("bg", (L.left, a, L.right, b + pad_bot), TINT, ACCENT, page=pi)

    if L.y + foot_h > L.bottom + 0.5:
        L.page_i += 1
        L.y = L.top
    fy = L.bottom - foot_h + 6
    L.deco("line", L.left, fy - 6, L.right, fy - 6, RULE, 0.5)
    L.items.append((L.page_i, "html", (L.left, fy, L.right, L.bottom + 2), foot_html, foot_css, None))

    n_pages = L.paint(out_pdf)

    line = d["base"] * lh
    available = (A4_H - 9 * MM - foot_h - 4) - content_top
    content_h = L.flow_height - (content_top - L.top)
    body_chars = sum(len(f["lead"]) + len(f["body"]) for f in findings) + sum(
        len(q["q"]) + len(q["body"]) + len(q["ask"]) for q in questions)
    fit = {"pages": n_pages, "density": density, "body_chars": body_chars}
    if n_pages == 1:
        fit["fill"] = round(content_h / available, 3)
        fit["free_lines"] = max(0, int((available - content_h) // line))
    tails = []
    done = pymupdf.open(out_pdf)
    for it in L.items:
        if it[1] == "html" and it[5]:
            rows = {}
            for b in done[it[0]].get_text("dict", clip=pymupdf.Rect(*it[2]))["blocks"]:
                for ln in b.get("lines", []):
                    key = round(ln["bbox"][3] / 3)
                    rows[key] = rows.get(key, "") + "".join(sp["text"] for sp in ln["spans"])
            if rows:
                last = rows[max(rows)].strip()
                tails.append({"where": it[5], "lines": len(rows), "last_line_chars": len(last)})
    done.close()
    fit["items"] = [dict(t) for t in tails]
    if n_pages > 1:
        over = max(line, content_h - available)
        fit["overflow_lines"] = int(over // line) + 1
        fit["cheapest_cuts"] = sorted(tails, key=lambda t: t["last_line_chars"])[:4]
    return fit


def render_html(data: dict, density: str, out_html: Path, draft: bool = False) -> None:
    tpl_path = Path(__file__).resolve().parent.parent / "assets" / "summary_template.html"
    if not tpl_path.is_file():
        core.fail("Не найден шаблон assets/summary_template.html.", "Проверьте, что папка assets/ загружена вместе с навыком.")
    tpl = tpl_path.read_text(encoding="utf-8")
    e = lambda s: core.esc_html(s).replace(core.NBSP, "&nbsp;")  # noqa: E731
    findings = "\n".join("      <li><b>%s</b> %s</li>" % (e(f["lead"]), e(f["body"])) for f in data["findings"])
    questions = "\n".join(
        '      <li>\n        <span class="q">%s</span>\n      </li>'
        % (e(q["q"]),) for q in data["questions"])
    dens_css = ""
    if density == "compact":
        dens_css = ("<style>body,.page,.findings li,.qa li,.qa li::before{font-size:10pt;line-height:1.38}"
                    "h1{font-size:13pt}h2,h2 .idx{font-size:11.5pt}h2 .idx{width:17pt;height:17pt}"
                    ".masthead{font-size:8.5pt}footer{font-size:8pt}</style>")
    repl = {
        "{{TITLE}}": e(data["title"]), "{{MASTHEAD_LEFT}}": e(data["masthead_left"]),
        "{{MASTHEAD_RIGHT}}": e(data["masthead_right"]), "{{LEDE}}": e(data["lede"]),
        "{{FINDINGS}}": findings, "{{QUESTIONS}}": questions,
        "{{SOURCE_FOOTER}}": e(data["source_footer"].rstrip(". ")), "{{PROVENANCE}}": e(data.get("_provenance") or PROVENANCE[()]), "{{DENSITY_CSS}}": dens_css,
    }
    if draft:
        repl["{{DENSITY_CSS}}"] += (
            "<style>.draft-banner{background:#B3261E;color:#fff;font:bold 11pt Arial,sans-serif;"
            "padding:8px 12px;text-align:center;margin:0 auto 8px;max-width:210mm}"
            ".page{position:relative}.page::after{content:'ЧЕРНОВИК';position:absolute;top:45%;left:0;right:0;"
            "text-align:center;font:bold 72pt Arial,sans-serif;color:rgba(179,38,30,.18);transform:rotate(-30deg);"
            "pointer-events:none}</style>")
    tpl = re.sub(r"\{\{[A-Z_]+\}\}", lambda m: repl.get(m.group(0), m.group(0)), tpl)
    if draft:
        tpl = tpl.replace('<div class="page">', '<div class="draft-banner">ЧЕРНОВИК — резюме не прошло проверку '
                          'скрипта и не готово к отправке</div>\n<div class="page">', 1)
    out_html.write_text(tpl, encoding="utf-8")


def apply_typography(data: dict) -> dict:
    def t(value) -> str:
        text = core.typo_ru(core.as_text(value))
        return re.sub(r"(?<=[^\W\d_])-(?=[^\W\d_])", "\u2011", text)

    res = dict(data)
    for k in ("masthead_left", "masthead_right", "title", "lede", "source_footer"):
        res[k] = t(data.get(k))
    res["lede"] = re.sub(r"^\s*Резюме для руководства\.?\s*", "", res["lede"])
    res["findings"] = [dict(f, lead=t(f.get("lead")), body=t(f.get("body"))) for f in (data.get("findings") or []) if isinstance(f, dict)]
    res["questions"] = [dict(q, q=t(q.get("q")), body=t(q.get("body")), ask=t(q.get("ask"))) for q in (data.get("questions") or []) if isinstance(q, dict)]
    return res


def cmd_schema(args) -> None:
    dens = args.density
    core.out({"ok": True, "summary_json": SCHEMA, "density": dens, "budget_chars": BUDGET[dens],
              "numbering": "В ответах build пункты называются «вывод 1», «вопрос 2» — нумерация с единицы, в порядке следования в JSON.",
              "fact_ids": "У каждого вывода и вопроса — fact_ids из реестра: по ним build проверяет статус, модальность и семь правил "
                          "(механизм, статус, недостающее, прецедент, бенефициары, постановка вопроса, модальность).",
              "lede": "Преамбула — ОДНО предложение (ориентир до 160 знаков, предел 200): кто, когда и о чём; 10 pt, интервал 1.",
              "one_page": "Резюме — ровно одна страница: при переполнении build вернёт shorten_required (до 5 попыток сокращения). "
                          "Затем — один раз humanize_required (проверка на человечность), и финальная сборка.",
              "questions": "Три открытых вопроса без «или» и без «да/нет», о разных предметах, без повторов. "
                           "Перед каждым — контекст: база знаний о Сбере (sber_kb.py search) и не больше 2 запросов в "
                           "интернет (компании отрасли в России и их связь со Сбером, уточнения по стране и банку). "
                           "scope, context_ids, known обязательны; players — если вопрос касается компаний отрасли. "
                           "Печатается только q.",
              "note": "Бюджет — ориентир: точный ответ «влезло или нет» даёт только build. "
                      "Плотность standard — требование к формату (Arial 12 pt, интервал 1,5); compact — только по просьбе пользователя."})


def natural_checks(data: dict, errors: list[dict], warnings: list[dict]) -> tuple[list[dict], list[dict], dict]:
    """Естественность и ясность (_natural.py) без дублей с замечаниями канона (PARASITES, STYLE_WARN, MORAL…).
    Если естественность считает ошибкой то, что канон дал предупреждением, остаётся ошибка."""
    nat_err, nat_warn, metrics = natural.check(data)

    def frags(text: str) -> list[str]:
        return [f.lower().strip(" .,…") for f in re.findall(r"«([^»]{2,})»", text)]

    def same(a: dict, b: dict) -> bool:
        if a["where"].split(".")[0] != b["where"].split(".")[0]:
            return False
        fa, fb = frags(a["problem"]), frags(b["problem"])
        return any(x and y and (x in y or y in x or x[:6] == y[:6]) for x in fa for y in fb)

    nat_err = [e for e in nat_err if not any(same(e, p) for p in errors)]
    nat_warn = [w for w in nat_warn if not any(same(w, p) for p in errors + warnings)]
    warnings[:] = [w for w in warnings if not any(same(w, e) for e in nat_err)]
    nat = {"status": "clean" if not nat_err and not nat_warn else "issues",
           "errors": len(nat_err), "warnings": len(nat_warn), "metrics": metrics}
    return nat_err, nat_warn, nat


PLAYER_RELATIONS = {"own": "наша компания (дочерняя или ассоциированная)", "related": "связана с группой: бывшая дочерняя, "
                    "партнёр, клиент банка", "competitor": "конкурент Сбера", "neutral": "независимая"}


def context_check(data: dict, jdir: Path) -> tuple[list[dict], list[dict]]:
    """Каждый вопрос написан после сбора контекста: база знаний о Сбере (kb) и до 2 запросов в интернет (web)."""
    errors, warnings = [], []
    ctx = ctxreg.load(jdir)
    used_slots: dict[str, int] = {}
    for i, q in enumerate(data.get("questions") or [], 1):
        if not isinstance(q, dict):
            continue
        where = "вопрос %d" % i
        scope = core.as_text(q.get("scope")).lower()
        ids = [core.as_text(x) for x in (q.get("context_ids") or []) if core.as_text(x)]
        known = core.as_text(q.get("known"))
        if scope not in ctxreg.SCOPES:
            errors.append({"where": where, "problem": "нет scope: company (вопрос о нашей компании) или country (о стране)"})
        if not ids:
            errors.append({"where": where, "problem": "вопрос написан без контекста: нет context_ids",
                           "fix": "до вопроса: sber_kb.py search (что Сбер уже делает, какие компании отрасли с ним связаны) "
                                  "и, если пользователь разрешил поиск (context.py consent), до 2 запросов в интернет"})
            continue
        missing = [x for x in ids if x not in ctx]
        if missing:
            errors.append({"where": where, "problem": "context_ids нет в реестре контекста: %s" % ", ".join(missing),
                           "fix": "возьмите id из ответов sber_kb.py search / context.py add (context.py list)"})
            continue
        entries = [ctx[x] for x in ids]
        slots = {e["slot"] for e in entries}
        if len(slots) > 1:
            errors.append({"where": where, "problem": "контекст из разных вопросов (%s): у одного вопроса — один slot" % ", ".join(sorted(slots))})
            continue
        slot = slots.pop()
        if slot in used_slots:
            errors.append({"where": where, "problem": "тот же контекст (%s), что у вопроса %d: у каждого вопроса — свой" % (slot, used_slots[slot])})
        used_slots[slot] = i
        if scope in ctxreg.SCOPES and any(e["scope"] != scope for e in entries):
            errors.append({"where": where, "problem": "scope вопроса «%s», а контекст собирали как «%s»" % (scope, entries[0]["scope"])})
        kinds = {e["kind"] for e in entries}
        if "kb" not in kinds:
            if scope == "company":
                errors.append({"where": where, "problem": "вопрос о компании без базы знаний о Сбере",
                               "fix": "sber_kb.py search <job> --slot %s --scope company --query '<тема вопроса>': что Сбер уже "
                                      "делает и какие компании отрасли с ним связаны" % slot})
            else:
                warnings.append({"where": where, "problem": "база знаний о Сбере не открыта",
                                 "fix": "если вопрос касается компаний или отрасли, где работает Сбер, — sber_kb.py search"})
        if not any(e.get("results") for e in entries):
            warnings.append({"where": where, "problem": "контекст не найден (%s): вопрос не сверен с тем, что уже известно"
                                                     % "; ".join(e.get("error") or "пусто" for e in entries),
                             "fix": "одной строкой скажите пользователю, что для этого вопроса контекст найти не удалось"})
        elif len(known) < 20:
            errors.append({"where": where, "problem": "нет known: что уже известно по найденному контексту",
                           "fix": "1–3 фразы со ссылками на id: что Сбер уже делает по теме, какие компании отрасли с ним "
                                  "связаны или конкурируют, что решено в стране — и почему ответа на вопрос ещё нет"})
        players = q.get("players") or []
        if not isinstance(players, list):
            errors.append({"where": where, "problem": "players — список объектов {name, relation, source}"})
            players = []
        for pl in players:
            if not isinstance(pl, dict) or not core.as_text(pl.get("name")):
                errors.append({"where": where, "problem": "у участника рынка в players нет name"})
                continue
            rel = core.as_text(pl.get("relation")).lower()
            src = core.as_text(pl.get("source"))
            if rel not in PLAYER_RELATIONS:
                errors.append({"where": where, "problem": "players «%s»: relation — own | related | competitor | neutral" % pl.get("name")})
            if not src or not (src.startswith("kb:") or src in ctx):
                errors.append({"where": where, "problem": "players «%s»: нет source — откуда известна связь со Сбером" % pl.get("name"),
                               "fix": "id из базы знаний (kb:co/…, kb:…) или id записи поиска (c001)"})
        if not players and any(e["kind"] == "web" and e.get("results") for e in entries) and \
                re.search(r"компани|производител|разработчик|игрок|заемщик|заёмщик|поставщик|стартап", core.as_text(q.get("q")).lower()):
            warnings.append({"where": where, "problem": "вопрос о компаниях отрасли, а players пуст",
                             "fix": "перечислите найденные компании отрасли в России и их связь со Сбером: own / related / competitor / neutral"})
    return errors, warnings


def text_checks(data: dict, jdir: Path, density: str, with_natural: bool = True) -> tuple[list[dict], list[dict], dict]:
    """Проверки текста без вёрстки: канон, числа, семь правил, контекст вопросов и (with_natural) естественность."""
    errors, warnings = lint(data, density)
    for fn in (verify_numbers, rules_check, context_check):
        e, w = fn(data, jdir)
        errors += e
        warnings += w
    if not with_natural:
        return errors, warnings, {"status": "skipped"}
    nat_err, nat_warn, nat = natural_checks(data, errors, warnings)
    return errors + nat_err, warnings + nat_warn, nat


SHORTEN_RULES = [
    "Сокращайте смыслом, а не телеграфным стилем. Порядок: (1) уберите из пунктов второстепенный факт или повтор тезиса в теле; "
    "(2) уберите лишние слова — уточнения, которые не меняют вывод; (3) если не хватает — уберите самый слабый пункт целиком "
    "(не меньше min_items). Прецедент, механизм, недостающее и бенефициары с relevance=high убирать нельзя — сокращайте их тело.",
    "Если лишних строк 1–3 — начните с пунктов из cheapest_cuts: уберите в пункте чуть больше знаков, чем в его последней строке "
    "(last_line_chars), и строка исчезнет. Преамбулу сократите до самого короткого варианта «кто, когда и о чём».",
    "Нельзя: заменять названия местоимениями и аббревиатурами; выбрасывать базу сравнения или период («на 27%» без «за 2025 г.»); "
    "склеивать два факта через тире или двоеточие; удалять связку, на которой держится логика («поэтому», «при этом», «но»); "
    "убирать подлежащее или сказуемое; усиливать модальность и статус («предлагается» → «делают»).",
    "Каждое оставшееся предложение читается само по себе, второе предложение пункта по-прежнему вытекает из первого; "
    "в вопросе остаются предмет и условие, без которых он непонятен. После правки перечитайте пункт глазами руководителя: если возник вопрос — сократите другое место.",
    "Числа остаются ровно как в документе, fact_ids — у каждого пункта. Шрифт, интервал и поля не меняются.",
]

READER_REVIEW = [
    "Прочитай каждый пункт как член правления, который не видел документ. После каждого предложения спроси: "
    "о ком или о чём речь (назван прямо, не местоимением)? с чем сравнивают и за какой период? почему так?",
    "Второе предложение пункта должно вытекать из первого: причина → следствие, факт → сравнение, проблема → масштаб. "
    "Если предложения можно поменять местами без потери смысла — связи нет, перепиши.",
    "Один предмет — одно название по всему тексту: не «банки… кредитные организации… игроки рынка».",
    "Если после пункта у читателя остаётся вопрос, ответ на который есть в реестре фактов, — добавь его, убрав менее важное; "
    "если ответа нет — сузь тезис до того, что доказано.",
    "Прочитай вслух: звучит как ведущий аналитик, объясняющий вывод правлению, а не как пресс-релиз, перевод или ответ чат-бота.",
]


def _plain(data: dict) -> list[str]:
    out = []
    for i, f in enumerate(data.get("findings") or [], 1):
        if isinstance(f, dict):
            out.append("вывод %d: %s %s" % (i, core.as_text(f.get("lead")), core.as_text(f.get("body"))))
    for i, q in enumerate(data.get("questions") or [], 1):
        if isinstance(q, dict):
            out.append("вопрос %d: %s" % (i, " ".join(t for t in (core.as_text(q.get(k)) for k in ("q", "body", "ask")) if t)))
    return out


def cmd_check(args) -> None:
    jdir = core.job_dir(args.job)
    data = core.load_payload(args, "summary.json")
    if not isinstance(data, dict):
        core.fail("summary.json должен быть объектом.", "Формат: summary.py schema")
    natural_on = bool(getattr(args, "natural", False))
    errors, warnings, nat = text_checks(data, jdir, args.density, with_natural=natural_on)
    if not natural_on:
        nat = {"status": "skipped",
               "reason": "естественность проверяется один раз — на этапе humanize, после того как резюме уместилось "
                         "на страницу или исчерпаны 5 сокращений"}
    verdict = "clean" if not errors else "fix_required"
    resp = {"ok": True, "verdict": verdict, "errors": errors, "warnings": warnings[:40], "naturalness": nat,
            "text": _plain(data)}
    resp["next"] = ("Исправьте errors и вызовите check снова; когда errors пуст — summary.py build." if errors else
                    "Канон, числа и семь правил в порядке. Дальше — summary.py build: он проверит число страниц. "
                    "Естественность сейчас не правьте — для неё будет отдельный шаг humanize после вёрстки.")
    core.out(resp)


def _read_ref(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return "(файл references/%s не найден в папке навыка)" % path.name


def cmd_factcheck(args) -> None:
    """Принять отчёт сверки фактов: проверить цитаты и числа, запомнить подтверждённое и найденные ошибки."""
    jdir = core.job_dir(args.job)
    report = core.load_payload(args, "отчёт сверки фактов")
    state_path = jdir / "out" / "fit_state.json"
    state = _load_state(state_path)
    issued = state.get("fc_issued") or {}
    if state.get("phase") != "factcheck" or not issued:
        core.fail("Сейчас сверка фактов не ожидается.",
                  "Сверка начинается, когда summary.py build вернёт verdict factcheck_required: отчёт — по его factcheck.claims.")
    errors, parsed = fc.validate(report, issued, jdir)
    if errors:
        core.out({"ok": True, "accepted": False, "errors": errors[:40],
                  "next": "Отчёт не принят: исправьте перечисленное (цитаты — дословно со страницы, вердикт для каждого id, "
                          "числа утверждения или исправления — в цитатах) и отправьте отчёт целиком снова."})
    verified = set(state.get("verified", []))
    to_fix = {}
    for cid, v in parsed.items():
        if v["verdict"] == "ok":
            verified.add(fc.norm(v["text"]))
        else:
            to_fix[cid] = v
            if v["correction"]:            # исправление уже опирается на цитаты: вписанное дословно повторно не сверяется
                verified.add(fc.norm(v["correction"]))
    state["verified"] = sorted(verified)
    state["to_fix"] = to_fix
    state["fc_reports"] = int(state.get("fc_reports", 0)) + 1
    state["corrected"] = sorted(set(state.get("corrected", [])) | set(to_fix))
    state["fc_issued"] = {}
    core.write_json(state_path, state)
    log = core.read_json(jdir / "out" / "factcheck_log.json", {"rounds": []})
    log["rounds"].append({"round": state["fc_reports"], "verdicts": parsed})
    core.write_json(jdir / "out" / "factcheck_log.json", log)
    fixes = [{"id": cid, "where": v["where"], "verdict": v["verdict"], "was": v["text"], "problem": v["problem"],
              "correction": v["correction"]} for cid, v in to_fix.items()]
    resp = {"ok": True, "accepted": True, "round": state["fc_reports"], "confirmed": sum(v["verdict"] == "ok" for v in parsed.values()),
            "fixes": fixes}
    resp["next"] = ("Все утверждения подтверждены документом. Вызовите summary.py build с тем же summary.json — это финальная сборка."
                    if not fixes else
                    "Найдено расхождений с документом: %d. Внесите в summary.json каждое исправление из fixes (предложение «was» → "
                    "«correction»; пустой correction — уберите предложение или сузьте тезис), остальной текст не трогайте, и вызовите "
                    "summary.py build: исправления, вписанные дословно, уже подтверждены цитатами; на сверку уйдут только "
                    "предложения, изменённые иначе." % len(fixes))
    core.out(resp)


def _humanize_text(data: dict) -> list[str]:
    t = core.as_text
    return ["заголовок: %s" % t(data.get("title")), "преамбула: %s" % t(data.get("lede"))] + _plain(data)


def _humanize_payload(data: dict, fit: dict, errors: list[dict], warnings: list[dict], fitted: bool) -> dict:
    """Всё, что нужно модели для одной финальной редактуры: инструкция, признаки, текст, предел длины."""
    nat_err, nat_warn, nat = natural_checks(data, list(errors), list(warnings))
    style = [w for w in warnings if w.get("category") in ("естественность", "ясность")
             or re.search(r"кальк|шаблон|штамп|усилител|связь|чисел|раскрыт", w.get("problem", ""))]
    lines_total = sum(t["lines"] for t in fit.get("items", [])) or 1
    cpl = max(40, round(fit["body_chars"] / lines_total))
    if fitted:
        spare = max(0, int(fit.get("free_lines", 0)) - 1) * cpl          # одна строка — запас
        max_chars = fit["body_chars"] + spare
        length_rule = ("Сейчас текст помещается на страницу (свободных строк: %d). Тело резюме — не больше %d знаков "
                       "(сейчас %d): связки и уточнения окупайте вычёркиванием лишнего."
                       % (fit.get("free_lines", 0), max_chars, fit["body_chars"]))
    else:
        max_chars = fit["body_chars"]
        length_rule = ("После 5 сокращений резюме всё ещё на %d стр. Редактура не должна удлинять текст: тело — не больше "
                       "%d знаков (сейчас столько же)." % (fit["pages"], max_chars))
    instruction = _read_ref(HUMANIZE_GUIDE)
    return {
        "fitted": fitted, "pages": fit["pages"], "body_chars": fit["body_chars"], "max_body_chars": max_chars,
        "length_rule": length_rule,
        "instruction": instruction,
        "signs": (nat_err + nat_warn + style)[:60],
        "metrics": nat.get("metrics", {}),
        "reader_review": READER_REVIEW,
        "text": _humanize_text(data),
    }


def _shorten_block(fit: dict, density: str, attempt: int, max_attempts: int, rules: list[str]) -> dict:
    lines_total = sum(t["lines"] for t in fit.get("items", [])) or 1
    cpl = max(40, round(fit["body_chars"] / lines_total))
    cut = (fit["overflow_lines"] + 1) * cpl
    bud = BUDGET[density]
    return {
        "attempt": attempt, "max_attempts": max_attempts, "pages": fit["pages"],
        "overflow_lines": fit["overflow_lines"], "chars_per_line": cpl, "cut_chars": cut,
        "target_body_chars": max(0, fit["body_chars"] - cut), "items": fit.get("items", []),
        "cheapest_cuts": fit.get("cheapest_cuts", []),
        "min_items": {"findings": bud["findings"][0], "questions": bud["questions"][0]},
        "rules": rules,
    }


TRIM_RULES = [
    "Редактура на человечность вывела текст за страницу. Уберите не меньше cut_chars знаков, не возвращая машинных оборотов: "
    "вычёркивайте второстепенный факт или лишнее уточнение, а не связки, которые только что появились.",
] + SHORTEN_RULES[1:]


def _is_length_error(e: dict) -> bool:
    return bool(re.search(r"\d+ знаков при ориентире", e.get("problem", "")))


def _load_state(path: Path) -> dict:
    st = core.read_json(path, {})
    if "phase" not in st:                         # файл версии 2.1: {"overflow_builds": N}
        st = {"phase": "fit", "shorten_attempts": int(st.get("overflow_builds", 0)), "trims": 0}
    st.setdefault("shorten_attempts", 0)
    st.setdefault("trims", 0)
    return st


def _count_build(jdir: Path, reset: bool = False) -> int:
    """Счётчик сборок задания (out/build_count.json): раньше его вёл внешний агент, теперь — сам навык.
    Сбрасывается pdf.py open, --reset и выдачей готового резюме."""
    path = jdir / "out" / "build_count.json"
    st = {} if reset else (core.read_json(path, {}) or {})
    n = int(st.get("builds", 0)) + 1
    core.write_json(path, {"builds": n})
    return n


def _clear_build_count(jdir: Path) -> None:
    path = jdir / "out" / "build_count.json"
    if path.is_file():
        path.unlink()


def cmd_build(args) -> None:
    pymupdf = core.require_pymupdf()
    jdir = core.job_dir(args.job)
    data = core.load_payload(args, "summary.json")
    if not isinstance(data, dict):
        core.fail("summary.json должен быть объектом.", "Формат: summary.py schema")
    builds = _count_build(jdir, reset=getattr(args, "reset", False))
    density = args.density
    asked = core.as_text(getattr(args, "user_request", None))
    if density == "compact" and len(re.sub(r"\W+", "", asked)) < 8:
        core.fail("Плотность compact (10 pt) включается только по прямой просьбе пользователя.",
                  "Оформление резюме фиксировано: 12 pt, интервал 1,5 — собирайте без --density и сокращайте текст до ~1 800 знаков "
                  "(summary.py schema). Если пользователь сам попросил мелкий шрифт или больше текста — повторите вызов с "
                  "--user-request '<его слова дословно>'.")
    errors, warnings = lint(data, density)
    structural = [e for e in errors if e["problem"] in ("поле пустое",) or "должн" in e["problem"] or "нужны" in e["problem"]]
    if structural and not (data.get("findings") and data.get("questions")):
        core.out({"ok": False, "error": "Структура summary.json неполная.", "verdict": "fix_required", "errors": errors,
                  "hint": "Формат: summary.py schema"}, code=2)
    errors, warnings, _nat = text_checks(data, jdir, density, with_natural=False)   # канон, числа, семь правил — всегда

    facts = core.read_json(jdir / "facts.json", {"facts": [], "skipped_pages": []})
    meta = core.read_json(jdir / "meta.json", {})
    seen = {f["page"] for f in facts.get("facts", [])} | set(facts.get("skipped_pages", []))
    unread = [n for n in range(1, int(meta.get("pages_total", 0)) + 1) if n not in seen]
    if unread:
        warnings.append({"where": "reestr", "problem": "страницы не прочитаны: %s" % ", ".join(map(str, unread[:30])),
                         "fix": "дочитайте их (pdf.py pages) и сдайте факты либо отметьте facts.py skip"})
    if facts.get("skip_reasons"):
        warnings.append({"where": "reestr", "problem": "пропущены страницы с текстом: %s" % ", ".join(sorted(facts["skip_reasons"], key=int)[:20]),
                         "fix": "одной строкой скажите пользователю, какие страницы не вошли в резюме и почему"})
    deal_src = any(re.search(r"agree\w* to acquire|agreement to acquire|to be acquired|announced (its |the )?(plan|intention|agreement)|"
                             r"subject to (regulatory )?approval|договорил\w+ о покупке|объявил\w* о (покупке|намерени)",
                             core.page_text(jdir, n), re.I) for n in range(1, int(meta.get("pages_extracted", 0)) + 1))
    if deal_src:
        for where, text in [("вывод %d" % i, "%s %s" % (core.as_text(f.get("lead")), core.as_text(f.get("body"))))
                            for i, f in enumerate(data.get("findings") or [], 1) if isinstance(f, dict)] + \
                           [("вопрос %d" % i, " ".join(core.as_text(q.get(k)) for k in ("q", "body", "ask")))
                            for i, q in enumerate(data.get("questions") or [], 1) if isinstance(q, dict)]:
            m = re.search(r"\b(поглотил\w*|купил\w*|приобр[её]л\w*|закрыл\w* сделку|завершил\w* (покупку|сделку|слияние))", text.lower())
            if m:
                warnings.append({"where": where, "problem": "«%s» — в источнике сделка только объявлена" % m.group(0),
                                 "fix": "пишите как в документе: «договорился о покупке», «объявил о покупке»"})

    clean = apply_typography(data)
    for k in ("masthead_left", "masthead_right", "title", "lede", "source_footer"):
        clean[k] = clean.get(k) or "—"
    clean["_provenance"] = provenance(data, jdir)
    out_dir = jdir / "out"
    out_dir.mkdir(exist_ok=True)
    tmp_pdf = out_dir / "build.tmp.pdf"
    fit = render_pdf(pymupdf, clean, density, tmp_pdf)

    # ---- этапы: fit (сокращение до MAX_SHORTEN раз) → humanize (один раз) → готово
    state_path = out_dir / "fit_state.json"
    if getattr(args, "reset", False) and state_path.is_file():
        state_path.unlink()
    state = _load_state(state_path)
    phase = state["phase"]
    shorten = humanize = factcheck = fact_summary = None
    nat = {"status": "pending", "reason": "естественность проверяется один раз — на этапе humanize"}

    def demote_length() -> None:
        """Ориентир длины пункта — средство уместить страницу. Когда сокращения исчерпаны или идёт финальная
        сборка, страница — единственный критерий: такие ошибки становятся замечаниями и не блокируют выдачу."""
        moved = [e for e in errors if _is_length_error(e)]
        errors[:] = [e for e in errors if not _is_length_error(e)]
        warnings[:0] = moved

    if phase == "fit":
        if fit["pages"] > 1 and state["shorten_attempts"] < MAX_SHORTEN:
            state["shorten_attempts"] += 1
            shorten = _shorten_block(fit, density, state["shorten_attempts"], MAX_SHORTEN, SHORTEN_RULES)
            verdict = "shorten_required"
        else:
            if fit["pages"] > 1:                   # 5 сокращений исчерпаны — дальше всё равно humanize
                demote_length()
            if errors:
                verdict = "fix_required"
            else:
                fitted = fit["pages"] == 1
                humanize = _humanize_payload(data, fit, errors, warnings, fitted)
                state.update({"phase": "humanize", "fitted": fitted, "body_chars_before": fit["body_chars"],
                              "pages_before": fit["pages"]})
                verdict = "humanize_required"
                nat = {"status": "humanize_required", "signs": len(humanize["signs"]), "metrics": humanize["metrics"]}
        core.write_json(state_path, state)
    else:                                          # humanize → factcheck: естественность повторно не проверяется
        nat = {"status": "done", "reason": "проверка на человечность выполнена; повторно не запускается"}
        if fit["pages"] > 1 and state.get("fitted") and state["trims"] < MAX_TRIMS:
            state["trims"] += 1
            shorten = _shorten_block(fit, density, state["trims"], MAX_TRIMS, TRIM_RULES)
            verdict = "trim_required"
        else:
            demote_length()
            if phase == "humanize":                # редактура принята — дальше сверка фактов с документом
                state.update({"phase": "factcheck", "verified": [], "to_fix": {}, "fc_reports": 0, "fc_issued": {}})
                old_log = out_dir / "factcheck_log.json"
                if old_log.is_file():
                    old_log.unlink()
            items = fc.claims(data, _sentences)
            fixed_wrong = {fc.norm(v["text"]): v for v in state.get("to_fix", {}).values()}
            for c in items:
                v = fixed_wrong.get(fc.norm(c["text"]))
                if v:
                    errors.append({"where": c["where"], "problem": "сверка с документом нашла ошибку, а предложение не исправлено: %s" % v["problem"],
                                   "fix": "замените на correction из отчёта сверки: «%s»%s" % (
                                       v["correction"][:300], "" if v["correction"] else " (пусто — уберите предложение)")})
            verified = set(state.get("verified", []))
            pending = [c for c in items if fc.norm(c["text"]) not in verified]
            if errors:
                verdict = "fix_required"
            elif pending and (state["fc_reports"] < MAX_FACTCHECK_ROUNDS or (
                    state["fc_reports"] < MAX_FACTCHECK_ROUNDS + FC_EXTRA_ROUNDS
                    and all(c["kind"] in FC_REQUIRED_KINDS for c in pending))):
                factcheck = fc.packet(pending, jdir)
                factcheck.update({"round": state["fc_reports"] + 1,
                                  "max_rounds": MAX_FACTCHECK_ROUNDS if state["fc_reports"] < MAX_FACTCHECK_ROUNDS
                                  else MAX_FACTCHECK_ROUNDS + FC_EXTRA_ROUNDS,
                                  "already_verified": len(items) - len(pending), "instruction": _read_ref(FACTCHECK_GUIDE)})
                state["fc_issued"] = {c["id"]: {k: c[k] for k in ("where", "kind", "text", "source_pages", "fact_ids")} for c in pending}
                verdict = "factcheck_required"
            elif pending:
                # раунды сверки исчерпаны, а утверждения не подтверждены: готовое резюме с ними не выдаётся (fail-closed)
                for c in pending:
                    required = c["kind"] in FC_REQUIRED_KINDS
                    errors.append({"where": c["where"], "problem": "после %d раундов сверки утверждение не подтверждено документом: «%s»"
                                   % (state["fc_reports"], c["text"][:160]),
                                   "fix": ("эту строку удалить нельзя: замените её дословно на correction из отчёта сверки или на "
                                           "уже подтверждённое предложение резюме и снова вызовите build" if required else
                                           "удалите это предложение из summary.json (или замените его дословно на correction из "
                                           "отчёта сверки, если она его дала) и снова вызовите build; новых формулировок не пишите")})
                verdict = "fix_required"
            else:
                verdict = "ready" if fit["pages"] == 1 else "ready_as_is"
                nat.update({"shorten_attempts": state["shorten_attempts"], "trims": state["trims"]})
                fact_summary = {"rounds": state["fc_reports"], "verified": len(items) - len(pending), "unverified": len(pending),
                                "corrected": len(state.get("corrected", []))}
        if verdict in ("ready", "ready_as_is"):
            if state_path.is_file():
                state_path.unlink()
        else:
            core.write_json(state_path, state)
    if verdict in ("ready", "humanize_required") and fit.get("fill", 1) < 0.85 and not state.get("shorten_attempts"):
        warnings.append({"where": "page", "problem": "лист заполнен на %d%%, свободно строк: %d" % (round(fit["fill"] * 100), fit["free_lines"]),
                         "fix": "при редактуре можно вернуть причину «почему так» в короткие пункты — не «воду»"})

    names = core.output_paths(jdir)
    final = {"pdf": names["summary_pdf"], "html": names["summary_html"], "json": names["summary_json"]}
    draft = {"pdf": names["draft_pdf"], "html": names["draft_html"], "json": names["draft_json"]}
    deliverable = verdict in ("ready", "ready_as_is")
    target = final if deliverable else draft
    for legacy in ("summary_ru.pdf", "summary_ru.html", "draft_summary_ru.pdf", "draft_summary_ru.html"):
        if (out_dir / legacy).is_file():
            (out_dir / legacy).unlink()
    if deliverable:
        os.replace(tmp_pdf, target["pdf"])
        for path in draft.values():
            if path.is_file():
                path.unlink()
    else:
        _stamp_draft(pymupdf, tmp_pdf, target["pdf"])
        tmp_pdf.unlink()
    render_html(clean, density, target["html"], draft=not deliverable)
    core.write_json(target["json"], {k: v for k, v in clean.items() if k != "_provenance"})

    resp = {"ok": True, "verdict": verdict, "phase": state["phase"] if not deliverable else "done", "fit": fit,
            "errors": errors, "warnings": warnings[:40], "naturalness": nat,
            "outputs": {k: str(v) for k, v in target.items()}, "file_name": target["pdf"].name,
            "build": {"attempt": builds, "max_attempts": MAX_BUILDS}}
    if deliverable:
        _clear_build_count(jdir)
    if shorten:
        resp["shorten"] = shorten
    if humanize:
        resp["humanize"] = humanize
    if factcheck:
        resp["factcheck"] = factcheck
    if fact_summary:
        resp["factcheck_summary"] = fact_summary
    if density == "compact":
        resp["density_note"] = ("Собрано уплотнённо (10 pt) по просьбе пользователя: «%s». Скажите ему об этом одной строкой." % asked[:200])
    if verdict == "ready":
        resp["next"] = ("Готово: сразу отдайте пользователю outputs.pdf под его собственным именем file_name — не переименовывайте. "
                        "Сначала скопируйте его без изменений в папку файлов пользователя (в ГигаАгенте — /data/user/Deliverables/, "
                        "создайте её при необходимости) и отправьте копию инструментом отправки файлов (send_file): новые версии "
                        "платформы не прикладывают файлы из папки навыка; если скопировать нельзя — отправьте outputs.pdf напрямую. "
                        "HTML не отправляйте вместо PDF; "
                        "отдельно, вторым файлом — только если пользователь сам просил HTML. "
                        "Одной строкой перечислите warnings, если они есть. Естественность повторно не проверяйте.")
    elif verdict == "ready_as_is":
        resp["next"] = ("Резюме прошло проверку на человечность и сверку фактов, но занимает %d стр. (сокращений: %d, подрезок после редактуры: %d). "
                        "По правилу навыка отдайте PDF как есть: скопируйте outputs.pdf без изменений в папку файлов пользователя "
                        "под именем file_name и отправьте. Одной строкой скажите пользователю, что резюме заняло %d стр."
                        % (fit["pages"], state["shorten_attempts"], state["trims"], fit["pages"]))
    elif verdict == "shorten_required":
        resp["deliverable"] = False
        resp["next"] = ("Резюме заняло %d стр. Попытка сокращения %d из %d: уберите не меньше shorten.cut_chars знаков "
                        "(лишних строк: %d) по правилам shorten.rules и снова вызовите summary.py build. Естественность сейчас "
                        "не проверяется и не правится — для неё будет отдельный шаг humanize, когда текст уместится на страницу "
                        "(или после 5-й попытки). Шрифт 12 pt и интервал 1,5 не меняются.%s"
                        % (fit["pages"], shorten["attempt"], MAX_SHORTEN, fit["overflow_lines"],
                           " Заодно исправьте errors." if errors else ""))
    elif verdict == "humanize_required":
        resp["deliverable"] = False
        resp["next"] = ("%s Теперь — проверка на человечность, один раз. Прочитайте humanize.instruction и следуйте ей: прочитайте "
                        "humanize.text целиком, учтите humanize.signs, перепишите summary.json полностью (числа, fact_ids, "
                        "source_pages, число пунктов, статус и модальность не меняются; тело не длиннее humanize.max_body_chars). "
                        "Затем вызовите summary.py build: дальше — сверка фактов с документом; естественность повторно не проверяется."
                        % ("Резюме на одной странице." if humanize["fitted"] else
                           "После %d сокращений резюме всё ещё на %d стр. — по правилу навыка проверка на человечность выполняется всё равно."
                           % (state["shorten_attempts"], fit["pages"])))
    elif verdict == "factcheck_required":
        resp["deliverable"] = False
        resp["next"] = ("Сверка фактов с документом, раунд %d из %d: утверждений на проверку — %d (уже подтверждено: %d). "
                        "Прочитайте factcheck.instruction. Для каждого утверждения из factcheck.claims сравните текст с excerpts "
                        "(при нехватке — pdf.py pages): тот ли показатель, период, единица, предмет, чья оценка, статус и модальность. "
                        "Отправьте отчёт: summary.py factcheck <job> --json '{\"claims\": [{\"id\", \"verdict\": ok|fix|unsupported, "
                        "\"evidence\": [{\"page\", \"quote\"}], \"problem\", \"correction\"}]}'. Цитаты — дословно со страницы."
                        % (factcheck["round"], factcheck["max_rounds"], len(factcheck["claims"]), factcheck["already_verified"]))
    elif verdict == "trim_required":
        resp["deliverable"] = False
        resp["next"] = ("После редактуры резюме заняло %d стр. Подрезка %d из %d: уберите не меньше shorten.cut_chars знаков по "
                        "shorten.rules и снова вызовите summary.py build. Естественность повторно не проверяется — не возвращайте "
                        "машинных оборотов при сокращении." % (fit["pages"], shorten["attempt"], MAX_TRIMS))
    else:
        resp["deliverable"] = False
        if final["pdf"].is_file():
            resp["last_ready_pdf"] = str(final["pdf"])
        resp["next"] = ("Исправьте errors в summary.json (канон, сверка чисел, семь правил) и снова вызовите build; этап (%s) не "
                        "меняется. Файлы в outputs — ЧЕРНОВИК: пользователю не отдавайте. Только если попытки исчерпаны "
                        "(build.attempt дошёл до build.max_attempts или кончается бюджет задачи) — отправьте ЧЕРНОВИК-PDF как есть, с пометкой, и прямо "
                        "напишите, что не сошлось. HTML вместо PDF не отправляйте никогда." % state["phase"])
    if not deliverable and builds >= MAX_BUILDS:
        resp["builds_exhausted"] = True
        resp["next"] = ("Это сборка %d из %d — предел. Больше не собирайте: отправьте пользователю ЧЕРНОВИК-PDF outputs.pdf "
                        "как есть (с пометкой, через копию в папке файлов пользователя) и прямо напишите, что не сошлось: "
                        "verdict %s, errors и незавершённый этап. HTML вместо PDF не отправляйте." % (builds, MAX_BUILDS, verdict))
    core.out(resp)


def _stamp_draft(pymupdf, src: Path, dst: Path) -> None:
    doc = pymupdf.open(src)
    font = pymupdf.Font("hebo")
    for page in doc:
        tw = pymupdf.TextWriter(page.rect, opacity=0.18, color=(0.8, 0.1, 0.1))
        text = "ЧЕРНОВИК"
        size = 92
        width = font.text_length(text, size)
        pivot = pymupdf.Point(page.rect.width / 2, page.rect.height / 2)
        tw.append((pivot.x - width / 2, pivot.y + size / 3), text, font=font, fontsize=size)
        tw.write_text(page, morph=(pivot, pymupdf.Matrix(35)))
    doc.save(dst, garbage=4, deflate=True)
    doc.close()


def main() -> None:
    core.setup_stdio()
    ap = core.JsonArgumentParser(prog="summary.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("schema"); p.add_argument("--density", choices=list(DENSITY), default="standard"); p.set_defaults(fn=cmd_schema)
    p = sub.add_parser("check"); p.add_argument("job"); p.add_argument("--json"); p.add_argument("--file")
    p.add_argument("--natural", action="store_true", help="диагностика: показать и признаки машинного текста")
    p.add_argument("--density", choices=list(DENSITY), default="standard"); p.set_defaults(fn=cmd_check)
    p = sub.add_parser("factcheck"); p.add_argument("job"); p.add_argument("--json"); p.add_argument("--file")
    p.set_defaults(fn=cmd_factcheck)
    p = sub.add_parser("build"); p.add_argument("job"); p.add_argument("--json"); p.add_argument("--file")
    p.add_argument("--density", choices=list(DENSITY), default="standard")
    p.add_argument("--user-request", dest="user_request")
    p.add_argument("--reset", action="store_true", help="начать этапы fit → humanize заново"); p.set_defaults(fn=cmd_build)
    args = ap.parse_args()
    if not getattr(args, "fn", None):
        core.fail("Не указана команда.", "Доступно: schema, check, build, factcheck.")
    args.fn(args)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        core.fail("Внутренняя ошибка summary.py: %s: %s" % (type(e).__name__, e))
