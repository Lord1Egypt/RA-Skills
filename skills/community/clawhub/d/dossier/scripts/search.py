#!/usr/bin/env python3
"""Поиск в интернете через Perplexity Sonar — основной инструмент сбора досье.

    search.py --wave1 "<Имя Фамилия>" [--org "<организация>"] [--latin "<Name Surname>"]
                         волна 1: личность и якоря (8 вопросов) — сначала она
    search.py --deep  "<Имя Фамилия>" [--org …] [--latin …]
                         волны 2–4 одним вызовом (24 вопроса): прошлое, связи,
                         свежая повестка и спорное
    search.py "<Имя>: вопрос 1" ["<Имя>: вопрос 2" ... до 8]
                         свои вопросы — что волны не закрыли (имя — в каждом)
    search.py --brief "<Имя Фамилия>"
                         БРИФ для текста: всё найденное про человека сжато,
                         с единой нумерацией источников и правилами записи JSON
    search.py --log [<Имя>]   сколько запросов уже сделано
    (--wave2, --wave3, --wave4 по отдельности тоже работают)

Почему вывод короткий, а полные ответы — в файле. В установке с малым
контекстом движок сжимает историю задачи, как только она перерастает порог,
и при сжатии от каждого старого ответа инструмента остаётся пересказ его
первых 2,5 тыс. знаков. Волна с полными ответами (30–35 тыс. знаков) сама
запускала это сжатие, и к моменту, когда агент садился писать досье, найденное
уже было пересказано в три строки — досье выходили тонкими. Теперь полные
ответы Sonar пишутся в research.jsonl рабочего каталога навыка, в чат идёт
выжимка, а перед записью досье «--brief» возвращает всё найденное одним
свежим блоком — его сжатие ещё не коснулось.

Каждый запрос пишется ещё и в search_log.jsonl: по нему сборка проверяет, что
поиск шёл через Sonar и был про этого человека.

Настройки: PERPLEXITY_API_KEY (обязателен), DOSSIER_SONAR_MODEL (по умолчанию
«sonar»), DOSSIER_SEARCH_TIMEOUT_SEC (по умолчанию 60).
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

sys.dont_write_bytecode = True

SONAR_URL = "https://api.perplexity.ai/chat/completions"
MAX_QUERIES = 8          # свои вопросы — до восьми за вызов, как в методике
LOG_NAME = "search_log.jsonl"
RESEARCH_NAME = "research.jsonl"
RESEARCH_MAX_BYTES = 6_000_000
RESEARCH_KEEP_DAYS = 3
SEARCH_WINDOW_HOURS = 12           # то же окно, что у сборки
DEADLINE_SEC = 250.0               # платформа убивает скрипт на 300 с
WORKERS = 8

# Сколько знаков ответа показывать в чате. Полный ответ — в research.jsonl.
SHOW_CHARS = {"wave1": 700, "deep": 230, "custom": 520, "wave": 420}
# Бриф: общий объём текста ответов и рамки на один ответ.
BRIEF_TEXT_CHARS = 17_000
BRIEF_MIN_PER = 300
BRIEF_MAX_PER = 900
BRIEF_MAX_SOURCES = 45

_DEADLINE_AT = [time.time() + DEADLINE_SEC]


def time_left() -> float:
    return _DEADLINE_AT[0] - time.time()


def work_dir() -> pathlib.Path:
    for env in ("OUROBOROS_SKILL_STATE_DIR", "OUROBOROS_TASK_DRIVE"):
        v = os.environ.get(env)
        if v:
            return pathlib.Path(v)
    return pathlib.Path.cwd()


def env_first(*names: str, default: str = "") -> str:
    for n in names:
        v = (os.environ.get(n) or "").strip()
        if v:
            return v
    return default


# Вопросы волн — слои поискового справочника и «поиск по прошлому».
# Формулировки — вопросами: Sonar понимает вопрос целиком и отвечает связно.
# Формулировки латиницей: для иностранцев англоязычные источники полнее.
WAVES = {
    "wave1": [
        "{name}{org} — кто это? Последняя известная должность и организация, с какого года — по официальным источникам",
        "{name}{org}: биография — полное имя, год и место рождения, гражданство",
        "{name}{org}: образование — вуз, факультет, годы, учёные степени",
        "{name}{org}: хронология карьеры — все работодатели и должности по годам",
        "{latin}{org_en}: LinkedIn profile, current role and career history",
        "{name}{org}: интервью, выступления, авторские колонки от первого лица",
        "{name}{org}: награды, звания, членство в советах директоров и ассоциациях",
        "Есть ли другие публичные люди с именем {name} (тёзки, однофамильцы) и чем они отличаются от {name}{org}?",
    ],
    "wave2": [
        "{name}{org}: что было до текущей должности — предыдущие компании, роли, годы, промежутки в карьере",
        "{name}{org}: ключевые проекты, сделки, запуски, публикации или патенты — с датами",
        "{name}{org}: публично заявленные позиции по отрасли, финансам, технологиям и искусственному интеллекту",
        "{name}{org}: стиль управления и принятия решений — свидетельства коллег и собственные слова",
        "{name}{org}: публичные конфликты, судебные споры, санкции, критика — со ссылками на документы",
        "{name}{org}: главные новости за последние 12 месяцев",
        "{latin}{org_en}: interviews and public statements 2025–2026",
        "{latin}{org_en}: early career, education and previous employers",
    ],
    # Волна 3 — обход графа связей: каждый именной объект — свой вопрос.
    "wave3": [
        "{name}{org}: сооснователи, партнёры, ключевые соратники и наставники — кто и в какие годы",
        "{name}{org}: компании, в которые инвестировал или где входит в совет директоров — с годами",
        "{name}{org}: крупнейшие сделки, слияния и поглощения с его участием — контрагенты, суммы, даты",
        "{name}{org}: книги, статьи, патенты, соавторы — с годами",
        "{name}{org}: выступления на конференциях и форумах за последние два года — где, о чём",
        "{name}{org}: кто публично критикует или оппонирует — суть и источники",
        "{latin}{org_en}: business partners, co-founders, board seats and major deals",
        "{latin}{org_en}: investments and portfolio companies with dates",
    ],
    # Волна 4 — свежая повестка (для «Тем на обсуждение») и перепроверка спорного.
    "wave4": [
        "{name}{org}: что публично заявлял за последние три месяца — темы, цитаты, даты",
        "{name}{org}: текущие приоритеты и стратегия организации на ближайшие годы",
        "{name}{org}: ближайшие события — сделки, отчётность, выступления, запуски",
        "{name}{org}: в чём источники расходятся — дата и место рождения, образование, даты назначений",
        "{name}{org}: какие цифры о нём и его компании чаще всего цитируют и насколько они точны",
        "{name}{org}: личные профессиональные интересы и темы, которые сам поднимает в интервью",
        "{latin}{org_en}: latest news and statements, last 3 months",
        "{latin}{org_en}: strategy, priorities and outlook 2026",
    ],
}
WAVE_FLAGS = tuple("--" + k for k in WAVES) + ("--deep",)
GROUP_TITLES = {
    "wave1": "Личность и якоря",
    "wave2": "Прошлое и проекты",
    "wave3": "Связи, сделки, выступления",
    "wave4": "Свежая повестка и спорное",
    "custom": "Свои вопросы",
}


def wave_queries(kind: str, name: str, org: str = "", latin: str = "") -> list:
    org_ru = f" ({org})" if org else ""
    org_en = f", {org}" if org else ""
    latin = latin or name
    kinds = ["wave2", "wave3", "wave4"] if kind == "deep" else [kind]
    out = []
    for k in kinds:
        out += [(k, q.format(name=name, org=org_ru, org_en=org_en, latin=latin)) for q in WAVES[k]]
    return out


PERSON = [""]  # имя из волны — в журнал: сборка и бриф узнают по нему, про кого поиск
ARGS = {"name": "", "org": "", "latin": ""}


def parse_wave_args(args: list):
    """--wave1 "Имя" [--org "…"] [--latin "…"] → (вид, [(волна, вопрос)]) или (None, ошибка)."""
    kind = args[0].lstrip("-")
    rest = args[1:]
    opts = {"org": "", "latin": ""}
    name_parts = []
    i = 0
    while i < len(rest):
        a = rest[i]
        if a in ("--org", "--latin"):
            if i + 1 < len(rest):
                opts[a[2:]] = rest[i + 1].strip()
            i += 2
            continue
        if a.startswith(("--org=", "--latin=")):
            k, _, v = a[2:].partition("=")
            opts[k] = v.strip()
            i += 1
            continue
        if a.startswith("--"):
            # Придуманный флаг ушёл бы в Sonar частью имени — восемь платных
            # запросов вида «Иван Петров --lang en (Пример) — кто это?».
            return None, (f"Флага {a} нет. Волна принимает только --org и --latin: "
                          f"search.py --{kind} \"Имя Фамилия\" --org \"…\" --latin \"…\"")
        name_parts.append(a)
        i += 1
    name = " ".join(x.strip() for x in name_parts if x.strip())
    if not name:
        return None, f"После --{kind} нужно имя человека: search.py --{kind} \"Имя Фамилия\" [--org \"…\"] [--latin \"…\"]"
    PERSON[0] = " / ".join(x for x in (name, opts["latin"]) if x)
    ARGS.update(name=name, org=opts["org"], latin=opts["latin"])
    return kind, wave_queries(kind, name, opts["org"], opts["latin"])


def _append_jsonl(name: str, record: dict) -> None:
    try:
        d = work_dir()
        d.mkdir(parents=True, exist_ok=True)
        with (d / name).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"  (файл {name} не записан: {exc})")


def _prune_research() -> None:
    """research.jsonl растёт на ~100 КБ за досье — держим последние дни."""
    path = work_dir() / RESEARCH_NAME
    try:
        if path.stat().st_size < RESEARCH_MAX_BYTES:
            return
        cutoff = time.time() - RESEARCH_KEEP_DAYS * 86400
        keep = []
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                if _ts(json.loads(line).get("ts")) >= cutoff:
                    keep.append(line)
            except (ValueError, json.JSONDecodeError):
                continue
        tmp = path.with_suffix(".tmp")
        tmp.write_text("\n".join(keep) + ("\n" if keep else ""), encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        pass


def _ts(value) -> float:
    try:
        return time.mktime(time.strptime(str(value), "%Y-%m-%dT%H:%M:%S"))
    except (ValueError, TypeError, OverflowError):
        return 0.0


def ask(query: str, key: str, model: str, timeout: float) -> dict:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Ты помогаешь собрать деловое досье. Отвечай по-русски, "
                                          "только фактами из источников, с датами. Если источники "
                                          "расходятся — укажи обе версии."},
            {"role": "user", "content": query},
        ],
        "temperature": 0,
    }
    last = ""
    for attempt in range(3):
        per_try = min(timeout, time_left() - 3)
        if per_try < 5:
            return {"ok": False, "error": last or "не хватило времени до предела скрипта — повторите вызов"}
        req = urllib.request.Request(
            SONAR_URL, data=json.dumps(body).encode(),
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=per_try) as resp:
                payload = json.load(resp)
            answer = str((payload.get("choices") or [{}])[0].get("message", {}).get("content") or "")
            answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.S).strip()
            results = []
            for r in payload.get("search_results") or []:
                if isinstance(r, dict) and r.get("url"):
                    # Дата публикации — для «свежести данных» и даты источника в досье.
                    date = str(r.get("date") or r.get("last_updated") or "")[:10]
                    results.append({"title": str(r.get("title") or "")[:120], "url": str(r["url"]), "date": date})
            # Номера [k] в ответе указывают на citations[k-1] — порядок важен.
            citations = [u if isinstance(u, str) else str((u or {}).get("url") or "")
                         for u in (payload.get("citations") or [])]
            citations = [u for u in citations if u] or [r["url"] for r in results]
            return {"ok": True, "answer": answer, "results": results, "citations": citations}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "ignore")[:160]
            if exc.code in (401, 403):
                return {"ok": False, "fatal": True, "error": f"Sonar отказал по ключу (HTTP {exc.code}): {detail}"}
            last = f"HTTP {exc.code}: {detail}"
            if exc.code == 429 and attempt < 2 and time_left() > 30:
                time.sleep(5 * (attempt + 1))
                continue
        except Exception as exc:  # noqa: BLE001
            last = f"{type(exc).__name__}: {str(exc)[:120]}"
        if attempt < 2 and time_left() > 15:
            time.sleep(2)
    return {"ok": False, "error": last}


# --- Чтение журнала и брифа ---------------------------------------------------

def _rd():
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import render_dossier  # noqa: E402 — только помощники сопоставления имени
    return render_dossier


def _about(text: str, name: str) -> bool:
    """Про этого человека: фамилия в любом падеже/написании или все части имени."""
    if not name.strip():
        return True
    try:
        return _rd()._about_person(text, {"name": name})
    except Exception:  # noqa: BLE001 — без сборщика: простое вхождение фамилии
        parts = [p for p in re.findall(r"[A-Za-zА-Яа-яЁё]+", name) if len(p) > 2]
        return any(p.lower()[:5] in str(text or "").lower() for p in parts[-1:])


def read_research(name: str = "", hours: float = SEARCH_WINDOW_HOURS) -> list:
    path = work_dir() / RESEARCH_NAME
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    now = time.time()
    out = []
    for line in lines:
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not rec.get("ok") or now - _ts(rec.get("ts")) > hours * 3600:
            continue
        if name and not (_about(rec.get("person") or "", name) or _about(rec.get("query") or "", name)):
            continue
        out.append(rec)
    # Повтор того же вопроса — берём последний ответ.
    latest = {}
    for rec in out:
        latest[rec.get("query")] = rec
    return sorted(latest.values(), key=lambda r: _ts(r.get("ts")))


def person_material(name: str) -> tuple:
    """(ответов Sonar про человека за окно, разных адресов в них) — для подсказок."""
    recs = read_research(name)
    urls = {u for r in recs for u in (r.get("citations") or [])}
    return len(recs), len(urls)


_MD_RE = [(re.compile(r"^\s*#{1,6}\s*", re.M), ""), (re.compile(r"\*\*|__"), ""),
          (re.compile(r"^\s*[-*]\s+", re.M), "• "), (re.compile(r"\s*\n+\s*"), " "),
          (re.compile(r"[ \t]{2,}"), " ")]


def clean(text: str) -> str:
    s = str(text or "")
    for rx, rep in _MD_RE:
        s = rx.sub(rep, s)
    return s.strip()


def cut(text: str, limit: int) -> str:
    """Обрезка по границе фразы, не посреди слова."""
    if len(text) <= limit:
        return text
    head = text[:limit]
    stop = max(head.rfind(". "), head.rfind("; "), head.rfind("! "), head.rfind("? "))
    if stop > limit * 0.55:
        return head[:stop + 1] + " …"
    return head.rsplit(" ", 1)[0] + " …"


def _domain(url: str) -> str:
    host = re.sub(r"^(?:[a-z]+://)?(?:www\.)?", "", str(url or "").lower()).split("/")[0]
    return host


def show_answer(answer: str, limit: int) -> str:
    """Выжимка для чата: без разметки и без номеров ссылок (они ведут в никуда)."""
    return cut(re.sub(r"\s*\[\d{1,2}\]", "", clean(answer)), limit)


def brief(name: str) -> int:
    recs = read_research(name)
    if not recs:
        print(f"[!] В research.jsonl нет ответов про «{name}» за {SEARCH_WINDOW_HOURS} ч.")
        print("    Сначала поиск: search.py --wave1 … и search.py --deep … (имя — в каждом вопросе).")
        return 1
    per = max(BRIEF_MIN_PER, min(BRIEF_MAX_PER, BRIEF_TEXT_CHARS // max(1, len(recs))))
    registry: dict = {}
    meta: dict = {}
    for rec in recs:
        for r in rec.get("results") or []:
            meta.setdefault(r.get("url"), r)

    def gnum(url: str) -> int:
        if url not in registry:
            registry[url] = len(registry) + 1
        return registry[url]

    groups: dict = {}
    for rec in recs:
        cits = rec.get("citations") or []
        text = cut(clean(rec.get("answer")), per)

        def remap(m, cits=cits):
            k = int(m.group(1))
            if 1 <= k <= len(cits) and (len(registry) < BRIEF_MAX_SOURCES or cits[k - 1] in registry):
                return f"[{gnum(cits[k - 1])}]"
            return ""
        text = re.sub(r"\[(\d{1,2})\]", remap, text)
        groups.setdefault(rec.get("wave") or "custom", []).append((rec.get("query"), text))

    print(f"БРИФ ДЛЯ ДОСЬЕ: {name} — {len(recs)} ответов Sonar, {len(registry)} источников.")
    print("Пишите досье ПО НЕМУ, а не по памяти и не по прошлым досье из чата. Номера [n] —")
    print("единые для всего брифа: ставьте их в текст как есть, сборка сама перенумерует.\n")
    order = ["wave1", "wave2", "wave3", "wave4", "custom"]
    for g in order + [k for k in groups if k not in order]:
        if g not in groups:
            continue
        print(f"== {GROUP_TITLES.get(g, g)}")
        for q, text in groups[g]:
            label = re.sub(r"^.*?[:—]\s*", "", str(q))[:70] or str(q)[:70]
            print(f"• {label}: {text}")
        print()
    print("== Источники (n · сайт · дата · заголовок · адрес)")
    for url, n in sorted(registry.items(), key=lambda kv: kv[1]):
        m = meta.get(url) or {}
        title = re.sub(r"\s+", " ", str(m.get("title") or "")).strip()[:70]
        print(f"[{n}] {_domain(url)} · {m.get('date') or 'дата ?'} · {title} · {url}")
    print()
    print(WRITE_CARD.format(name=name))
    return 0


WRITE_CARD = """КАК ЗАПИСАТЬ dossier.json — сразу, одним write_file(root="task_drive", path="dossier.json"):
• Источники — только из списка выше. В тексте номер из брифа ([7]); в "sources" — те же
  {{"n": 7, "url", "title", "date", "strength"}} для каждого номера из текста (сильный | средний |
  слабый | первое лицо; энциклопедии — не «сильный»). Лишние и порядок сборка поправит сама.
