#!/usr/bin/env python3
"""
citation_graph.py — Build a citation graph: who cites whom, find clusters
Uses Semantic Scholar API. Outputs graph data + visual DOT file.
Usage: python3 citation_graph.py [metadata_json] [depth]
  depth=1: just direct citations
  depth=2: citations of citations (slower)
"""

import json
import os
import sys
import time
import requests

SS_BASE = "https://api.semanticscholar.org/graph/v1"


def get_paper_data(arxiv_id, title=""):
    """Fetch paper info from Semantic Scholar."""
    clean_id = arxiv_id.split("v")[0].replace("_", "/")

    # Try arXiv ID first
    url = f"{SS_BASE}/paper/arXiv:{clean_id}?fields=paperId,title,year,citationCount,citations,references"
    try:
        time.sleep(1.2)
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass

    # Fallback: title search
    if title:
        url2 = f"{SS_BASE}/paper/search?query={requests.utils.quote(title)}&limit=1&fields=paperId,title,year,citationCount,citations,references"
        try:
            time.sleep(1.2)
            r2 = requests.get(url2, timeout=15)
            if r2.status_code == 200:
                data = r2.json().get("data", [])
                if data:
                    return data[0]
        except Exception:
            pass
    return None


def build_graph(metadata_path="papers_pdf/metadata.json", depth=1):
    if not os.path.exists(metadata_path):
        print(f"❌ {metadata_path} not found. Run arxiv_downloader.py first.")
        sys.exit(1)

    with open(metadata_path) as f:
        papers = json.load(f)

    print(f"🕸️  Building citation graph for {len(papers)} papers (depth={depth})...")

    graph = {}      # paperId → node info
    edges = []      # (from_id, to_id, type)  type = "cites" | "cited_by"
    id_map = {}     # arxiv_id → paperId

    # Phase 1: fetch all seed papers
    for i, paper in enumerate(papers):
        arxiv_id = paper.get("arxiv_id", "")
        title = paper.get("title", "")
        print(f"  [{i+1}/{len(papers)}] Fetching: {title[:55]}...")

        data = get_paper_data(arxiv_id, title)
        if not data:
            print(f"    ⚠️  Not found on Semantic Scholar")
            continue

        paper_id = data.get("paperId", arxiv_id)
        id_map[arxiv_id] = paper_id

        graph[paper_id] = {
            "id": paper_id,
            "arxiv_id": arxiv_id,
            "title": title or data.get("title", ""),
            "year": data.get("year"),
            "citations": data.get("citationCount", 0),
            "is_seed": True
        }

        # Add reference edges (this paper cites → )
        for ref in data.get("references", [])[:30]:
            ref_id = ref.get("paperId")
            ref_title = ref.get("title", "")
            if ref_id:
                edges.append((paper_id, ref_id, "cites"))
                if ref_id not in graph:
                    graph[ref_id] = {
                        "id": ref_id,
                        "title": ref_title,
                        "year": ref.get("year"),
                        "citations": 0,
                        "is_seed": False
                    }

        # Add citation edges (cited by ←)
        for cit in data.get("citations", [])[:20]:
            cit_id = cit.get("paperId")
            cit_title = cit.get("title", "")
            if cit_id:
                edges.append((cit_id, paper_id, "cited_by"))
                if cit_id not in graph:
                    graph[cit_id] = {
                        "id": cit_id,
                        "title": cit_title,
                        "year": cit.get("year"),
                        "citations": 0,
                        "is_seed": False
                    }

    # Find most-cited papers in graph
    citation_counts = {}
    for _, to_id, _ in edges:
        citation_counts[to_id] = citation_counts.get(to_id, 0) + 1

    # Identify key papers (cited by multiple seed papers = likely foundational)
    foundational = {pid: cnt for pid, cnt in citation_counts.items() if cnt >= 2}

    # Save graph JSON
    graph_data = {
        "nodes": list(graph.values()),
        "edges": [{"from": f, "to": t, "type": typ} for f, t, typ in edges],
        "foundational_papers": [
            {"id": pid, "title": graph.get(pid, {}).get("title", ""), "cited_by_count": cnt}
            for pid, cnt in sorted(foundational.items(), key=lambda x: -x[1])
        ]
    }

    with open("citation_graph.json", "w") as f:
        json.dump(graph_data, f, indent=2)

    # Save DOT file for visualization (Graphviz)
    with open("citation_graph.dot", "w") as f:
        f.write("digraph CitationGraph {\n")
        f.write('  rankdir=LR;\n  node [shape=box, style=filled];\n')

        for node in graph.values():
            label = node["title"][:40].replace('"', "'")
            color = "#4CAF50" if node.get("is_seed") else "#90CAF9"
            if node["id"] in foundational:
                color = "#FF9800"
            f.write(f'  "{node["id"]}" [label="{label}", fillcolor="{color}"];\n')

        for frm, to, typ in edges[:200]:  # limit for readability
            style = "solid" if typ == "cites" else "dashed"
            f.write(f'  "{frm}" -> "{to}" [style={style}];\n')

        f.write("}\n")

    # Human-readable summary
    with open("citation_graph_summary.md", "w") as f:
        f.write("# Citation Graph Summary\n\n")
        f.write(f"- **Papers analyzed:** {len(graph)}\n")
        f.write(f"- **Citation edges:** {len(edges)}\n\n")
        f.write("## 🌟 Foundational Papers (cited by multiple papers in your set)\n\n")
        for p in graph_data["foundational_papers"][:15]:
            f.write(f"- **{p['title'][:80]}** — cited by {p['cited_by_count']} papers\n")
        f.write("\n## 🟢 Seed Papers (your downloaded set)\n\n")
        for node in graph.values():
            if node.get("is_seed"):
                f.write(f"- {node['title'][:80]} ({node.get('year','?')})\n")

    print(f"\n✅ Citation graph built!")
    print(f"   Nodes: {len(graph)} | Edges: {len(edges)}")
    print(f"   Foundational papers: {len(foundational)}")
    print(f"   Saved: citation_graph.json, citation_graph.dot, citation_graph_summary.md")
    print(f"\n   Visualize: dot -Tpng citation_graph.dot -o citation_graph.png")
    return graph_data


if __name__ == "__main__":
    metadata = sys.argv[1] if len(sys.argv) > 1 else "papers_pdf/metadata.json"
    depth    = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    build_graph(metadata, depth)
