# -*- coding: utf-8 -*-
"""_factcheck.py — сверка утверждений резюме с текстом документа (без модели, без сети).

Скрипт не решает, верен ли факт: это делает модель. Скрипт
  1) делит резюме на проверяемые утверждения (заголовок, преамбула, тезисы и предложения выводов,
     предложения обоснований вопросов) — claims();
  2) собирает к каждому утверждению доказательную базу: факты реестра из fact_ids и фрагменты страниц
     документа вокруг его чисел и цитат — packet();
  3) принимает отчёт модели и проверяет, что он опирается на документ: каждая цитата-доказательство
     дословно есть на указанной странице, каждое число утверждения (и исправления) есть в цитатах — validate().

Нормализованный текст подтверждённых утверждений хранится в out/fit_state.json (verified): если модель
потом меняет предложение, оно снова уходит на проверку; неизменённое повторно не проверяется.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import _core as core

WINDOW = 210            # знаков по обе стороны от найденного числа или цитаты
MAX_EXCERPTS = 3        # фрагментов страниц на одно утверждение
QUOTE_MIN, QUOTE_MAX = 12, 300
VERDICTS = ("ok", "fix", "unsupported")


# ----------------------------------------------------------------- нормализация
_TRANS = str.maketrans({"\u00a0": " ", "\u2009": " ", "\u202f": " ", "\u2007": " ", "\u2002": " ", "\u2003": " ",
                        "\u2013": "-", "\u2014": "-", "\u2011": "-", "\u2212": "-", "\u2010": "-",
                        "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u00ab": '"', "\u00bb": '"',
                        "\u2018": "'", "\u2019": "'", "\u00ad": None, "ё": "е", "Ё": "Е"})


def norm(text: str) -> str:
    """Для сравнения текста: регистр, пробелы, тире, кавычки, переносы строк и слов."""
    t = unicodedata.normalize("NFKC", text or "").translate(_TRANS)      # NFKC: лигатуры «ﬁ» → «fi»
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)          # перенос слова по слогам в PDF
    t = re.sub(r"(\w)-\s+(?=[a-zа-я])", r"\1", t)          # тот же перенос, когда строки уже склеены пробелом
    t = re.sub(r"\s+", " ", t)
    return t.strip().lower()


def _loose(text: str) -> str:
    """Ещё грубее: без пунктуации, кроме цифр, букв, % и $ — для поиска цитаты в тексте страницы."""
    return re.sub(r"[^\w%$.,]+", " ", norm(text)).strip()


MAX_GAP = 14            # слов «чужой» колонки, которые PDF может вклинить между словами цитаты
# Пропущенные без многоточия слова не должны менять смысл цитаты: отрицание, оговорка, модальность,
# условие, приблизительность, сравнение и любые числа. Если такое слово попало в пропуск — цитата не дословная.
MEANING_WORDS = frozenset("""
not no never none nor neither without unless except excluding only t cannot hardly barely rarely seldom
may might could would should must if whether unlikely likely possibly potentially potential perhaps
expect expected expects forecast forecasts estimate estimated estimates projected plan plans planned
proposed propose consider considering approximately about around almost nearly roughly up over under
below above less more than fewer least most excl ex pro forma adjusted
не нет ни без кроме исключая лишь только может могут мог могла могли могло бы если ли либо
около примерно приблизительно почти порядка до свыше более менее больше меньше 
планирует планируют планируется планировал прогноз прогнозирует ожидается ожидает ожидают оценка
оценке оценивается предлагается предлагает рассматривает изучает возможно вероятно скорее
""".split())


def _gap_changes_meaning(skipped: list[str]) -> bool:
    return any(w in MEANING_WORDS or any(ch.isdigit() for ch in w) for w in skipped)


def _tokens(text: str) -> list[str]:
    return re.findall(r"[\w%$]+(?:[.,]\d+)*", norm(text))


def quote_on_page(quote: str, page_txt: str) -> bool:
    """Дословно — с точностью до пробелов, переносов, лигатур и вставок соседней колонки: слова цитаты идут
    на странице в том же порядке, между соседними — не больше MAX_GAP чужих слов, всего пропущено не больше
    слов, чем в цитате, и среди пропущенных нет слов, меняющих смысл (MEANING_WORDS, числа). Пропуск, который
    меняет смысл, допустим только явно — многоточием: оно делит цитату на части, каждая ищется так же и по порядку."""
    q, p = norm(quote), norm(page_txt)
    if q and q in p:
        return True
    lq, lp = _loose(quote), _loose(page_txt)
    if lq and lq in lp:
        return True
    page = _tokens(page_txt)
    pos = 0
    for part in re.split(r"\.\.\.|…", quote):
        qt = _tokens(part)
        if not qt:
            continue
        found = None
        for start in range(pos, len(page)):
            if page[start] != qt[0]:
                continue
            i, ok, skipped = start, True, 0
            for tok in qt[1:]:
                nxt = next((k for k in range(i + 1, min(len(page), i + 2 + MAX_GAP)) if page[k] == tok), None)
                if nxt is None or _gap_changes_meaning(page[i + 1:nxt]):
                    ok = False
                    break
                skipped += nxt - i - 1
                i = nxt
            if ok and skipped > len(qt):        # пропущено больше слов, чем в самой цитате, — это не цитата
                ok = False
            if ok:
                found = i
                break
        if found is None:
            return False
        pos = found + 1
    return pos > 0


# ----------------------------------------------------------------- утверждения резюме
def claims(data: dict, sentences) -> list[dict]:
    t = core.as_text
    out: list[dict] = []
    all_pages = sorted({int(p) for item in (data.get("findings") or []) + (data.get("questions") or []) if isinstance(item, dict)
                        for p in (item.get("source_pages") or []) if str(p).isdigit()})
    all_ids = [i for item in (data.get("findings") or []) if isinstance(item, dict) for i in (item.get("fact_ids") or [])]

    def add(cid, where, kind, text, pages, ids):
        text = t(text)
        if text:
            out.append({"id": cid, "where": where, "kind": kind, "text": text,
                        "source_pages": [int(p) for p in (pages or []) if str(p).isdigit()], "fact_ids": list(ids or [])})

    add("title", "заголовок", "заголовок", data.get("title"), all_pages, all_ids)
    add("lede", "преамбула", "преамбула", data.get("lede"), [1], [])
    for i, f in enumerate(data.get("findings") or [], 1):
        if not isinstance(f, dict):
            continue
        pages, ids = f.get("source_pages"), f.get("fact_ids")
        add("f%d.lead" % i, "вывод %d, тезис" % i, "тезис", f.get("lead"), pages, ids)
        for j, s in enumerate(sentences(t(f.get("body"))), 1):
            add("f%d.s%d" % (i, j), "вывод %d, предложение %d" % (i, j), "факт", s, pages, ids)
    for i, q in enumerate(data.get("questions") or [], 1):
        if not isinstance(q, dict):
            continue
        pages, ids = q.get("source_pages"), q.get("fact_ids")
        if re.search(r"\d", t(q.get("q"))):
            add("q%d.q" % i, "вопрос %d" % i, "факт в вопросе", q.get("q"), pages, ids)
        for j, s in enumerate(sentences(t(q.get("body"))), 1):
            add("q%d.s%d" % (i, j), "вопрос %d, обоснование, предложение %d" % (i, j), "факт", s, pages, ids)
        if re.search(r"\d", t(q.get("ask"))):
            add("q%d.ask" % i, "вопрос %d, приписка" % i, "факт в вопросе", q.get("ask"), pages, ids)
    return out


# ----------------------------------------------------------------- доказательная база
def _number_spans(page_txt: str, forms: set[str]) -> list[tuple[int, int]]:
    spans = []
    clean = core._clean(page_txt)
    for m in core._NUM_RE.finditer(clean):
        for tok in core.find_number_tokens(m.group(0)):
            if core.number_forms(tok) & forms:
                spans.append((m.start(), m.end()))
                break
    return spans


def _quote_span(quote: str, page_txt: str) -> tuple[int, int] | None:
    q = (quote or "").strip()
    if len(q) < 15:
        return None
    head = re.escape(q[:40]).replace(r"\ ", r"\s+")
    m = re.search(head, page_txt, re.I)
    return (m.start(), m.start() + len(q)) if m else None


def _excerpts(claim: dict, facts_by_id: dict, jdir: Path, pages_total: int) -> list[dict]:
    pages = set(claim["source_pages"])
    pages |= {int(facts_by_id[i]["page"]) for i in claim["fact_ids"] if i in facts_by_id and str(facts_by_id[i].get("page", "")).isdigit()}
    pages = sorted(p for p in pages if 1 <= p <= pages_total)
    forms: set[str] = set()
    for tok in core.find_number_tokens(claim["text"]):
        if len(re.sub(r"\D", "", tok)) >= 2 or "," in tok or "." in tok:     # одиночные цифры дают шум
            forms |= core.number_forms(tok)
    hits: list[tuple[int, int, int]] = []          # (страница, начало, конец)
    for p in pages:
        txt = core.page_text(jdir, p)
        for fid in claim["fact_ids"]:
            f = facts_by_id.get(fid)
            if f and int(f.get("page", 0) or 0) == p:
                sp = _quote_span(f.get("quote", ""), txt)
                if sp:
                    hits.append((p, *sp))
        for sp in _number_spans(txt, forms):
            hits.append((p, *sp))
    # окна вокруг найденного, слить пересекающиеся
    windows: dict[int, list[list[int]]] = {}
    for p, a, b in hits:
        txt_len = len(core.page_text(jdir, p))
        lo, hi = max(0, a - WINDOW), min(txt_len, b + WINDOW)
        lst = windows.setdefault(p, [])
        for w in lst:
            if lo <= w[1] and hi >= w[0]:
                w[0], w[1] = min(w[0], lo), max(w[1], hi)
                break
        else:
            lst.append([lo, hi])
    out = []
    for p, lst in windows.items():
        txt = core.page_text(jdir, p)
        for lo, hi in lst:
            frag = re.sub(r"\s+", " ", txt[lo:hi]).strip()
            out.append({"page": p, "text": ("…" if lo else "") + frag + ("…" if hi < len(txt) else "")})
    out.sort(key=lambda e: -len(e["text"]))
    return out[:MAX_EXCERPTS]


def packet(items: list[dict], jdir: Path) -> dict:
    facts = core.read_json(jdir / "facts.json", {"facts": []}).get("facts", [])
    by_id = {f.get("id"): f for f in facts}
    total = int(core.read_json(jdir / "meta.json", {}).get("pages_extracted", 0))
    used: dict[str, dict] = {}
    claims_out = []
    for c in items:
        for fid in c["fact_ids"]:
            f = by_id.get(fid)
            if f and fid not in used:
                used[fid] = {k: f.get(k) for k in ("page", "kind", "claim", "quote", "numbers", "status", "modality",
                                                    "attribution", "party", "from_image") if f.get(k) not in (None, "", [])}
        claims_out.append({**c, "excerpts": _excerpts(c, by_id, jdir, total)})
    return {"claims": claims_out, "facts": used}


# ----------------------------------------------------------------- проверка отчёта модели
def _years_tolerated(missing: list[str], pages_txt: str, quotes_txt: str) -> list[str]:
    """Год в русской записи («во II кв. 2026 г.») при «2Q26» в цитате: допускается, если год есть на странице
    или две последние цифры года есть в цитате."""
    rest = []
    for n in missing:
        if re.fullmatch(r"(19|20)\d\d", n) and (n in pages_txt or re.search(r"(?<!\d)%s(?!\d)" % n[2:], quotes_txt)):
            continue
        rest.append(n)
    return rest


def validate(report, issued: dict, jdir: Path) -> tuple[list[dict], dict]:
    """issued: {id: claim}. Возвращает (ошибки отчёта, разобранные вердикты {id: {...}})."""
    errors: list[dict] = []
    parsed: dict[str, dict] = {}
    rows = report.get("claims") if isinstance(report, dict) else report
    if not isinstance(rows, list):
        return [{"where": "отчёт", "problem": "нужен объект {\"claims\": [...]} или массив вердиктов"}], {}
    facts = {f.get("id"): f for f in core.read_json(jdir / "facts.json", {"facts": []}).get("facts", [])}
    total = int(core.read_json(jdir / "meta.json", {}).get("pages_extracted", 0))
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append({"where": "отчёт", "problem": "каждый вердикт — объект"})
            continue
        cid = core.as_text(row.get("id"))
        if cid not in issued:
            errors.append({"where": cid or "?", "problem": "такого утверждения нет в factcheck.claims этого раунда"})
            continue
        seen.add(cid)
        claim = issued[cid]
        verdict = core.as_text(row.get("verdict")).lower()
        if verdict not in VERDICTS:
            errors.append({"where": cid, "problem": "verdict должен быть ok | fix | unsupported"})
            continue
        ev = row.get("evidence") or []
        if isinstance(ev, dict):
            ev = [ev]
        quotes, pages_used, bad = [], set(), False
        for e in ev:
            if not isinstance(e, dict):
                continue
            if e.get("fact_id"):
                f = facts.get(core.as_text(e["fact_id"]))
                if not f or not f.get("from_image"):
                    errors.append({"where": cid, "problem": "ссылка на факт %s допустима только для чисел с графика "
                                                            "(from_image); для текста приведите цитату со страницы" % e["fact_id"]})
                    bad = True
                    continue
                quotes.append(" ; ".join(f.get("numbers", [])) + " " + core.as_text(f.get("quote")))
                continue
            page, quote = e.get("page"), core.as_text(e.get("quote"))
            if not str(page).isdigit() or not (1 <= int(page) <= total):
                errors.append({"where": cid, "problem": "evidence.page «%s» — нет такой страницы" % page})
                bad = True
                continue
            if not (QUOTE_MIN <= len(quote) <= QUOTE_MAX):
                errors.append({"where": cid, "problem": "цитата %d знаков: нужна дословная цитата %d–%d знаков" % (len(quote), QUOTE_MIN, QUOTE_MAX)})
                bad = True
                continue
            if not quote_on_page(quote, core.page_text(jdir, int(page))):
                errors.append({"where": cid, "problem": "цитаты нет на с. %s: «%s»" % (page, quote[:80]),
                               "fix": "скопируйте фрагмент дословно из excerpts или pdf.py pages; не переводите и не пересказывайте"})
                bad = True
                continue
            quotes.append(quote)
            pages_used.add(int(page))
        if bad:
            continue
        correction = core.as_text(row.get("correction"))
        problem = core.as_text(row.get("problem"))
        need_ev = verdict in ("ok", "fix") or bool(correction)
        if need_ev and not quotes:
            errors.append({"where": cid, "problem": "нет evidence: для «%s» нужна хотя бы одна дословная цитата со страницы" % verdict})
            continue
        if verdict == "fix" and not correction:
            errors.append({"where": cid, "problem": "verdict fix без correction: дайте исправленный текст утверждения"})
            continue
        if verdict in ("fix", "unsupported") and not problem:
            errors.append({"where": cid, "problem": "опишите в problem, что именно не совпадает с документом"})
            continue
        quotes_txt = " ; ".join(quotes)
        idx = core.number_index(quotes_txt)
        pages_txt = " ".join(core.page_text(jdir, p) for p in pages_used)
        target = claim["text"] if verdict == "ok" else correction
        if target:
            missing, _minor = core.check_numbers(target, idx)
            missing = _years_tolerated(missing, pages_txt, quotes_txt)
            if missing:
                errors.append({"where": cid, "problem": "числа %s %s нет в приведённых цитатах"
                                                        % (", ".join(missing), "утверждения" if verdict == "ok" else "исправления"),
                               "fix": "добавьте цитату, где стоит это число (относящееся к тому же показателю), или исправьте число"})
                continue
        parsed[cid] = {"verdict": verdict, "text": claim["text"], "where": claim["where"], "correction": correction,
                       "problem": problem, "evidence": [q[:200] for q in quotes]}
    for cid in issued:
        if cid not in seen:
            errors.append({"where": cid, "problem": "нет вердикта: проверьте каждое утверждение из factcheck.claims"})
    return errors, parsed
