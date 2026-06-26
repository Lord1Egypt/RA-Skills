#!/usr/bin/env python3
"""
knowledge_graph — Build/update a knowledge graph from workspace markdown files.
Extracts entities and relationships using LLM.

Usage:
    knowledge_graph [--rebuild] [--dry-run] [--debug]
"""
from __future__ import annotations
import os, sys
# Cross-platform PATH setup
if sys.platform == "darwin":
    os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("HOME", "") + "/.bun/bin:" + os.environ.get("PATH", "")

import argparse, glob, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import load_config, call_llm_json


ENTITY_PROMPT = """Extract entities and relationships from this document.

Document: {filepath}
Content (truncated):
{content}

Return JSON:
{{"entities": [
  {{"name": "Entity Name", "type": "person|tool|project|agent|infra|concept|company", "description": "Brief desc", "relations": [
    {{"target": "Other Entity", "type": "uses|manages|deploys_on|part_of|depends_on|communicates_with", "description": "Brief"}}
  ]}}
]}}

Rules:
- Only extract clearly named entities (people, tools, projects, machines, companies)
- Max 5 entities per document
- Only extract relationships explicitly stated in the text
- Use existing entity names when possible — reuse names already in the graph"""


def scan_files(workspace: str, skip: list[str] | None = None) -> list[str]:
    """Find markdown files to process."""
    if skip is None:
        skip = [".cache", "node_modules", "brain/references", "docs/web", ".git"]
    
    files = []
    for f in glob.glob(os.path.join(workspace, "**/*.md"), recursive=True):
        rel = os.path.relpath(f, workspace)
        if any(rel.startswith(s) for s in skip):
            continue
        files.append(rel)
    return sorted(files)


def extract_entities(filepath: str, content: str, cfg: dict, debug: bool = False) -> list[dict]:
    """Extract entities from a single file."""
    # Truncate to ~2000 chars for LLM
    truncated = content[:2000]
    
    prompt = ENTITY_PROMPT.format(filepath=filepath, content=truncated)
    result = call_llm_json(prompt, cfg, debug)
    
    if result and "entities" in result:
        return result["entities"]
    return []


