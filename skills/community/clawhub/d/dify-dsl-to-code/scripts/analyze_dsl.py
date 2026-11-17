#!/usr/bin/env python3
"""Analyze a Dify exported DSL (YAML) file.

Outputs a structured JSON analysis used to plan code generation:
- app metadata (name / mode / description / dsl version)
- node inventory (id, type, title, key config)
- edge graph
- external requirements (model providers, tools/plugins, knowledge bases,
  http endpoints, env/secret variables) == the "missing info" checklist
- functional blocks (linear chains between branch/merge points) for
  multi-agent, block-by-block implementation of large workflows

Usage:
    python analyze_dsl.py <dsl_file> [--out analysis.json] [--blocks-dir blocks/]

Exit codes: 0 ok, 1 file/parse error, 2 missing dependency (pyyaml).
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERROR: pyyaml not installed. Run: pip install pyyaml\n"
    )
    sys.exit(2)

# Node types that end a chain (terminals) or split/merge flow (junctions)
JUNCTION_TYPES = {"if-else", "question-classifier", "iteration", "loop",
                  "variable-aggregator", "answer", "end"}
TERMINAL_TYPES = {"answer", "end"}

# Config keys per node type that matter for code generation
KEY_CONFIG = {
    "llm": ["model", "prompt_template", "structured_output_enabled",
            "vision_enabled"],
    "agent": ["agent_strategy", "tools"],
    "code": ["code_language", "code", "outputs"],
    "template-transform": ["template"],
    "http-request": ["method", "url", "headers", "body", "authorization"],
    "tool": ["provider_id", "provider_type", "tool_name",
             "tool_configurations"],
    "knowledge-retrieval": ["dataset_ids", "retrieval_mode",
                            "multiple_retrieval_config"],
    "question-classifier": ["classes", "model"],
    "if-else": ["conditions", "logical_operator"],
    "parameter-extractor": ["parameters", "model"],
    "document-extractor": ["variable_selector"],
    "list-operator": ["filter_conditions"],
    "variable-assigner": ["items"],
    "iteration": ["iterator_selector", "output_selector"],
    "loop": ["loop_variables", "break_conditions"],
    "start": ["variables"],
    "answer": ["answer"],
    "end": ["outputs"],
}

SECRET_RE = re.compile(r"\{\{\s*#?(secret|env)\.[^}]*\}\}")


def load_dsl(path):
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    if not isinstance(doc, dict) or "workflow" not in doc:
        raise ValueError(
            "Not a recognizable Dify workflow/chatflow DSL: "
            "top-level 'workflow' key missing. "
            "(Agent / basic-chat apps export differently — check app.mode)"
        )
    return doc


def node_key_config(node):
    data = node.get("data", {})
    ntype = data.get("type", "unknown")
    cfg = {}
    for key in KEY_CONFIG.get(ntype, []):
        if key in data:
            val = data[key]
            # Truncate large inline code/prompt blobs, keep them discoverable
            s = json.dumps(val, ensure_ascii=False)
            cfg[key] = val if len(s) <= 600 else (
                s[:600] + f"... [TRUNCATED {len(s)} chars total]"
            )
    return cfg


def scan_secrets(obj, hits):
    """Recursively find {{secret.*}} / {{env.*}} variable references."""
    if isinstance(obj, str):
        for m in SECRET_RE.finditer(obj):
            hits.add(m.group(0))
    elif isinstance(obj, dict):
        for v in obj.values():
            scan_secrets(v, hits)
    elif isinstance(obj, list):
        for v in obj:
            scan_secrets(v, hits)


def build_blocks(nodes, edges):
    """Split graph into functional blocks: maximal linear chains between
    junction nodes (branch/merge/loop) and terminals. Deterministic so
    multiple agents can each own one block and reassemble consistently."""
    node_ids = {n["id"] for n in nodes}
    out_deg = defaultdict(int)
    in_deg = defaultdict(int)
    adj = defaultdict(list)
    for e in edges:
        s, t = e.get("source"), e.get("target")
        if s in node_ids and t in node_ids:
            adj[s].append(t)
            out_deg[s] += 1
            in_deg[t] += 1

    ntype = {n["id"]: n.get("data", {}).get("type", "") for n in nodes}
    ntitle = {n["id"]: (n.get("data", {}).get("title")
                       or n.get("data", {}).get("type")
                       or n["id"]) for n in nodes}

    def is_boundary(nid):
        return (out_deg[nid] != 1 or in_deg[nid] > 1
                or ntype[nid] in JUNCTION_TYPES)

    visited_edges = set()
    blocks = []
    starts = [nid for nid in node_ids if in_deg[nid] == 0] or \
             [n["id"] for n in nodes[:1]]
    queue = list(starts)
    seen_start = set()
    while queue:
        start = queue.pop(0)
        for nxt in adj.get(start, []):
            if (start, nxt) in visited_edges:
                continue
            chain = [start] if is_boundary(start) or in_deg[start] == 0 else []
            cur = nxt
            while True:
                visited_edges.add((chain[-1] if chain else start, cur)
                                  if chain else (start, cur))
                chain.append(cur)
                if is_boundary(cur) or not adj.get(cur):
                    for d in adj.get(cur, []):
                        if (cur, d) not in visited_edges and d not in seen_start:
                            queue.append(cur)
                            seen_start.add(cur)
                    break
                nxt2 = adj[cur][0]
                cur = nxt2
            if chain:
                blocks.append(chain)

    # Any nodes never visited (isolated) become singleton blocks
    covered = {nid for b in blocks for nid in b}
    for nid in node_ids - covered:
        blocks.append([nid])

    return [
        {
            "block_id": f"block_{i + 1:02d}",
            "name": (ntitle[b[0]] if b[0] == b[-1]
                     else f"{ntitle[b[0]]} → {ntitle[b[-1]]}"),
            "node_ids": b,
            "node_types": [ntype[nid] for nid in b],
            "entry": b[0],
            "exit": b[-1],
            "size": len(b),
        }
        for i, b in enumerate(blocks)
    ]


def analyze(path):
    doc = load_dsl(path)
    app = doc.get("app", {})
    wf = doc.get("workflow", {})
    graph = wf.get("graph", {})
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []

    node_list = [
        {
            "id": n["id"],
            "type": n.get("data", {}).get("type", "unknown"),
            "title": n.get("data", {}).get("title", n["id"]),
            "config": node_key_config(n),
        }
        for n in nodes
    ]

    # --- External requirements / missing-info checklist ---
    model_providers = sorted({
        n.get("data", {}).get("model", {}).get("provider")
        for n in nodes if n.get("data", {}).get("type") in ("llm", "agent",
                                                            "question-classifier",
                                                            "parameter-extractor")
        and n.get("data", {}).get("model", {}).get("provider")
    })
    tools = sorted({
        f'{n.get("data", {}).get("provider_id")}/{n.get("data", {}).get("tool_name")}'
        for n in nodes if n.get("data", {}).get("type") == "tool"
    } - {"/"})
    datasets = sorted({
        ds for n in nodes
        if n.get("data", {}).get("type") == "knowledge-retrieval"
        for ds in (n.get("data", {}).get("dataset_ids") or [])
    })
    http_endpoints = sorted({
        n.get("data", {}).get("url", "")
        for n in nodes if n.get("data", {}).get("type") == "http-request"
    } - {""})

    secret_refs = set()
    scan_secrets(doc, secret_refs)
    env_vars = [
        {"name": v.get("name"), "value_type": v.get("value_type"),
         "has_value": bool(v.get("value"))}
        for v in (wf.get("environment_variables") or [])
    ]
    conv_vars = [
        {"name": v.get("name"), "value_type": v.get("value_type")}
        for v in (wf.get("conversation_variables") or [])
    ]
    plugin_deps = []
    for d in (doc.get("dependencies") or []):
        v = d.get("value") or {}
        ident = v.get("marketplace_plugin_unique_identifier")
        if ident:
            plugin_deps.append(ident.split("@")[0])
        elif v.get("plugin_unique_identifier"):
            plugin_deps.append(v["plugin_unique_identifier"].split("@")[0])
        else:
            plugin_deps.append(str(v)[:120])

    agent_strategies = sorted({
        n.get("data", {}).get("agent_strategy", {}).get("name", "unknown")
        if isinstance(n.get("data", {}).get("agent_strategy"), dict)
        else str(n.get("data", {}).get("agent_strategy"))
        for n in nodes if n.get("data", {}).get("type") == "agent"
    } - {""})

    # --- flags: things that force a user decision during codegen ---
    js_code_nodes = [
        n.get("data", {}).get("title", n["id"])
        for n in nodes
        if n.get("data", {}).get("type") == "code"
        and n.get("data", {}).get("code_language") == "javascript"
    ]
    features = wf.get("features") or {}
    file_upload = features.get("file_upload") or {}
    file_inputs = [
        v.get("variable")
        for n in nodes if n.get("data", {}).get("type") == "start"
        for v in (n.get("data", {}).get("variables") or [])
        if v.get("type") in ("file", "file-list")
    ]
    types_present = {n.get("data", {}).get("type") for n in nodes}
    flags = {
        "file_upload_enabled": bool(file_upload.get("enabled")),
        "file_input_variables": file_inputs,
        "javascript_code_nodes": js_code_nodes,
        "has_iteration": "iteration" in types_present,
        "has_loop": "loop" in types_present,
        "uses_conversation_variables": bool(conv_vars)
        or "variable-assigner" in types_present,
    }

    blocks = build_blocks(nodes, edges)

    return {
        "app": {
            "name": app.get("name", "unnamed-app"),
            "mode": app.get("mode", "unknown"),
            "description": app.get("description", ""),
            "icon": app.get("icon", ""),
        },
        "dsl_version": doc.get("version", "unknown"),
        "stats": {
            "nodes": len(nodes),
            "edges": len(edges),
            "blocks": len(blocks),
            "file_bytes": os.path.getsize(path),
        },
        "nodes": node_list,
        "edges": [
            {"source": e.get("source"), "target": e.get("target"),
             "sourceHandle": e.get("sourceHandle")}
            for e in edges
        ],
        "external_requirements": {
            "model_providers": model_providers,
            "tools": tools,
            "agent_strategies": agent_strategies,
            "knowledge_datasets": datasets,
            "http_endpoints": http_endpoints,
            "secret_variable_refs": sorted(secret_refs),
            "environment_variables": env_vars,
            "conversation_variables": conv_vars,
            "plugin_dependencies": plugin_deps,
        },
        "flags": flags,
        "blocks": blocks,
    }


def write_block_dsls(doc, blocks, out_dir):
    """Write per-block subgraph YAML files so each agent gets a focused slice."""
    os.makedirs(out_dir, exist_ok=True)
    graph = doc["workflow"]["graph"]
    nodes_by_id = {n["id"]: n for n in graph.get("nodes", [])}
    written = []
    for b in blocks:
        ids = set(b["node_ids"])
        sub = {
            "block_id": b["block_id"],
            "block_name": b["name"],
            "entry": b["entry"],
            "exit": b["exit"],
            "nodes": [nodes_by_id[i] for i in b["node_ids"] if i in nodes_by_id],
            "edges": [e for e in graph.get("edges", [])
                      if e.get("source") in ids and e.get("target") in ids],
            # boundary edges tell the agent how this block connects outward
            "incoming_edges": [e for e in graph.get("edges", [])
                               if e.get("target") in ids
                               and e.get("source") not in ids],
            "outgoing_edges": [e for e in graph.get("edges", [])
                               if e.get("source") in ids
                               and e.get("target") not in ids],
        }
        safe = "".join(c if c.isalnum() else "_" for c in b["name"])[:40]
        path = os.path.join(out_dir, f'{b["block_id"]}_{safe}.yaml')
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(sub, f, allow_unicode=True, sort_keys=False)
        written.append(path)
    return written


def main():
    ap = argparse.ArgumentParser(description="Analyze a Dify DSL export.")
    ap.add_argument("dsl_file")
    ap.add_argument("--out", help="Write analysis JSON here (default: stdout)")
    ap.add_argument("--blocks-dir",
                    help="Also write per-block subgraph YAMLs to this dir")
    args = ap.parse_args()

    if not os.path.isfile(args.dsl_file):
        sys.stderr.write(f"ERROR: file not found: {args.dsl_file}\n")
        sys.exit(1)
    try:
        result = analyze(args.dsl_file)
    except Exception as e:  # noqa: BLE001 - surface any parse issue clearly
        sys.stderr.write(f"ERROR: failed to parse DSL: {e}\n")
        sys.exit(1)

    if args.blocks_dir:
        doc = load_dsl(args.dsl_file)
        files = write_block_dsls(doc, result["blocks"], args.blocks_dir)
        result["block_files"] = files

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        sys.stderr.write(f"Analysis written to {args.out}\n")
    else:
        print(payload)


if __name__ == "__main__":
    main()
