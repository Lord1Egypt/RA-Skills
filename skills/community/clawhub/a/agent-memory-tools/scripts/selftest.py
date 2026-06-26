#!/usr/bin/env python3
"""
selftest — Quick validation of agent-memory-tools setup.
Checks: config, LLM server, embed server, QMD, knowledge graph.

Usage:
    selftest [--preset ollama|openai] [--fix]
"""
from __future__ import annotations
import os, sys
# Cross-platform PATH setup
if sys.platform == "darwin":
    os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("HOME", "") + "/.bun/bin:" + os.environ.get("PATH", "")

import argparse, json, subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import load_config, check_server, embed, call_llm


def check_qmd() -> dict:
    """Check QMD availability and collections."""
    try:
        result = subprocess.run(["qmd", "search", "test", "--limit", "1"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return {"ok": True, "output": result.stdout.strip()}
        return {"ok": False, "error": result.stderr.strip()}
    except FileNotFoundError:
        return {"ok": False, "error": "QMD not found. Install: bun install -g qmd"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def check_graph(cfg: dict) -> dict:
    """Check knowledge graph file."""
    ws = cfg["paths"]["workspace"]
    path = os.path.join(ws, cfg["paths"]["knowledgeGraph"])
    if os.path.exists(path):
        try:
            with open(path) as f:
                g = json.load(f)
            stats = g.get("stats", {})
            return {"ok": True, "entities": stats.get("total_entities", 0), "relations": stats.get("total_relations", 0)}
        except Exception as e:
            return {"ok": False, "error": f"Parse error: {e}"}
    return {"ok": False, "error": f"Not found: {path}"}


def run(preset: str | None = None):
    """Run all checks."""
    cfg = load_config(preset=preset)
    results = {}
    all_ok = True
    
    # 1. Config
    print("📋 Config")
    print(f"   LLM: {cfg['llm']['model']} @ {cfg['llm']['baseUrl']}")
    print(f"   Embed: {cfg['embeddings']['model']} @ {cfg['embeddings']['baseUrl']}")
    print(f"   Workspace: {cfg['paths']['workspace']}")
    print()
    
    # 2. Server connectivity
    print("🔌 Servers")
    status = check_server(cfg)
    for key in ["llm", "embeddings"]:
        ok = status[key]
        icon = "✅" if ok else "❌"
        models = status.get(f"{key}_models", [])
        model_info = f" ({len(models)} models)" if models else ""
        print(f"   {icon} {key}{model_info}")
        if not ok:
            all_ok = False
    print()
    
    # 3. Embed test
    print("🧮 Embedding")
    vecs = embed(["test embedding"], cfg)
    if vecs and len(vecs) > 0:
        print(f"   ✅ dims={len(vecs[0])}")
    else:
        print("   ❌ Embed failed")
        all_ok = False
    print()
    
    # 4. LLM test
    print("🤖 LLM")
    resp = call_llm('Reply with exactly this JSON: {"status": "ok"}', cfg)
    if resp and "ok" in resp:
        print(f"   ✅ Response received ({len(resp)} chars)")
    else:
        print(f"   ❌ LLM failed: {resp[:100] if resp else 'no response'}")
        all_ok = False
    print()
    
    # 5. QMD
    print("🔍 QMD")
    qmd = check_qmd()
    if qmd["ok"]:
        print(f"   ✅ {qmd['output'][:100]}")
    else:
        print(f"   ❌ {qmd['error']}")
        all_ok = False
    print()
    
    # 6. Knowledge graph
    print("🕸️  Knowledge Graph")
    graph = check_graph(cfg)
    if graph["ok"]:
        print(f"   ✅ {graph['entities']} entities, {graph['relations']} relations")
    else:
        print(f"   ⚠️  {graph['error']}")
    print()
    
    # Summary
    icon = "✅" if all_ok else "⚠️"
    print(f"{icon} {'All checks passed' if all_ok else 'Some checks failed'}")
    return 0 if all_ok else 1


def main():
    parser = argparse.ArgumentParser(description="Self-test agent-memory-tools")
    parser.add_argument("--preset", help="Config preset (ollama, openai)")
    args = parser.parse_args()
    
    sys.exit(run(preset=args.preset))


if __name__ == "__main__":
    main()
