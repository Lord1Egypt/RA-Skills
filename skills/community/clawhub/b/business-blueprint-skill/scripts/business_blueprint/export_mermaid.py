from __future__ import annotations

from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

# Watermark — injected as Mermaid comment at top of file
_WATERMARK_COMMENT = "%% business-blueprint-skill v{version}"


def _get_version() -> str:
    try:
        from importlib.metadata import version
        return version("business-blueprint-skill")
    except Exception:
        return "0.1.0"


def export_mermaid(blueprint: dict[str, Any], target: Path) -> None:
    """Export blueprint as Mermaid diagram with smart grid layout.

    Key layout strategy:
    - Use flowchart TB (top-bottom) for vertical data flow
    - Group capabilities into domain subgraphs, max 4 per row
    - Systems at top, capabilities in middle, actors at bottom
    """
    library = blueprint.get("library", {})
    capabilities = library.get("capabilities", [])
    systems = library.get("systems", [])
    actors = library.get("actors", [])
    flow_steps = library.get("flowSteps", [])

    MAX_COLS = 4
    lines = ["flowchart TB"]

    # ── Systems layer (top) ──
    if systems:
        lines.append('    subgraph Systems["Application Systems"]')
        lines.append("        direction LR")
        for sys in systems:
            label = escape(sys.get("name", sys["id"]))
            lines.append(f'        {sys["id"]}["{label}"]')
        lines.append("    end")

    # ── Capabilities grouped by domain/category ──
    if capabilities:
        domains: dict[str, list[dict]] = {}
        for cap in capabilities:
            domain = cap.get("category", cap.get("domain", ""))
            domains.setdefault(domain or "核心能力", []).append(cap)

        for domain_name, caps in domains.items():
            safe_name = domain_name.replace(" ", "_").replace("-", "_")
            lines.append(f'    subgraph {safe_name}["{escape(domain_name)}"]')
            lines.append("        direction TB")

            # Split into rows of MAX_COLS using subgraph for horizontal layout
            for chunk_start in range(0, len(caps), MAX_COLS):
                chunk = caps[chunk_start:chunk_start + MAX_COLS]
                if len(chunk) > 1:
                    subgraph_id = f"row_{safe_name}_{chunk_start}"
                    lines.append(f'        subgraph {subgraph_id}[""]')
                    lines.append("            direction LR")
                    for cap in chunk:
                        label = escape(cap.get("name", cap["id"]))
                        lines.append(f'            {cap["id"]}["{label}"]')
                    lines.append("        end")
                else:
                    cap = chunk[0]
                    label = escape(cap.get("name", cap["id"]))
                    lines.append(f'        {cap["id"]}["{label}"]')
            lines.append("    end")

    # ── Actors layer (bottom) ──
    if actors:
        lines.append('    subgraph Actors["参与者"]')
        lines.append("        direction LR")
        for actor in actors:
            label = escape(actor.get("name", actor["id"]))
            lines.append(f'        {actor["id"]}["{label}"]')
        lines.append("    end")

    # ── System → Capability links ──
    for sys in systems:
        for cap_id in sys.get("capabilityIds", []):
            lines.append(f'    {sys["id"]} --> {cap_id}')

    # ── Actor → Flow Step links ──
    for step in flow_steps:
        aid = step.get("actorId", "")
        if aid:
            lines.append(f'    {aid} --> {step["id"]}')

    # ── Explicit relations ──
    for rel in blueprint.get("relations", []):
        src = rel.get("from", rel.get("sourceId", rel.get("source", "")))
        tgt = rel.get("to", rel.get("targetId", rel.get("target", "")))
        label = escape(rel.get("label", rel.get("type", "")))
        if src and tgt and isinstance(src, str) and isinstance(tgt, str) and src.strip() and tgt.strip():
            lines.append(f'    {src} -- "{label}" --> {tgt}')

    content = _WATERMARK_COMMENT.format(version=_get_version()) + "\n" + "\n".join(lines) + "\n"
    target.write_text(content, encoding="utf-8")
