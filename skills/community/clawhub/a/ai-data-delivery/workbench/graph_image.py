"""Render an immutable, bounded view of one saved revision as a local SVG."""
import html
import re
import unicodedata

from workbench.semantic_package import KIND_LABELS


def _clean(value):
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff\ufffe\uffff]", "", str(value))


def _text(x, y, value, width, size=17, color="#203733"):
    value = _clean(value)
    label, units = [], 0
    for char in " ".join(value.split()):
        units += 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
        if (units + 2) * size * 0.59 > width:
            label.append("…")
            break
        label.append(char)
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}"><title>{html.escape(value)}</title>'
            f'{html.escape("".join(label))}</text>')


def _notes(focus, sources, zh):
    props = focus.get("properties", {})
    conflict = props.get("unresolved_conflicts")
    if conflict:
        pending = list(conflict) if isinstance(conflict, list) else [conflict]
        claims = []
        for item in pending:
            if isinstance(item, dict) and isinstance(item.get("claims"), list):
                pending.extend(item["claims"])
                continue
            claim = (item.get("claim") or item.get("quote")) if isinstance(item, dict) else item
            if claim:
                name = sources.get(item.get("source_id")) if isinstance(item, dict) else None
                claims.append(f"{name} · {claim}" if name else str(claim))
        header = ("来源说法待核对" if zh else "Unresolved source claims") + f" · {len(claims)}"
        return [header, *claims[:4]]
    decisions = props.get("conflict_resolutions")
    if isinstance(decisions, list) and decisions and isinstance(decisions[-1], dict) and decisions[-1].get("decision"):
        return [("已记录裁决 · " if zh else "Recorded decision · ") + str(decisions[-1]["decision"]),
                ("当前定义 · " if zh else "Current definition · ") + str(focus["definition"])]
    evidence = focus.get("evidence", [])
    quote = next((e.get("quote") for e in evidence if e.get("quote")), None)
    return [(("依据摘录 · " if zh else "Evidence excerpt · ") + str(quote))] if quote else []


def render_graph(state, focus_id, language):
    assets = state["document"].get("model", {}).get("semantic", {}).get("assets", [])
    index = {a["id"]: a for a in assets if a["status"] != "retired"}
    zh = language == "zh"
    edges = [a for a in index.values() if a["kind"] in {"relation", "mapping"}
             and a.get("from") in index and a.get("to") in index]
    if focus_id is None:
        focus_id = edges[0]["from"] if edges else next(iter(index), None)
    if focus_id not in index:
        raise ValueError("Choose an active asset in this revision / 请选择该修订中有效的对象")
    focus = index[focus_id]
    rows = [(index[e["from"]], e, index[e["to"]]) for e in edges
            if focus_id in (e["id"], e["from"], e["to"])]
    for asset in index.values():
        for ref in asset.get("refs", []):
            if ref in index and focus_id in (asset["id"], ref):
                rows.append((asset, None, index[ref]))
    shown = rows[:6]
    source_names = {s["id"]: s["name"] for s in state["document"].get("knowledge", {}).get("sources", [])}
    notes = _notes(focus, source_names, zh)
    height = 227 + len(shown) * 84 + max(0, len(notes)-1)*24
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="{height}" viewBox="0 0 1040 {height}" role="img">',
           f'<title>{html.escape(_clean(focus["name"]))}</title>',
           '<style>text{font-family:"Segoe UI","Microsoft YaHei","Noto Sans CJK SC",sans-serif}</style>',
           '<rect width="100%" height="100%" fill="#f5f8f6"/>',
           _text(30,36,("模型修订 " if zh else "Model revision ") + str(state["revision"]),970,16),
           _text(30,80,focus["name"],970,31)]
    meta = f'{KIND_LABELS.get(focus["kind"], focus["kind"]) if zh else focus["kind"]} · {focus["id"]}'
    svg.append(_text(30,111,meta,970,16))
    status_names = {"confirmed":"已确认","draft":"草稿","needs_review":"待复核"}
    def card(x, y, asset):
        status = status_names.get(asset["status"], asset["status"]) if zh else asset["status"]
        kind = KIND_LABELS.get(asset["kind"], asset["kind"]) if zh else asset["kind"]
        aid = asset["id"]
        role = asset.get("properties", {}).get("role")
        identity = f"{role} · {aid}" if role else aid
        return (f'<g data-asset-id="{html.escape(_clean(aid), quote=True)}">'
                f'<rect x="{x}" y="{y}" rx="7" width="305" height="69" fill="white" stroke="#809e93"/>'
                + _text(x+14,y+24,asset["name"],280,19)
                + _text(x+14,y+43,identity,277,14)
                + _text(x+14,y+61,f'{kind} · {status}',275,13) + '</g>')
    for i, (left, edge, right) in enumerate(shown):
        y = 134 + i*84
        svg.extend([card(30,y,left),card(705,y,right),
                    f'<path d="M335 {y+37}H697m-9 -5 9 5 -9 5" fill="none" stroke="#39745f" stroke-width="2"/>'])
        label = (edge.get("predicate") or edge["name"]) if edge else ("定义引用" if zh else "Definition reference")
        svg.append(_text(354,y+26,label,328,17))
        if edge:
            count = len(edge.get("evidence", []))
            status = status_names.get(edge["status"], edge["status"]) if zh else edge["status"]
            svg.append(_text(354,y+59,f'{status} · {count} ' + ("项依据" if zh else "evidence items"),328,14))
    if not shown:
        svg.append(_text(30,149,"当前对象没有已声明的关系" if zh else "No declared connections for this object",960))
    for i, line in enumerate(notes):
        svg.append(_text(30,height-54-(len(notes)-1-i)*24,line,980,16))
    summary = f'显示 {len(shown)} / {len(rows)} 条直接关联' if zh else f'Showing {len(shown)} of {len(rows)} direct connections'
    svg.extend([_text(30,height-22,summary,960,15)," </svg>"])
    return "\n".join(svg), {"revision": state["revision"], "focus_id": focus_id,
                             "shown": len(shown), "total_connections": len(rows)}
