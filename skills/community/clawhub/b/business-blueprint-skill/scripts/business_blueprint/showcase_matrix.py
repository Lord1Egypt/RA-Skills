from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

try:
    from .export_knowledge import is_knowledge_blueprint
    from .export_routes import resolve_export_route
    from .export_svg import export_svg_auto
    from .render_png import render_svg_to_png
    from .visual_profiles import VISUAL_PROFILE_IDS
except ImportError:
    from export_knowledge import is_knowledge_blueprint
    from export_routes import resolve_export_route
    from export_svg import export_svg_auto
    from render_png import render_svg_to_png
    from visual_profiles import VISUAL_PROFILE_IDS


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDUSTRIES = ("common", "retail", "finance", "manufacturing", "cross-border-ecommerce")


def build_showcase_matrix(
    *,
    output_dir: Path,
    industries: list[str] | None = None,
    visual_profiles: list[str] | None = None,
    theme: str = "dark",
    render_png: bool = False,
) -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    selected_industries = industries or list(DEFAULT_INDUSTRIES)
    selected_profiles = visual_profiles or list(VISUAL_PROFILE_IDS)

    entries: list[dict[str, Any]] = []
    for industry in selected_industries:
        blueprint = _load_demo_blueprint(industry)
        blueprint_type = blueprint.get("meta", {}).get("blueprintType", "architecture")
        route = "knowledge" if is_knowledge_blueprint(blueprint) else resolve_export_route(blueprint).route
        for profile in selected_profiles:
            target_dir = output_dir / industry / profile
            target_dir.mkdir(parents=True, exist_ok=True)
            svg_path = target_dir / "solution.svg"
            export_svg_auto(
                copy.deepcopy(blueprint),
                svg_path,
                theme=theme,
                industry=industry,
                visual_profile=profile,
            )
            png_status = "disabled"
            png_path: str | None = None
            if render_png:
                result = render_svg_to_png(svg_path)
                png_status = result.reason
                png_path = str(result.png_path) if result.ok and result.png_path else None
            entries.append(
                {
                    "industry": industry,
                    "blueprintType": blueprint_type,
                    "route": route,
                    "visualProfile": profile,
                    "theme": theme,
                    "svgPath": str(svg_path),
                    "pngPath": png_path,
                    "pngStatus": png_status,
                }
            )

    summary = {
        "version": "1.0",
        "entryCount": len(entries),
        "industries": selected_industries,
        "visualProfiles": selected_profiles,
        "entries": entries,
    }
    (output_dir / "showcase-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def _load_demo_blueprint(industry: str) -> dict[str, Any]:
    demo_path = REPO_ROOT / "demos" / f"{industry}.blueprint.json"
    if demo_path.exists():
        return json.loads(demo_path.read_text(encoding="utf-8"))
    if industry == "cross-border-ecommerce":
        return _cross_border_knowledge_demo()
    raise FileNotFoundError(f"No demo blueprint found for industry: {industry}")


def _cross_border_knowledge_demo() -> dict[str, Any]:
    return {
        "version": "1.0",
        "meta": {
            "title": "跨境电商广告投放 know-how",
            "industry": "cross-border-ecommerce",
            "blueprintType": "domain-knowledge",
        },
        "context": {
            "clarifyRequests": [
                {
                    "targetEntityId": "pain-roas",
                    "question": "主要投放平台和目标市场是什么？",
                    "rationale": "ROAS 基准因平台和区域差异很大。",
                }
            ]
        },
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
            "knowledge": {
                "painPoints": [{"id": "pain-roas", "name": "ROAS 波动", "audience": "品牌方/DTC"}],
                "strategies": [{"id": "strategy-attribution", "name": "统一归因模型", "audience": "品牌方/DTC"}],
                "rules": [{"id": "rule-policy", "name": "平台政策红线"}],
                "metrics": [{"id": "metric-roas", "name": "ROAS 提升", "forecast": {"direction": "up", "magnitude": 25, "unit": "%"}}],
                "practices": [{"id": "practice-creative", "name": "素材 7 天迭代"}],
                "pitfalls": [{"id": "pitfall-platform", "name": "单平台依赖"}],
            },
        },
        "relations": [
            {"from": "strategy-attribution", "to": "pain-roas", "type": "solves"},
            {"from": "strategy-attribution", "to": "metric-roas", "type": "measures"},
            {"from": "rule-policy", "to": "strategy-attribution", "type": "enforces"},
            {"from": "pitfall-platform", "to": "pain-roas", "type": "causes"},
        ],
        "views": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="showcase-matrix")
    parser.add_argument("--output", required=True)
    parser.add_argument("--industries", default=",".join(DEFAULT_INDUSTRIES))
    parser.add_argument("--visual-profiles", default=",".join(VISUAL_PROFILE_IDS))
    parser.add_argument("--theme", default="dark", choices=["light", "dark"])
    parser.add_argument("--png", action="store_true", help="Attempt optional CairoSVG PNG rendering.")
    args = parser.parse_args()

    summary = build_showcase_matrix(
        output_dir=Path(args.output),
        industries=_split_csv(args.industries),
        visual_profiles=_split_csv(args.visual_profiles),
        theme=args.theme,
        render_png=args.png,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
