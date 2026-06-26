#!/usr/bin/env python3
"""Repair agentmemory knowledge graph updates and backfill on Windows."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


GENERIC_TITLES = {
    "bash",
    "edit",
    "glob",
    "grep",
    "read",
    "write",
    "todowrite",
    "post_tool_use",
    "post_tool_failure",
    "prompt_submit",
    "stop",
}

STOP_EXTRACT_OLD = """async function extractGraphForSession(sessionId) {
\tif (process.env["GRAPH_EXTRACTION_ENABLED"] !== "true") return;
\tconst result = await getJson(`observations?sessionId=${encodeURIComponent(sessionId)}`, 30000);
\tconst observations = (result && Array.isArray(result.observations) ? result.observations : [])
\t\t.filter((o) => o && typeof o.title === "string" && o.title.length > 0);
\tif (observations.length === 0) return;
\tawait postJson("graph/extract", { observations }, 120000);
}"""

STOP_EXTRACT_NEW = """async function serverFlagEnabled(key) {
\tconst config = await getJson("config/flags", 5000);
\tconst flags = config && Array.isArray(config.flags) ? config.flags : [];
\tconst flag = flags.find((f) => f && f.key === key);
\treturn !flag || flag.enabled !== false;
}

async function extractGraphForSession(sessionId) {
\tif (process.env["GRAPH_EXTRACTION_ENABLED"] === "false") return;
\tif (process.env["GRAPH_EXTRACTION_ENABLED"] !== "true" && !(await serverFlagEnabled("GRAPH_EXTRACTION_ENABLED"))) return;
\tconst result = await getJson(`observations?sessionId=${encodeURIComponent(sessionId)}`, 30000);
\tconst observations = (result && Array.isArray(result.observations) ? result.observations : [])
\t\t.filter((o) => o && typeof o.title === "string" && o.title.length > 0);
\tif (observations.length === 0) return;
\tconst batchSize = Number.parseInt(process.env["AGENTMEMORY_GRAPH_BATCH_SIZE"] || "25", 10) || 25;
\tfor (let i = 0; i < observations.length; i += batchSize) {
\t\tawait postJson("graph/extract", { observations: observations.slice(i, i + batchSize) }, 120000);
\t}
}"""

GRAPH_EDGE_OLD = """\t\t\tconst existingNodes = await kv.list(KV.graphNodes);
\t\t\tconst existingEdges = await kv.list(KV.graphEdges);
\t\t\tfor (const node of nodes) {
\t\t\t\tconst existing = existingNodes.find((n) => n.name === node.name && n.type === node.type);
\t\t\t\tif (existing) {
\t\t\t\t\tconst merged = {
\t\t\t\t\t\t...existing,
\t\t\t\t\t\tsourceObservationIds: [...new Set([...existing.sourceObservationIds, ...obsIds])],
\t\t\t\t\t\tproperties: {
\t\t\t\t\t\t\t...existing.properties,
\t\t\t\t\t\t\t...node.properties
\t\t\t\t\t\t}
\t\t\t\t\t};
\t\t\t\t\tawait kv.set(KV.graphNodes, existing.id, merged);
\t\t\t\t\tconst idx = existingNodes.findIndex((n) => n.id === existing.id);
\t\t\t\t\tif (idx !== -1) existingNodes[idx] = merged;
\t\t\t\t} else {
\t\t\t\t\tawait kv.set(KV.graphNodes, node.id, node);
\t\t\t\t\texistingNodes.push(node);
\t\t\t\t}
\t\t\t}
\t\t\tfor (const edge of edges) {
\t\t\t\tconst edgeKey = `${edge.sourceNodeId}|${edge.targetNodeId}|${edge.type}`;
\t\t\t\tconst existingEdge = existingEdges.find((e) => `${e.sourceNodeId}|${e.targetNodeId}|${e.type}` === edgeKey);"""

GRAPH_EDGE_NEW = """\t\t\tconst existingNodes = await kv.list(KV.graphNodes);
\t\t\tconst existingEdges = await kv.list(KV.graphEdges);
\t\t\tconst nodeIdMap = /* @__PURE__ */ new Map();
\t\t\tfor (const node of nodes) {
\t\t\t\tconst existing = existingNodes.find((n) => n.name === node.name && n.type === node.type);
\t\t\t\tif (existing) {
\t\t\t\t\tnodeIdMap.set(node.id, existing.id);
\t\t\t\t\tconst merged = {
\t\t\t\t\t\t...existing,
\t\t\t\t\t\tsourceObservationIds: [...new Set([...(existing.sourceObservationIds || []), ...obsIds])],
\t\t\t\t\t\tproperties: {
\t\t\t\t\t\t\t...existing.properties,
\t\t\t\t\t\t\t...node.properties
\t\t\t\t\t\t}
\t\t\t\t\t};
\t\t\t\t\tawait kv.set(KV.graphNodes, existing.id, merged);
\t\t\t\t\tconst idx = existingNodes.findIndex((n) => n.id === existing.id);
\t\t\t\t\tif (idx !== -1) existingNodes[idx] = merged;
\t\t\t\t} else {
\t\t\t\t\tnodeIdMap.set(node.id, node.id);
\t\t\t\t\tawait kv.set(KV.graphNodes, node.id, node);
\t\t\t\t\texistingNodes.push(node);
\t\t\t\t}
\t\t\t}
\t\t\tconst persistedNodeIds = new Set(existingNodes.map((n) => n.id));
\t\t\tfor (const edge of edges) {
\t\t\t\tedge.sourceNodeId = nodeIdMap.get(edge.sourceNodeId) || edge.sourceNodeId;
\t\t\t\tedge.targetNodeId = nodeIdMap.get(edge.targetNodeId) || edge.targetNodeId;
\t\t\t\tif (!persistedNodeIds.has(edge.sourceNodeId) || !persistedNodeIds.has(edge.targetNodeId)) continue;
\t\t\t\tconst edgeKey = `${edge.sourceNodeId}|${edge.targetNodeId}|${edge.type}`;
\t\t\t\tconst existingEdge = existingEdges.find((e) => `${e.sourceNodeId}|${e.targetNodeId}|${e.type}` === edgeKey);"""


def parse_args() -> argparse.Namespace:
    default_codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=default_codex_home)
    parser.add_argument("--url", default=None, help="agentmemory REST URL")
    parser.add_argument("--secret", default=None, help="agentmemory bearer secret")
    parser.add_argument("--plugin-root", type=Path, default=None)
    parser.add_argument("--agentmemory-package-root", type=Path, action="append", default=[])
    parser.add_argument("--state-store-dir", type=Path, default=Path.home() / "data" / "state_store.db")
    parser.add_argument("--patch-hooks", action="store_true", help="Patch stop.mjs graph finalization.")
    parser.add_argument("--patch-service", action="store_true", help="Patch dist/index.mjs graph edge ID remapping.")
    parser.add_argument("--backfill", action="store_true", help="Backfill graph from existing observations.")
    parser.add_argument("--all", action="store_true", help="Patch hooks, patch service, and backfill.")
    parser.add_argument("--restart-service", action="store_true", help="Restart local agentmemory after patching.")
    parser.add_argument("--min-importance", type=int, default=5)
    parser.add_argument("--max-files", type=int, default=2)
    parser.add_argument("--max-concepts", type=int, default=3)
    parser.add_argument("--no-title-concepts", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    out = path.with_name(f"{path.name}.bak-agentmemory-graph-{stamp()}")
    shutil.copy2(path, out)
    return out


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_if_changed(path: Path, text: str, dry_run: bool) -> bool:
    if read_text(path) == text:
        return False
    if dry_run:
        print(f"would update: {path}")
        return True
    backup(path)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def read_agentmemory_env() -> dict[str, str]:
    path = Path.home() / ".agentmemory" / ".env"
    if not path.exists():
        return {}
    env: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if value[:1] in {"'", '"'}:
            quote = value[0]
            end = value.find(quote, 1)
            value = value[1:end] if end != -1 else value[1:]
        else:
            value = re.sub(r"\s+#.*$", "", value).strip()
        env[key.strip()] = value
    return env


def extract_config_value(config: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*['\"]([^'\"]*)['\"]", config)
    return match.group(1) if match else None


def read_codex_agentmemory_env(codex_home: Path) -> dict[str, str]:
    config = read_text(codex_home.expanduser() / "config.toml")
    out: dict[str, str] = {}
    for key in ("AGENTMEMORY_URL", "AGENTMEMORY_SECRET"):
        value = extract_config_value(config, key)
        if value:
            out[key] = value
    return out


def npm_global_root() -> Path | None:
    try:
        proc = subprocess.run(
            ["npm.cmd", "root", "-g"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    root = Path(proc.stdout.strip())
    return root if root.exists() else None


def discover_package_roots(explicit: list[Path]) -> list[Path]:
    candidates = [p.expanduser() for p in explicit]
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "npm" / "node_modules" / "@agentmemory" / "agentmemory")
    global_root = npm_global_root()
    if global_root:
        candidates.append(global_root / "@agentmemory" / "agentmemory")
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        candidates.extend(Path(localappdata).glob(r"npm-cache\_npx\*\node_modules\@agentmemory\agentmemory"))

    roots: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            key = str(candidate.resolve()).lower()
        except OSError:
            continue
        if key in seen:
            continue
        seen.add(key)
        if (candidate / "dist" / "index.mjs").exists():
            roots.append(candidate)
    return roots


def discover_stop_scripts(codex_home: Path, plugin_root: Path | None, package_roots: list[Path]) -> list[Path]:
    candidates: list[Path] = []
    if plugin_root:
        candidates.append(plugin_root / "scripts" / "stop.mjs")
    cache_root = codex_home / "plugins" / "cache" / "agentmemory" / "agentmemory"
    if cache_root.exists():
        candidates.extend(cache_root.glob(r"*\scripts\stop.mjs"))
    for root in package_roots:
        candidates.append(root / "plugin" / "scripts" / "stop.mjs")
        candidates.append(root / "dist" / "hooks" / "stop.mjs")

    out: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            key = str(candidate.resolve()).lower()
        except OSError:
            continue
        if key not in seen and candidate.exists():
            seen.add(key)
            out.append(candidate)
    return out


def patch_stop_script(path: Path, dry_run: bool) -> bool:
    text = read_text(path)
    if "serverFlagEnabled(\"GRAPH_EXTRACTION_ENABLED\")" in text and "AGENTMEMORY_GRAPH_BATCH_SIZE" in text:
        print(f"already patched stop hook: {path}")
        return False
    if STOP_EXTRACT_OLD not in text:
        print(f"skip unrecognized stop hook shape: {path}")
        return False
    final = text.replace(STOP_EXTRACT_OLD, STOP_EXTRACT_NEW, 1)
    changed = write_if_changed(path, final, dry_run)
    if changed:
        verb = "would patch" if dry_run else "patched"
        print(f"{verb} stop hook graph extraction: {path}")
    return changed


def patch_service_bundle(path: Path, dry_run: bool) -> bool:
    text = read_text(path)
    if "const nodeIdMap = /* @__PURE__ */ new Map();" in text:
        print(f"already patched graph edge remap: {path}")
        return False
    if GRAPH_EDGE_OLD not in text:
        print(f"skip unrecognized graph service shape: {path}")
        return False
    final = text.replace(GRAPH_EDGE_OLD, GRAPH_EDGE_NEW, 1)
    changed = write_if_changed(path, final, dry_run)
    if changed:
        verb = "would patch" if dry_run else "patched"
        print(f"{verb} graph edge remap: {path}")
    return changed


def request_json(base_url: str, path: str, secret: str, method: str = "GET", body: object | None = None) -> object:
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if secret:
        headers["Authorization"] = f"Bearer {secret}"
    req = Request(f"{base_url.rstrip('/')}/agentmemory/{path.lstrip('/')}", data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=180) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"{method} {path} failed {exc.code}: {raw[:500]}") from exc
    return json.loads(raw) if raw else {}


def hash_id(prefix: str, value: str) -> str:
    return f"{prefix}_det_{hashlib.sha1(value.encode('utf-8')).hexdigest()[:16]}"


def node_key(kind: str, name: str) -> str:
    return f"{kind}:{name.strip().lower()}"


def edge_key(source: str, target: str, kind: str) -> str:
    return f"{source}|{target}|{kind}"


def merge_id(values: object, value: str) -> list[str]:
    result = list(values) if isinstance(values, list) else []
    if value and value not in result:
        result.append(value)
    return result


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", value).strip() if isinstance(value, str) else ""


def normalize_concept(value: object) -> str:
    text = normalize_text(value)
    if len(text) < 2 or len(text) > 120 or re.match(r"^https?://", text, re.I):
        return ""
    return text


def normalize_file(value: object) -> str:
    text = normalize_text(value).replace("\\", "/")
    if len(text) < 2 or len(text) > 260:
        return ""
    return text


def build_graph(export_data: dict, args: argparse.Namespace) -> tuple[list[dict], list[dict], dict[str, int]]:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    nodes_by_key: dict[str, dict] = {}
    nodes_by_id: dict[str, dict] = {}
    edges_by_key: dict[str, dict] = {}

    for node in export_data.get("graphNodes") or []:
        if not all(node.get(k) for k in ("id", "type", "name")):
            continue
        clone = dict(node)
        nodes_by_key[node_key(clone["type"], clone["name"])] = clone
        nodes_by_id[clone["id"]] = clone
    for edge in export_data.get("graphEdges") or []:
        if not all(edge.get(k) for k in ("id", "sourceNodeId", "targetNodeId", "type")):
            continue
        clone = dict(edge)
        edges_by_key[edge_key(clone["sourceNodeId"], clone["targetNodeId"], clone["type"])] = clone

    def ensure_node(kind: str, name: str, obs_id: str) -> dict:
        key = node_key(kind, name)
        existing = nodes_by_key.get(key)
        if existing:
            existing["sourceObservationIds"] = merge_id(existing.get("sourceObservationIds"), obs_id)
            props = dict(existing.get("properties") or {})
            props["deterministicBackfill"] = "true"
            props["lastBackfilledAt"] = now
            existing["properties"] = props
            return existing
        node = {
            "id": hash_id("gn", key),
            "type": kind,
            "name": name,
            "properties": {"deterministicBackfill": "true", "createdBy": "repair_agentmemory_graph_windows"},
            "sourceObservationIds": [obs_id] if obs_id else [],
            "createdAt": now,
        }
        nodes_by_key[key] = node
        nodes_by_id[node["id"]] = node
        return node

    def ensure_edge(source: dict, target: dict, kind: str, obs_id: str, weight: float) -> None:
        if not source or not target or source["id"] == target["id"]:
            return
        key = edge_key(source["id"], target["id"], kind)
        existing = edges_by_key.get(key)
        if existing:
            existing["sourceObservationIds"] = merge_id(existing.get("sourceObservationIds"), obs_id)
            existing["weight"] = max(float(existing.get("weight") or 0), weight)
            return
        edges_by_key[key] = {
            "id": hash_id("ge", key),
            "type": kind,
            "sourceNodeId": source["id"],
            "targetNodeId": target["id"],
            "weight": weight,
            "sourceObservationIds": [obs_id] if obs_id else [],
            "createdAt": now,
            "context": {"source": "deterministic-backfill"},
        }

    considered = 0
    linked = 0
    for session_id, observations in (export_data.get("observations") or {}).items():
        if not isinstance(observations, list):
            continue
        for obs in observations:
            if not isinstance(obs, dict) or not obs.get("id") or not obs.get("title"):
                continue
            if int(obs.get("importance") or 0) < args.min_importance:
                continue
            considered += 1
            obs_id = obs["id"]
            files = list(dict.fromkeys(filter(None, (normalize_file(f) for f in obs.get("files") or []))))[: args.max_files]
            concepts_raw = list(obs.get("concepts") or [])
            if not args.no_title_concepts:
                title = normalize_concept(obs.get("title"))
                if title and title.lower() not in GENERIC_TITLES:
                    concepts_raw.append(title)
            concepts = list(dict.fromkeys(filter(None, (normalize_concept(c) for c in concepts_raw))))[: args.max_concepts]
            if not files and not concepts:
                continue
            linked += 1
            file_nodes = [ensure_node("file", file, obs_id) for file in files]
            concept_nodes = [ensure_node("concept", concept, obs_id) for concept in concepts]
            for file_node in file_nodes:
                for concept_node in concept_nodes:
                    ensure_edge(file_node, concept_node, "related_to", obs_id, 0.65)
            for i, source in enumerate(concept_nodes):
                for target in concept_nodes[i + 1 : min(len(concept_nodes), 4)]:
                    ensure_edge(source, target, "related_to", obs_id, 0.4)

    counts = {
        "observationsConsidered": considered,
        "observationsLinked": linked,
        "nodes": len(nodes_by_id),
        "edges": len(edges_by_key),
    }
    return list(nodes_by_id.values()), list(edges_by_key.values()), counts


def backup_graph_bins(state_store_dir: Path, dry_run: bool) -> None:
    for name in ("mem%3Agraph%3Anodes.bin", "mem%3Agraph%3Aedges.bin"):
        path = state_store_dir.expanduser() / name
        if path.exists():
            if dry_run:
                print(f"would backup graph bin: {path}")
            else:
                print(f"graph bin backup: {backup(path)}")


def backfill_graph(base_url: str, secret: str, args: argparse.Namespace) -> None:
    before = request_json(base_url, "graph/stats", secret)
    export_data = request_json(base_url, "export", secret)
    nodes, edges, counts = build_graph(export_data, args)
    summary = {
        "before": {"nodes": before.get("totalNodes"), "edges": before.get("totalEdges")},
        "candidate": counts,
        "delta": {
            "nodes": len(nodes) - len(export_data.get("graphNodes") or []),
            "edges": len(edges) - len(export_data.get("graphEdges") or []),
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.dry_run:
        return
    backup_graph_bins(args.state_store_dir, dry_run=False)
    payload = {
        "strategy": "merge",
        "exportData": {
            "version": export_data.get("version") or "0.9.21",
            "sessions": [],
            "memories": [],
            "summaries": [],
            "observations": {},
            "graphNodes": nodes,
            "graphEdges": edges,
        },
    }
    imported = request_json(base_url, "import", secret, method="POST", body=payload)
    after = request_json(base_url, "graph/stats", secret)
    print(json.dumps({"imported": imported, "after": after}, ensure_ascii=False, indent=2))


def restart_service(dry_run: bool) -> None:
    command = r"""
$owners = Get-NetTCPConnection -LocalPort 3111,3113 -ErrorAction SilentlyContinue |
  Where-Object { $_.OwningProcess -ne 0 } |
  Select-Object -ExpandProperty OwningProcess -Unique
foreach ($id in $owners) { Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 2
$cmd = Join-Path $env:APPDATA 'npm\agentmemory.cmd'
Start-Process -FilePath $cmd -WorkingDirectory $env:USERPROFILE -WindowStyle Hidden
for ($i = 0; $i -lt 30; $i++) {
  Start-Sleep -Seconds 2
  try {
    $r = Invoke-WebRequest -Uri 'http://localhost:3111/agentmemory/health' -UseBasicParsing -TimeoutSec 5
    if ($r.StatusCode -eq 200) { Write-Output 'agentmemory restarted'; exit 0 }
  } catch {}
}
Write-Error 'agentmemory did not become healthy in time'
exit 1
"""
    if dry_run:
        print("would restart local agentmemory service")
        return
    subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], check=True)


def main() -> None:
    args = parse_args()
    selected = args.patch_hooks or args.patch_service or args.backfill
    if args.all or not selected:
        args.patch_hooks = args.patch_service = args.backfill = True

    env = {**read_agentmemory_env(), **read_codex_agentmemory_env(args.codex_home), **os.environ}
    base_url = args.url or env.get("AGENTMEMORY_URL") or "http://localhost:3111"
    secret = args.secret or env.get("AGENTMEMORY_SECRET") or ""
    package_roots = discover_package_roots(args.agentmemory_package_root)

    print(f"agentmemory URL: {base_url}")
    if package_roots:
        print("package roots:")
        for root in package_roots:
            print(f"  {root}")

    if args.patch_hooks:
        stop_scripts = discover_stop_scripts(args.codex_home.expanduser(), args.plugin_root, package_roots)
        if not stop_scripts:
            print("no stop.mjs hooks found")
        for path in stop_scripts:
            patch_stop_script(path, args.dry_run)

    service_changed = False
    if args.patch_service:
        for root in package_roots:
            service_changed = patch_service_bundle(root / "dist" / "index.mjs", args.dry_run) or service_changed

    if args.restart_service and service_changed:
        restart_service(args.dry_run)
    elif service_changed:
        print("Restart agentmemory so the patched service bundle is loaded.")

    if args.backfill:
        if not secret:
            print("AGENTMEMORY_SECRET not found; continuing without Authorization header.")
        backfill_graph(base_url, secret, args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
