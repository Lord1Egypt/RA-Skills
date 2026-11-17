from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Any

from .base import BuildInspection, BuildPlan, BuildResult, BuilderCapability, SupportLevel

_DEFAULT_RUNTIME = Path(__file__).resolve().parents[1] / "runtime" / "pptxgenjs"


class PptxGenJsAdapter:
    name = "pptxgenjs"

    def __init__(self, runtime_dir: Path | None = None, timeout_seconds: float = 60.0) -> None:
        self.runtime_dir = Path(runtime_dir) if runtime_dir is not None else _DEFAULT_RUNTIME
        self.timeout_seconds = timeout_seconds

    def probe(self) -> BuilderCapability:
        node = shutil.which("node")
        module_manifest = self.runtime_dir / "node_modules" / "pptxgenjs" / "package.json"
        jszip_manifest = self.runtime_dir / "node_modules" / "jszip" / "package.json"
        script = self.runtime_dir / "build-deck.mjs"
        errors: list[str] = []
        version = None
        if node is None:
            errors.append("NODE_RUNTIME_NOT_FOUND")
        if not module_manifest.is_file():
            errors.append("PPTXGENJS_MODULE_NOT_FOUND")
        else:
            try:
                version = str(json.loads(module_manifest.read_text(encoding="utf-8"))["version"])
            except (OSError, KeyError, TypeError, json.JSONDecodeError):
                errors.append("PPTXGENJS_MODULE_MANIFEST_INVALID")
        if not script.is_file():
            errors.append("PPTXGENJS_RUNTIME_SCRIPT_NOT_FOUND")
        if not jszip_manifest.is_file():
            errors.append("JSZIP_MODULE_NOT_FOUND")
        if node is not None and module_manifest.is_file() and jszip_manifest.is_file():
            try:
                load_check = subprocess.run(
                    [node, "--input-type=module", "-e", "await import('pptxgenjs'); await import('jszip');"],
                    cwd=self.runtime_dir,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=min(self.timeout_seconds, 5.0),
                )
                if load_check.returncode != 0:
                    errors.append("PPTXGENJS_RUNTIME_MODULE_LOAD_FAILED")
            except subprocess.TimeoutExpired:
                errors.append("PPTXGENJS_RUNTIME_MODULE_LOAD_TIMEOUT")
            except OSError:
                errors.append("PPTXGENJS_RUNTIME_MODULE_LOAD_FAILED")
        available = not errors
        return BuilderCapability(
            name=self.name,
            available=available,
            version=version if available else None,
            command=node if available else None,
            features={
                "native_text": True,
                "native_table": True,
                "native_chart": True,
                "native_connector": True,
                "svg_embed": True,
                "speaker_notes": True,
                "theme": "partial",
                "slide_master": "partial",
                "readback": False,
            },
            warnings=[] if available else ["Local Node/PptxGenJS runtime is unavailable."],
            errors=errors,
        )

    def supports(self, component_type: str, delivery_route: str) -> SupportLevel:
        if delivery_route in {"native_ppt", "native_chart", "native_table", "native_diagram"}:
            return "partial" if delivery_route == "native_diagram" else "full"
        if delivery_route in {"svg_component", "hybrid_overlay", "generated_image", "background_image"}:
            return "visual_only"
        return "unsupported"

    def plan(self, ppt_ir: dict[str, Any], style_contract: dict[str, Any], delivery_plan: dict[str, Any]) -> BuildPlan:
        object_plans = {
            (obj.get("slide_id"), obj.get("object_id")): obj
            for slide in delivery_plan.get("slides", []) or []
            for obj in slide.get("objects", []) or []
            if isinstance(obj, dict)
        }
        slides = []
        for slide in ppt_ir.get("slides", []) or []:
            planned_objects = []
            for obj in slide.get("objects", []) or []:
                planned = dict(obj)
                planned["delivery_plan"] = object_plans.get((slide.get("id"), obj.get("id")), {})
                planned_objects.append(planned)
            slide_plan = dict(slide)
            slide_plan["objects"] = planned_objects
            slides.append(slide_plan)
        return BuildPlan(builder=self.name, slides=slides, style_contract=dict(style_contract))

    def build(
        self,
        build_plan: BuildPlan,
        output_dir: Path,
        *,
        visual_plan: dict[str, Any] | None = None,
    ) -> BuildResult:
        # The pipeline compiles the visual plan into PPT IR before Builder
        # planning. Accept the common Builder interface so PptxGenJS consumes
        # the same invocation contract as python-pptx without duplicating it
        # in the runtime payload.
        del visual_plan
        capability = self.probe()
        if not capability.available or capability.command is None:
            return BuildResult(
                builder=self.name,
                status="failed",
                errors=[{
                    "code": "PPTXGENJS_RUNTIME_UNAVAILABLE",
                    "message": "PptxGenJS requires Node, the local module, and build-deck.mjs. Run `python3 scripts/bootstrap_pptxgenjs_runtime.py` (which executes lockfile-pinned `npm ci`) from the article-html-to-ppt root, then retry.",
                    "details": capability.errors,
                }],
            )

        output_dir.mkdir(parents=True, exist_ok=True)
        input_path = output_dir / "build-plan.json"
        result_path = output_dir / "runtime-result.json"
        deck_path = output_dir / "deck.pptx"
        for current_run_artifact in (result_path, deck_path):
            current_run_artifact.unlink(missing_ok=True)
        run_id = uuid.uuid4().hex
        input_path.write_text(
            json.dumps({"run_id": run_id, "builder": build_plan.builder, "slides": build_plan.slides, "style_contract": build_plan.style_contract}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        command = [capability.command, str(self.runtime_dir / "build-deck.mjs"), str(input_path), str(output_dir)]
        try:
            completed = subprocess.run(
                command,
                cwd=self.runtime_dir,
                text=True,
                capture_output=True,
                check=False,
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            return BuildResult(
                builder=self.name,
                status="failed",
                errors=[{"code": "PPTXGENJS_RUNTIME_TIMEOUT", "message": f"Runtime exceeded {self.timeout_seconds:g} seconds.", "stdout": _summary(exc.stdout), "stderr": _summary(exc.stderr)}],
            )
        except OSError as exc:
            return BuildResult(builder=self.name, status="failed", errors=[{"code": "PPTXGENJS_PROCESS_START_FAILED", "message": str(exc)}])

        runtime_result = _read_runtime_result(result_path)
        if completed.returncode != 0:
            runtime_errors = runtime_result.get("errors", []) if runtime_result else []
            return BuildResult(
                builder=self.name,
                status="failed",
                errors=(runtime_errors or [{"code": "PPTXGENJS_RUNTIME_FAILED", "message": f"Runtime exited {completed.returncode}.", "stdout": _summary(completed.stdout), "stderr": _summary(completed.stderr)}]),
            )
        if runtime_result is None:
            return BuildResult(
                builder=self.name,
                status="failed",
                errors=[{
                    "code": "PPTXGENJS_RUNTIME_RESULT_MISSING",
                    "message": f"Runtime exited {completed.returncode} without a valid result file.",
                    "stdout": _summary(completed.stdout),
                    "stderr": _summary(completed.stderr),
                }],
            )
        if runtime_result.get("run_id") != run_id:
            return BuildResult(builder=self.name, status="failed", errors=[{"code": "PPTXGENJS_RUNTIME_RESULT_ID_MISMATCH", "message": "Runtime result does not belong to the current build run."}])
        errors = runtime_result.get("errors", []) or []
        status = runtime_result.get("status", "failed")
        if status == "created" and (not deck_path.is_file() or deck_path.stat().st_size == 0):
            status = "failed"
            errors.append({"code": "PPTXGENJS_OUTPUT_MISSING", "message": "Runtime reported success without a non-empty deck.pptx."})
        return BuildResult(
            builder=self.name,
            status=status,
            pptx=str(deck_path) if status == "created" else None,
            object_results=runtime_result.get("object_results", []) or [],
            fallbacks=runtime_result.get("fallbacks", []) or [],
            warnings=runtime_result.get("warnings", []) or [],
            errors=errors,
        )

    def inspect_output(self, pptx_path: Path) -> BuildInspection:
        try:
            from ppt_qa.package_inspector import inspect_package
        except Exception as exc:
            return BuildInspection(builder=self.name, status="failed", errors=[{"code": "BUILDER_INSPECT_IMPORT_FAILED", "message": str(exc)}])
        inspection = inspect_package(pptx_path)
        return BuildInspection(
            builder=self.name,
            status="passed" if inspection.status == "passed" else "failed",
            issues=[issue.__dict__ for issue in inspection.issues],
        )


def _read_runtime_result(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _summary(value: str | bytes | None, limit: int = 2000) -> str:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    return (value or "")[-limit:]