def merge_entities(existing: dict, new_entities: list[dict], source_file: str) -> dict:
    """Merge new entities into existing graph."""
    entities_by_name = {}
    for e in existing.get("entities", []):
        entities_by_name[e["name"].lower()] = e
    
    for e in new_entities:
        name_lower = e["name"].lower()
        if name_lower in entities_by_name:
            # Merge relations
            existing_rels = {(r.get("target", "").lower(), r.get("type", "")) 
                          for r in entities_by_name[name_lower].get("relations", [])}
            for rel in e.get("relations", []):
                key = (rel.get("target", "").lower(), rel.get("type", ""))
                if key not in existing_rels:
                    entities_by_name[name_lower].setdefault("relations", []).append(rel)
            # Add source
            sources = entities_by_name[name_lower].get("sources", [])
            if source_file not in sources:
                sources.append(source_file)
                entities_by_name[name_lower]["sources"] = sources
        else:
            e["sources"] = [source_file]
            entities_by_name[name_lower] = e
    
    existing["entities"] = list(entities_by_name.values())
    
    # Update stats
    total_relations = sum(len(e.get("relations", [])) for e in existing["entities"])
    entity_types = set(e.get("type", "") for e in existing["entities"])
    existing["stats"] = {
        "total_entities": len(existing["entities"]),
        "total_relations": total_relations,
        "entity_types": sorted(entity_types),
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    
    return existing


def build_graph(workspace: str | None = None, rebuild: bool = False,
                dry_run: bool = False, cfg: dict | None = None, debug: bool = False) -> dict:
    """Build or update the knowledge graph."""
    if cfg is None:
        cfg = load_config()
    if workspace is None:
        workspace = cfg["paths"]["workspace"]
    
    graph_path = os.path.join(workspace, cfg["paths"]["knowledgeGraph"])
    
    # Load existing graph
    graph = {}
    if not rebuild and os.path.exists(graph_path):
        try:
            with open(graph_path) as f:
                graph = json.load(f)
        except Exception:
            pass
    
    processed = set()
    for e in graph.get("entities", []):
        for s in e.get("sources", []):
            processed.add(s)
    
    # Find files to process
    files = scan_files(workspace)
    new_files = [f for f in files if rebuild or f not in processed]
    
    if debug or dry_run:
        print(f"Total files: {len(files)}, New: {len(new_files)}", file=sys.stderr)
    
    if dry_run:
        for f in new_files[:20]:
            print(f"  Would process: {f}")
        if len(new_files) > 20:
            print(f"  ... and {len(new_files) - 20} more")
        return graph
    
    # Process new files
    for i, filepath in enumerate(new_files):
        full_path = os.path.join(workspace, filepath)
        try:
            with open(full_path) as f:
                content = f.read()
        except Exception:
            continue
        
        if len(content) < 100:  # Skip tiny files
            continue
        
        if debug:
            print(f"  [{i+1}/{len(new_files)}] {filepath}...", file=sys.stderr)
        
        entities = extract_entities(filepath, content, cfg, debug)
        if entities:
            graph = merge_entities(graph, entities, filepath)
            if debug:
                print(f"    → {len(entities)} entities", file=sys.stderr)
    
    # Save
    os.makedirs(os.path.dirname(graph_path), exist_ok=True)
    with open(graph_path, "w") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    stats = graph.get("stats", {})
    print(f"✅ Graph: {stats.get('total_entities', 0)} entities, {stats.get('total_relations', 0)} relations")
    
    return graph


def update_graph_incremental(changed_files: list[str], cfg: dict = None, debug: bool = False) -> dict | None:
    """Update knowledge graph with only the changed files. Called by auto_ingest.
    Returns updated graph stats or None if no graph/LLM available."""
    if cfg is None:
        cfg = load_config(script="graph")
    else:
        # Apply graph script overrides
        graph_cfg = load_config(script="graph")
        cfg = {**cfg, "llm": graph_cfg.get("llm", cfg.get("llm", {}))}
    
    ws = cfg.get("paths", {}).get("workspace", ".")
    graph_path = os.path.join(ws, cfg["paths"].get("knowledgeGraph", ".cache/knowledge-graph.json"))
    
    # Load existing graph
    graph = {"entities": {}, "stats": {"total_entities": 0, "total_relations": 0}, "sources": {}}
    if os.path.isfile(graph_path):
        try:
            with open(graph_path) as f:
                graph = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    
    # Filter to .md files that exist
    md_files = [f for f in changed_files if f.endswith(".md") and os.path.isfile(f)]
    if not md_files:
        return None
    
    updated = 0
    for filepath in md_files:
        try:
            with open(filepath) as f:
                content = f.read()
        except OSError:
            continue
        
        if len(content.strip()) < 100:
            continue
        
        # Truncate for LLM
        content = content[:3000]
        
        if debug:
            print(f"  🔗 Graph update: {os.path.basename(filepath)}...", file=sys.stderr)
        
        entities = extract_entities(filepath, content, cfg, debug)
        if entities:
            graph = merge_entities(graph, entities, filepath)
            updated += 1
    
    if updated > 0:
        # Save
        os.makedirs(os.path.dirname(graph_path), exist_ok=True)
        with open(graph_path, "w") as f:
            json.dump(graph, f, ensure_ascii=False, indent=2)
        
        stats = graph.get("stats", {})
        if debug:
            print(f"  🔗 Graph: {stats.get('total_entities', 0)} entities, {stats.get('total_relations', 0)} relations", file=sys.stderr)
        return stats
    
    return None


def main():
    parser = argparse.ArgumentParser(description="Build knowledge graph from workspace")
    parser.add_argument("--rebuild", action="store_true", help="Full rebuild (ignore cache)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--preset", help="Config preset")
    parser.add_argument("--workspace", help="Override workspace path")
    args = parser.parse_args()
    
    cfg = load_config(preset=args.preset)
    if args.workspace:
        cfg["paths"]["workspace"] = args.workspace
    
    build_graph(rebuild=args.rebuild, dry_run=args.dry_run, cfg=cfg, debug=args.debug)


if __name__ == "__main__":
    main()