• "summary" «Одним абзацем»: 3–4 предложения, 350–500 знаков — кто сейчас, путь, чем
  примечателен, почему важен для встречи. Факты с [n]; связка без номера, без «самый/крупнейший».
• "who" «Кто он/она» (до 600): «Последнее известное место работы — …, по состоянию на <дата> [n]»,
  путь до этого, образование, возраст (выведенный — «около»). Номер у КАЖДОЙ фразы; «;» — тоже граница.
• "known_for" (до 900): 3–4 пункта — факт, год, [n]. Оценки — в "analysis".
• "topics" (до 1500): 4–5 пунктов по 200–300 знаков: тема → почему уместна (зацепка из биографии
  с [n]) → на что выйти в разговоре. Есть в запросе или памяти, для кого досье ("owner_context")
  или контекст встречи ("meeting_context") — темы на их стыке с опытом человека.
• "avoid" (до 300): конкретика или «специфических тем под запретом не выявлено». Семья, здоровье,
  утраты — только словами «личная жизнь и семья».
• "unconfirmed" (до 400): 5–10 слов на пункт, с [n]; расхождения — обе версии («1990 [3] или 1992 [5]»).
• "analysis" (до 400): «[Анализ] …» с опорой на [n]. "completeness": «Данных достаточно: N/10 якорей …»
  или «Данных мало: …». Ещё: "name", "gender" ('m'/'f'), "last_known_role", "as_of", "prepared".
