"""Read-only 3D projection shared by the local editor and standalone snapshots."""
import base64
import hashlib
import json
from pathlib import Path

STATIC = Path(__file__).with_name("static")
EDGE_KINDS = {"relation", "mapping"}
LOCAL_LIMIT = 80


def project_view(state, focus=None, full=False, *, all_neighbors=False):
    doc = state["document"]
    events = doc.get("knowledge", {}).get("change_events", [])
    event = next((e for e in reversed(events) if e.get("changed_asset_ids")), {})
    return projection(doc.get("model", {}).get("semantic", {}).get("assets", []),
                      state["revision"], focus, full, event, all_neighbors=all_neighbors)


def _scope_text(value):
    if isinstance(value, dict):
        return " · ".join(f"{key}: {_scope_text(item)}" for key, item in value.items())
    if isinstance(value, list):
        return ", ".join(_scope_text(item) for item in value)
    return "" if value is None else str(value)


def _details(asset):
    properties = asset.get("properties", {})
    evidence = [{k: e[k] for k in ("type", "source_id", "revision", "fragment_id", "quote") if k in e}
                for e in asset.get("evidence", []) if isinstance(e, dict)]
    values = dict(domain=asset.get("domain"), definition=asset.get("definition"),
                  scopeText=_scope_text(asset.get("scope")), evidence=evidence,
                  gaps=properties.get("knowledge_gaps"))
    if asset["kind"] == "metric":
        values.update((key, properties.get(key)) for key in ("inclusions", "exclusions", "grain"))
    return {key: value for key, value in values.items() if value}


def projection(assets, revision, focus=None, full=False, event=None, *, all_neighbors=False):
    if focus and full:
        raise ValueError("Choose one scope / 指定对象或全量图，请选其一")
    if all_neighbors and not focus:
        raise ValueError("Use --all-neighbors with --id / 展开全部直接关系时请指定对象 ID")
    event = event or {}
    changes = set(event.get("changed_asset_ids", []))
    active = {a["id"]: a for a in assets if a.get("status") != "retired"}
    if focus and focus not in active:
        raise ValueError("Asset is absent or retired at this revision / 此修订中找不到该有效对象")
    # A relationship is normally an edge. Give it a selectable node as well when
    # another definition references it or the author has only supplied one end.
    proxies = set()
    for i, a in active.items():
        endpoints = {a.get("from"), a.get("to")}
        refs = set(a.get("refs", []))
        if a["kind"] in EDGE_KINDS:
            if refs - endpoints or not all(end in active for end in endpoints):
                proxies.add(i)
            refs.update(endpoints)
        proxies.update(key for key in refs if key in active and active[key]["kind"] in EDGE_KINDS)
    objects = {i: a for i, a in active.items() if a["kind"] not in EDGE_KINDS or i in proxies}
    edges = []
    for i, a in active.items():
        is_edge = a["kind"] in EDGE_KINDS
        if is_edge:
            if a.get("from") in objects and a.get("to") in objects:
                edges.append(dict(id=i, source=a["from"], target=a["to"], kind=a["kind"],
                                  label=a.get("predicate") or a["name"], status=a["status"], changed=i in changes))
            if i in proxies:
                for role in ("from", "to"):
                    if a.get(role) in objects:
                        edges.append(dict(id=f"end/{i}/{role}", source=i, target=a[role], kind=role, changed=False))
        if i in objects:
            for j, target in enumerate(a.get("refs", [])):
                if target not in objects or (is_edge and target in (a.get("from"), a.get("to"))):
                    continue
                kind = "owner" if a["kind"] == "field" and objects[target]["kind"] == "dataset" else "ref"
                edges.append(dict(id=f"ref/{i}/{j}", source=i, target=target, kind=kind, changed=False))
    connections = {e["id"]: e for e in edges if e["kind"] in EDGE_KINDS}
    def priority(i):
        a = active[i]
        return (a["kind"] == "field", a["kind"] not in EDGE_KINDS, a["kind"] == "dataset", i)
    roots = [focus] if focus else sorted(changes & active.keys(), key=priority)
    if not roots and not changes and objects:
        roots = [min(objects, key=priority)]
    anchors = {}
    for i in roots:
        if i in objects:
            anchors[i] = None
        if i in connections:
            e = connections[i]
            anchors.update(dict.fromkeys((e["source"], e["target"])))
    if focus and not anchors:
        raise ValueError("This relationship has no drawable endpoints / 此关系没有可绘制的两端")
    neighborhood = dict(anchors)
    if not full:
        for e in edges:
            if e["source"] in anchors or e["target"] in anchors:
                neighborhood.update(dict.fromkeys((e["source"], e["target"])))
    shown = objects.keys() if full else (neighborhood.keys() if all_neighbors else set(list(neighborhood)[:LOCAL_LIMIT]))
    nodes = [dict(id=i, label=a["name"], kind=a["kind"], status=a["status"], changed=i in changes, **_details(a))
             for i, a in objects.items() if i in shown]
    links = edges if full else [e for e in edges if e["source"] in shown and e["target"] in shown]
    for edge in links:
        if edge["kind"] in EDGE_KINDS:
            edge.update(_details(active[edge["id"]]))
    inactive = [c for c in event.get("asset_changes", []) if c["id"] not in active] if not focus else []
    return dict(revision=revision, changeRevision=event.get("revision"), full=full, focus=focus, allNeighbors=all_neighbors,
                center=next(iter(anchors), None), nodes=nodes, edges=links,
                eligible=len(objects) if full else len(neighborhood), total=len(objects),
                changedCount=len(changes), inactiveCount=len(inactive),
                inactiveNames=[c["name"] for c in inactive[:10]])


