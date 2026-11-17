# -*- coding: utf-8 -*-
"""facts.py — реестр фактов документа (память агента вне контекста).

Зачем: агент читает документ порциями и не должен тащить все страницы в контексте.
Каждый факт сразу сдаётся в реестр; скрипт тут же сверяет числа факта с текстом
страницы и возвращает отказ, если числа на странице нет. Так «выдуманные» и
пересчитанные цифры отсекаются до того, как попадут в резюме.

Команды:
  add   <job> --json '[{...}, ...]' | --file <путь>   добавить факты
  skip  <job> --pages 1,2,15 [--reason '…']           отметить страницы без фактов (обложка, оглавление);
                                                       страницу с текстом без фактов — только с --reason
  list  <job> [--relevance high,medium] [--offset N]   компактный реестр для сборки резюме
  stats <job>                                          покрытие страниц и состав реестра
  drop  <job> --ids f003,f010                          удалить факты

Поля факта: page (обязательно, одно число), kind, topic, claim (по-русски, одно предложение, языком
профессионального переводчика), numbers (список строк — ровно как в источнике), attribution, quote
(дословная формулировка оригинала до 200 знаков), relevance (high|medium|low), why, focus (номера пунктов
отраслевых правил: ["F2"]), status (стадия инициативы), modality (модальная формула источника по-русски),
party (сторона — для kind=beneficiary), from_image (true, если число прочитано с графика глазами).

Факты принимаются только после выбора сектора (facts_rules.py set): правила извлечения зависят от отрасли.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _core as core  # noqa: E402
import facts_rules as rules  # noqa: E402

KINDS = {"fact", "trend", "forecast", "estimate", "opinion", "recommendation", "term",
         "mechanism", "gap", "precedent", "beneficiary"}
STATUSES = rules.STATUSES
RELEVANCE = {"high", "medium", "low"}
FIELDS = {"page", "kind", "topic", "claim", "numbers", "attribution", "quote", "quote_en", "relevance",
          "business_relevance", "why", "from_image", "focus", "status", "modality", "party"}
ALIASES = {"stage": "status", "modal": "modality", "beneficiary": "party", "focus_ids": "focus",
           "source_pages": "page", "pages": "page", "source_page": "page", "p": "page",
           "text": "claim", "statement": "claim", "fact": "claim", "values": "numbers", "source": "attribution"}
SKIP_MIN_LETTERS = 600
LEGAL_RE = re.compile(r"not intended (to be relied upon|as an offer)|forward-looking|all rights reserved|disclaimer|important (information|disclosures)"
                      r"|analyst certification|не является (инвестиционной )?рекомендаци|все права защищены|раскрытие информации", re.I)
FIGURE_RE = re.compile(r"\b(Figure|Fig\.|Chart|Exhibit|Рис\.|Рисунок|График|Диаграмма)\s*\d", re.I)
LIST_CAP = 60_000


def _norm(s: str) -> str:
    return re.sub(r"[\W_]+", " ", (s or "").lower()).strip()


def _load(jdir: Path) -> dict:
    return core.read_json(jdir / "facts.json", {"seq": 0, "facts": [], "skipped_pages": []})


def cmd_add(args) -> None:
    jdir = core.job_dir(args.job)
    meta = core.read_json(jdir / "meta.json", {})
    total = int(meta.get("pages_extracted", 0))
    page_kinds = {int(p["n"]): p.get("kind", "text") for p in meta.get("page_info", []) if "n" in p}
    sector = rules.load(jdir)
    if not sector:
        core.fail("Сектор документа не выбран — факты пока не принимаются.",
                  "Сначала facts_rules.py detect %s, затем facts_rules.py set %s --sector <id> (или general): "
                  "правила извлечения фактов зависят от отрасли." % (args.job, args.job))
    focus_known = rules.focus_ids(sector["sector"], sector.get("secondary"))
    data = core.load_payload(args, "список фактов")
    if isinstance(data, dict):
        if all(re.fullmatch(r"\d+", str(k)) for k in data.keys()):
            flat = []
            for k, v in data.items():
                for item in v if isinstance(v, list) else [v]:
                    if isinstance(item, dict):
                        item.setdefault("page", int(k))
                        flat.append(item)
            data = flat
        else:
            data = [data]
    if not isinstance(data, list):
        core.fail("Ожидался JSON-массив фактов.")

    store = _load(jdir)
    known = {(f["page"], _norm(f["claim"])) for f in store["facts"]}
    accepted, rejected, renamed, unknown, chart_pages = [], [], set(), set(), set()
    notes = []
    for raw in data:
        if not isinstance(raw, dict):
            rejected.append({"fact": str(raw)[:80], "reason": "факт должен быть объектом"})
            continue
        raw = dict(raw)
        for alias, field in ALIASES.items():
            if alias in raw and field not in raw:
                val = raw.pop(alias)
                if field == "page" and isinstance(val, (list, tuple)):
                    val = val[0] if val else None
                raw[field] = val
                renamed.add("%s→%s" % (alias, field))
        unknown |= set(raw) - FIELDS
        claim = core.as_text(raw.get("claim"))
        try:
            if isinstance(raw.get("page"), bool):
                raise ValueError
            page = int(raw.get("page"))
        except Exception:
            rejected.append({"claim": claim[:80], "reason": "нет номера страницы: поле page — одно число",
                             "fix": 'пример: {"page": 3, "claim": "…", "numbers": ["42%"]}'})
            continue
        if not (1 <= page <= total):
            rejected.append({"claim": claim[:80], "reason": "страницы %s нет в документе" % page})
            continue
        if len(claim) < 8:
            rejected.append({"page": page, "reason": "пустое утверждение: текст факта кладётся в поле claim"})
            continue
        if (page, _norm(claim)) in known:
            continue
        numbers = raw.get("numbers") or []
        if not isinstance(numbers, (list, tuple)):
            numbers = [numbers]
        numbers = [core.as_text(x) for x in numbers if core.as_text(x)]
        from_image = bool(raw.get("from_image"))

        # числа и цитата сверяются только с указанной страницей: соседние — лишь для подсказки, где число на самом деле
        ctx = core.page_text_for_numbers(jdir, page)
        idx = core.number_index(ctx)
        declared_missing, declared_minor = core.check_numbers(" ; ".join(numbers), idx)
        missing, _minor = core.check_numbers(claim, idx)
        missing = list(dict.fromkeys(declared_missing + declared_minor + missing))
        if missing and not from_image:
            item = {
                "page": page,
                "claim": claim[:120],
                "reason": "чисел нет в тексте страницы %d: %s" % (page, ", ".join(missing)),
                "fix": "Перепишите число ровно как в источнике (без округления и пересчёта). "
                       "Если число прочитано с графика глазами — добавьте \"from_image\": true.",
            }
            near = [n for n in (page - 1, page + 1) if 1 <= n <= total and
                    not core.check_numbers(" ; ".join(missing), core.number_index(core.page_text_for_numbers(jdir, n)))[0]]
            if near:
                item["fix"] = ("Эти числа стоят на странице %s, а не %d: укажите её в page (факт, где числа с разных страниц, "
                               "разбейте на два). " % (" или ".join(map(str, near)), page)) + item["fix"]
            pk = page_kinds.get(page, "text")
            if pk in ("scan", "broken", "mixed"):
                item["fix"] += (" Страница распознана OCR (%s): цифра могла быть прочитана с ошибкой — сверьте её по pdf.py pages "
                                "и берите число строго как там; если страница ещё не распознана, сначала pdf.py ocr." % pk)
            rejected.append(item)
            continue

        quote = (core.as_text(raw.get("quote")) or core.as_text(raw.get("quote_en")))[:240]
        quote_found = None
        if quote:
            q = _norm(quote)
            quote_found = bool(q) and q[:60] in _norm(ctx)

        kind = core.as_text(raw.get("kind")).lower() or "fact"
        relevance = (core.as_text(raw.get("relevance")) or core.as_text(raw.get("business_relevance")) or "medium").lower()
        store["seq"] += 1
        fact = {
            "id": "f%03d" % store["seq"],
            "page": page,
            "kind": kind if kind in KINDS else "fact",
            "topic": core.as_text(raw.get("topic"))[:60],
            "claim": claim[:600],
            "numbers": numbers[:12],
            "attribution": (core.as_text(raw.get("attribution")) or None),
            "quote": quote,
            "relevance": relevance if relevance in RELEVANCE else "medium",
            "why": core.as_text(raw.get("why"))[:160],
        }
        focus = raw.get("focus") or []
        if not isinstance(focus, (list, tuple)):
            focus = re.split(r"[,; ]+", core.as_text(focus))
        focus = [core.as_text(x).upper() for x in focus if core.as_text(x)]
        bad_focus = [x for x in focus if x not in focus_known]
        focus = [x for x in focus if x in focus_known]
        if bad_focus:
            notes.append("%s: неизвестные пункты focus %s — допустимы %s" % (fact["id"], bad_focus, sorted(focus_known)))
        if focus:
            fact["focus"] = focus[:4]
        status = core.as_text(raw.get("status")).lower()
        if status:
            if status in STATUSES:
                fact["status"] = status
            else:
                notes.append("%s: status «%s» не из списка %s — не записан" % (fact["id"], status, sorted(STATUSES)))
        elif fact["kind"] in ("mechanism", "recommendation"):
            notes.append("%s (%s): укажите status — стадию инициативы (proposed, announced, pilot, operating…)" % (fact["id"], fact["kind"]))
        modality = core.as_text(raw.get("modality"))[:120]
        if modality:
            fact["modality"] = modality
        party = core.as_text(raw.get("party"))[:60]
        if party:
            fact["party"] = party
        elif fact["kind"] == "beneficiary":
            notes.append("%s: для kind=beneficiary нужно поле party — какая сторона выигрывает" % fact["id"])
        if from_image:
            fact["from_image"] = True
        if quote_found is False:
            fact["quote_not_found"] = True
        store["facts"].append(fact)
        if numbers and FIGURE_RE.search(ctx):
            chart_pages.add(page)
        known.add((page, _norm(claim)))
        accepted.append(fact["id"])

    core.write_json(jdir / "facts.json", store)
    resp = {
        "ok": True,
        "accepted": len(accepted),
        "accepted_ids": accepted,
        "rejected": rejected,
        "facts_total": len(store["facts"]),
    }
    if chart_pages:
        resp["chart_hint"] = ("На страницах %s есть графики: их подписи в тексте идут вперемешку по годам и рядам. Проверьте, что "
                              "в claim у каждого числа назван год и ряд так, как на графике (pdf.py render), — сверка чисел этого "
                              "не ловит." % sorted(chart_pages)[:10])
    if renamed:
        resp["fields_renamed"] = sorted(renamed)
    if unknown:
        resp["fields_ignored"] = sorted(unknown)[:12]
    if renamed or unknown:
        resp["fields_hint"] = "Поля факта: " + ", ".join(sorted(FIELDS)) + ". Страница — page (одно число)."
    if notes:
        resp["field_notes"] = notes[:20]
    if rejected:
        resp["note"] = "Отклонённые факты (rejected) в реестр НЕ попали: исправьте и сдайте повторно."
    resp["sector"] = sector["sector"] + ("+" + sector["secondary"] if sector.get("secondary") else "")
    resp["next"] = ("Читайте следующую порцию страниц (pdf.py pages) и сдавайте факты; когда документ прочитан — "
                    "facts.py stats %s, затем facts.py list %s." % (args.job, args.job))
    core.out(resp)


def _letters(jdir: Path, n: int) -> int:
    return len(re.findall(r"[^\W\d_]", core.page_text(jdir, n)))


def cmd_skip(args) -> None:
    jdir = core.job_dir(args.job)
    meta = core.read_json(jdir / "meta.json", {})
    pages = core.parse_pages(args.pages, int(meta.get("pages_extracted", 0)))
    store = _load(jdir)
    with_facts = {f["page"] for f in store["facts"]}
    reason = core.as_text(args.reason)
    heavy = [n for n in pages if n not in with_facts and _letters(jdir, n) >= SKIP_MIN_LETTERS
             and not LEGAL_RE.search(core.page_text(jdir, n))]
    if heavy and len(reason) < 15:
        core.fail("Страницы %s содержат текст (от %d букв) и ни одного факта — пропускать их нельзя." % (heavy[:20], SKIP_MIN_LETTERS),
                  "skip — только для обложки, оглавления, сносок, дисклеймера. Прочитайте страницы (pdf.py pages) и сдайте факты. "
                  "Если на странице действительно нет ничего для резюме — повторите с --reason 'почему' (от 15 знаков).",
                  pages_blocked=heavy[:40])
    store["skipped_pages"] = sorted(set(store.get("skipped_pages", [])) | set(pages))
    if heavy:
        reasons = store.setdefault("skip_reasons", {})
        for n in heavy:
            reasons[str(n)] = reason[:200]
    core.write_json(jdir / "facts.json", store)
    core.out({"ok": True, "skipped_pages": store["skipped_pages"],
              "next": "Проверьте покрытие: facts.py stats %s" % args.job})


def _coverage(jdir: Path, store: dict) -> dict:
    meta = core.read_json(jdir / "meta.json", {})
    total = int(meta.get("pages_total", 0))
    seen = {f["page"] for f in store["facts"]} | set(store.get("skipped_pages", []))
    unread = [n for n in range(1, total + 1) if n not in seen]
    res = {"pages_total": total, "pages_reviewed": total - len(unread), "pages_not_reviewed": unread[:80]}
    if store.get("skip_reasons"):
        res["skipped_with_text"] = store["skip_reasons"]
    return res


def cmd_stats(args) -> None:
    jdir = core.job_dir(args.job)
    store = _load(jdir)
    by_kind, by_rel = {}, {}
    for f in store["facts"]:
        by_kind[f["kind"]] = by_kind.get(f["kind"], 0) + 1
        by_rel[f["relevance"]] = by_rel.get(f["relevance"], 0) + 1
    cov = _coverage(jdir, store)
    resp = {"ok": True, "facts_total": len(store["facts"]), "by_kind": by_kind, "by_relevance": by_rel}
    resp.update(cov)
    sector = rules.load(jdir)
    if sector:
        known = rules.focus_ids(sector["sector"], sector.get("secondary"))
        cnt = {k: 0 for k in known}
        for f in store["facts"]:
            for x in f.get("focus", []):
                if x in cnt:
                    cnt[x] += 1
        resp["sector"] = sector["name"] + (" + " + sector["secondary_name"] if sector.get("secondary_name") else "")
        resp["focus_coverage"] = cnt
        empty = {k: known[k] for k, v in cnt.items() if not v}
        if empty:
            resp["focus_uncovered"] = empty
            resp["focus_hint"] = ("По этим пунктам отраслевых правил фактов нет. Если в документе о них что-то есть — "
                                  "вернись к нужным страницам и сдай факты; если нет — так и оставь, это тоже вывод.")
        missing_kinds = [k for k in ("mechanism", "gap", "precedent", "beneficiary") if not by_kind.get(k)]
        if missing_kinds:
            resp["rules_check"] = ("Нет фактов видов %s. Проверь по семи правилам: описан ли в документе новый порядок "
                                   "работы (mechanism), чего не хватает для внедрения (gap), есть ли «впервые» (precedent), "
                                   "что получает каждая сторона (beneficiary). Если в документе этого нет — ничего не добавляй."
                                   % ", ".join(missing_kinds))
    else:
        resp["sector"] = None
    if cov["pages_not_reviewed"]:
        resp["next"] = "Есть непрочитанные страницы: дочитайте их или отметьте facts.py skip."
    else:
        resp["next"] = "Все страницы просмотрены: facts.py list %s, затем summary.py schema и summary.py build." % args.job
    core.out(resp)


def cmd_list(args) -> None:
    jdir = core.job_dir(args.job)
    store = _load(jdir)
    allow = {x.strip() for x in (args.relevance or "high,medium,low").split(",")}
    rows, used, shown = [], 0, 0
    facts = [f for f in store["facts"] if f["relevance"] in allow]
    offset = max(0, args.offset or 0)
    for f in facts[offset:]:
        line = "%s | с.%d | %s | %s | %s | %s" % (
            f["id"], f["page"], f["kind"], f["relevance"], f["topic"], f["claim"],
        )
        if f["numbers"]:
            line += " | числа: " + "; ".join(f["numbers"])
        if f.get("attribution"):
            line += " | источник оценки: " + f["attribution"]
        if f.get("status"):
            line += " | статус: " + f["status"]
        if f.get("modality"):
            line += " | модальность: " + f["modality"]
        if f.get("party"):
            line += " | сторона: " + f["party"]
        if f.get("focus"):
            line += " | focus: " + ",".join(f["focus"])
        if f.get("from_image"):
            line += " | [с графика, в тексте нет]"
        if used + len(line) > LIST_CAP:
            break
        rows.append(line)
        used += len(line)
        shown += 1
    resp = {"ok": True, "format": "id | страница | вид | важность | тема | утверждение | числа", "facts": rows,
            "shown": shown, "matched": len(facts)}
    if offset + shown < len(facts):
        resp["next"] = "Продолжение: facts.py list %s --offset %d" % (args.job, offset + shown)
    resp.update(_coverage(jdir, store))
    core.out(resp)


def cmd_drop(args) -> None:
    jdir = core.job_dir(args.job)
    store = _load(jdir)
    ids = {x.strip() for x in args.ids.split(",") if x.strip()}
    before = len(store["facts"])
    store["facts"] = [f for f in store["facts"] if f["id"] not in ids]
    core.write_json(jdir / "facts.json", store)
    core.out({"ok": True, "removed": before - len(store["facts"]), "facts_total": len(store["facts"])})


def main() -> None:
    core.setup_stdio()
    ap = core.JsonArgumentParser(prog="facts.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("add"); p.add_argument("job"); p.add_argument("--json"); p.add_argument("--file"); p.set_defaults(fn=cmd_add)
    p = sub.add_parser("skip"); p.add_argument("job"); p.add_argument("--pages", required=True); p.add_argument("--reason")
    p.set_defaults(fn=cmd_skip)
    p = sub.add_parser("list"); p.add_argument("job"); p.add_argument("--relevance"); p.add_argument("--offset", type=int); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("stats"); p.add_argument("job"); p.set_defaults(fn=cmd_stats)
    p = sub.add_parser("drop"); p.add_argument("job"); p.add_argument("--ids", required=True); p.set_defaults(fn=cmd_drop)
    args = ap.parse_args()
    if not getattr(args, "fn", None):
        core.fail("Не указана команда.", "Доступно: add, skip, list, stats, drop.")
    args.fn(args)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        core.fail("Внутренняя ошибка facts.py: %s: %s" % (type(e).__name__, e))