• "figures": каждое число от двух цифр в тексте (кроме годов и дней месяца) — {{"value", "source",
  "quote": дословно из источника}} или {{"value", "derived_from"}} и «около» в тексте.
• Объём — в полную силу лимитов: в прошлых прогонах главным дефектом были тонкие разделы.
Дальше: verify_facts.py dossier.json — он сам проверит и форму. Потеряли нить — guide.py status."""


def show_log(name: str = "") -> int:
    path = work_dir() / LOG_NAME
    try:
        lines = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    except (OSError, json.JSONDecodeError):
        lines = []
    now = time.time()
    recent = [x for x in lines if x.get("ok") and now - _ts(x.get("ts")) <= SEARCH_WINDOW_HOURS * 3600]
    if name:
        mine = [x for x in recent if _about(x.get("person") or "", name) or _about(x.get("query") or "", name)]
        print(f"Успешных запросов Sonar про «{name}» за {SEARCH_WINDOW_HOURS} ч: {len(mine)} "
              f"(всего в журнале за это время: {len(recent)}).")
    else:
        print(f"Успешных запросов Sonar за {SEARCH_WINDOW_HOURS} ч: {len(recent)} "
              f"(за всё время в журнале: {len(lines)}). Журнал: {path}")
    return 0


def _run(queries: list, key: str, model: str, timeout: float) -> list:
    """Параллельно, до восьми сразу; ожидание ограничено пределом скрипта."""
    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutTimeout
    pool = ThreadPoolExecutor(max_workers=min(WORKERS, len(queries)))
    futures = [pool.submit(ask, q, key, model, timeout) for _k, q in queries]
    results = []
    for fut in futures:
        try:
            results.append(fut.result(timeout=max(1.0, time_left() + 5)))
        except FutTimeout:
            results.append({"ok": False, "error": "не уложились в предел скрипта — повторите вызов"})
        except Exception as exc:  # noqa: BLE001
            results.append({"ok": False, "error": f"{type(exc).__name__}: {str(exc)[:100]}"})
    try:
        pool.shutdown(wait=False, cancel_futures=True)
    except TypeError:
        pool.shutdown(wait=False)
    return results


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 64
    if args[0] == "--log":
        return show_log(" ".join(args[1:]).strip())
    if args[0] == "--brief":
        name = " ".join(a for a in args[1:] if not a.startswith("--")).strip()
        if not name:
            print('[!] Укажите имя: search.py --brief "Имя Фамилия"')
            return 64
        return brief(name)
    mode = "custom"
    if args[0] in WAVE_FLAGS:
        kind, queries = parse_wave_args(args)
        if kind is None:
            print(f"[!] {queries}")
            return 64
        mode = kind
    elif args[0].startswith("--"):
        # Незнакомый флаг не уходит в Sonar вопросом.
        print(f"[!] Флага {args[0]} нет. Есть: --wave1, --deep, --brief, --log (и --wave2..4); "
              f"свои вопросы — без флагов: search.py \"<Имя>: вопрос 1\" … (до 8).")
        return 64
    else:
        queries = [("custom", a.strip()) for a in args if a.strip()][:MAX_QUERIES]
        if len([a for a in args if a.strip()]) > MAX_QUERIES:
            print(f"[!] За один вызов — не больше {MAX_QUERIES} своих вопросов; лишние отброшены.")

    key = (os.environ.get("PERPLEXITY_API_KEY") or "").strip()
    if not key:
        print("[!] PERPLEXITY_API_KEY не передан скрипту. Проверьте ключ в настройках и доступ "
              "к нему в карточке навыка.", file=sys.stderr)
        return 1
    model = env_first("DOSSIER_SONAR_MODEL", "OUROBOROS_SONAR_MODEL", default="sonar")
    try:
        timeout = float(env_first("DOSSIER_SEARCH_TIMEOUT_SEC", default="60"))
    except ValueError:
        timeout = 60.0

    started = time.time()
    results = _run(queries, key, model, timeout)
    _prune_research()

    failed, fatal = 0, False
    show = SHOW_CHARS.get(mode, SHOW_CHARS["wave"]) if mode in SHOW_CHARS else SHOW_CHARS["wave"]
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    for i, ((wave, q), res) in enumerate(zip(queries, results), 1):
        ok = bool(res.get("ok"))
        cits = res.get("citations") or [r.get("url") for r in res.get("results") or [] if r.get("url")] \
            or [s[1] for s in res.get("sources") or [] if len(s) > 1]
        _append_jsonl(LOG_NAME, {"ts": stamp, "query": q, "ok": ok, "sources": len(cits), "model": model,
                                 "wave": wave, "person": PERSON[0],
                                 # Адреса источников Sonar — сборка сверяет с ними источники досье.
                                 "urls": cits[:15]})
        if ok:
            _append_jsonl(RESEARCH_NAME, {"ts": stamp, "ok": True, "person": PERSON[0], "wave": wave,
                                          "query": q, "answer": res.get("answer", ""),
                                          "citations": cits, "results": res.get("results") or []})
        if not ok:
            failed += 1
            fatal = fatal or bool(res.get("fatal"))
            print(f"{i}. [!] {q[:90]} — ошибка: {res.get('error')}")
            continue
        doms = []
        for u in cits:
            d = _domain(u)
            if d and d not in doms:
                doms.append(d)
        src = f" [{', '.join(doms[:4])}{f' +{len(doms) - 4}' if len(doms) > 4 else ''}]" if doms else ""
        if mode == "deep":
            label = re.sub(r"^.*?[:—]\s*", "", q)[:48]
            print(f"{i:2d}. {label}: {show_answer(res.get('answer'), show)}{src}")
        else:
            print(f"\n=== {i}. {q}")
            print(show_answer(res.get("answer"), show) + src)

    n_ok = len(queries) - failed
    print(f"\n{len(queries)} запросов, успешно {n_ok}, ошибок {failed}, {time.time() - started:.0f} с. "
          f"Полные ответы сохранены (research.jsonl) — их соберёт «--brief».")
    if fatal:
        print("Проверьте PERPLEXITY_API_KEY — без него поиск и триангуляция невозможны.")
    if failed:
        print("Упавшие запросы — повторите ТОТ ЖЕ вызов (сохранённое не пропадёт); встроенный поиск не замена.")
    name = ARGS["name"] or ""
    flags = (f' --org "{ARGS["org"]}"' if ARGS["org"] else "") + (f' --latin "{ARGS["latin"]}"' if ARGS["latin"] else "")
    if mode == "wave1":
        print("\nЛИЧНОСТЬ: закрепите человека двумя признаками (организация и должность, страна, год рождения,")
        print("написание имени). Есть тёзки — дальше только тот, кто совпал по двум признакам; сомнение —")
        print("в первую строку полноты данных. Ошиблись организацией — повторите волну 1 с верной --org.")
        print(f'Дальше: search.py --deep "{name}"{flags}   (24 вопроса: прошлое, связи, свежая повестка)')
    elif mode == "deep":
        print("\nДальше: незакрытые якоря (образование, годы, прежние работодатели, текущая роль) и каждый")
        print("новый работодатель/сделку/вуз — своими вопросами, до 8 за вызов, с именем в каждом:")
        print(f'  search.py "{name or "<Имя>"}: …" "{name or "<Имя>"}: …"')
        print(f'Затем: search.py --brief "{name or "<Имя Фамилия>"}" — и сразу пишите dossier.json по брифу.')
    elif mode in ("wave2", "wave3"):
        nxt = "wave3" if mode == "wave2" else "wave4"
        print(f'\nДальше: search.py --{nxt} "{name}"{flags} — или сразу все волны 2–4 одним вызовом --deep.')
    else:
        print('\nДальше: при пробелах — ещё вопросы (до 8, с именем); затем search.py --brief "<Имя Фамилия>".')
    print("Ищите только через search.py: встроенный поиск агента здесь не Sonar, и источники из него сборка не примет.")
    return 1 if failed == len(queries) else 0


if __name__ == "__main__":
    sys.exit(main())