def save_html(data, output, language):
    output = Path(output)
    if output.suffix.lower() != ".html":
        raise ValueError("Choose a new .html file / 请选择新的 .html 文件")
    template = (STATIC / "graph-view.html").read_text(encoding="utf8")
    script_hashes = []
    for src in ("vendor/force-graph-3d.js", "graph-view.js"):
        js = (STATIC / src).read_text(encoding="utf8").replace("</script", "<\\/script")
        digest = base64.b64encode(hashlib.sha256(js.encode("utf8")).digest()).decode("ascii")
        script_hashes.append(f"'sha256-{digest}'")
        template = template.replace(f'<script src="/{src}"></script>', '<script>'+js+'</script>')
    policy = ("default-src 'none'; connect-src 'none'; script-src " + " ".join(script_hashes)
              + "; style-src 'unsafe-inline'; img-src data: blob:; base-uri 'none'; form-action 'none'")
    template = template.replace('<meta charset="utf-8">', '<meta charset="utf-8">'
                                f'<meta http-equiv="Content-Security-Policy" content="{policy}">')
    css = (STATIC / "graph-view.css").read_text(encoding="utf8")
    template = template.replace('<link rel="stylesheet" href="/graph-view.css">', '<style>'+css+'</style>')
    notices = (STATIC / "vendor/force-graph-3d-LICENSE.txt").read_text(encoding="utf8")
    # This file can travel separately from the installed skill.
    notice_data = json.dumps(notices, ensure_ascii=True).replace("<", "\\u003c")
    template = template.replace("</head>", '<script type="application/json" id="third-party-notices">'
                                + notice_data + '</script></head>')
    payload = json.dumps(dict(data=data, language=language), ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    template = template.replace('<meta name="session-token" content="__SESSION_TOKEN__">',
                                '<script type="application/json" id="snapshot">'+payload+'</script>')
    written = False
    try:
        with output.open("x", encoding="utf8", newline="\n") as stream:
            written = True
            stream.write(template)
    except OSError:
        if written:
            output.unlink(missing_ok=True)
        raise
    scope = "all" if data["full"] else ("neighbors" if data.get("allNeighbors") else "local")
    return {"revision": data["revision"], "output": str(output.resolve()), "scope": scope,
            "nodes": len(data["nodes"]), "edges": len(data["edges"]), "eligible_nodes": data["eligible"]}
