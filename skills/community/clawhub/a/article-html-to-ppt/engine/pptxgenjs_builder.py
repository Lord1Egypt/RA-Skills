"""Primary v4 builder: render_plan -> deck.pptx via PptxGenJS (Node runtime).

Consumes the builder-agnostic render_plan directly (no format translation:
EMU -> inches is a unit conversion, not a schema change). python-pptx
(pptx_builder.build_pptx) remains the fallback when the Node runtime is
unavailable.

This builder reproduces v3's visual quality: full connectors, gradients,
shadows and rich charts come from PptxGenJS rather than python-pptx's
limited shape API.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parents[1] / "runtime" / "pptxgenjs"
_SCRIPT = _RUNTIME_DIR / "build-deck-v4.mjs"


class PptxGenJsUnavailable(RuntimeError):
    pass


def probe() -> dict:
    """Report Node/PptxGenJS availability without raising."""
    node = shutil.which("node")
    errors = []
    if node is None:
        errors.append("NODE_RUNTIME_NOT_FOUND")
    if not (_RUNTIME_DIR / "node_modules" / "pptxgenjs" / "package.json").is_file():
        errors.append("PPTXGENJS_MODULE_NOT_FOUND")
    if not _SCRIPT.is_file():
        errors.append("PPTXGENJS_RUNTIME_SCRIPT_NOT_FOUND")
    if not errors:
        check = subprocess.run(
            [node, "--input-type=module", "-e",
             "await import('pptxgenjs');"],
            cwd=str(_RUNTIME_DIR), text=True, capture_output=True,
            check=False, timeout=10)
        if check.returncode != 0:
            errors.append("PPTXGENJS_RUNTIME_MODULE_LOAD_FAILED")
    return {"available": not errors, "node": node, "errors": errors}


def available() -> bool:
    return probe()["available"]


def build_pptx(plan: dict, output_path: str | Path) -> Path:
    """Render the render_plan with PptxGenJS. Raises on any failure."""
    capability = probe()
    if not capability["available"]:
        raise PptxGenJsUnavailable(
            "PptxGenJS runtime unavailable: " + "; ".join(capability["errors"]))

    output = Path(output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    # The runtime reads render-plan.json itself; we drop a copy beside it for
    # reproducibility, then point Node at that file (absolute paths — the
    # Node process cwd is the runtime dir, not the repo root).
    plan_path = output.parent / "render-plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2),
                         encoding="utf-8")

    proc = subprocess.run(
        [capability["node"], str(_SCRIPT), str(plan_path), str(output.parent)],
        cwd=str(_RUNTIME_DIR), text=True, capture_output=True, check=False,
        timeout=120)

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "unknown error"
        raise PptxGenJsUnavailable(f"PptxGenJS build failed: {detail}")

    result_path = output.parent / "pptxgenjs-result.json"
    if result_path.is_file():
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if not result.get("ok"):
            raise PptxGenJsUnavailable(
                "PptxGenJS reported failure: " + json.dumps(result.get("errors")))

    if not output.is_file():
        raise PptxGenJsUnavailable(f"deck not produced at {output}")
    return output
