#!/usr/bin/env python3
"""Run the PPTSmith v2 production gates as one resumable command."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REGISTRY = ROOT / "references" / "component-registry.json"
OUTPUT_OWNERSHIP_MARKER = ".pptsmith-output"
STAGES = [
    "prepare_inputs",
    "validate_inputs",
    "route_audience",
    "route_task",
    "design_evidence",
    "plan_visual_narrative",
    "validate_visual_plan",
    "compile_visual_plan",
    "enrich_ir",
    "ir_quality_floor",
    "deck_rhythm",
    "resolve_profile",
    "capability_probe",
    "resolve_delivery",
    "validate_delivery",
    "build",
    "inspect",
    "verify",
    "visual_revision",
    "score",
    "prepare_delivery",
    "package_delivery",
]


def _validate_pipeline_paths(work: Path, output: Path) -> None:
    work = Path(work).resolve()
    output = Path(output).resolve()
    broad_paths = {
        Path("/").resolve(),
        Path.home().resolve(),
        Path.cwd().resolve(),
        ROOT.resolve(),
    }
    if work in broad_paths:
        raise ValueError(f"unsafe work directory: {work}")
    if output in broad_paths:
        raise ValueError(f"unsafe output directory: {output}")
    if (
        work == output
        or work in output.parents
        or output in work.parents
    ):
        raise ValueError("work and output directories must be distinct and non-overlapping")


def _validate_output_reset(output: Path) -> None:
    output = Path(output)
    if not output.exists():
        return
    if not output.is_dir() or output.is_symlink():
        raise ValueError(f"output path is not a safe directory: {output}")
    entries = list(output.iterdir())
    if entries and not (output / OUTPUT_OWNERSHIP_MARKER).is_file():
        raise ValueError(
            f"output directory is not owned by PPTSmith and will not be reset: {output}"
        )


class StageFailure(RuntimeError):
    def __init__(self, stage: str, message: str, returncode: int = 1) -> None:
        super().__init__(message)
        self.stage = stage
        self.returncode = returncode


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return document


def fingerprint(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def copy_input(source: Path, target: Path) -> None:
    if not source.is_file():
        raise ValueError(f"Input does not exist: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the end-to-end PPTSmith v2 production pipeline.")
    parser.add_argument("--requirements", type=Path, required=True)
    parser.add_argument("--ppt-ir", type=Path, required=True)
    parser.add_argument("--style", type=Path, required=True)
    parser.add_argument("--assets", "--asset-manifest", dest="assets", type=Path)
    parser.add_argument("--content-analysis", type=Path)
    parser.add_argument("--storyline", type=Path)
    parser.add_argument("--source-context-brief", type=Path)
    parser.add_argument("--visual-system", type=Path)
    parser.add_argument("--builder", choices=["auto", "python_pptx", "pptxgenjs"], default="auto")
    parser.add_argument("--profile", choices=["fast", "standard", "premium"], default="standard")
    parser.add_argument("--rubric-case", type=Path, help="Benchmark case containing an explicit human/model reference rubric for Premium final.")
    parser.add_argument("--use-reference-rubric", action="store_true", help="Use the rubric referenced by --rubric-case as the final judgment.")
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--json-output", action="store_true")
    args = parser.parse_args(argv)
    if bool(args.content_analysis) != bool(args.storyline):
        parser.error("--content-analysis and --storyline must be provided together")
    if args.content_analysis and not args.source_context_brief:
        parser.error("--source-context-brief is required when visual narrative inputs are provided")
    return args


class Pipeline:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.work = args.work_dir.resolve()
        self.output = args.output_dir.resolve()
        _validate_pipeline_paths(self.work, self.output)
        self.contracts = self.work / "contracts"
        self.qa = self.work / "qa"
        self.logs = self.work / "logs"
        self.build_dir = self.work / "builds" / "final"
        self.state_path = self.work / "state.json"
        self.previous = load_json(self.state_path) if self.state_path.exists() else None
        prior_attempts = list((self.previous or {}).get("attempts", []))
        if self.previous and not prior_attempts:
            prior_attempts.append(self.attempt_snapshot(self.previous))
        self.attempts = prior_attempts[-19:]
        self.inputs = {
            "requirements": str(args.requirements.resolve()),
            "ppt_ir": str(args.ppt_ir.resolve()),
            "style": str(args.style.resolve()),
            "asset_manifest": str(args.assets.resolve()) if args.assets else None,
            "content_analysis": str(args.content_analysis.resolve()) if args.content_analysis else None,
            "storyline": str(args.storyline.resolve()) if args.storyline else None,
            "source_context_brief": str(args.source_context_brief.resolve()) if args.source_context_brief else None,
            "visual_system": str(args.visual_system.resolve()) if args.visual_system else None,
            "builder": args.builder,
            "profile": args.profile,
            "rubric_case": str(args.rubric_case.resolve()) if args.rubric_case else None,
            "use_reference_rubric": args.use_reference_rubric,
            "work_dir": str(self.work),
            "output_dir": str(self.output),
        }
        now = iso_now()
        self.state: dict[str, Any] = {
            "schema_version": "1.0",
            "command_inputs": self.inputs,
            "input_fingerprints": {},
            "attempt": int((self.previous or {}).get("attempt", 0)) + 1,
            "resumed_from": (self.previous or {}).get("last_successful_stage") if self.previous else None,
            "current_stage": None,
            "last_successful_stage": None,
            "failed_stage": None,
            "status": "running",
            "started_at": now,
            "updated_at": now,
            "completed_at": None,
            "error": None,
            "stage_order": [],
            "visual_revision_count": 0,
            "attempts": self.attempts,
        }
        self.attempts.append(self.attempt_snapshot(self.state))
        self.state["attempts"] = self.attempts

    @staticmethod
    def attempt_snapshot(state: dict[str, Any]) -> dict[str, Any]:
        return {
            "attempt": state.get("attempt"),
            "command_inputs": state.get("command_inputs", {}),
            "input_fingerprints": state.get("input_fingerprints", {}),
            "status": state.get("status"),
            "last_successful_stage": state.get("last_successful_stage"),
            "failed_stage": state.get("failed_stage"),
            "error": state.get("error"),
            "started_at": state.get("started_at"),
            "completed_at": state.get("completed_at"),
        }

    def save_state(self) -> None:
        self.state["updated_at"] = iso_now()
        self.attempts[-1] = self.attempt_snapshot(self.state)
        self.state["attempts"] = self.attempts
        write_json(self.state_path, self.state)

    def run_command(self, stage: str, command: list[str], *, cwd: Path = ROOT, accepted: set[int] | None = None) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
        self.logs.mkdir(parents=True, exist_ok=True)
        (self.logs / f"{STAGES.index(stage) + 1:02d}-{stage}.log").write_text(
            "$ " + " ".join(command) + "\n\nSTDOUT\n" + completed.stdout + "\nSTDERR\n" + completed.stderr,
            encoding="utf-8",
        )
        if completed.returncode not in (accepted or {0}):
            detail = (completed.stderr or completed.stdout).strip()
            raise StageFailure(stage, detail or f"Command exited {completed.returncode}", completed.returncode)
        return completed

    def stage(self, name: str, action: Any) -> None:
        self.state["current_stage"] = name
        self.save_state()
        action()
        self.state["last_successful_stage"] = name
        self.state["stage_order"].append(name)
        self.save_state()

    def prepare_inputs(self) -> None:
        self.work.mkdir(parents=True, exist_ok=True)
        # Every attempt deterministically rebuilds derived artifacts. This is the
        # safe resume path: validated source contracts survive, stale products do not.
        for path in (self.qa, self.logs, self.build_dir.parent):
            if path.exists():
                shutil.rmtree(path)
        _validate_output_reset(self.output)
        if self.output.exists():
            shutil.rmtree(self.output)
        contract_stage = self.work / ".contracts.current"
        contract_backup = self.work / ".contracts.previous"
        for path in (contract_stage, contract_backup):
            if path.exists():
                shutil.rmtree(path)
        contract_stage.mkdir(parents=True)
        sources = {
            "requirements": self.args.requirements,
            "ppt_ir": self.args.ppt_ir,
            "style": self.args.style,
        }
        if self.args.assets:
            sources["asset_manifest"] = self.args.assets
        if self.args.content_analysis:
            sources["content_analysis"] = self.args.content_analysis
        if self.args.storyline:
            sources["storyline"] = self.args.storyline
        if self.args.source_context_brief:
            sources["source_context_brief"] = self.args.source_context_brief
        if self.args.visual_system:
            sources["visual_system"] = self.args.visual_system
        targets = {
            "requirements": contract_stage / "requirements.json",
            "ppt_ir": contract_stage / "ppt-ir.json",
            "style": contract_stage / "style-contract.json",
            "asset_manifest": contract_stage / "asset-manifest.json",
            "content_analysis": contract_stage / "content-analysis.json",
            "storyline": contract_stage / "storyline.json",
            "source_context_brief": contract_stage / "source-context-brief.json",
            "visual_system": contract_stage / "visual-system.json",
        }
        for name, source in sources.items():
            copy_input(source, targets[name])
            self.state["input_fingerprints"][name] = fingerprint(source)
        if self.args.profile == "premium" and not self.args.assets:
            write_json(targets["asset_manifest"], {"schema_version": "2.0", "assets": []})
        requirements = load_json(targets["requirements"])
        requirements["production_profile"] = self.args.profile
        write_json(targets["requirements"], requirements)
        if self.contracts.exists():
            self.contracts.replace(contract_backup)
        contract_stage.replace(self.contracts)
        if contract_backup.exists():
            shutil.rmtree(contract_backup)
        targets = {
            "requirements": self.contracts / "requirements.json",
            "ppt_ir": self.contracts / "ppt-ir.json",
            "style": self.contracts / "style-contract.json",
            "asset_manifest": self.contracts / "asset-manifest.json",
            "content_analysis": self.contracts / "content-analysis.json",
            "storyline": self.contracts / "storyline.json",
            "source_context_brief": self.contracts / "source-context-brief.json",
            "visual_system": self.contracts / "visual-system.json",
        }
        analysis = self.work / "analysis"
        analysis.mkdir(parents=True, exist_ok=True)
        (analysis / "content-lock.md").write_text("# Content Lock\n\nSource contracts are locked by the pipeline input fingerprints in `state.json`.\n", encoding="utf-8")
        if self.args.profile in {"standard", "premium"}:
            ppt_ir = load_json(targets["ppt_ir"])
            lines = ["# Storyboard", ""] + [f"- {slide.get('id', '?')}: {slide.get('title', '')}" for slide in ppt_ir.get("slides", [])]
            (analysis / "storyboard.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    @property
    def visual_enabled(self) -> bool:
        return bool(self.args.content_analysis and self.args.storyline)

    def route_task(self) -> None:
        self.run_command(
            "route_task",
            [
                sys.executable,
                str(SCRIPTS / "route_task.py"),
                "--analysis",
                str(self.contracts / "content-analysis.json"),
                "--output",
                str(self.contracts / "task-route.json"),
            ],
        )

    def route_audience(self) -> None:
        completed = self.run_command(
            "route_audience",
            [
                sys.executable,
                str(SCRIPTS / "route_audience.py"),
                "--brief",
                str(self.contracts / "source-context-brief.json"),
                "--output",
                str(self.contracts / "audience-route.json"),
            ],
            accepted={0, 2},
        )
        decision = load_json(self.contracts / "audience-route.json")
        if completed.returncode != 0 or decision.get("status") != "ready":
            codes = decision.get("blocking_codes", [])
            raise StageFailure("route_audience", ", ".join(str(code) for code in codes) or "AUDIENCE_ROUTE_BLOCKED", completed.returncode or 2)

    def design_evidence(self) -> None:
        from visual_narrative.design_evidence import consume_design_evidence

        task_route = load_json(self.contracts / "task-route.json")
        if task_route.get("selected_route") != "product_prd":
            return
        output = self.contracts / "design-evidence.json"
        self.run_command(
            "design_evidence",
            [
                sys.executable,
                str(SCRIPTS / "extract_design_evidence.py"),
                "--analysis",
                str(self.contracts / "content-analysis.json"),
                "--output",
                str(output),
            ],
        )
        evidence = load_json(output)
        ppt_ir_path = self.contracts / "ppt-ir.json"
        evidence, ppt_ir = consume_design_evidence(evidence, load_json(ppt_ir_path))
        write_json(output, evidence)
        write_json(ppt_ir_path, ppt_ir)
        codes = evidence.get("blocking_codes")
        if evidence.get("status") == "blocked" and isinstance(codes, list):
            raise StageFailure("design_evidence", ", ".join(str(code) for code in codes))

    def visual_style_id(self) -> str:
        path = self.contracts / "visual-system.json"
        if not path.is_file():
            return "azure-insight-architecture"
        value = load_json(path)
        style_id = value.get("style_id")
        if not isinstance(style_id, str) or not style_id.strip():
            raise StageFailure("plan_visual_narrative", "VISUAL_SYSTEM_STYLE_ID_REQUIRED")
        return style_id.strip()

    def plan_visual_narrative(self) -> None:
        self.run_command(
            "plan_visual_narrative",
            [
                sys.executable,
                str(SCRIPTS / "plan_visual_narrative.py"),
                "--task-route",
                str(self.contracts / "task-route.json"),
                "--audience-route",
                str(self.contracts / "audience-route.json"),
                "--storyline",
                str(self.contracts / "storyline.json"),
                "--style-id",
                self.visual_style_id(),
                "--output",
                str(self.contracts / "visual-plan.json"),
            ],
        )

    def validate_visual_plan(self) -> None:
        self.run_command(
            "validate_visual_plan",
            [
                sys.executable,
                str(SCRIPTS / "validate_contracts.py"),
                "--task-route",
                str(self.contracts / "task-route.json"),
                "--visual-plan",
                str(self.contracts / "visual-plan.json"),
                "--strict",
                "--json-output",
            ],
        )

    def compile_visual_plan(self) -> None:
        self.run_command(
            "compile_visual_plan",
            [
                sys.executable,
                str(SCRIPTS / "compile_visual_plan.py"),
                "--ppt-ir",
                str(self.contracts / "ppt-ir.json"),
                "--visual-plan",
                str(self.contracts / "visual-plan.json"),
                "--output",
                str(self.contracts / "ppt-ir.compiled.json"),
            ],
        )
        compiled = self.contracts / "ppt-ir.compiled.json"
        compiled.replace(self.contracts / "ppt-ir.json")

    def ir_quality_floor(self) -> None:
        self.run_command(
            "ir_quality_floor",
            [
                sys.executable,
                str(SCRIPTS / "ir_quality_floor.py"),
                "--ppt-ir",
                str(self.contracts / "ppt-ir.json"),
                "--output",
                str(self.contracts / "ir-quality-floor.json"),
                "--strict",
            ],
        )

    def enrich_ir(self) -> None:
        from ir_enrichment import enrich_ppt_ir

        path = self.contracts / "ppt-ir.json"
        write_json(path, enrich_ppt_ir(load_json(path)))

    def deck_rhythm(self) -> None:
        from visual_narrative.rhythm import evaluate_deck_rhythm

        report = evaluate_deck_rhythm(load_json(self.contracts / "visual-plan.json"))
        write_json(self.contracts / "deck-rhythm-report.json", report)
        if report.get("status") != "passed":
            codes = [
                str(item.get("code"))
                for item in report.get("issues", [])
                if isinstance(item, dict) and item.get("code")
            ]
            raise StageFailure("deck_rhythm", ", ".join(codes) or "DECK_RHYTHM_FAILED")

    def validate(self, stage: str, *, include_delivery: bool = False, include_build: bool = False) -> None:
        command = [sys.executable, str(SCRIPTS / "validate_contracts.py")]
        # When visual narrative is enabled, skip ppt-ir validation before compile_visual_plan replaces it.
        # The second validate_inputs after compile_visual_plan will validate the compiled ppt-ir.
        ppt_ir_ready = (
            not self.visual_enabled
            or stage != "validate_inputs"
            or (self.contracts / "visual-plan.json").exists()
        )
        if ppt_ir_ready:
            command += ["--ppt-ir", str(self.contracts / "ppt-ir.json")]
        command += ["--style", str(self.contracts / "style-contract.json")]
        if (self.contracts / "asset-manifest.json").exists():
            command += ["--assets", str(self.contracts / "asset-manifest.json")]
        if include_delivery:
            command += ["--delivery", str(self.contracts / "delivery-plan.json")]
        if include_build:
            command += ["--build", str(self.contracts / "build-manifest.json")]
        command += ["--strict", "--json-output"]
        self.run_command(stage, command)

    def resolve_profile(self) -> None:
        self.run_command("resolve_profile", [
            sys.executable, str(SCRIPTS / "resolve_production_profile.py"),
            "--requirements", str(self.contracts / "requirements.json"),
            "--ppt-ir", str(self.contracts / "ppt-ir.json"),
            "--output", str(self.contracts / "production-profile.json"),
        ])

    def capability_probe(self) -> None:
        # Run from the pinned local Node runtime so its package is discoverable.
        runtime = ROOT / "runtime" / "pptxgenjs"
        self.run_command("capability_probe", [
            sys.executable, str(SCRIPTS / "capability_probe.py"),
            "--style", str(self.contracts / "style-contract.json"),
            "--registry", str(REGISTRY),
            "--output", str(self.contracts / "capability-report.json"),
        ], cwd=runtime if runtime.is_dir() else ROOT)
        fault = os.environ.get("PPTSMITH_TEST_CAPABILITIES")
        if fault:
            report = load_json(self.contracts / "capability-report.json")
            for name, builder in (report.get("builders", {}) or {}).items():
                if fault == "none" or fault == f"{name}_unavailable":
                    builder["available"] = False
            write_json(self.contracts / "capability-report.json", report)

    def resolve_delivery(self) -> None:
        self.run_command("resolve_delivery", [
            sys.executable, str(SCRIPTS / "resolve_component_delivery.py"),
            "--ppt-ir", str(self.contracts / "ppt-ir.json"),
            "--style", str(self.contracts / "style-contract.json"),
            "--registry", str(REGISTRY),
            "--capabilities", str(self.contracts / "capability-report.json"),
            "--profile", self.args.profile,
            "--builder", self.args.builder,
            "--output", str(self.contracts / "delivery-plan.json"),
            "--strict",
        ], accepted={0, 1})
        plan = load_json(self.contracts / "delivery-plan.json")
        builder = plan.get("builder") if isinstance(plan.get("builder"), dict) else {}
        selected = str(builder.get("selected") or "unknown")
        errors = [str(item) for item in builder.get("errors", [])]
        unsupported = int((plan.get("summary") or {}).get("unsupported_count", 0))
        # A forced Builder can be selected as the named candidate even when it
        # is unavailable. Preserve that candidate's capability error instead
        # of collapsing it to the generic delivery-plan error.
        if not errors and self.args.builder != "auto":
            for candidate in builder.get("candidates", []) or []:
                if (
                    isinstance(candidate, dict)
                    and candidate.get("builder") == self.args.builder
                    and (candidate.get("available") is False or unsupported)
                ):
                    errors = [str(item) for item in candidate.get("errors", [])]
                    if errors:
                        break
        if errors or selected not in {"python_pptx", "pptxgenjs"} or unsupported:
            codes = errors or (["BUILDER_SELECTION_UNKNOWN"] if selected == "unknown" else ["DELIVERY_PLAN_UNSUPPORTED"])
            raise StageFailure("resolve_delivery", ", ".join(codes))
        if self.args.builder != "auto" and selected != self.args.builder:
            raise StageFailure("resolve_delivery", f"CAPABILITY_FORCED_BUILDER_REJECTED: requested={self.args.builder}, selected={selected}")

    def approved_builder(self) -> str:
        return str(load_json(self.contracts / "delivery-plan.json")["builder"]["selected"])

    def build(self) -> None:
        self.build_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            sys.executable, str(SCRIPTS / "build_deck.py"),
            "--ppt-ir", str(self.contracts / "ppt-ir.json"),
            "--style", str(self.contracts / "style-contract.json"),
            "--delivery", str(self.contracts / "delivery-plan.json"),
            "--builder", self.approved_builder(),
            "--output-dir", str(self.build_dir),
            "--build-manifest", str(self.contracts / "build-manifest.json"),
        ]
        visual_plan = self.contracts / "visual-plan.json"
        if visual_plan.exists():
            cmd += ["--visual-plan", str(visual_plan)]
        self.run_command("build", cmd)

    def deck_path(self) -> Path:
        manifest = load_json(self.contracts / "build-manifest.json")
        raw = Path(str(manifest.get("outputs", {}).get("deck", "deck.pptx")))
        return raw if raw.is_absolute() else self.build_dir / raw

    def inspect(self) -> None:
        self.run_command("inspect", [
            sys.executable, str(SCRIPTS / "inspect_pptx.py"), str(self.deck_path()),
            "--ppt-ir", str(self.contracts / "ppt-ir.json"),
            "--style", str(self.contracts / "style-contract.json"),
            "--delivery", str(self.contracts / "delivery-plan.json"),
            "--build", str(self.contracts / "build-manifest.json"),
            "--output", str(self.qa / "pptx-inspection.json"),
        ])

    def verify(self) -> None:
        command = [
            sys.executable, str(SCRIPTS / "verify_deck.py"), str(self.deck_path()),
            "--ppt-ir", str(self.contracts / "ppt-ir.json"),
            "--style", str(self.contracts / "style-contract.json"),
            "--delivery", str(self.contracts / "delivery-plan.json"),
            "--build", str(self.contracts / "build-manifest.json"),
            "--inspection-report", str(self.qa / "pptx-inspection.json"),
            "--capabilities", str(self.contracts / "capability-report.json"),
            "--profile", self.args.profile,
            "--output", str(self.qa / "qa-report.json"),
        ]
        accepted = {0, 1}  # verifier uses 1 for warning-only reports as well as hard QA failures
        if self.args.profile in {"standard", "premium"}:
            render_output = self.work / "renders"
            if render_output.exists():
                shutil.rmtree(render_output)
            command += ["--render", "--render-output", str(render_output), "--write-render-report", str(self.qa / "render-report.json")]
            if self.args.profile == "premium":
                command.append("--render-required")
            accepted.add(2)  # truthful renderer-unavailable evidence; packaging remains blocked
        completed = self.run_command("verify", command, accepted=accepted)
        report = load_json(self.qa / "qa-report.json")
        renderer_unavailable = any(
            isinstance(issue, dict) and issue.get("issue_code") == "RENDER_ENGINE_UNAVAILABLE"
            for issue in report.get("issues", [])
        )
        if renderer_unavailable:
            self.state["provisional_reason"] = "RENDER_ENGINE_UNAVAILABLE"
        if report.get("status") in {"fail", "blocked"}:
            raise StageFailure("verify", f"QA hard failure: {report.get('status')}", completed.returncode or 1)

    def visual_revision(self) -> None:
        from visual_narrative.revision import build_revision_request

        visual_plan = load_json(self.contracts / "visual-plan.json")
        storyline = load_json(self.contracts / "storyline.json")
        request = build_revision_request(
            visual_plan,
            storyline.get("revision_observations"),
            rubric_score=storyline.get("rubric_score"),
            contact_sheet_metrics=storyline.get("contact_sheet_metrics"),
        )
        request_path = self.contracts / "visual-revision-request.json"
        write_json(request_path, request)
        self.run_command(
            "visual_revision",
            [
                sys.executable,
                str(SCRIPTS / "validate_contracts.py"),
                "--visual-revision",
                str(request_path),
                "--strict",
                "--json-output",
            ],
        )
        if request.get("status") != "revision_required":
            return
        if int(self.state.get("visual_revision_count", 0)) >= 1:
            raise StageFailure("visual_revision", "VISUAL_REVISION_LIMIT_EXCEEDED")

        initial = self.work / "revisions" / "initial"
        if initial.exists():
            shutil.rmtree(initial)
        initial.mkdir(parents=True)
        shutil.copy2(self.deck_path(), initial / "deck.pptx")
        shutil.copy2(self.contracts / "build-manifest.json", initial / "build-manifest.json")
        shutil.copy2(self.qa / "pptx-inspection.json", initial / "pptx-inspection.json")
        shutil.copy2(self.qa / "qa-report.json", initial / "qa-report.json")
        self._apply_visual_revision_once(visual_plan, request)
        self.state["visual_revision_count"] = 1
        self.save_state()
        self.build()
        self.inspect()
        self.verify()

    def _apply_visual_revision_once(
        self,
        visual_plan: dict[str, Any],
        request: dict[str, Any],
    ) -> None:
        actions_by_slide = {
            item.get("slide_id"): item.get("actions", [])
            for item in request.get("slides", [])
            if isinstance(item, dict)
        }
        for slide in visual_plan.get("slides", []):
            if not isinstance(slide, dict):
                continue
            actions = actions_by_slide.get(slide.get("slide_id"))
            if not actions:
                continue
            slide["revision"] = {
                "iteration": 1,
                "actions": actions,
                "protected_fields": request.get("protected_fields", []),
            }
            action_names = {
                action.get("action")
                for action in actions
                if isinstance(action, dict)
            }
            if "enlarge_primary_anchor" in action_names:
                layout = slide.get("layout")
                if isinstance(layout, dict):
                    layout["primary_zone_ratio"] = max(
                        float(layout.get("primary_zone_ratio", 0.0)),
                        0.68,
                    )
            if "rebalance_density" in action_names:
                density = slide.get("density")
                if isinstance(density, dict):
                    density["level"] = "medium"
        write_json(self.contracts / "visual-plan.json", visual_plan)

    def score(self) -> None:
        if self.args.profile != "premium":
            return
        if not self.args.rubric_case or not self.args.use_reference_rubric:
            raise StageFailure(
                "score",
                "PREMIUM_RUBRIC_REQUIRED: pass --rubric-case and --use-reference-rubric; "
                "automatic metrics cannot grant final status",
            )
        completed = self.run_command(
            "score",
            [
                sys.executable,
                str(SCRIPTS / "score_deck.py"),
                "--case",
                str(self.args.rubric_case.resolve()),
                "--ppt-ir",
                str(self.contracts / "ppt-ir.json"),
                "--qa-report",
                str(self.qa / "qa-report.json"),
                "--build-manifest",
                str(self.contracts / "build-manifest.json"),
                "--pptx",
                str(self.deck_path()),
                "--output",
                str(self.qa / "benchmark-score.json"),
                "--use-reference-rubric",
            ],
            accepted={0, 1},
        )
        if completed.returncode != 0:
            score_path = self.qa / "benchmark-score.json"
            if score_path.exists():
                score = load_json(score_path)
                raise StageFailure(
                    "score",
                    f"PREMIUM_RUBRIC_FAILED: total={score.get('total_score')} "
                    f"status={score.get('overall_status')}",
                    completed.returncode,
                )
            raise StageFailure("score", "PREMIUM_RUBRIC_SCORER_FAILED", completed.returncode)

    def create_contact_sheet(self, render_report: dict[str, Any]) -> None:
        from PIL import Image, ImageDraw

        slide_paths = [
            Path(str(item.get("image")))
            for item in render_report.get("slides", [])
            if item.get("image")
        ]
        if not slide_paths or any(not path.is_file() for path in slide_paths):
            raise StageFailure("prepare_delivery", "PREMIUM_CONTACT_SHEET_INPUT_MISSING")
        thumb_width = 480
        margin = 20
        label_height = 30
        thumbs: list[Image.Image] = []
        for path in slide_paths:
            with Image.open(path) as source:
                thumb = source.convert("RGB")
                thumb.thumbnail((thumb_width, 300))
                thumbs.append(thumb.copy())
        columns = 3
        cell_width = thumb_width + margin * 2
        cell_height = max(image.height for image in thumbs) + label_height + margin * 2
        rows = (len(thumbs) + columns - 1) // columns
        sheet = Image.new("RGB", (cell_width * columns, cell_height * rows), "white")
        draw = ImageDraw.Draw(sheet)
        for index, thumb in enumerate(thumbs):
            x = (index % columns) * cell_width + margin
            y = (index // columns) * cell_height + margin + label_height
            draw.text((x, y - label_height + 5), f"Slide {index + 1}", fill="black")
            sheet.paste(thumb, (x, y))
        target = self.work / "renders" / "contact-sheet.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(target)

    def prepare_delivery(self) -> None:
        build_path = self.contracts / "build-manifest.json"
        build = load_json(build_path)
        qa = load_json(self.qa / "qa-report.json")
        inspection = load_json(self.qa / "pptx-inspection.json")
        benchmark = (
            load_json(self.qa / "benchmark-score.json")
            if (self.qa / "benchmark-score.json").exists()
            else None
        )
        from package_delivery import calculate_delivery_status

        trusted = calculate_delivery_status(
            profile=self.args.profile,
            build_manifest=build,
            qa_report=qa,
            benchmark_score=benchmark,
            pptx_path=self.deck_path(),
        )
        qa["trusted_delivery_status"] = trusted
        write_json(self.qa / "qa-report.json", qa)
        build["status"] = trusted if trusted in {"created", "rendered", "read_back", "verified", "final"} else "failed"
        build["last_successful_stage"] = "verify"
        build["failed_stage"] = None if qa.get("status") not in {"fail", "blocked"} else "verify"
        build["contract_refs"]["qa_report"] = "../../qa/qa-report.json"
        build["contract_refs"]["production_profile"] = "production-profile.json"
        build["stages"].update({
            "read_back": inspection.get("status") == "passed",
            "verified": trusted in {"verified", "final"},
            "qa_passed": qa.get("status") in {"pass", "warning"},
            "rendered": bool((qa.get("evidence", {}).get("render_report") or {}).get("status") == "passed"),
        })
        build["metrics"].update(qa.get("metrics", {}))
        build["outputs"]["deck"] = str(self.deck_path().resolve())
        report = self.build_dir / "verification-report.md"
        report.write_text(
            "# Verification Report\n\n"
            f"- Profile: {self.args.profile}\n- Structural inspection: {inspection.get('status')}\n"
            f"- QA status: {qa.get('status')}\n- Trusted delivery status: {trusted}\n",
            encoding="utf-8",
        )
        build["outputs"]["verification_report"] = str(report.resolve())
        render = qa.get("evidence", {}).get("render_report")
        render_pdf = (
            render.get("pdf") or render.get("pdf_path")
            if isinstance(render, dict)
            else None
        )
        if isinstance(render, dict) and render.get("status") == "passed" and render_pdf:
            pdf = Path(str(render_pdf))
            if pdf.is_file():
                target = self.build_dir / "deck-preview.pdf"
                shutil.copy2(pdf, target)
                build["outputs"]["preview_pdf"] = str(target.resolve())
            if self.args.profile == "premium":
                self.create_contact_sheet(render)
        write_json(build_path, build)
        self.validate("prepare_delivery", include_delivery=True, include_build=True)

    def package(self) -> None:
        manifest = self.output / "delivery-manifest.json"
        command = [
            sys.executable, str(SCRIPTS / "package_delivery.py"),
            "--workdir", str(self.work),
            "--profile", self.args.profile,
            "--output", str(self.output),
            "--manifest", str(manifest),
            "--strict",
        ]
        self.run_command("package_delivery", command)
        (self.output / OUTPUT_OWNERSHIP_MARKER).write_text(
            "PPTSmith managed output directory.\n",
            encoding="utf-8",
        )

    def run(self) -> int:
        self.work.mkdir(parents=True, exist_ok=True)
        self.save_state()
        try:
            self.stage("prepare_inputs", self.prepare_inputs)
            self.stage("validate_inputs", lambda: self.validate("validate_inputs"))
            if self.visual_enabled:
                self.stage("route_audience", self.route_audience)
                self.stage("route_task", self.route_task)
                self.stage("design_evidence", self.design_evidence)
                self.stage("plan_visual_narrative", self.plan_visual_narrative)
                self.stage("validate_visual_plan", self.validate_visual_plan)
                self.stage("compile_visual_plan", self.compile_visual_plan)
            self.stage("enrich_ir", self.enrich_ir)
            self.stage("ir_quality_floor", self.ir_quality_floor)
            if self.visual_enabled:
                self.stage("deck_rhythm", self.deck_rhythm)
            self.stage("resolve_profile", self.resolve_profile)
            self.stage("capability_probe", self.capability_probe)
            self.stage("resolve_delivery", self.resolve_delivery)
            self.stage("validate_delivery", lambda: self.validate("validate_delivery", include_delivery=True))
            self.stage("build", self.build)
            self.stage("inspect", self.inspect)
            self.stage("verify", self.verify)
            if self.visual_enabled:
                self.stage("visual_revision", self.visual_revision)
            self.stage("score", self.score)
            self.stage("prepare_delivery", self.prepare_delivery)
            self.stage("package_delivery", self.package)
        except (StageFailure, OSError, ValueError, json.JSONDecodeError) as exc:
            failed_stage = exc.stage if isinstance(exc, StageFailure) else str(self.state.get("current_stage") or "initialize")
            self.state.update({"status": "blocked" if self.state.get("provisional_reason") else "failed", "failed_stage": failed_stage, "current_stage": failed_stage, "error": str(exc), "completed_at": iso_now()})
            self.save_state()
            print(f"run_pipeline [{failed_stage}]: {exc}", file=sys.stderr)
            return exc.returncode if isinstance(exc, StageFailure) and exc.returncode else 1
        self.state.update({"status": "completed", "failed_stage": None, "current_stage": None, "error": None, "completed_at": iso_now()})
        self.save_state()
        if self.args.json_output:
            print(json.dumps({"ok": True, "state": str(self.state_path), "output": str(self.output)}, indent=2))
        return 0


def main(argv: list[str]) -> int:
    return Pipeline(parse_args(argv)).run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
