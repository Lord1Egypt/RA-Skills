# -*- coding: utf-8 -*-
"""sber_kb.py — база знаний о Сбере (data/sber_knowledge_base.json) для этапа составления вопросов.

Зачем: прежде чем спрашивать правление о кредитовании, инвестициях или запуске чего-либо, нужно знать,
что Сбер уже делает и какие компании отрасли ему принадлежат, принадлежали или связаны с ним. Пример
ошибки без базы: вопрос «кредитуем ли мы компании беспилотного транспорта», когда одна из двух таких
компаний — бывшая «дочка» Сбера (Navio), а вторая — прямой конкурент.

Команды:
  topics                                         тематики базы: id, название, описание, ключевые слова
  search <job> --slot q1 --scope company|country --query 'беспилотные грузовики'
                                                 найти факты и карточки компаний; результат записывается
                                                 в реестр контекста (context.json) как запись kind=kb

Каждый результат несёт id (kb:<тематика>/<путь> или kb:co/<компания>), статус достоверности, дату и источник.
Статусы: confirmed — подтверждено; reported — сообщают СМИ; rumor_denied — опровергнуто (не факт!);
analyst_estimate — оценка аналитиков; historical — может быть неактуально. Для компаний важно поле
relationship: subsidiary/associate — наша; former — Сбер вышел из капитала (не называть «дочкой»);
unclear — владение неясно.

Обновить базу — заменить файл data/sber_knowledge_base.json (тот же формат: meta + topics).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _core as core  # noqa: E402
import context as ctxreg  # noqa: E402

KB_PATH = Path(__file__).resolve().parent.parent / "data" / "sber_knowledge_base.json"   # файл в папке навыка
FACT_KEYS = ("fact", "deal", "event")
SKIP_KEYS = {"title", "description", "routing_keywords", "source", "sources", "relationship_legend", "segments",
             "companies", "data_as_of", "supervisory_board_source", "historical_divestments_2022"}
STOP = {"сбер", "сбербанк", "банк", "банка", "росси", "россия", "российск", "компан", "компании", "наши", "нашего",
        "этого", "котор", "также", "более", "через", "после", "группа", "групп"}
MAX_ITEMS, MAX_COMPANIES = 15, 6


def load_kb() -> dict:
    kb = core.read_json(KB_PATH, None)
    if not isinstance(kb, dict) or "topics" not in kb:
        core.fail("База знаний о Сбере не найдена или повреждена: %s" % KB_PATH,
                  "Положите sber_knowledge_base.json в папку data/ навыка.")
    return kb


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").lower().replace("ё", "е"))


def stems(query: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-zа-я0-9]+", _norm(query)):
        if re.fullmatch(r"[a-z0-9]+", w):
            s = w if len(w) >= 3 else ""
        else:
            s = w[:max(5, len(w) - 3)] if len(w) >= 6 else (w if len(w) >= 4 else "")
        if s and not any(s.startswith(x) or x.startswith(s) for x in STOP) and s not in out:
            out.append(s)
    return out


def _sources(node: dict) -> str:
    src = node.get("source") or node.get("sources") or ""
    return src[0] if isinstance(src, list) and src else str(src)


def flatten(topic_id: str, node, path: str = "") -> list[dict]:
    """Все утверждения тематики: факты, сделки, события, строки в списках и полях."""
    items = []
    if isinstance(node, dict):
        key = next((k for k in FACT_KEYS if isinstance(node.get(k), str)), None)
        if key:
            text = node[key]
            for extra in ("amount", "notes", "date" if key == "event" else ""):
                if extra and node.get(extra) and extra != "date":
                    text += " (%s)" % node[extra]
            if key == "event" and node.get("date"):
                text = "%s: %s" % (node["date"], text)
            items.append({"id": "kb:%s/%s" % (topic_id, path.strip("/")), "text": text, "status": node.get("status", ""),
                          "date": node.get("date", "") if key != "event" else "", "source": _sources(node)})
            return items
        for k, v in node.items():
            if k in SKIP_KEYS:
                continue
            p = "%s/%s" % (path, k)
            if isinstance(v, str):
                items.append({"id": "kb:%s%s" % (topic_id, p), "text": v, "status": node.get("status", "") if k != "status" else "",
                              "date": "", "source": _sources(node)})
            elif isinstance(v, (dict, list)):
                items += flatten(topic_id, v, p)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            p = "%s/%d" % (path, i)
            if isinstance(v, str):
                items.append({"id": "kb:%s%s" % (topic_id, p), "text": v, "status": "", "date": "", "source": ""})
            else:
                items += flatten(topic_id, v, p)
    return [x for x in items if x["text"] and not re.fullmatch(r"(confirmed|reported|rumor_denied|analyst_estimate|historical|expected)", x["text"])]


def company_card(c: dict, legend: dict) -> dict:
    card = {"id": "kb:co/%s" % c.get("id"), "name": c.get("name"), "aliases": c.get("aliases", [])[:4],
            "relationship": c.get("relationship"), "relationship_meaning": legend.get(c.get("relationship"), ""),
            "sber_stake": c.get("sber_stake", ""), "ownership_status": c.get("ownership_status", ""),
            "activity": c.get("activity", "")}
    for k in ("agent_note", "data_gap", "see_also"):
        if c.get(k):
            card[k] = c[k]
    card["key_facts"] = [{"text": f.get("fact"), "status": f.get("status", ""), "date": f.get("date", "")}
                         for f in (c.get("key_facts") or [])[:3] if isinstance(f, dict)]
    return card


def _hits(st: list[str], text: str) -> int:
    t = _norm(text)
    return sum(1 for s in st if s in t)


def search_kb(kb: dict, query: str) -> dict:
    st = stems(query)
    topics = kb["topics"]
    scored = []
    for tid, t in topics.items():
        kws = " | ".join(t.get("routing_keywords", []))
        score = 3 * _hits(st, kws) + _hits(st, t.get("title", "") + " " + t.get("description", ""))
        scored.append((score, tid))
    scored.sort(reverse=True)
    top_topics = [tid for s, tid in scored if s > 0][:3]
    items = []
    for tid, t in topics.items():
        if tid == "group_companies_registry":
            continue
        for it in flatten(tid, t):
            h = _hits(st, it["text"])
            if tid in top_topics and re.search(r"agent_instruction|status_vs_sber|agent_note", it["id"]):
                h += 10                            # оговорки о владении и указания агенту — всегда первыми
            if tid in top_topics:                  # тематика выбрана по ключевым словам — её факты нужны и без совпадений
                items.append((h + 2 if h else 1, it))
            elif h >= 2:
                items.append((h, it))
    items.sort(key=lambda x: -x[0])
    reg = topics.get("group_companies_registry", {})
    legend = reg.get("relationship_legend", {})
    comps = []
    for c in reg.get("companies", []):
        names = " | ".join([c.get("name", "")] + c.get("aliases", []) + c.get("routing_keywords", []))
        h = 3 * _hits(st, names) + _hits(st, c.get("activity", "") + " " + c.get("segment", "").replace("_", " "))
        if h:
            comps.append((h, c))
    comps.sort(key=lambda x: -x[0])
    return {"stems": st,
            "topics": [{"id": tid, "title": topics[tid].get("title"), "description": topics[tid].get("description")} for tid in top_topics],
            "items": [it for _, it in items[:MAX_ITEMS]],
            "companies": [company_card(c, legend) for _, c in comps[:MAX_COMPANIES]],
            "registry_instructions": reg.get("agent_instructions", []) if comps else []}


def cmd_topics(args) -> None:
    kb = load_kb()
    core.out({"ok": True, "entity": kb.get("meta", {}).get("entity"), "data_as_of": kb.get("meta", {}).get("data_as_of"),
              "topics": [{"id": tid, "title": t.get("title"), "description": t.get("description"),
                          "keywords": t.get("routing_keywords", [])[:10]} for tid, t in kb["topics"].items()],
              "important_upcoming_event": kb.get("meta", {}).get("important_upcoming_event", "")})


def cmd_search(args) -> None:
    jdir = core.job_dir(args.job)
    kb = load_kb()
    slot, scope, query = (args.slot or "").lower(), (args.scope or "").lower(), core.as_text(args.query)
    if len(query) < 3:
        core.fail("Пустой запрос.", "Пишите тему вопроса: «беспилотные грузовики», «гуманоидные роботы», «кредитование МСБ».")
    store = ctxreg.load_store(jdir)
    why = ctxreg.check_slot(store, slot, scope, "kb")
    if why:
        core.fail(why)
    found = search_kb(kb, query)
    meta = kb.get("meta", {})
    results = [{"id": it["id"], "snippet": it["text"], "status": it["status"], "date": it["date"], "url": it["source"],
                "title": "база знаний"} for it in found["items"]]
    results += [{"id": c["id"], "title": c["name"], "url": "", "date": "", "status": c["ownership_status"],
                 "snippet": "%s; связь со Сбером: %s (%s); доля: %s; %s%s" % (
                     c["activity"], c["relationship"], c["relationship_meaning"], c["sber_stake"],
                     c.get("agent_note", ""), (" Данных нет: " + c["data_gap"]) if c.get("data_gap") else "")}
                for c in found["companies"]]
    entry = ctxreg.record(jdir, {"slot": slot, "scope": scope, "kind": "kb", "query": query, "provider": "sber_kb",
                                 "results": results, "error": "" if results else "в базе знаний ничего не найдено"})
    core.out({"ok": True, "id": entry["id"], "slot": slot, "scope": scope, "kind": "kb", "query_stems": found["stems"],
              "data_as_of": meta.get("data_as_of"), "topics": found["topics"], "items": found["items"],
              "companies": found["companies"], "registry_instructions": found["registry_instructions"],
              "status_legend": meta.get("fact_status_legend", {}),
              "next": ("Прочитайте найденное: что Сбер уже делает по теме, какие компании отрасли — наши, бывшие наши "
                       "(former: не называть дочкой), ассоциированные. rumor_denied — не факт. Затем — поиск в интернете "
                       "(не больше 2 запросов): какие ещё компании работают в отрасли в России и кто из них конкурент Сбера. "
                       "Ничего не нашлось — переформулируйте тему (синонимы, название продукта или компании)."
                       if results else
                       "В базе ничего нет по этой теме: попробуйте синонимы (sber_kb.py topics покажет тематики) или "
                       "опирайтесь на поиск в интернете.")})


def main() -> None:
    core.setup_stdio()
    ap = core.JsonArgumentParser(prog="sber_kb.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("topics"); p.set_defaults(fn=cmd_topics)
    p = sub.add_parser("search"); p.add_argument("job"); p.add_argument("--slot", required=True)
    p.add_argument("--scope", required=True); p.add_argument("--query", required=True); p.set_defaults(fn=cmd_search)
    args = ap.parse_args()
    if not getattr(args, "fn", None):
        core.fail("Не указана команда.", "Доступно: topics, search.")
    args.fn(args)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        core.fail("Внутренняя ошибка sber_kb.py: %s: %s" % (type(e).__name__, e))
