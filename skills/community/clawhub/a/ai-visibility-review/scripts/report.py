#!/usr/bin/env python3
"""Validate and render a private AEO checkpoint. Standard library; no network."""
import argparse
import csv
from datetime import datetime
from decimal import Decimal
import html
import ipaddress
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, parse_qs
from uuid import UUID

TOOLS = {"chatgpt": "dataforseo.chatgpt-search", "gemini": "cloro.gemini-search",
         "google_ai_mode": "cloro.google-ai-mode"}
COMPARE_FIELDS = ("schema_version", "method", "brand", "rivals", "market",
                  "questions", "by_name_question", "engines")
SETTINGS = {"chatgpt": "location_name language_name force_web_search",
            "gemini": "country", "google_ai_mode": "gl hl"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def fields(value, allowed, label):
    require(isinstance(value, dict), f"{label} must be an object")
    require(not set(value).difference(allowed.split()), f"Undeclared fields in {label}; keep raw metadata outside the checkpoint")


def money(value):
    require(isinstance(value, str) and re.fullmatch(r"\d+(?:\.\d{1,6})?", value),
            "Money must be a nonnegative USD decimal string, at most six decimals")
    return Decimal(value)


def public_url(value):
    require(isinstance(value, str), "URL must be text")
    url = urlsplit(value)
    require(url.scheme in ("https", "http") and url.hostname and "." in url.hostname
            and not url.username and not url.password, "Expected public HTTP(S) URL")
    try:
        ipaddress.ip_address(url.hostname)
    except ValueError:
        pass
    else:
        raise ValueError("IP addresses are not public citation domains")
    require(not re.search(r"(?:^|\.)(?:local|localhost|internal|invalid|test)$", url.hostname)
            and not any(re.search(r"token|secret|api.?key|password|signature|authorization", k, re.I)
                        for k in parse_qs(url.query)), "Private URL is not report evidence")
    return value


def canonical_url(value):
    url = urlsplit(public_url(value))
    return (url.hostname.lower(), url.path.rstrip("/") or "/", url.query)


def owns(url, domains):
    host = urlsplit(public_url(url)).hostname.lower()
    return any(host == d.lower() or host.endswith("." + d.lower()) for d in domains)


def timestamp(value):
    require(isinstance(value, str), "Timestamp must be ISO text")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamp needs timezone")


def validate(data):
    fields(data, "schema_version method brand rivals market questions by_name_question engines "
           "approved_max_usd budget_note scope_note observations receipts opportunities by_name_findings changes", "checkpoint")
    require(data.get("schema_version") == 1 and data.get("method") == "aeo-v4",
            "Use the aeo-v4 checkpoint contract")
    require(nonempty(data.get("scope_note")), "Explain the scope and omissions")
    require(nonempty(data.get("market", {}).get("country"))
            and nonempty(data.get("market", {}).get("language")), "Market is required")
    require(nonempty(data.get("by_name_question")), "By-name prompt is required")
    fields(data["market"], "country language", "market")
    brands = [data["brand"], *data["rivals"]]
    names = [b["name"] for b in brands]
    require(len(names) == len(set(names)) and all(nonempty(n) for n in names), "Brand names must be unique")
    for brand in brands:
        fields(brand, "name domains aliases", "brand")
        require(isinstance(brand.get("aliases"), list) and all(nonempty(a) for a in brand["aliases"]),
                "Declare brand aliases, even if empty")
        require(isinstance(brand.get("domains"), list) and brand["domains"], "Declare owned domains")
        for domain in brand["domains"]:
            require(isinstance(domain, str) and "/" not in domain and ":" not in domain, "Use bare domains")
            public_url("https://" + domain)
    for question in data["questions"]:
        fields(question, "id text", "question")
    questions = {q["id"]: q["text"] for q in data["questions"]}
    require(1 <= len(questions) <= 5 and len(questions) == len(data["questions"])
            and all(nonempty(k) and nonempty(v) for k, v in questions.items()), "Invalid buyer questions")
    engines = {e["id"]: e for e in data["engines"]}
    require(engines and len(engines) == len(data["engines"]), "Unique engines required")
    for key, engine in engines.items():
        fields(engine, "id tool_id surface settings rounds", "engine")
        require(key in TOOLS and engine.get("tool_id") == TOOLS[key]
                and engine.get("surface") == "logged_out_web", "Unsupported engine/tool/surface")
        require(type(engine.get("rounds")) is int and 2 <= engine["rounds"] <= 5, "Use two to five rounds")
        require(isinstance(engine.get("settings"), dict) and engine["settings"], "Exact settings required")
        fields(engine["settings"], SETTINGS[key], "engine settings")
        require(all(type(value) is bool if setting == "force_web_search" else nonempty(value)
                    for setting, value in engine["settings"].items()), "Settings must use the declared scalar types")
        if key == "chatgpt":
            require(engine["settings"].get("force_web_search") is False, "Buyer ChatGPT web search must not be forced")
    cap = money(data["approved_max_usd"]) if data["approved_max_usd"] is not None else None
    require(data.get("budget_note") is None or isinstance(data["budget_note"], str), "Budget note must be text")
    if cap is None:
        require(nonempty(data.get("budget_note")), "An unrecorded wallet ceiling needs a budget explanation")
    receipts = {}
    for receipt in data["receipts"]:
        fields(receipt, "run_id tool_id cost_usd", "receipt")
        run_id = receipt["run_id"]
        UUID(run_id)
        require(run_id not in receipts and nonempty(receipt.get("tool_id")), "Duplicate or invalid receipt")
        if receipt["cost_usd"] is not None:
            money(receipt["cost_usd"])
        receipts[run_id] = receipt
    slots, observed = set(), {}
    for row in data["observations"]:
        fields(row, "run_id engine phase question_id round requested_prompt requested_settings status reason "
               "retrieved_at model answer sources reviewed verdicts", "observation")
        run_id, engine, phase = row["run_id"], row["engine"], row["phase"]
        require(run_id not in observed and engine in engines and phase in ("buyer", "by_name", "source"),
                "Duplicate run or unknown engine/phase")
        require(run_id in receipts and receipts[run_id]["tool_id"] == engines[engine]["tool_id"],
                "Every observation needs its matching actual-cost receipt")
        question = data["by_name_question"] if phase == "by_name" else questions.get(row["question_id"])
        require(question and row["requested_prompt"] == question, "Observation prompt does not match plan")
        require(phase != "by_name" or row["question_id"] == "by-name", "By-name question ID must be by-name")
        require(type(row["round"]) is int and 1 <= row["round"] <= engines[engine]["rounds"], "Invalid round")
        require(phase != "source" or (engine == "chatgpt" and row["round"] == 1), "Source pass is ChatGPT round 1")
        expected_settings = dict(engines[engine]["settings"])
        if phase == "source":
            expected_settings["force_web_search"] = True
        require(row.get("requested_settings") == expected_settings,
                "Actual request settings do not match the saved measurement plan")
        require(all(row.get(key) is None or isinstance(row[key], str) for key in ("answer", "reason")),
                "Answer and reason must be text")
        require("reviewed" not in row or type(row["reviewed"]) is bool, "Reviewed must be boolean")
        for source in row.get("sources") or []:
            fields(source, "url title", "source")
            public_url(source["url"])
            require(source.get("title") is None or isinstance(source["title"], str), "Source title must be text")
        for verdict in row.get("verdicts") or []:
            fields(verdict, "brand mention_quote recommendation_quote first", "verdict")
            require(nonempty(verdict.get("brand")) and type(verdict.get("first")) is bool
                    and all(verdict.get(key) is None or isinstance(verdict[key], str)
                            for key in ("mention_quote", "recommendation_quote")), "Invalid verdict scalar fields")
        slot = (engine, phase, row["question_id"], row["round"])
        require(slot not in slots, "Duplicate observation slot; do not hide a failed attempt")
        slots.add(slot)
        timestamp(row["retrieved_at"])
        require(row.get("model") is None or nonempty(row["model"]), "Model must be reported text or null")
        require(row["status"] in ("ok", "failed", "refused", "unusable"), "Invalid terminal status")
        if row["status"] == "ok":
            require(row.get("reviewed") is True and nonempty(row.get("answer")), "Usable answers need adjudication")
            require("sources" in row and (row["sources"] is None or isinstance(row["sources"], list)),
                    "Distinguish missing citations from an empty list")
            for source in row["sources"] or []:
                public_url(source["url"])
            voted, first = set(), 0
            for verdict in row["verdicts"]:
                brand = verdict["brand"]
                require(brand in names and brand not in voted, "Unknown or duplicate brand verdict")
                voted.add(brand)
                mention, recommendation = verdict.get("mention_quote"), verdict.get("recommendation_quote")
                require(nonempty(mention) and mention in row["answer"], "Mention quote must occur in exact answer")
                require(recommendation is None or (nonempty(recommendation) and recommendation in row["answer"]),
                        "Recommendation quote must occur in exact answer")
                require(type(verdict.get("first")) is bool and (not verdict["first"] or recommendation),
                        "First requires an explicit recommendation")
                first += int(verdict["first"])
            require(first <= 1, "Only one first recommendation per answer")
        else:
            require(nonempty(row.get("reason")), "Unusable observations need an explanation")
        observed[run_id] = row
    for page in data.get("opportunities", []):
        fields(page, "url kind opened_at excerpt gap action owner effort recheck observation_ids contact draft", "opportunity")
        require(page.get("draft") is None or isinstance(page["draft"], str), "Draft must be text")
        url = public_url(page["url"])
        timestamp(page["opened_at"])
        require(all(nonempty(page.get(k)) for k in ("excerpt", "gap", "action", "owner", "effort", "recheck")),
                "An opportunity needs checked evidence and an actionable plan")
        require(page["kind"] in ("owned", "third_party"), "Unknown opportunity kind")
        require(page.get("observation_ids") and len(set(page["observation_ids"])) == len(page["observation_ids"]),
                "Opportunity needs unique supporting observations")
        if page["kind"] == "owned":
            require(owns(url, data["brand"]["domains"]), "Owned opportunity must use an owned domain")
        for run_id in page["observation_ids"]:
            require(run_id in observed and observed[run_id]["status"] == "ok", "Opportunity refers to absent/unusable evidence")
            if page["kind"] == "third_party":
                require(canonical_url(url) in {canonical_url(s["url"]) for s in observed[run_id]["sources"] or []},
                        "Third-party opportunity was not cited by its supporting observation")
        if page.get("contact"):
            fields(page["contact"], "label source_url", "contact")
            require(nonempty(page["contact"].get("label")), "Contact label required")
            public_url(page["contact"]["source_url"])
    for finding in data.get("by_name_findings", []):
        fields(finding, "engine quote fact source_url", "by-name finding")
        require(nonempty(finding.get("fact")) and nonempty(finding.get("quote")), "Finding requires quote and verified fact")
        require(owns(finding["source_url"], data["brand"]["domains"]), "Fact check needs an official page")
        require(any(r["engine"] == finding["engine"] and r["phase"] == "by_name" and r["status"] == "ok"
                    and finding["quote"] in r["answer"] for r in observed.values()), "By-name finding lacks a grounded quote")
    for change in data.get("changes", []):
        fields(change, "date description url", "change")
        require(nonempty(change.get("date")) and nonempty(change.get("description")), "Describe and date each change")
        if change.get("url"):
            public_url(change["url"])
    spent = sum((money(r["cost_usd"]) for r in receipts.values() if r["cost_usd"] is not None), Decimal(0))
    require(cap is None or spent <= cap, "Recorded spend exceeds approved maximum; reconcile before reporting")
    return data


def tally(rows, brand):
    usable = [r for r in rows if r["status"] == "ok"]
    known = [r for r in usable if r["sources"] is not None]
    verdicts = [v for r in usable for v in r["verdicts"] if v["brand"] == brand["name"]]
    return {"usable": len(usable), "attempted": len(rows), "mentioned": len(verdicts),
            "recommended": sum(bool(v.get("recommendation_quote")) for v in verdicts),
            "first": sum(v["first"] for v in verdicts), "citation_known": len(known),
            "cited": sum(any(owns(s["url"], brand["domains"]) for s in r["sources"]) for r in known)}


def summarize(data):
    validate(data)
    groups = {}
    plan_limitations = []
    missing_engines = sorted(set(TOOLS).difference(e["id"] for e in data["engines"]))
    if missing_engines:
        plan_limitations.append("Missing core engines: " + ", ".join(missing_engines))
    if len(data["questions"]) < 5:
        plan_limitations.append(f"Reduced buyer questions: {len(data['questions'])}/5")
    for engine in data["engines"]:
        if engine["rounds"] < 3:
            plan_limitations.append(f"{engine['id']}: reduced rounds {engine['rounds']}/3")
    for engine in data["engines"]:
        key = engine["id"]
        rows = [r for r in data["observations"] if r["engine"] == key and r["phase"] == "buyer"]
        planned = len(data["questions"]) * engine["rounds"]
        total = tally(rows, data["brand"])
        models = sorted({r["model"] for r in rows if r["status"] == "ok" and r["model"] is not None})
        questions = {q["id"]: tally([r for r in rows if r["question_id"] == q["id"]], data["brand"]) for q in data["questions"]}
        flags = []
        if (planned - total["usable"]) * 5 > planned or any(q["usable"] < 2 for q in questions.values()):
            flags.append("Insufficient buyer coverage")
        if len(models) > 1:
            flags.append("Observed model changed within sample")
        by_name = tally([r for r in data["observations"] if r["engine"] == key and r["phase"] == "by_name"], data["brand"])
        source = tally([r for r in data["observations"] if r["engine"] == key and r["phase"] == "source"], data["brand"])
        secondary_flags = []
        if by_name["usable"] < engine["rounds"]:
            secondary_flags.append(f"By-name fact-check coverage incomplete: {by_name['usable']}/{engine['rounds']} usable")
        if key == "chatgpt" and source["usable"] < len(data["questions"]):
            secondary_flags.append(f"Forced source-pass coverage incomplete: {source['usable']}/{len(data['questions'])} usable")
        groups[key] = {**total, "planned": planned, "missing": planned - len(rows), "models": models,
                       "model_unknown": any(r["status"] == "ok" and r["model"] is None for r in rows),
                       "flags": flags, "secondary_flags": secondary_flags, "questions": questions,
                       "rivals": {b["name"]: tally(rows, b) for b in data["rivals"]},
                       "rival_questions": {b["name"]: {
                           q["id"]: tally([r for r in rows if r["question_id"] == q["id"]], b)
                           for q in data["questions"]} for b in data["rivals"]},
                       "by_name": by_name, "source": source}
    total = sum((money(r["cost_usd"]) for r in data["receipts"] if r["cost_usd"] is not None), Decimal(0))
    return {"engines": groups, "plan_limitations": plan_limitations, "known_cost_usd": format(total, ".6f"),
            "unknown_cost_receipts": sum(r["cost_usd"] is None for r in data["receipts"])}


def compare(before, after):
    left, right = summarize(before), summarize(after)
    reasons = [f"Changed {field}" for field in COMPARE_FIELDS if before.get(field) != after.get(field)]
    for key, current in right["engines"].items():
        previous = left["engines"].get(key)
        if not previous:
            continue
        if current["flags"] or previous["flags"]:
            reasons.append(f"{key}: incomplete coverage or mixed models")
        if previous["models"] != current["models"]:
            reasons.append(f"{key}: observed model disclosure/version changed")
    scope = "Comparison is limited to the declared reduced plan. " if left["plan_limitations"] or right["plan_limitations"] else ""
    return {"comparable": not reasons, "reasons": reasons, "before": left, "after": right,
            "limit": scope + "Comparison covers buyer answers only; by-name and source-pass coverage is separate. Matched request settings do not control unknown model versions. Before/after movement is not proof of causation."}


def render(data, summary, comparison=None):
    validate(data)
    escape = lambda value: html.escape(str(value), quote=True)
    def link(url, label=None):
        return f'<a href="{escape(public_url(url))}" rel="noreferrer">{escape(label or url)}</a>'
    def table(headers, rows):
        return "<table><thead><tr>" + "".join(f"<th>{escape(h)}</th>" for h in headers) + "</tr></thead><tbody>" + "".join(
            "<tr>" + "".join(f"<td>{escape(c)}</td>" for c in row) + "</tr>" for row in rows) + "</tbody></table>"
    def fraction(row, key, denominator="usable"):
        return f'{row[key]}/{row[denominator]}' if row[denominator] else "unavailable (0 usable)" if denominator == "usable" else "unknown (0 citation records)"
    metrics = (("mentioned", "usable"), ("recommended", "usable"), ("first", "usable"), ("cited", "citation_known"))
    def counts(row):
        return [fraction(row, key, denominator) for key, denominator in metrics]
    parts = [f"<h1>{escape(data['brand']['name'])}: AI visibility and citation plan</h1>",
             f"<p>{escape(data['market']['country'])} · {escape(data['market']['language'])} · {escape(data['scope_note'])}</p>",
             "<p>Counts from a small repeated sample. Engines are separate; missing citations are not zero. Nothing has been sent or published.</p>"]
    groups = summary["engines"]
    if summary["plan_limitations"]:
        parts.append("<p><strong>Core plan incomplete:</strong> " + escape("; ".join(summary["plan_limitations"]))
                     + ". Counts and comparisons describe only the declared reduced plan.</p>")
    parts.append(table(["Engine", "Usable / attempted / planned", "Mentioned", "Recommended", "First", "Site cited / known"],
                       [[key, f"{r['usable']} / {r['attempted']} / {r['planned']}", fraction(r, "mentioned"),
                         fraction(r, "recommended"), fraction(r, "first"), fraction(r, "cited", "citation_known")] for key, r in groups.items()]))
    for key, row in groups.items():
        coverage = "Buyer coverage sufficient within the declared reduced plan" if summary["plan_limitations"] else "Buyer coverage sufficient for a descriptive comparison"
        parts.append(f"<p><strong>{escape(key)}</strong>: {escape('; '.join(row['flags']) or coverage)}. "
                     f"Model: {escape(', '.join(row['models']) or 'not reported')}{'; some versions unknown' if row['model_unknown'] else ''}.</p>")
        if row["secondary_flags"]:
            parts.append(f"<p><strong>Incomplete workflow — {escape(key)}:</strong> {escape('; '.join(row['secondary_flags']))}. "
                         "Buyer counts remain separate; factual-accuracy and citation-opportunity conclusions have limited coverage.</p>")
    parts.append("<h2>Next actions and citation opportunities</h2>")
    if not data.get("opportunities"):
        parts.append("<p>No checked opportunities recorded. Do not invent a top-three list.</p>")
    for page in data.get("opportunities", []):
        citation_counts = {}
        for row in data["observations"]:
            if row["status"] == "ok" and any(canonical_url(s["url"]) == canonical_url(page["url"]) for s in row["sources"] or []):
                group = row["engine"] + " / " + row["phase"]
                citation_counts[group] = citation_counts.get(group, 0) + 1
        parts.extend([f"<article><h3>{link(page['url'])}</h3>", f"<blockquote>{escape(page['excerpt'])}</blockquote>",
                      f"<p>{escape(page['gap'])}</p><p><strong>Action:</strong> {escape(page['action'])}</p>",
                      f"<p>{escape(page['owner'])} · {escape(page['effort'])} · Recheck: {escape(page['recheck'])}</p>",
                      f"<p>Checked {escape(page['opened_at'])}. Cited observations: {escape(json.dumps(citation_counts))}</p>"])
        parts.append("<p>Supporting observations: " + ", ".join(
            f'<a href="#observation-{escape(run_id)}">{escape(run_id)}</a>' for run_id in page["observation_ids"]) + "</p>")
        if page.get("contact"):
            parts.append(f"<p>Public contact source: {link(page['contact']['source_url'], page['contact']['label'])}</p>")
        if page.get("draft"):
            parts.append(f"<details><summary>Unsent draft</summary><pre>{escape(page['draft'])}</pre></details>")
        parts.append("</article>")
    parts.append("<h2>Questions and rivals</h2>")
    for key, row in groups.items():
        parts.append(f"<h3>{escape(key)}</h3>")
        question_rows = []
        for q in data["questions"]:
            question_rows.append([q["text"], data["brand"]["name"], *counts(row["questions"][q["id"]])])
            question_rows.extend([q["text"], name, *counts(questions[q["id"]])]
                                 for name, questions in row["rival_questions"].items())
        parts.append(table(["Buyer question", "Brand", "Mentioned", "Recommended", "First", "Site cited / known"], question_rows))
        if row["rivals"]:
            parts.append(table(["Rival — all buyer questions", "Mentioned", "Recommended", "First", "Site cited / known"],
                               [[name, *counts(r)] for name, r in row["rivals"].items()]))
        parts.append(f"<p>Separate by-name pass: {row['by_name']['usable']} usable / {row['by_name']['attempted']} attempted / {next(e['rounds'] for e in data['engines'] if e['id'] == key)} planned. "
                     f"Source pass: {row['source']['usable']} usable / {row['source']['attempted']} attempted / {len(data['questions']) if key == 'chatgpt' else 0} planned.</p>")
    parts.append("<h2>By-name fact checks</h2>")
    for finding in data.get("by_name_findings", []):
        parts.append(f"<p>{escape(finding['engine'])}: “{escape(finding['quote'])}” → {escape(finding['fact'])} {link(finding['source_url'])}</p>")
    parts.append("<h2>Recheck</h2><p>Agree a date after changes, normally 3–4 weeks. No recurring run has been scheduled.</p>")
    if comparison:
        parts.append(f"<p>{'Comparable request plan' if comparison['comparable'] else 'Inconclusive comparison'}: {escape('; '.join(comparison['reasons']))}</p>")
        if comparison["comparable"]:
            parts.append(table(["Engine", "Before recommended", "After recommended"],
                               [[key, fraction(comparison["before"]["engines"][key], "recommended"), fraction(row, "recommended")] for key, row in groups.items()]))
            for key, row in groups.items():
                parts.append(f"<h3>{escape(key)}: question movement (before → after)</h3>")
                movements = []
                previous = comparison["before"]["engines"][key]
                for q in data["questions"]:
                    for brand in [data["brand"], *data["rivals"]]:
                        name = brand["name"]
                        old = previous["questions"][q["id"]] if name == data["brand"]["name"] else previous["rival_questions"][name][q["id"]]
                        new = row["questions"][q["id"]] if name == data["brand"]["name"] else row["rival_questions"][name][q["id"]]
                        movements.append([q["text"], name, *[f"{left} → {right}" for left, right in zip(counts(old), counts(new))]])
                parts.append(table(["Buyer question", "Brand", "Mentioned", "Recommended", "First", "Site cited / known"], movements))
        parts.append(f"<p>{escape(comparison['limit'])}</p>")
    for change in data.get("changes", []):
        parts.append(f"<p>{escape(change['date'])}: {escape(change['description'])}</p>")
    ceiling = (f" of ${escape(data['approved_max_usd'])} approved" if data["approved_max_usd"] is not None
               else "; no aggregate customer-wallet ceiling was recorded")
    parts.append(f"<h2>Receipts and evidence</h2><p>Known charged total ${summary['known_cost_usd']}{ceiling}; "
                 f"{summary['unknown_cost_receipts']} receipts have unknown cost.</p>")
    if data.get("budget_note"):
        parts.append(f"<p>{escape(data['budget_note'])}</p>")
    parts.append("<details><summary>Exact plan and requested settings</summary><pre>" + escape(json.dumps(
        {key: data[key] for key in COMPARE_FIELDS}, ensure_ascii=False, indent=2)) + "</pre></details>")
    parts.append(table(["Run ID", "Tool", "Charged USD"], [[r["run_id"], r["tool_id"], r["cost_usd"] if r["cost_usd"] is not None else "unknown"] for r in data["receipts"]]))
    for row in data["observations"]:
        parts.append(f"<details id=\"observation-{escape(row['run_id'])}\"><summary>{escape(row['engine'])} · {escape(row['phase'])} · {escape(row['question_id'])} · "
                     f"round {row['round']} · {escape(row['status'])}</summary><pre>{escape(json.dumps(row, ensure_ascii=False, indent=2))}</pre></details>")
    return """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>AI visibility and citation plan</title><style>body{font:16px/1.55 system-ui;max-width:1100px;margin:40px auto;padding:0 24px;color:#17212b;background:#fafbfc}h1,h2,h3{line-height:1.2}h2{margin-top:40px}table{border-collapse:collapse;width:100%;display:block;overflow:auto;margin:16px 0}th,td{text-align:left;padding:10px;border-bottom:1px solid #d8dee5;vertical-align:top}th{background:#eaf0f5}article{background:white;border:1px solid #d8dee5;padding:20px;margin:16px 0;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef2f5;padding:16px}a{color:#075e9b;overflow-wrap:anywhere}summary{cursor:pointer;padding:8px}blockquote{margin-left:0;border-left:3px solid #8bacc5;padding-left:16px}</style><body>""" + "\n".join(parts) + "</body></html>"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="New private directory")
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text())
        summary = summarize(data)
        comparison = compare(json.loads(args.baseline.read_text()), data) if args.baseline else None
        report = render(data, summary, comparison)
        args.output.mkdir(mode=0o700, parents=True, exist_ok=False)
        files = {"report.html": report, "checkpoint.json": json.dumps(data, indent=2, ensure_ascii=False),
                 "summary.json": json.dumps({**summary, "comparison": comparison}, indent=2, ensure_ascii=False)}
        for name, content in files.items():
            path = args.output / name
            path.touch(mode=0o600)
            path.write_text(content + "\n")
        path = args.output / "observations.csv"
        path.touch(mode=0o600)
        with path.open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["engine", "phase", "question", "round", "status", "run_id", "model", "retrieved_at"])
            for row in data["observations"]:
                # Spreadsheet formula injection protection for every text cell.
                writer.writerow([("'" + str(v)) if re.match(r"^\s*[=+\-@]|^[\t\r\n]", str(v)) else v for v in
                                 [row["engine"], row["phase"], row["question_id"], row["round"], row["status"], row["run_id"], row["model"] or "unknown", row["retrieved_at"]]])
        print(args.output / "report.html")
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, f"Cannot build report: {error}\n")


if __name__ == "__main__":
    main()
