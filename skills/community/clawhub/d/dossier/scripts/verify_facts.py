#!/usr/bin/env python3
"""Триангуляция фактов досье через Sonar — ДО сборки документа.

Зачем отдельный шаг, а не проверка при вёрстке. Проверка чисел в
`render_dossier.py` стоит на выходе: она ловит число без доказательства, но
доказательством считает то, что модель сама же и записала. И главное —
текст в чат владелец получает из того же JSON, а не из документа. Значит,
непроверенное утверждение доходит до человека раньше, чем что-либо
успевает отказать.

Здесь проверка идёт наружу, к настоящим источникам, и до того, как
владелец что-либо увидит. Семь раз отмерь: волны поиска → кросс-проверка
подагентами по инструкции → ЭТОТ скрипт → и только потом вёрстка.

Что делает:

  1. Собирает утверждения — ВСЕ числа из `figures` и ВСЕ фактические фразы
     со ссылкой на источник из «Одним абзацем», «Кто он», «Чем известен»,
     «Тем на обсуждение» и должности.
     Предела нет: проверяется каждое. Обращения идут в восемь потоков,
     поэтому семнадцать утверждений занимают шестнадцать секунд, а не две
     минуты, и ограничивать их число не приходится.
  2. По каждому идёт в Sonar с САМИМ утверждением, а не с именем человека.
  3. Считает домены, которые НА САМОМ ДЕЛЕ подтверждают: в сниппете есть
     само число (для величин) или минимум два значимых слова утверждения
     (для фактов). Подтверждение — совпадение в двух РАЗНЫХ доменах.
     Просто присутствие домена в выдаче не считается: на утверждение про
     диплом приходило 15 доменов, включая книжный магазин и Газпром.
  3a. Для чисел вдобавок открывается САМА цитируемая страница и число
     ищется на ней. Поиск по интернету атрибуцию не устанавливает.
  4. Утверждения, опирающиеся только на первоисточник, который по природе
     уникален — LinkedIn, GitHub, arXiv, Google Scholar, ORCID, — кросс-
     проверку не проходят: требовать второй источник для того, что
     существует в одном месте, значит запретить верный факт.

  verify_facts.py dossier.json                проверить ВСЕ утверждения
  verify_facts.py dossier.json --dry-run      показать план без обращений к сети
  verify_facts.py dossier.json --fresh        проверить заново, не используя кэш
  verify_facts.py --explain                   как устроена проверка

Время. У скрипта жёсткий предел платформы (300 с). Проверка идёт с общим
дедлайном: всё, что не успело, помечается «НЕ ПРОВЕРЕНО (время)» — это
отказ, а не пропуск. Уже подтверждённое кэшируется в рабочем каталоге
навыка, поэтому повторный вызов с тем же файлом проверяет только остаток.

Настройки: PERPLEXITY_API_KEY (обязателен), DOSSIER_SONAR_MODEL (по
умолчанию «sonar»), DOSSIER_VERIFY_TIMEOUT_SEC (таймаут одного запроса,
по умолчанию 45), DOSSIER_VERIFY_DEADLINE_SEC (общий дедлайн, по
умолчанию 240).

Код возврата 1 — есть неподтверждённые утверждения. Это отказ, а не
предупреждение: досье уносят на встречу, и там цена ошибки выше цены
задержки.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.dont_write_bytecode = True  # каталог навыка может быть только для чтения

# Источники, уникальные по своей природе: карьерный трек человека, его
# репозитории, его препринты, его публикации. Второго независимого
# подтверждения у них не бывает и быть не может — требовать его значит
# выбрасывать верные факты. Профиль первого лица здесь и есть первоисточник.
PRIMARY_ONLY_DOMAINS = {
    "linkedin.com", "github.com", "arxiv.org", "scholar.google.com",
    "orcid.org", "researchgate.net", "gitlab.com", "huggingface.co",
    "elibrary.ru", "istina.msu.ru",
}

# Разделы, из которых берутся фактические утверждения. «Анализ» не берём
# намеренно: это помеченный вывод, а не факт, и проверять его как факт —
# смешивать то, что инструкция велит разделять.
# «Одним абзацем» и «Темы» проверяются тоже: в прогоне фраза «в октябре
# 2026 года TIME назвал его человеком года [2]» стояла в «Одним абзацем» —
# самом читаемом разделе — и прошла без проверки (на деле: декабрь 2025,
# и не он один). Свежие поводы в «Темах» — ровно то место, где дата или
# событие выдумываются легче всего. Фразы без номера источника (вопросы,
# советы) не берутся, как и везде.
CLAIM_SECTIONS = ("last_known_role", "summary", "who", "known_for", "topics")

CITE_RE = re.compile(r"\[(\d+(?:\s*[,;–—-]\s*\d+)*)\]")


def cite_numbers(text: str) -> list:
    """Номера источников из «[1]», «[1, 2]», «[1–3]» — в одном списке."""
    out = []
    for group in CITE_RE.findall(str(text or "")):
        for part in re.split(r"\s*[,;]\s*", group):
            m = re.fullmatch(r"(\d+)\s*[–—-]\s*(\d+)", part)
            if m and int(m.group(1)) <= int(m.group(2)) <= int(m.group(1)) + 20:
                out.extend(str(i) for i in range(int(m.group(1)), int(m.group(2)) + 1))
            elif part.strip().isdigit():
                out.append(part.strip())
    return out
SENT_SPLIT = re.compile(r"(?<=[.!?;])\s+|\n+")
# Сокращения, после которых точка — не конец фразы («1969 г. в Тайнане»,
# «Л. Су», «т.е.»). Без этого утверждение резалось на обрубки: обрубок без
# номера источника отбраковывался, а обрубок «Родилась 7 ноября 1969 г.»
# уходил на проверку без места рождения.
ABBR_END = re.compile(
    r"(?:(?<![\w-])(?:г|гг|в|вв|т\.е|т\.д|т\.п|т\.к|др|пр|им|ул|д|стр|см|ср|рис|тыс|млн|млрд|трлн|"
    r"руб|долл|пос|обл|р-н|проф|акад|чл\.-корр|доц|ген|напр|англ|рус|кит|нем|фр|"
    r"inc|ltd|corp|co|dr|mr|mrs|ms|jr|sr|vs|no|st|u\.s|e\.g|i\.e)|(?<![\w-])[A-ZА-ЯЁ])\.$",
    re.I)


def split_sentences(text: str) -> list:
    """Фразы: строки списка отдельно, внутри строки — по концу фразы, не
    разрывая на сокращениях."""
    out = []
    for line in str(text or "").split("\n"):
        merged = []
        for part in re.split(r"(?<=[.!?;])\s+", line):
            if merged and ABBR_END.search(merged[-1]):
                merged[-1] = merged[-1] + " " + part
            else:
                merged.append(part)
        out.extend(merged)
    return out
SONAR_URL = "https://api.perplexity.ai/chat/completions"

# Предела нет и быть не должно: проверяется КАЖДОЕ утверждение. Сначала
# стоял срез на 15 — он молча отсекал хвост, и агент отчитывался «все 15
# подтверждены» при 17 в досье. Потом отказ выше тридцати — но отказ вместо
# проверки это та же непроверенная выдача, только с другой стороны.
#
# Единственная настоящая причина, по которой хотелось ограничить, — время:
# обращения к Sonar шли по очереди, и 17 утверждений съедали две минуты из
# трёх отпущенных скрипту. Правильный ответ на нехватку времени — считать
# параллельно, а не отказываться считать. Восьми потоков хватает на сотню
# утверждений внутри лимита.
VERIFY_WORKERS = 8

# Общий дедлайн проверки. Платформа убивает скрипт на 300 секундах, и убитый
# скрипт не печатает ничего — агент видит обрыв и не знает, что проверено.
# Поэтому свой дедлайн раньше платформенного: не успели — честно говорим,
# что именно не проверено, и кэшируем подтверждённое для повторного вызова.
DEFAULT_DEADLINE_SEC = 240.0
DEFAULT_REQUEST_TIMEOUT_SEC = 45.0
_DEADLINE_AT = [time.time() + DEFAULT_DEADLINE_SEC]


def time_left() -> float:
    return _DEADLINE_AT[0] - time.time()


def env_first(*names: str, default: str = "") -> str:
    for n in names:
        v = (os.environ.get(n) or "").strip()
        if v:
            return v
    return default


def work_dir() -> pathlib.Path:
    """Куда разрешено писать кэш: каталог навыка, иначе задачи, иначе текущий."""
    for env in ("OUROBOROS_SKILL_STATE_DIR", "OUROBOROS_TASK_DRIVE"):
        v = os.environ.get(env)
        if v:
            return pathlib.Path(v)
    return pathlib.Path.cwd()


def task_drive_roots() -> list:
    """Каталоги, где лежат рабочие каталоги задач (``task_drives``).

    Скрипт запускается в каталоге навыка, а агент сохраняет dossier.json в
    каталог своей задачи — и переменной с его адресом в окружении скрипта
    может не быть. Каталог задач ищется рядом с каталогом состояния навыка:
    на стандартной установке оба лежат в одном каталоге данных.
    """
    roots = []
    state = os.environ.get("OUROBOROS_SKILL_STATE_DIR")
    if state:
        for parent in pathlib.Path(state).resolve().parents:
            cand = parent / "task_drives"
            if cand.is_dir():
                roots.append(cand)
                break
    for cand in (pathlib.Path("/data/task_drives"),
                 pathlib.Path.home() / "ouroboros-data" / "data" / "task_drives"):
        if cand.is_dir() and cand not in roots:
            roots.append(cand)
    return roots


FRESH_INPUT_HOURS = 6


CONCURRENT_WINDOW_SEC = 30 * 60
AMBIGUOUS = []  # заполняется find_in_task_drives: файлы параллельных задач


def find_in_task_drives(rel: pathlib.Path):
    """Самый свежий файл с таким относительным путём в каталогах задач.

    Только свежий (до FRESH_INPUT_HOURS): старое досье с тем же именем из
    прошлой задачи не должно подхватиться вместо нынешнего. Если за последние
    полчаса файл с этим именем меняли в НЕСКОЛЬКИХ задачах (параллельные
    досье), угадывать нельзя — возвращается None, а список кладётся в AMBIGUOUS.
    """
    best = None
    recent = []
    AMBIGUOUS.clear()
    now = time.time()
    for root in task_drive_roots():
        try:
            dirs = [d for d in root.iterdir() if d.is_dir()]
        except OSError:
            continue
        for d in dirs:
            f = d / rel
            try:
                if f.is_file():
                    m = f.stat().st_mtime
                    if now - m <= CONCURRENT_WINDOW_SEC:
                        recent.append(f)
                    if now - m <= FRESH_INPUT_HOURS * 3600 and (best is None or m > best[0]):
                        best = (m, f)
            except OSError:
                continue
    if len(recent) > 1:
        AMBIGUOUS.extend(str(f) for f in recent)
        return None
    return best[1] if best else None


def resolve_input(raw: str) -> tuple:
    """Найти JSON досье: как передан, затем в каталоге задачи и навыка, затем
    самый свежий файл с таким именем среди каталогов задач."""
    # Порядок важен. Каталог состояния навыка — общий для всех задач, и файл
    # с тем же именем, оставленный там прошлой задачей (раньше туда писал
    # --fit), подменял текущее досье — в том числе чужое, через дни. Поэтому
    # сначала каталог задачи, а каталог навыка — последним и только свежий.
    p = pathlib.Path(raw).expanduser()
    tried = []
    candidates = [p]
    if not p.is_absolute():
        v = os.environ.get("OUROBOROS_TASK_DRIVE")
        if v:
            candidates.append(pathlib.Path(v) / p)
    for c in candidates:
        tried.append(str(c))
        if c.is_file():
            return c, tried
    if not p.is_absolute():
        found = find_in_task_drives(p)
        roots = ", ".join(str(r) for r in task_drive_roots()) or "каталог задач не найден"
        tried.append(f"<каталоги задач>/*/{p} в {roots} (только файлы свежее {FRESH_INPUT_HOURS} ч)")
        if found is not None:
            return found, tried
        if AMBIGUOUS:
            tried.append("несколько задач меняли файл с этим именем за последние полчаса — "
                         "какой ваш, не угадать: " + "; ".join(AMBIGUOUS[:5]))
            return None, tried
        state = os.environ.get("OUROBOROS_SKILL_STATE_DIR")
        if state:
            c = pathlib.Path(state) / p
            tried.append(f"{c} (только свежее {FRESH_INPUT_HOURS} ч)")
            try:
                if c.is_file() and time.time() - c.stat().st_mtime <= FRESH_INPUT_HOURS * 3600:
                    return c, tried
            except OSError:
                pass
    return None, tried


CACHE_NAME = "verify_cache.json"


def claim_key(claim: dict, srcmap: dict) -> str:
    """Ключ кэша: текст утверждения + адреса его источников.

    Поменялся текст или ссылка — это другое утверждение, и оно проверяется
    заново. Кэшируется только подтверждённое: отказ всегда перепроверяется.
    """
    # Номера [n], регистр, пробелы и пунктуация в ключ не входят, порядок
    # источников — тоже: перенумерация списка источников или запятая не должны
    # отправлять уже подтверждённое утверждение в Sonar заново — повторная
    # проверка того же факта иногда возвращает «ЧАСТИЧНО», и круг правок растёт.
    # Префикс «Имя: » тоже не входит: агент дописывает в name отчество или
    # латиницу — и без этого весь кэш сбрасывался и шёл в Sonar заново.
    text = str(claim.get("text") or "")
    if claim.get("person") and text.startswith(str(claim["person"]) + ": "):
        text = text[len(str(claim["person"])) + 2:]
    text = CITE_RE.sub(" ", text).lower()
    text = re.sub(r"[^\w%$€₽]+", " ", text).strip()
    urls = sorted({str((srcmap.get(str(n)) or {}).get("url") or "").rstrip("/")
                   for n in claim.get("sources") or []})
    raw = json.dumps([claim.get("kind"), text, str(claim.get("value") or "").strip(), urls],
                     ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def load_cache() -> dict:
    try:
        data = json.loads((work_dir() / CACHE_NAME).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


STATUS_NAME = "verify_status.json"


def write_status(status: str, detail: str, src=None, failing=None) -> None:
    """Итог последнего запуска — для render_dossier.py и guide.py status.

    Флаг --unverified разрешён только после настоящего сбоя триангуляции
    (нет ключа, отказ по ключу, сеть). Иначе агент мог решить «ключа нет»,
    не запуская проверку, и собрать досье без неё — так и было в прогоне.
    Список отказов хранится здесь же: после сжатия контекста агент теряет
    вывод проверки, а guide.py status печатает его заново.
    """
    try:
        d = work_dir()
        d.mkdir(parents=True, exist_ok=True)
        (d / STATUS_NAME).write_text(json.dumps({
            "status": status, "detail": detail, "ts": time.time(),
            "file": str(src) if src else "", "failing": failing or [],
        }, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


# Статусы, с которыми утверждение не мешает сборке. «ДОПУЩЕНО (темы)» — частичное
# подтверждение в «Темах на обсуждение»: это зацепки для разговора, а не
# утверждения досье. В 1.1.7 «Темы» проверялись так же строго, как биография, и
# агент в малом контексте не уточнял их, а вырезал: в прогоне на 12 замечаний
# раздел сжался до трёх пунктов. Опровергнутое и числа в «Темах» по-прежнему
# останавливают сборку.
GOOD_STATUSES = ("ПОДТВЕРЖДЕНО", "ПЕРВОИСТОЧНИК", "ПОДТВЕРЖДЕНО (источник не открылся)",
                 "ДОПУЩЕНО (темы)")
SOFT_IN_TOPICS = ("ЧАСТИЧНО", "ОДИН ИСТОЧНИК", "НЕТ ПОДТВЕРЖДЕНИЙ", "НЕЯСНО")


def save_cache(cache: dict) -> None:
    try:
        d = work_dir()
        d.mkdir(parents=True, exist_ok=True)
        tmp = d / (CACHE_NAME + ".tmp")
        tmp.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, d / CACHE_NAME)
    except Exception as exc:  # noqa: BLE001
        print(f"  (кэш не записан: {type(exc).__name__}: {str(exc)[:80]})")

# Слово короче этого в сравнении не участвует: «года», «был», «для» есть
# в любом тексте и подтверждают что угодно.
MIN_TOKEN_LEN = 5
STOPWORDS = {
    "который", "которая", "которые", "также", "более", "менее", "после",
    "перед", "между", "около", "самым", "своей", "своих", "этого", "этой",
}


def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "\n".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def registrable_domain(url: str) -> str:
    """Домен без www и поддоменов: два последних ярлыка.

    Грубо, но для счёта независимости достаточно: example.ru и press.example.ru —
    один источник, а не два. Тонкости вроде co.uk здесь не важны: они дают
    ошибку в сторону строгости, а не наоборот.
    """
    try:
        host = urllib.parse.urlparse(url).netloc.lower().split(":")[0]
    except Exception:  # noqa: BLE001
        return ""
    host = host[4:] if host.startswith("www.") else host
    parts = [p for p in host.split(".") if p]
    if len(parts) >= 3 and parts[-2] in {"co", "com", "gov", "org", "ac", "edu"}:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def normalize_aliases(data: dict) -> dict:
    """Частые описки в именах полей — чиним, а не отказываем.

    В двух живых прогонах подряд агент писал `source_id` вместо `source` в
    figures и `id` вместо `n` в sources и тратил на это по несколько ходов.
    Смысл однозначен, поэтому поле просто переименовывается.
    """
    for s in data.get("sources") or []:
        if isinstance(s, dict) and s.get("n") is None:
            for alt in ("id", "num", "number"):
                if s.get(alt) is not None:
                    s["n"] = s[alt]
                    break
    for f in data.get("figures") or []:
        if isinstance(f, dict) and f.get("source") in (None, ""):
            for alt in ("source_id", "source_n", "src"):
                if f.get(alt) not in (None, ""):
                    f["source"] = f[alt]
                    break
    return data


def sources_by_number(data: dict) -> dict[str, dict]:
    out = {}
    for s in data.get("sources") or []:
        if isinstance(s, dict) and s.get("n") is not None:
            out[str(s["n"])] = s
    return out


def collect_claims(data: dict) -> list[dict]:
    """Числа из figures и фактические фразы со ссылкой — в один список."""
    claims: list[dict] = []
    seen: set[str] = set()
    person = as_text(data.get("name"))
    stated = _stated_figures(data)

    for fig in data.get("figures") or []:
        if not isinstance(fig, dict):
            continue
        value = str(fig.get("value") or "").strip()
        if not value:
            continue
        quote = str(fig.get("quote") or "").strip()
        derived = str(fig.get("derived_from") or "").strip()
        if derived and not quote:
            # Выведенное число проверять внешним поиском нечего: оно и не
            # утверждается как прочитанное. Его страхует пометка «около».
            continue
        if stated is not None and not _figure_stated(value, stated):
            # Число стоит только в «Не подтверждено» (там и место спорному:
            # «200 [1] или 350 [2]») или его уже нет в тексте — запись в figures
            # осталась от прошлой правки. Проверять его как утверждение нельзя:
            # иначе оно возвращает отказ за то, чего досье не утверждает.
            continue
        text = f"{person}: {quote or value}" if person else (quote or value)
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        claims.append({
            "kind": "число",
            "text": text,
            "value": value,
            "person": person,
            "sources": [str(fig.get("source"))] if fig.get("source") else [],
        })

    for section in CLAIM_SECTIONS:
        for sentence in split_sentences(as_text(data.get(section))):
            sentence = sentence.strip(" -•\t")
            if "[Анализ]" in sentence:
                continue  # помеченный вывод, не факт: прогноз Sonar не подтвердит
            refs = cite_numbers(sentence)
            if not refs or len(sentence) < 25:
                continue
            bare = CITE_RE.sub("", sentence).strip()
            if bare.endswith("?"):
                continue  # вопрос к собеседнику в «Темах» — не утверждение
            key = bare.lower()
            if key in seen:
                continue
            seen.add(key)
            claims.append({
                "kind": "факт",
                "text": f"{person}: {bare}" if person else bare,
                "value": "",
                "person": person,
                "sources": refs,
                "section": section,
            })
    return claims


def _stated_figures(data: dict):
    """Числа, которые досье УТВЕРЖДАЕТ: все разделы, кроме «Не подтверждено»."""
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import render_dossier as rd  # noqa: E402
        frags = [frag for key, frag in rd._numeric_claims(data) if key != "unconfirmed"]
        return [rd._norm_figure(f) for f in frags]
    except Exception:  # noqa: BLE001 — без сборщика проверяем все записи, как раньше
        return None


def _figure_stated(value: str, stated: list) -> bool:
    try:
        import render_dossier as rd  # noqa: E402
        v = rd._norm_figure(value)
    except Exception:  # noqa: BLE001
        return True
    return any(v and (v in s or s in v) for s in stated)


def primary_only(claim: dict, srcmap: dict[str, dict]) -> str:
    """Если утверждение опирается ТОЛЬКО на уникальный первоисточник — его имя."""
    doms = []
    for n in claim.get("sources") or []:
        url = str((srcmap.get(str(n)) or {}).get("url") or "")
        dom = registrable_domain(url)
        if not dom:
            return ""
        doms.append(dom)
    if not doms:
        return ""
    if all(d in PRIMARY_ONLY_DOMAINS for d in doms):
        return ", ".join(sorted(set(doms)))
    # Правило 1 методики: факт от первого лица (интервью, личный сайт) — один
    # источник допустим, если в тексте так и сказано: «по его словам».
    text = str(claim.get("text") or "").lower()
    first_person = all("перв" in str((srcmap.get(str(n)) or {}).get("strength") or "").lower()
                       or "first" in str((srcmap.get(str(n)) or {}).get("strength") or "").lower()
                       for n in claim.get("sources") or [])
    if first_person and re.search(r"со слов|по (его|её|ее|собственным) словам|по словам", text):
        return "первое лицо: " + ", ".join(sorted(set(doms)))
    return ""


def numeric_core(value: str) -> str:
    """Числовое ядро величины: «1 млн+» → «1 млн», «около 47 лет» → «47»."""
    v = str(value or "").lower().replace(" ", " ")
    # Десятичная запятая — не разделитель: «79,1 млн» → «79.1 млн», иначе
    # ниже она превратилась бы в пробел и число «79 1» не нашлось бы нигде.
    v = re.sub(r"(\d),(\d{1,2})(?!\d)", r"\1.\2", v)
    m = re.search(r"\d[\d\s.,]*\s*(?:трлн|млн|млрд|тыс\w*|%|миллион\w*|миллиард\w*|триллион\w*)?", v)
    if not m:
        return ""
    core = re.sub(r"[\s,]+", " ", m.group(0)).strip(" .")
    return core


# --- Одно число в разных языках --------------------------------------------------
# Досье пишется по-русски, а источники чаще английские: «$10 млрд» в тексте и
# «$10 billion» на странице — одна величина. Прежняя проверка сравнивала
# строки, и в живом прогоне агент потратил два десятка ходов, подгоняя
# цитаты. Теперь числа сравниваются как числа: значение × шкала, проценты
# отдельно. Совпадение точное — «$3 трлн» не подтверждается «$3.1 trillion».
_SCALE_WORDS = [
    (r"трлн|триллион\w*|trillion\w*|tn(?![a-z])", 10**12),
    (r"млрд|миллиард\w*|billion\w*|bn(?![a-z])", 10**9),
    (r"млн|миллион\w*|million\w*|mln(?![a-z])|mn(?![a-z])", 10**6),
    (r"тыс\.?|тысяч\w*|thousand\w*", 10**3),
]
_SCALE_LETTER = {"t": 10**12, "b": 10**9, "m": 10**6, "k": 10**3}
_AMOUNT_RE = re.compile(
    r"(?<![\d.,])(\d{1,3}(?:[   ']\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)*)"
    r"(?:\s*(%|percent\b|per cent\b|процент\w*|" + "|".join(p for p, _ in _SCALE_WORDS) + r")"
    r"|([tbmkTBMK])(?![A-Za-zА-Яа-я]))?",
    re.I)


def _parse_number(raw: str):
    s = re.sub(r"[   ']", "", raw)
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", "") if re.fullmatch(r"\d{1,3}(,\d{3})+", s) else s.replace(",", ".")
    elif s.count(".") > 1:
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def amounts(text: str) -> list:
    """Все величины в тексте как (число с учётом шкалы, это_процент)."""
    out = []
    for m in _AMOUNT_RE.finditer(str(text or "")):
        num = _parse_number(m.group(1))
        if num is None:
            continue
        word = (m.group(2) or "").lower()
        letter = (m.group(3) or "").lower()
        pct = word.startswith(("%", "percent", "per cent", "процент"))
        mult = _SCALE_LETTER.get(letter, 1)
        for pat, factor in _SCALE_WORDS:
            if word and re.fullmatch(pat, word):
                mult = factor
                break
        out.append((num * mult, pct))
    return out


_EN_UNITS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen".split())}
_EN_TENS = {w: (i + 2) * 10 for i, w in enumerate(
    "twenty thirty forty fifty sixty seventy eighty ninety".split())}
_RU_WORDS = [
    (r"дв[аеу]х?|двум[яи]?|две", 2), (r"тр[её]х|тр[её]м|тремя|три", 3),
    (r"четыр[её]х|четыр[её]м|четырьмя|четыре", 4), (r"пят[иь]ю?|пять", 5),
    (r"шест[иь]ю?|шесть", 6), (r"сем[иь]ю?|семь", 7), (r"восьм[иь]ю?|восемь", 8),
    (r"девят[иь]ю?|девять", 9), (r"десят[иь]ю?|десять", 10),
    (r"одиннадцат\w*", 11), (r"двенадцат\w*", 12), (r"тринадцат\w*", 13),
    (r"четырнадцат\w*", 14), (r"пятнадцат\w*", 15), (r"шестнадцат\w*", 16),
    (r"семнадцат\w*", 17), (r"восемнадцат\w*", 18), (r"девятнадцат\w*", 19),
    (r"двадцат\w*", 20), (r"тридцат\w*", 30), (r"сорок\w*", 40),
    (r"пят[ьи]десят\w*", 50), (r"шест[ьи]десят\w*", 60), (r"сем[ьи]десят\w*", 70),
    (r"восемьдесят\w*|восьмидесят\w*", 80), (r"девяност\w*", 90),
]


def _word_value(word: str):
    w = word.lower()
    if w in _EN_UNITS:
        return _EN_UNITS[w]
    if w in _EN_TENS:
        return _EN_TENS[w]
    for pat, val in _RU_WORDS:
        if re.fullmatch(pat, w):
            return val
    return None


def words_to_digits(text: str) -> str:
    """«seven» → «7», «twenty-one» → «21», «семи» → «7»: числа словами в цитате
    источника. В прогоне цитата «seven» не совпала со значением «7»."""
    tokens = re.split(r"([A-Za-zА-Яа-яЁё]+)", str(text or ""))
    out, i = [], 0
    while i < len(tokens):
        tok = tokens[i]
        val = _word_value(tok) if tok and tok[0].isalpha() else None
        if val is None:
            out.append(tok)
            i += 1
            continue
        # Составное: «twenty-one», «двадцать семь».
        if val >= 20 and val % 10 == 0 and i + 2 < len(tokens) and tokens[i + 1] in ("-", " "):
            nxt = _word_value(tokens[i + 2])
            if nxt is not None and 0 < nxt < 10:
                out.append(str(val + nxt))
                i += 3
                continue
        out.append(str(val))
        i += 1
    return "".join(out)


def figure_in_text(value: str, text: str) -> bool:
    """Есть ли величина из value в тексте — независимо от языка и записи."""
    wanted = amounts(value)
    if not wanted:
        return False
    have = amounts(text)
    spelled = words_to_digits(text)
    if spelled != str(text or ""):
        have = have + amounts(spelled)
    for num, pct in wanted:
        if not any(p == pct and abs(n - num) <= max(abs(num), 1) * 1e-9 for n, p in have):
            return False
    return True


def literal_present(core: str, haystack: str) -> bool:
    """Стоит ли число в тексте доказательства ДОСЛОВНО.

    Проверка нарочно тупая и не зависит от суждения модели. Именно она даёт
    гарантию: Sonar может назвать фразу подтверждённой, проглотив цифру, —
    здесь цифра либо есть в источниках, либо её нет.
    """
    if not core:
        return False
    hay = re.sub(r"[\s, ]+", " ", str(haystack or "").lower())
    if core in hay:
        return True
    if figure_in_text(core, haystack):
        return True
    # «1 млн» и «1 000 000» — одно и то же число, записанное по-разному.
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(млн|млрд|тыс\w*|миллион\w*|миллиард\w*)?$", core)
    if not m:
        return False
    num, scale = m.group(1), (m.group(2) or "")
    mult = {"млн": 10**6, "миллион": 10**6, "млрд": 10**9, "миллиард": 10**9, "тыс": 10**3}
    factor = next((v for k, v in mult.items() if scale.startswith(k)), 1)
    try:
        full = int(float(num) * factor)
    except (TypeError, ValueError):
        return False
    if factor == 1:
        return False
    plain = str(full)
    grouped = f"{full:,}".replace(",", " ")
    return plain in hay.replace(" ", "") or grouped in hay


_TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.I | re.S)
_ANY_TAG = re.compile(r"<[^>]+>")


def fetch_source_text(url: str, timeout: float = 20.0) -> tuple[str, str]:
    """Текст страницы источника. Возвращает (текст, причина отказа)."""
    timeout = min(timeout, time_left())
    if timeout < 3:
        return "", "не хватило времени до дедлайна"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
            "Accept-Language": "ru,en;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(1_500_000)
            ctype = str(resp.headers.get("Content-Type") or "").lower()
            charset = resp.headers.get_content_charset() or ""
    except Exception as exc:  # noqa: BLE001
        return "", f"{type(exc).__name__}: {str(exc)[:90]}"
    # PDF (годовой отчёт, раскрытие) — сжатый поток, текста в нём не найти:
    # честное «не проверить», а не «числа на странице нет».
    if raw[:5] == b"%PDF-" or "application/pdf" in ctype:
        return "", "PDF — текст страницы не читается"
    html_text = ""
    for enc in [charset, "utf-8", "cp1251"]:
        if not enc:
            continue
        try:
            html_text = raw.decode(enc)
            break
        except (LookupError, UnicodeDecodeError):
            continue
    if not html_text:
        html_text = raw.decode("utf-8", "replace")
    import html as _html
    text = _html.unescape(_ANY_TAG.sub(" ", _TAG_RE.sub(" ", html_text)))
    return re.sub(r"\s+", " ", text), ""


def check_cited_source(claim: dict, srcmap: dict[str, dict]) -> tuple[str, str]:
    """Стоит ли число в САМОМ источнике, на который ссылается досье.

    Самый сильный слой проверки и единственный, который устанавливает
    атрибуцию. Поиск по интернету её не устанавливает: «1 млн» встречается в
    статьях про популярные инвестиционные сервисы, и триангуляция по этому совпадению дважды из
    пяти признавала выдумку подтверждённой. Вопрос не «есть ли такое число
    где-нибудь», а «есть ли оно ТАМ, куда поставлена ссылка».

    Возвращает (вердикт, пояснение): ЕСТЬ / НЕТ / НЕ ПРОВЕРИТЬ.
    """
    core = numeric_core(claim.get("value") or "")
    if not core:
        return "НЕ ПРОВЕРИТЬ", "величину не разобрать"
    urls = [str((srcmap.get(str(n)) or {}).get("url") or "") for n in claim.get("sources") or []]
    urls = [u for u in urls if u.startswith("http")]
    if not urls:
        return "НЕ ПРОВЕРИТЬ", "у источника нет адреса"
    reasons = []
    # Первые две ссылки, а не все: утверждение обычно опирается на один-два
    # источника, а каждая загрузка страницы — это секунды. Проверять пятую
    # ссылку смысла мало, а общий бюджет скрипта она съедает заметно.
    for url in urls[:2]:
        text, err = fetch_source_text(url)
        if err:
            reasons.append(f"{registrable_domain(url)}: {err}")
            continue
        if literal_present(core, text):
            return "ЕСТЬ", f"число найдено на {registrable_domain(url)}"
        reasons.append(f"{registrable_domain(url)}: числа на странице нет")
    if all("числа на странице нет" in r for r in reasons) and reasons:
        return "НЕТ", "; ".join(reasons)
    return "НЕ ПРОВЕРИТЬ", "; ".join(reasons) or "страницу не открыть"


def significant_tokens(text: str) -> set[str]:
    """Слова, по которым можно узнать утверждение среди чужих текстов."""
    words = re.findall(r"[А-Яа-яЁёA-Za-z][А-Яа-яЁёA-Za-z-]+", str(text or "").lower())
    return {w for w in words if len(w) >= MIN_TOKEN_LEN and w not in STOPWORDS}


def supporting_domains(results: list, claim_text: str, figure: str) -> list[str]:
    """Домены, которые НА САМОМ ДЕЛЕ подтверждают утверждение.

    Раньше считались все домены из выдачи, и порог «не меньше двух» не
    проверял ничего: на утверждение про диплом приходило 15 доменов, среди
    которых книжный магазин, музей вычислительной техники и Газпром. Пятнадцать
    нерелевантных проходили порог так же, как два релевантных, и вся тяжесть
    решения ложилась на суждение модели.

    Теперь домен засчитывается, только если в его сниппете есть чем
    подтвердить: для числа — само число, для факта — минимум два значимых
    слова утверждения. Это и есть перекрёстная проверка: повторение в разных
    независимых источниках, а не совпадение в поисковой выдаче.
    """
    core = numeric_core(figure) if figure else ""
    # Имя человека из префикса «Имя: …» есть в любом сниппете о нём и ничего
    # не подтверждает — в счёт совпадений оно не идёт.
    name, sep, body = claim_text.partition(": ")
    tokens = cross_tokens(body) - cross_tokens(name) if sep else cross_tokens(claim_text)
    years = _years(body if sep else claim_text)
    good: dict[str, str] = {}
    for r in results:
        if not isinstance(r, dict):
            continue
        dom = registrable_domain(str(r.get("url") or ""))
        if not dom or dom in good:
            continue
        snippet = f"{r.get('title') or ''} {r.get('snippet') or ''}"
        if not snippet.strip():
            continue
        if core:
            if literal_present(core, snippet):
                good[dom] = "число в сниппете"
            continue
        hit = tokens & cross_tokens(snippet)
        if years:
            # Год в утверждении обязан стоять и в источнике: иначе «CEO AMD»
            # подтверждало бы и верный, и неверный год назначения.
            if not (years & hit) or len(hit - years) < 1:
                continue
        elif len(hit) < 2:
            continue
        good[dom] = ", ".join(sorted(hit)[:3])
    return sorted(good)


# --- Русское утверждение против английского сниппета -----------------------------
# Утверждения пишутся по-русски, а сниппеты источников чаще английские. Раньше
# совпадение искалось по русским словам от пяти букв, и «CEO AMD с октября
# 2014 года» при десятке англоязычных подтверждений получало «0 доменов»:
# CEO и AMD короче порога, «октября» не равно «October», год не считался.
# Верный факт уезжал в «Не подтверждено». Теперь в сравнение идут латинские
# аббревиатуры и названия от трёх букв, годы и месяцы на обоих языках.
_MONTHS_RU_EN = {
    "январ": "january", "феврал": "february", "март": "march", "апрел": "april",
    "мая": "may", "май": "may", "июн": "june", "июл": "july", "август": "august",
    "сентябр": "september", "октябр": "october", "ноябр": "november", "декабр": "december",
}
_LATIN_STOP = {"the", "and", "for", "with", "from", "that", "this", "was", "has", "his", "her",
               "its", "are", "were", "into", "inc", "ltd", "com", "www", "http", "https"}


def _years(text: str) -> set:
    return set(re.findall(r"(?<!\d)(1[89]\d\d|20\d\d)(?!\d)", str(text or "")))


def cross_tokens(text: str) -> set:
    s = str(text or "")
    out = set(significant_tokens(s))
    low = s.lower()
    out |= {w for w in re.findall(r"[a-z][a-z0-9&-]{2,}", low) if w not in _LATIN_STOP}
    out |= _years(s)
    # Русские аббревиатуры (МГИМО, ВШЭ, МТС, ВТБ): короче порога слов, но в
    # утверждениях о вузе и работодателе это и есть суть.
    out |= {w.lower() for w in re.findall(r"(?<![А-Яа-яЁё])[А-ЯЁ]{2,6}(?![А-Яа-яЁё])", s)}
    for word in re.findall(r"[а-яё]+", low):
        for stem, en in _MONTHS_RU_EN.items():
            if word.startswith(stem):
                out.add(en)
                break
    return out


def ask_sonar(claim_text: str, *, key: str, model: str, timeout: float,
              figure: str = "") -> dict:
    """Один проверочный вопрос к Sonar. Возвращает вердикт, домены и доказательства."""
    if figure:
        # Для числа спрашиваем ПРО ЧИСЛО, а не про смысл фразы. Разница
        # решающая: на вопрос «верно ли, что она отвечает за аналитику для
        # 1 млн+ частных инвесторов» Sonar дважды из трёх отвечал
        # «подтверждено» — он подтверждал аналитику, а величину проглатывал.
        prompt = (
            "Проверь ТОЛЬКО числовую величину в утверждении, не общий смысл. "
            "Если источники подтверждают суть, но НЕ называют именно это число — "
            "это НЕ ПОДТВЕРЖДЕНО. Ответь СТРОГО в формате:\n"
            "ВЕРДИКТ: ПОДТВЕРЖДЕНО | НЕ ПОДТВЕРЖДЕНО | ЧАСТИЧНО\n"
            "ПОЧЕМУ: одно предложение\n\n"
            f"Проверяемая величина: {figure}\n"
            f"Утверждение целиком: {claim_text}"
        )
    else:
        prompt = (
            "Проверь утверждение по открытым источникам. Ответь СТРОГО в формате:\n"
            "ВЕРДИКТ: ПОДТВЕРЖДЕНО | НЕ ПОДТВЕРЖДЕНО | ЧАСТИЧНО\n"
            "ПОЧЕМУ: одно предложение\n\n"
            f"Утверждение: {claim_text}"
        )
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Ты проверяешь факты. Отвечай на русском, кратко, только по источникам."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }
    last = ""
    for attempt in range(3):
        per_try = min(timeout, time_left())
        if per_try < 5:
            last = last or "не хватило времени до дедлайна"
            return {"verdict": "НЕ ПРОВЕРЕНО (время)", "why": last, "domains": [], "urls": [],
                    "evidence": ""}
        # Запрос создаётся заново на каждой попытке: тело уже отправленного
        # объекта прочитано, и повтор ушёл бы пустым.
        req = urllib.request.Request(
            SONAR_URL, data=json.dumps(body).encode(),
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=per_try) as resp:
                payload = json.load(resp)
            break
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "ignore")[:160]
            if exc.code in (401, 403):
                raise SystemExit(
                    f"[!] Sonar отказал по ключу (HTTP {exc.code}): {detail}\n"
                    f"    Проверьте PERPLEXITY_API_KEY. Без него триангуляция невозможна,\n"
                    f"    и собирать досье нельзя: непроверенные факты уйдут владельцу.")
            last = f"HTTP {exc.code}: {detail}"
            if exc.code == 429 and attempt < 2 and time_left() > 20:
                time.sleep(5 * (attempt + 1))  # лимит запросов: подождать дольше
                continue
        except Exception as exc:  # noqa: BLE001
            last = f"{type(exc).__name__}: {str(exc)[:120]}"
        if attempt < 2 and time_left() > 10:
            time.sleep(2)
    else:
        return {"verdict": "СБОЙ", "why": last, "domains": [], "urls": [], "evidence": ""}

    answer = str((payload.get("choices") or [{}])[0].get("message", {}).get("content") or "")
    results = payload.get("search_results") or []
    urls = [str(r.get("url") or "") for r in results if r.get("url")]
    for u in payload.get("citations") or []:
        if isinstance(u, str):
            urls.append(u)
        elif isinstance(u, dict) and u.get("url"):
            urls.append(str(u["url"]))
    domains = sorted({d for d in (registrable_domain(u) for u in urls) if d})
    # ВАЖНО: ответ модели в доказательства НЕ входит. Sonar пересказывает
    # проверяемое утверждение вместе с числом, и число начинает подтверждать
    # само себя: на выдуманном «1 млн+» так проходило два прогона из пяти.
    # Доказательство — только текст, пришедший из найденных источников.
    evidence = " ".join(
        [str(r.get("snippet") or "") for r in results]
        + [str(r.get("title") or "") for r in results]
    )

    upper = answer.upper()
    # Вердикт — из строки «ВЕРДИКТ: …», а не из всего ответа: слово «частично»
    # в пояснении превращало «ПОДТВЕРЖДЕНО» в «ЧАСТИЧНО» и запускало круг правок.
    found = [m for line in upper.splitlines() if "|" not in line
             for m in re.finditer(r"ВЕРДИКТ\W*\s*(НЕ\s+ПОДТВЕРЖДЕНО|ЧАСТИЧНО|ПОДТВЕРЖДЕНО)", line)]
    mv = found[-1] if found else None
    if mv:
        verdict = "НЕ ПОДТВЕРЖДЕНО" if mv.group(1).startswith("НЕ") else mv.group(1)
    elif "НЕ ПОДТВЕРЖДЕНО" in upper:
        verdict = "НЕ ПОДТВЕРЖДЕНО"
    elif "ЧАСТИЧНО" in upper:
        verdict = "ЧАСТИЧНО"
    elif "ПОДТВЕРЖДЕНО" in upper:
        verdict = "ПОДТВЕРЖДЕНО"
    else:
        verdict = "НЕЯСНО"
    why = ""
    m = re.search(r"ПОЧЕМУ:\s*(.+)", answer)
    if m:
        why = " ".join(m.group(1).split())[:160]
    return {"verdict": verdict, "why": why,
            "domains": supporting_domains(results, claim_text, figure),
            "all_domains": domains, "urls": urls[:6], "evidence": evidence}


MAX_ROWS_PRINTED = 150


def preflight_sonar(timeout: float = 8.0) -> str:
    """Дешёвая проверка, что API Sonar вообще достижим — до запуска потоков.

    Без неё сетевой сбой проявлялся восемью параллельными таймаутами по 45
    секунд. Любой HTTP-ответ (даже 401/404/405) означает, что сеть есть;
    ошибка соединения — что нет. Возвращает пустую строку или причину.
    """
    req = urllib.request.Request("https://api.perplexity.ai/", method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout):
            return ""
    except urllib.error.HTTPError:
        return ""
    except Exception as exc:  # noqa: BLE001
        return f"{type(exc).__name__}: {str(exc)[:120]}"


def main() -> int:
    args = [a for a in sys.argv[1:]]
    if "--explain" in args:
        print(__doc__)
        return 0
    dry = "--dry-run" in args
    fresh = "--fresh" in args
    paths = [a for a in args if not a.startswith("--") and not a.isdigit()]
    if not paths:
        return _die("[!] Укажите файл досье: verify_facts.py <абсолютный путь>/dossier.json")
    src, tried = resolve_input(paths[0])
    if src is None:
        return _die(f"[!] Нет файла {paths[0]}. Искал:\n    " + "\n    ".join(tried)
                    + "\n    Передайте АБСОЛЮТНЫЙ путь к dossier.json в каталоге задачи.")
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _die(f"[!] {src} — не JSON: {exc}")
    if not isinstance(data, dict):
        return _die(f"[!] {src}: ожидается JSON-объект досье (см. render_dossier.py --schema)")
    normalize_aliases(data)

    srcmap = sources_by_number(data)
    claims = collect_claims(data)
    if not claims:
        # Честное короткое досье «данных мало» — законный исход: всё спорное
        # уже в «Не подтверждено». Отказ здесь не оставлял пути его сдать.
        print("Проверять нечего: в утверждающих разделах нет ни чисел, ни фраз со ссылкой.")
        print("Это допустимо только для досье «данных мало»: полнота данных прямо говорит,")
        print("что сведений нет, а всё найденное — в «Не подтверждено».")
        write_status("ok", "утверждений нет — досье «данных мало»", src)
        print("\nГОДНО: проверять нечего. Можно рендерить.")
        return 0

    # Сначала бесплатная проверка формы (объём, числа, ссылки, частное):
    # если сборка всё равно откажет, платить за Sonar рано — после правки
    # формулировки изменятся и уйдут на проверку снова.
    if not dry:
        try:
            sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
            import render_dossier as rd  # noqa: E402
            form = rd.validate(data)
        except Exception:  # noqa: BLE001
            form = []
        if form:
            print(f"НЕ ГОДИТСЯ ещё до проверки фактов — замечаний по форме: {len(form)}.")
            print("Исправьте ВСЕ одним write_file и вызовите verify_facts.py снова (Sonar ещё не тратился).")
            for item in form:
                print(f"  [!] {item}")
            print("Превышен объём — render_dossier.py --fit <файл> срежет необязательное сам. Текст досье не "
                  "перед глазами — read_file того же файла.")
            write_status("form_failed", f"замечаний по форме: {len(form)}", src,
                         [{"status": "форма", "text": i[:160], "why": ""} for i in form[:12]])
            return 1
        # Тонкое досье при богатом материале — главный дефект прогонов в малом
        # контексте: агент писал коротко, а потом при каждом замечании ещё и
        # вырезал. Один раз — до платной проверки — показываем недобор и даём
        # дописать по брифу. Повторный вызов проверяет как есть: это подсказка,
        # а не условие сборки.
        try:
            short = rd.underfill(data)
        except Exception:  # noqa: BLE001
            short = []
        first = _first_look(src, data)  # отмечаем первый вызов в любом случае
        if short and first:
            print("ДОРАБОТАЙТЕ ОБЪЁМ — материала найдено больше, чем вошло в досье (подсказка, один раз):")
            for item in short:
                print(f"  [i] {item}")
            print("Допишите по брифу (search.py --brief \"<Имя Фамилия>\" — если его уже нет перед глазами),")
            print("одним write_file, и вызовите verify_facts.py снова. Добавлять нечего — просто вызовите снова:")
            print("второй вызов проверит факты как есть.")
            write_status("underfill", "досье короче материала — показан недобор", src)
            return 1

    print(f"Файл: {src}")
    print(f"Утверждений к проверке: {len(claims)}")
    print("Проверяется КАЖДОЕ. Предела нет, пропусков нет.")
    print()

    if dry:
        for i, c in enumerate(claims, 1):
            exempt = primary_only(c, srcmap)
            mark = f"первоисточник {exempt}" if exempt else "идёт в Sonar"
            print(f"  {i:2d}. [{c['kind']}] {c['text'][:96]}")
            print(f"      источники {c['sources'] or '—'} · {mark}")
        print("\nЭто план. Обращений к сети не было.")
        return 0

    key = (os.environ.get("PERPLEXITY_API_KEY") or "").strip()
    if not key:
        write_status("no_key", "PERPLEXITY_API_KEY не передан скрипту", src)
        return _die(
            "[!] PERPLEXITY_API_KEY не передан скрипту.\n"
            "    Навык объявляет его в env_from_settings; проверьте, что ключ есть в\n"
            "    настройках и владелец выдал доступ в карточке навыка. Без ключа\n"
            "    триангуляции нет, а без триангуляции досье собирать нельзя.")
    model = env_first("DOSSIER_SONAR_MODEL", "OUROBOROS_SONAR_MODEL", default="sonar")
    try:
        timeout = float(env_first("DOSSIER_VERIFY_TIMEOUT_SEC", "OUROBOROS_VERIFY_TIMEOUT_SEC",
                                  default=str(DEFAULT_REQUEST_TIMEOUT_SEC)))
        deadline = float(env_first("DOSSIER_VERIFY_DEADLINE_SEC", default=str(DEFAULT_DEADLINE_SEC)))
    except ValueError:
        timeout, deadline = DEFAULT_REQUEST_TIMEOUT_SEC, DEFAULT_DEADLINE_SEC
    # Дедлайн не может быть позже платформенного предела в 300 секунд.
    _DEADLINE_AT[0] = time.time() + max(30.0, min(deadline, 270.0))

    GOOD = GOOD_STATUSES
    cache = {} if fresh else load_cache()

    reason = preflight_sonar()
    if reason:
        write_status("network", f"api.perplexity.ai недоступен: {reason}", src)
        return _die(
            f"[!] API Sonar (api.perplexity.ai) недоступен: {reason}\n"
            "    Проверить факты нечем — досье не отдаётся. Повторите позже или\n"
            "    проверьте сетевой доступ навыка (разрешение net).")

    import threading
    cache_lock = threading.Lock()

    def remember(claim: dict, outcome: tuple) -> tuple:
        # Подтверждённое сохраняется сразу, а не в конце: если платформа
        # оборвёт скрипт, повторный вызов не начнёт с нуля.
        if outcome[0] in GOOD:
            with cache_lock:
                cache[claim_key(claim, srcmap)] = {"status": outcome[0], "domains": outcome[1],
                                                   "text": claim["text"][:200]}
                save_cache(cache)
        return outcome

    def verify_one(claim: dict) -> tuple:
        """Проверка одного утверждения. Возвращает (статус, домены, пояснение)."""
        exempt = primary_only(claim, srcmap)
        if exempt:
            return "ПЕРВОИСТОЧНИК", [exempt], f"уникальный источник {exempt}"
        ck = claim_key(claim, srcmap)
        hit = cache.get(ck)
        if isinstance(hit, dict) and hit.get("status") in GOOD:
            return hit["status"], list(hit.get("domains") or []), "из кэша прошлой проверки"
        if time_left() < 8:
            return "НЕ ПРОВЕРЕНО (время)", [], "не хватило времени до дедлайна — повторите вызов"
        figure = claim.get("value") or ""
        res = ask_sonar(claim["text"], key=key, model=model, timeout=timeout, figure=figure)
        if res["verdict"] == "НЕ ПРОВЕРЕНО (время)":
            return res["verdict"], [], res["why"]
        doms = res["domains"]
        ok = res["verdict"] == "ПОДТВЕРЖДЕНО" and len(doms) >= 2
        status = "ПОДТВЕРЖДЕНО" if ok else res["verdict"]
        if res["verdict"] == "ПОДТВЕРЖДЕНО" and len(doms) < 2:
            # Ноль и один — разные факты, и называть их одинаково нечестно:
            # «один источник» при нуле подтверждений вводит в заблуждение
            # ровно там, где нужна точность.
            status = "ОДИН ИСТОЧНИК" if doms else "НЕТ ПОДТВЕРЖДЕНИЙ"
        # Вердикт модели — мнение, и оно гуляет: на выдуманном «1 млн+» Sonar
        # дважды из трёх отвечал «подтверждено», подтверждая суть фразы и
        # проглатывая величину. Поэтому для чисел последнее слово за тупой
        # сверкой с САМОЙ цитируемой страницей.
        if figure:
            cited, why_cited = check_cited_source(claim, srcmap)
            if cited == "НЕТ":
                return "ЧИСЛА НЕТ В ЦИТИРУЕМОМ ИСТОЧНИКЕ", doms, why_cited
            if cited == "НЕ ПРОВЕРИТЬ":
                core = numeric_core(figure)
                if core and not literal_present(core, res.get("evidence", "")):
                    return "ЧИСЛА НЕТ В НАЙДЕННЫХ ИСТОЧНИКАХ", doms, res["why"]
                if ok:
                    return "ПОДТВЕРЖДЕНО (источник не открылся)", doms, res["why"]
        if claim.get("section") == "topics" and status in SOFT_IN_TOPICS:
            return "ДОПУЩЕНО (темы)", doms, f"{status.lower()}: {res['why']}".strip(": ")
        return status, doms, res["why"]

    def safe_verify(claim: dict) -> tuple:
        # Ошибка в одном утверждении не должна ронять проверку остальных и
        # тем более выглядеть как «всё прошло».
        try:
            return remember(claim, verify_one(claim))
        except SystemExit:
            raise
        except Exception as exc:  # noqa: BLE001
            return "СБОЙ", [], f"{type(exc).__name__}: {str(exc)[:100]}"

    # Считаем параллельно. Последовательный проход упирался в лимит скрипта на
    # полутора десятках утверждений — и это была единственная причина, по
    # которой хотелось ограничить их число. Ограничивать проверку нельзя,
    # ускорить её можно.
    from concurrent.futures import ThreadPoolExecutor

    workers = max(1, min(VERIFY_WORKERS, len(claims)))
    started = time.time()
    pool = ThreadPoolExecutor(max_workers=workers)
    try:
        # Ожидание каждого результата ограничено общим дедлайном (с запасом на
        # уже идущий запрос): зависший поток — например, на разрешении имени
        # до сетевого таймаута — не держит скрипт до убийства платформой.
        from concurrent.futures import TimeoutError as _FutTimeout
        futures = [pool.submit(safe_verify, c) for c in claims]
        outcomes = []
        for fut in futures:
            try:
                outcomes.append(fut.result(timeout=max(1.0, time_left() + 15)))
            except _FutTimeout:
                outcomes.append(("НЕ ПРОВЕРЕНО (время)", [],
                                 "не уложились в дедлайн — повторите тот же вызов"))
    except BaseException as exc:
        if isinstance(exc, SystemExit) and "ключу" in str(exc):
            write_status("auth", str(exc).splitlines()[0][:200], src)
        # Прерывание (SIGTERM/KeyboardInterrupt): не ждём зависшие запросы.
        try:
            pool.shutdown(wait=False, cancel_futures=True)  # Python 3.9+
        except TypeError:
            pool.shutdown(wait=False)  # Python 3.8: без отмены очереди
        save_cache(cache)
        raise
    # Не ждём отставшие потоки: их итог уже записан как «не проверено», а
    # подтверждённое сохранено в кэш по ходу.
    try:
        pool.shutdown(wait=False, cancel_futures=True)  # Python 3.9+
    except TypeError:
        pool.shutdown(wait=False)

    rows, failed, timed_out = [], 0, 0
    counts: dict = {}
    for claim, (status, doms, why) in zip(claims, outcomes):
        counts[status] = counts.get(status, 0) + 1
        if status in GOOD:
            cache[claim_key(claim, srcmap)] = {"status": status, "domains": doms,
                                               "text": claim["text"][:200]}
        else:
            failed += 1
            if status == "НЕ ПРОВЕРЕНО (время)":
                timed_out += 1
        rows.append((claim, status, doms, why))
    save_cache(cache)
    # Вывод короткий намеренно. Отказ скрипта движок помечает «⚠️» и такие
    # ответы не сжимает — они остаются в контексте до конца задачи. Полная
    # таблица на 20 утверждений там лишь вытесняла найденное; печатаем только
    # итог и то, что надо исправить.
    soft = counts.get("ДОПУЩЕНО (темы)", 0)
    tally = (f"подтверждено {counts.get('ПОДТВЕРЖДЕНО', 0) + counts.get('ПОДТВЕРЖДЕНО (источник не открылся)', 0)}, "
             f"первоисточник {counts.get('ПЕРВОИСТОЧНИК', 0)}"
             + (f", допущено в «Темах» {soft}" if soft else ""))
    print(f"Проверено {len(claims) - timed_out} из {len(claims)} за {time.time() - started:.0f} с: {tally}.")
    if failed:
        print()
        if timed_out:
            print(f"НЕ ГОДИТСЯ — проверка не завершена: {timed_out} утверждений не успели. Подтверждённое "
                  f"сохранено; повторите ТОТ ЖЕ вызов — проверится только остаток.")
        print(f"НЕ ГОДИТСЯ: {failed} из {len(claims)} без подтверждения. Исправьте ВСЕ пункты одним "
              f"write_file и вызовите снова (подтверждённое в кэше):")
        failing = []
        for claim, status, doms, why in rows:
            if status in GOOD:
                continue
            short_text = claim["text"].split(": ", 1)[-1] if claim.get("person") else claim["text"]
            failing.append({"status": status, "text": short_text[:160], "why": why[:160] if why else ""})
            print(f"  [{status}] «{short_text[:110]}»")
            if why and status not in ("НЕ ПРОВЕРЕНО (время)",):
                print(f"     Sonar: {why[:150]}")
            if status == "НЕ ПРОВЕРЕНО (время)":
                print("     → повторите вызов: проверка продолжится с этого места.")
            elif status == "СБОЙ":
                print("     → сбой запроса, а не опровержение: повторите ТОТ ЖЕ вызов, текст не меняйте.")
            elif claim["kind"] == "число":
                print("     → уберите число (фраза остаётся без него) или запишите так, как в цитируемом источнике.")
            elif status == "ЧАСТИЧНО":
                print("     → поправьте по пояснению Sonar, если оно прямо называет верное (дату, должность);"
                      " иначе уберите спорную часть.")
            elif status == "ОДИН ИСТОЧНИК":
                print("     → один вопрос search.py за вторым независимым источником — или коротко в «Не подтверждено»;"
                      " слова самого человека — «по его/её словам» и strength «первое лицо».")
            else:
                print("     → уберите или коротко перенесите в «Не подтверждено».")
        print("Правила правки: верную версию берите только из пояснения Sonar или брифа; новых фактов взамен не")
        print("дописывайте — каждый проверяется заново. Текст досье не перед глазами — read_file того же файла.")
        room = _unconfirmed_room(data)
        if room:
            used, limit = room
            print(f"«Не подтверждено» сейчас {used} из {limit} знаков — переносите по 5–10 слов с номером источника.")
        rounds = _count_round(src, data)
        if rounds >= 3:
            print(f"Это уже {rounds}-й круг проверки этого досье: перенесите ВСЁ оставшееся спорное в «Не "
                  f"подтверждено» как есть и запустите проверку последний раз.")
        bad = [(status, why) for _c, status, _d, why in rows if status not in GOOD]
        # «Сеть» (а с ней и --unverified) — только если ВСЕ запросы упали на
        # соединении. Ответ сервера с ошибкой (429, 5xx) — временный сбой:
        # повторить, а не собирать без проверки.
        if bad and all(st == "СБОЙ" and not str(w).startswith("HTTP ") for st, w in bad) \
                and len(bad) == len(rows):
            write_status("network", "все запросы к Sonar упали на соединении", src, failing)
        else:
            write_status("claims_failed", f"{failed} из {len(claims)} без подтверждения", src, failing)
        return 1

    notes = [(c, w) for c, st, _d, w in rows if st == "ДОПУЩЕНО (темы)"]
    for claim, why in notes[:3]:
        short_text = claim["text"].split(": ", 1)[-1]
        print(f"[i] «Темы»: «{short_text[:80]}» — {why[:110]}. Сборку не останавливает.")
    write_status("ok", f"все {len(claims)} утверждений прошли проверку", src)
    print(f"ГОДНО: все {len(claims)} утверждений прошли проверку. Дальше: render_dossier.py "
          f"<этот файл> \"Досье — <Фамилия Имя> — <ГГГГ-ММ-ДД>.docx\", затем send_file и «ТЕКСТ ДЛЯ ЧАТА» как есть.")
    return 0


def _unconfirmed_room(data: dict):
    """(занято, лимит) раздела «Не подтверждено» — по правилам сборщика."""
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import render_dossier as rd  # noqa: E402
        return len(as_text(data.get("unconfirmed"))), int(rd.limits_for(data)["unconfirmed"])
    except Exception:  # noqa: BLE001 — подсказка необязательна
        return None


def _first_look(src, data: dict) -> bool:
    """Первый ли раз за 2 часа это досье приходит на проверку (для подсказки
    о недоборе: она показывается один раз и больше не останавливает)."""
    path = work_dir() / "underfill_seen.json"
    key = f"{src}|{as_text(data.get('name'))}"
    now = time.time()
    try:
        seen = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(seen, dict):
            seen = {}
    except Exception:  # noqa: BLE001
        seen = {}
    seen = {k: t for k, t in seen.items() if now - float(t) < 2 * 3600}
    first = key not in seen
    seen[key] = now
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(seen), encoding="utf-8")
    except OSError:
        pass
    return first


def _count_round(src, data: dict) -> int:
    """Сколько раз за 2 часа проверка этого досье заканчивалась отказом."""
    path = work_dir() / "verify_rounds.json"
    key = f"{src}|{as_text(data.get('name'))}"
    now = time.time()
    try:
        rounds = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rounds, dict):
            rounds = {}
    except Exception:  # noqa: BLE001
        rounds = {}
    stamps = [t for t in rounds.get(key, []) if now - float(t) < 2 * 3600] + [now]
    rounds = {k: v for k, v in rounds.items() if k == key or any(now - float(t) < 2 * 3600 for t in v)}
    rounds[key] = stamps
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rounds), encoding="utf-8")
    except OSError:
        pass
    return len(stamps)


def _die(message: str) -> int:
    """Отказ печатаем в stderr, а не в stdout.

    Stdout — это результат проверки, его модель читает как отчёт. Сообщение
    о том, что проверка вообще не началась, в отчёт попадать не должно:
    иначе «нет ключа» выглядит как строка отчёта, а не как срыв запуска.
    """
    print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
