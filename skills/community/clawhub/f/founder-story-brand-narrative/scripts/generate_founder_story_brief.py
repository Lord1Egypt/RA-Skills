#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class FounderStoryBrief:
    brand_name: str = ""
    category: str = ""
    products: List[str] = None  # type: ignore[assignment]
    founder_name: str = ""
    founder_role: str = ""
    location: str = ""
    origin: str = ""
    mission: str = ""
    audience: str = ""
    differentiators: List[str] = None  # type: ignore[assignment]
    values: List[str] = None  # type: ignore[assignment]
    proof: List[str] = None  # type: ignore[assignment]
    tone: str = ""
    constraints: List[str] = None  # type: ignore[assignment]
    primary_cta: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "products", self.products or [])
        object.__setattr__(self, "differentiators", self.differentiators or [])
        object.__setattr__(self, "values", self.values or [])
        object.__setattr__(self, "proof", self.proof or [])
        object.__setattr__(self, "constraints", self.constraints or [])


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        v = value.strip()
        return [v] if v else []
    return [str(value).strip()]


def parse_brief(data: Dict[str, Any]) -> FounderStoryBrief:
    return FounderStoryBrief(
        brand_name=str(data.get("brand_name", "")).strip(),
        category=str(data.get("category", "")).strip(),
        products=_as_list(data.get("products")),
        founder_name=str(data.get("founder_name", "")).strip(),
        founder_role=str(data.get("founder_role", "")).strip(),
        location=str(data.get("location", "")).strip(),
        origin=str(data.get("origin", "")).strip(),
        mission=str(data.get("mission", "")).strip(),
        audience=str(data.get("audience", "")).strip(),
        differentiators=_as_list(data.get("differentiators")),
        values=_as_list(data.get("values")),
        proof=_as_list(data.get("proof")),
        tone=str(data.get("tone", "")).strip(),
        constraints=_as_list(data.get("constraints")),
        primary_cta=str(data.get("primary_cta", "")).strip(),
    )


def narrative_spine(brief: FounderStoryBrief) -> str:
    brand = brief.brand_name or "[Brand]"
    origin = brief.origin or "[origin]"
    mission = brief.mission or "[mission]"
    audience = brief.audience or "[audience]"
    diff = brief.differentiators[0] if brief.differentiators else "[key differentiator]"
    return f"We started {brand} because {origin}. Today we {mission} for {audience} by {diff}."


def to_markdown(brief: FounderStoryBrief) -> str:
    brand = brief.brand_name or "[Brand]"
    founder = brief.founder_name or "[Founder]"
    founder_role = brief.founder_role or "[founder role]"

    def bullets(items: List[str], empty_placeholder: str) -> str:
        if not items:
            return f"- {empty_placeholder}\n"
        return "".join(f"- {x}\n" for x in items)

    products_line = ", ".join(brief.products) if brief.products else "[list key products]"
    proof_block = bullets(brief.proof, "[proof / credibility to add]")
    constraints_block = bullets(brief.constraints, "[constraints / compliance notes]")

    location = f" ({brief.location})" if brief.location else ""
    tone = brief.tone or "[voice: warm, direct, no hype]"
    cta = brief.primary_cta or "[primary CTA: Shop the collection]"

    md = []
    md.append(f"# Founder Story Brief: {brand}\n")
    md.append("## Snapshot\n")
    md.append(f"- **Category**: {brief.category or '[category]'}\n")
    md.append(f"- **Products**: {products_line}\n")
    md.append(f"- **Founder**: {founder}{location} — {founder_role}\n")
    md.append(f"- **Audience**: {brief.audience or '[who this is for]'}\n")
    md.append(f"- **Brand voice**: {tone}\n")
    md.append(f"- **Primary CTA**: {cta}\n\n")

    md.append("## Narrative spine (one sentence)\n\n")
    md.append(f"> {narrative_spine(brief)}\n\n")

    md.append("## Origin (why it started)\n\n")
    md.append(f"{brief.origin or '[Write 2–4 sentences: the moment/problem/turning point that started the brand.]'}\n\n")

    md.append("## Mission (what you exist to do)\n\n")
    md.append(f"{brief.mission or '[One sentence: what you do for the customer, not what you like doing.]'}\n\n")

    md.append("## Differentiators (concrete, verifiable)\n\n")
    md.append(bullets(brief.differentiators, "[Add 1–3 concrete process/material/ingredient differentiators]"))
    md.append("\n")

    md.append("## Values (2–4 principles)\n\n")
    md.append(bullets(brief.values, "[Add values that show up in product or behavior]"))
    md.append("\n")

    md.append("## Proof / credibility (if any)\n\n")
    md.append(proof_block)
    md.append("\n")

    md.append("## Constraints (what not to claim or mention)\n\n")
    md.append(constraints_block)
    md.append("\n")

    md.append("## Placement plan\n\n")
    md.append("- **About / Brand page**: Full origin + mission + values + proof. (300–800 words, scannable sections)\n")
    md.append("- **Homepage hero**: One headline + one sub + one CTA. No long paragraphs.\n")
    md.append("- **PDP brand block**: 2–4 sentences: origin + process + for-whom. Avoid repeating the full About.\n")
    md.append("- **Packaging / insert**: 1–2 sentences with one memorable line.\n\n")

    md.append("## Notes for copywriting\n\n")
    md.append("- Replace generic claims with concrete process/origin/proof.\n")
    md.append("- Keep hero copy short; let product and CTA do the work.\n")
    md.append("- Keep origin and mission consistent across placements; only length changes.\n")

    return "".join(md)


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in {path}: {e}") from e


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate a standardized Founder Story Brief markdown from a JSON input."
    )
    p.add_argument("--in", dest="in_path", required=True, help="Path to input JSON (brief.json).")
    p.add_argument("--out", dest="out_path", required=True, help="Path to output markdown (brief.md).")
    return p


def main() -> None:
    args = build_parser().parse_args()
    in_path = Path(args.in_path).expanduser()
    out_path = Path(args.out_path).expanduser()
    data = read_json(in_path)
    brief = parse_brief(data)
    md = to_markdown(brief)
    write_text(out_path, md)


if __name__ == "__main__":
    main()

