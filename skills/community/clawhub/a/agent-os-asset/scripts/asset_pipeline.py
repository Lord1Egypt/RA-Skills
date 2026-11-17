#!/usr/bin/env python3
"""Orchestrate the Agent Asset pipeline through project adapters / 通过项目 adapters 编排 Agent Asset pipeline。

This script intentionally does not implement file extraction itself.  It
coordinates stage commands and delegates concrete conversion/review behavior to
a project adapter such as ``tools/cleanup_convert.py``.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = SKILL_ROOT / "skills"
DEFAULT_SECOND_BRAIN_ROUTINE = SKILL_ROOT / "skills" / "second-brain" / "scripts" / "routine_update.py"
DEFAULT_RETRIEVAL_QUALITY_SCRIPT = SKILL_ROOT / "skills" / "second-brain" / "scripts" / "retrieval_quality.py"
DEFAULT_INDEX_DIR = ".cleanup-extracted/second-brain-asset-index"
DEFAULT_DECISION_LEDGER = ".cleanup-extracted/asset-decisions.json"
DEFAULT_MIXED_FOLDER_ADAPTER = SKILL_ROOT / "scripts" / "mixed_folder_adapter.py"


def default_index_registry() -> Path:
    """Resolve the registry from the bundled child's portable runtime settings."""
    spec = importlib.util.spec_from_file_location(
        "_agent_asset_runtime_paths", DEFAULT_SECOND_BRAIN_ROUTINE.parent / "runtime_paths.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.resolve_paths().asset_registry.expanduser().resolve()


DEFAULT_INDEX_REGISTRY = default_index_registry()

PIPELINES = {
    "review": ["inventory", "suggest", "workbench", "audit"],
    "prepare": ["inventory", "extract", "suggest", "workbench"],
    "apply": ["apply-dry-run", "apply", "audit"],
    "maintain": ["sync", "index"],
    "index": ["audit", "index"],
    "full": ["inventory", "extract", "suggest", "workbench", "apply-dry-run", "apply", "audit", "index"],
    "optimize-retrieval": ["retrieval-audit", "retrieval-refresh", "index", "retrieval-verify"],
}


@dataclass
class StagePlan:
    stage: str
    command: list[str]
    description: str
    blocked_reason: str = ""
    mutates_sources: bool = False
    allow_returncodes: tuple[int, ...] = (0,)


@dataclass
class StageResult:
    stage: str
    status: str
    command: list[str]
    returncode: int | None = None
    stdout: str = ""
    stderr: str = ""
    blocked_reason: str = ""


def display_path(path: Path) -> str:
    return path.expanduser().resolve(strict=False).as_posix()


def default_cleanup_tool(root: Path) -> Path:
    """Source folders are data, never an executable-discovery search path."""
    return DEFAULT_MIXED_FOLDER_ADAPTER


def validate_workspace(root: Path, scope: str) -> str:
    """Validate resolved paths before any subprocess or state write."""
    root = root.resolve()
    scoped = (root / scope).resolve()
    scoped.relative_to(root)
    state = root / ".cleanup-extracted"
    for path in (state, state / "asset-decisions.json", state / "asset-manifest.jsonl",
                 state / "second-brain-asset-index", state / "retrieval-benchmark.json",
                 state / "second-brain-routine.log", state / "second-brain-routine.lock",
                 state / "retrieval-quality-strict-top1.json", state / "retrieval-quality-semantic-top1.json"):
        path.resolve().relative_to(state)
        if path.is_symlink():
            raise ValueError("run-state paths cannot be symlinks / 运行状态路径不能是符号链接")
    return scoped.relative_to(root).as_posix()


def index_scope_error(root: Path, scope: str) -> str:
    """Fail closed if the workspace-wide indexer would exceed this request.

    The bundled SecondBrain routine has no scope flag. Do not silently broaden
    a subdirectory request, or temporarily rewrite the shared source manifest.
    """
    root = root.resolve()
    try:
        validate_workspace(root, scope)
        active = (root / scope).resolve()
        archive = root / "Archived" / active.relative_to(root)
        manifest = root / ".cleanup-extracted" / "asset-manifest.jsonl"
        if not manifest.exists():
            return ""  # The configured routine owns missing-manifest diagnostics.
        if not manifest.is_file() or manifest.stat().st_size > 64 * 1024 * 1024:
            return "asset manifest is not a bounded regular file / 资产清单不是大小受限的普通文件"
        with manifest.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                if not isinstance(row, dict):
                    return "invalid manifest row / 无效的清单行"
                if str(row.get("index_status", "")).lower() not in {"final", "keep", "retained", "indexed"}:
                    continue
                if str(row.get("asset_type", "")).lower() in {"embedded_attachment", "temp", "generated_report"}:
                    continue
                if row.get("privacy") != "non_pii":
                    return "final asset privacy must be explicitly non_pii / 最终资产必须显式标注 non_pii 隐私状态"
                references = []
                for field in ("source_paths", "semantic_paths"):
                    values = row.get(field, [])
                    if not isinstance(values, list) or any(not isinstance(value, str) or not value for value in values):
                        return "invalid manifest paths / 无效的清单路径"
                    references.extend(values)
                if row.get("path"):
                    if not isinstance(row["path"], str):
                        return "invalid manifest path / 无效的清单路径"
                    references.append(row["path"])
                if not references:
                    return "final asset has no scoped paths / 最终资产缺少范围内的路径"
                for reference in references:
                    path = (root / reference).resolve()
                    path.relative_to(root)
                    if not (path.is_relative_to(active) or path.is_relative_to(archive)):
                        return (
                            "workspace-wide indexer would include final assets outside --scope; retain the prior index and request a separately approved whole-workspace or isolated index / 工作区索引器会纳入 --scope 外的最终资产；保留原索引，需另行批准整个工作区索引或隔离索引"
                        )
    except (OSError, ValueError, RuntimeError) as exc:
        return f"unsafe index input / 不安全的索引输入: {type(exc).__name__}"
    return ""


def index_effects(args: argparse.Namespace) -> str:
    return (f"index output={display_path(args.index_out)}; registry={display_path(DEFAULT_INDEX_REGISTRY)}; "
            f"log/lock under {display_path(args.root / '.cleanup-extracted')} / 索引输出、注册表及日志与锁的实际写入位置如上")


def scope_args(scope: str) -> list[str]:
    if not scope or scope == ".":
        return []
    return ["--scope", scope]


def cleanup_command(args: argparse.Namespace, *extra: str) -> list[str]:
    return ["python3", display_path(args.cleanup_tool), *scope_args(args.scope), *extra]


def index_requested(args: argparse.Namespace) -> bool:
    if args.pipeline == "index":
        return True
    return any("index" in {part.strip() for part in item.split(",")} for item in (args.stage or []))


def parse_json_output(value: str) -> dict[str, object]:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def post_apply_index_ready(apply_payload: dict[str, object], audit_payload: dict[str, object]) -> tuple[bool, str]:
    if apply_payload.get("success") is not True:
        return False, "apply reported failed delete effects"
    summary = apply_payload.get("summary", {})
    if not isinstance(summary, dict) or summary.get("unmatched_decisions", 0) != 0:
        return False, "apply reported unmatched decision IDs"
    audit_summary = audit_payload.get("summary", {})
    if not isinstance(audit_summary, dict):
        return False, "audit did not return a summary"
    blockers = [
        name for name in ("candidate", "review", "missing_source", "missing_semantic", "final_pii", "delete_failed")
        if audit_summary.get(name, 0) != 0
    ]
    if audit_summary.get("ready_for_scope_index") is not True or blockers:
        return False, "scope is not index-ready" + (": " + ", ".join(blockers) if blockers else "")
    return True, "scope is index-ready"


def automatic_index_command(args: argparse.Namespace) -> list[str]:
    command = [
        "python3",
        display_path(args.second_brain_routine),
        "--vault",
        display_path(args.root),
        "--out",
        display_path(args.index_out),
        "--source-mode",
        "asset-manifest",
        "--json",
        "--log", display_path(args.root / ".cleanup-extracted/second-brain-routine.log"),
        "--lock", display_path(args.root / ".cleanup-extracted/second-brain-routine.lock"),
        "--asset-index-registry", display_path(DEFAULT_INDEX_REGISTRY),
    ]
    if args.force_index:
        command.append("--force")
    return command


def retrieval_report_path(args: argparse.Namespace, semantic_rerank: str = "never") -> Path:
    suffix = "semantic-top1" if semantic_rerank != "never" else "strict-top1"
    return args.root / ".cleanup-extracted" / f"retrieval-quality-{suffix}.json"


def retrieval_quality_command(args: argparse.Namespace, semantic_rerank: str = "never") -> list[str]:
    command = [
        "python3",
        display_path(DEFAULT_RETRIEVAL_QUALITY_SCRIPT),
        "--index",
        display_path(args.index_out / "documents.jsonl"),
        "--benchmark",
        display_path(args.retrieval_benchmark),
        "--out",
        display_path(retrieval_report_path(args, semantic_rerank)),
        "--json",
    ]
    if semantic_rerank != "never":
        command.extend(["--semantic-rerank", semantic_rerank])
    return command


def stage_plan(stage: str, args: argparse.Namespace) -> StagePlan:
    cleanup_stages = {
        "inventory", "extract", "suggest", "workbench", "apply-dry-run", "apply", "sync", "audit",
        "retrieval-audit", "retrieval-refresh",
    }
    if stage in cleanup_stages and not args.cleanup_tool.exists():
        return StagePlan(
            stage=stage,
            command=[],
            description="Project cleanup adapter is missing / 缺少项目 cleanup adapter。",
            blocked_reason=f"missing cleanup adapter / 缺少 cleanup adapter: {display_path(args.cleanup_tool)}",
        )

    if stage == "inventory":
        return StagePlan(
            stage=stage,
            command=cleanup_command(args),
            description="Build inventory and working manifest through the project adapter / 通过项目 adapter 构建 inventory 与 working manifest。",
        )
    if stage == "extract":
        if not args.execute_extraction:
            return StagePlan(
                stage=stage,
                command=cleanup_command(args, "--execute"),
                description="Run extraction or conversion and archive originals through the project adapter / 通过项目 adapter 执行提取或转换并归档 originals。",
                blocked_reason="extract mutates source layout; rerun with --execute-extraction / extract 会修改 source layout；请使用 --execute-extraction 重新运行",
                mutates_sources=True,
            )
        return StagePlan(
            stage=stage,
            command=cleanup_command(args, "--execute"),
            description="Run extraction or conversion and archive originals through the project adapter / 通过项目 adapter 执行提取或转换并归档 originals。",
            mutates_sources=True,
        )
    if stage == "suggest":
        return StagePlan(
            stage=stage,
            command=cleanup_command(args, "--suggest-asset-decisions"),
            description="Generate KB Review asset decision suggestions / 生成 KB Review 资产决策建议。",
        )
    if stage == "workbench":
        command = cleanup_command(args, "--build-asset-review-workbench")
        if args.workbench_decisions:
            command.extend(["--workbench-decisions", args.workbench_decisions])
        return StagePlan(
            stage=stage,
            command=command,
            description="Build or refresh the asset review workbench / 构建或刷新资产 review workbench。",
        )
    if stage == "apply-dry-run":
        if not args.decisions:
            return StagePlan(
                stage=stage,
                command=[],
                description="Dry-run exported asset decisions / 对导出的资产决策执行 dry-run。",
                blocked_reason="missing --decisions / 缺少 --decisions",
            )
        return StagePlan(
            stage=stage,
            command=cleanup_command(args, "--apply-decisions", args.decisions),
            description="Dry-run exported asset decisions / 对导出的资产决策执行 dry-run。",
        )
    if stage == "apply":
        if not args.decisions:
            return StagePlan(
                stage=stage,
                command=[],
                description="Apply exported asset decisions / 应用导出的资产决策。",
                blocked_reason="missing --decisions / 缺少 --decisions",
                mutates_sources=True,
            )
        if not args.execute_decisions:
            return StagePlan(
                stage=stage,
                command=cleanup_command(args, "--apply-decisions", args.decisions, "--execute"),
                description="Apply exported asset decisions / 应用导出的资产决策。",
                blocked_reason="apply can move delete decisions to system Trash; rerun with --execute-decisions / apply 可能把 delete 决策移入系统 Trash；请使用 --execute-decisions 重新运行",
                mutates_sources=True,
            )
        return StagePlan(
            stage=stage,
            command=cleanup_command(args, "--apply-decisions", args.decisions, "--execute"),
            description=(
                "Apply exported asset decisions; conditional fresh audit / 应用导出的资产决策；按条件重新审计。 " + index_effects(args)
                if args.after_apply_index == "auto"
                else "Apply exported asset decisions; no automatic index / 应用导出的资产决策；不自动索引。"
            ),
            mutates_sources=True,
        )
    if stage == "sync":
        command = cleanup_command(args, "--sync", "--execute")
        if args.auto_keep:
            command.append("--auto-keep")
        if not args.execute_sync:
            return StagePlan(
                stage=stage,
                command=command,
                description="Reconcile source additions, modifications, removals, and Agent Assets / 协调 source 新增、修改、删除与 Agent Assets。",
                blocked_reason="sync writes semantic entries and manifest state; rerun with --execute-sync / sync 会写入 semantic entries 与 manifest state；请使用 --execute-sync 重新运行",
                mutates_sources=True,
            )
        return StagePlan(
            stage=stage,
            command=command,
            description="Reconcile source additions, modifications, removals, and Agent Assets / 协调 source 新增、修改、删除与 Agent Assets。",
            mutates_sources=True,
        )
    if stage == "audit":
        return StagePlan(
            stage=stage,
            command=cleanup_command(args, "--audit-agent-assets"),
            description="Audit readiness before final SecondBrain indexing / 在最终 SecondBrain indexing 前审计就绪状态。",
            allow_returncodes=(0,) if args.strict_audit or index_requested(args) else (0, 2),
        )
    if stage == "retrieval-audit":
        return StagePlan(
            stage=stage,
            command=cleanup_command(args, "--audit-retrieval-quality"),
            description="Audit final project semantic entries for low-signal retrieval metadata / 审计 final project semantic entries 中的低信号检索元数据。",
        )
    if stage == "retrieval-refresh":
        command = cleanup_command(args, "--refresh-retrieval", "--execute")
        if not args.execute_retrieval_refresh:
            return StagePlan(
                stage=stage,
                command=command,
                description="Regenerate weak final repo entries from bounded project evidence / 根据有边界的项目证据重建低质量 final repo entries。",
                blocked_reason="retrieval refresh rewrites selected repo.agent.md entries; rerun with --execute-retrieval-refresh / retrieval refresh 会重写选中的 repo.agent.md entries；请使用 --execute-retrieval-refresh 重新运行",
                mutates_sources=True,
            )
        if args.pipeline == "optimize-retrieval" and not args.stage and not args.execute_index:
            return StagePlan(
                stage=stage, command=command,
                description="Regenerate weak final repo entries from bounded project evidence / 根据有边界的项目证据重建低质量 final repo entries。",
                blocked_reason="optimize-retrieval also requires --execute-index before refreshing entries / optimize-retrieval 刷新条目前还需要 --execute-index",
                mutates_sources=True,
            )
        return StagePlan(
            stage=stage,
            command=command,
            description="Regenerate weak final repo entries from bounded project evidence / 根据有边界的项目证据重建低质量 final repo entries。",
            mutates_sources=True,
        )
    if stage == "retrieval-verify":
        if not DEFAULT_RETRIEVAL_QUALITY_SCRIPT.exists():
            return StagePlan(
                stage=stage,
                command=[],
                description="Evaluate strict Top-1 retrieval quality after rebuilding the project index / 重建项目索引后评估 strict Top-1 检索质量。",
                blocked_reason=f"missing retrieval quality script / 缺少 retrieval quality script: {display_path(DEFAULT_RETRIEVAL_QUALITY_SCRIPT)}",
            )
        if not args.retrieval_benchmark.exists():
            return StagePlan(
                stage=stage,
                command=[],
                description="Evaluate strict Top-1 retrieval quality after rebuilding the project index / 重建项目索引后评估 strict Top-1 检索质量。",
                blocked_reason=f"missing retrieval benchmark / 缺少 retrieval benchmark: {display_path(args.retrieval_benchmark)}",
            )
        return StagePlan(
            stage=stage,
            command=retrieval_quality_command(args),
            description="Evaluate strict Top-1 retrieval quality and flag embedding-rerank escalation when needed / 评估 strict Top-1 检索质量，并在需要时标记 embedding-rerank escalation。",
            allow_returncodes=(0, 3),
        )
    if stage == "index":
        auto_maintain_index = args.pipeline == "maintain" and args.auto_keep and args.execute_sync
        if not args.execute_index and not auto_maintain_index:
            return StagePlan(
                stage=stage,
                command=[],
                description="Build final SecondBrain index from the reviewed asset manifest / 从已 review 的 asset manifest 构建最终 SecondBrain index。",
                blocked_reason="final indexing is disabled until --execute-index is set / 设置 --execute-index 前，final indexing 保持禁用",
            )
        if not args.second_brain_routine.exists():
            return StagePlan(
                stage=stage,
                command=[],
                description="Build final SecondBrain index from the reviewed asset manifest / 从已 review 的 asset manifest 构建最终 SecondBrain index。",
                blocked_reason=f"missing second-brain routine / 缺少 second-brain routine: {display_path(args.second_brain_routine)}",
            )
        ledger = args.root / DEFAULT_DECISION_LEDGER
        if not args.skip_decision_ledger_check and not auto_maintain_index and not ledger.exists():
            return StagePlan(
                stage=stage,
                command=[],
                description="Build final SecondBrain index from the reviewed asset manifest / 从已 review 的 asset manifest 构建最终 SecondBrain index。",
                blocked_reason=f"missing reviewed decision ledger / 缺少已 review 的 decision ledger: {ledger.as_posix()}",
            )
        command = automatic_index_command(args)
        return StagePlan(
            stage=stage,
            command=command,
            description="Build final SecondBrain index after fresh audit and scope check / 重新审计并检查范围后构建最终 SecondBrain 索引。 " + index_effects(args),
        )
    raise ValueError(f"unknown stage: {stage}")


def selected_stages(args: argparse.Namespace) -> list[str]:
    stages: list[str] = []
    if args.stage:
        for item in args.stage:
            stages.extend(part.strip() for part in item.split(",") if part.strip())
    else:
        stages.extend(PIPELINES[args.pipeline])
        if args.pipeline == "maintain" and not args.auto_keep and not args.execute_index:
            stages.remove("index")
    valid = set().union(*PIPELINES.values())
    invalid = [stage for stage in stages if stage not in valid]
    if invalid:
        raise ValueError(f"unknown stage(s): {', '.join(invalid)}")
    return stages


def build_plan(args: argparse.Namespace) -> list[StagePlan]:
    return [stage_plan(stage, args) for stage in selected_stages(args)]


def print_plan(plan: list[StagePlan], json_output: bool) -> None:
    payload = [asdict(item) for item in plan]
    if json_output:
        print(json.dumps({"plan": payload}, ensure_ascii=False, indent=2))
        return
    for item in plan:
        status = "BLOCKED" if item.blocked_reason else "READY"
        print(f"[{status}] {item.stage}: {item.description}")
        if item.blocked_reason:
            print(f"  reason / 原因: {item.blocked_reason}")
        if item.command:
            print("  command / 命令: " + shlex.join(item.command))


def run_plan(args: argparse.Namespace, plan: list[StagePlan]) -> list[StageResult]:
    validate_workspace(args.root, args.scope)
    results: list[StageResult] = []
    for item in plan:
        if item.stage == "index" and args.pipeline == "maintain" and args.auto_keep:
            prior_sync = next((result for result in reversed(results) if result.stage == "sync"), None)
            try:
                sync_payload = json.loads(prior_sync.stdout) if prior_sync else {}
            except json.JSONDecodeError:
                sync_payload = {}
            if not isinstance(sync_payload, dict) or sync_payload.get("index_ready") is not True:
                results.append(
                    StageResult(
                        stage="index",
                        status="skipped",
                        command=item.command,
                        blocked_reason="sync reported no fully-final successful change set; retaining the prior index",
                    )
                )
                continue
        if item.blocked_reason:
            result = StageResult(
                stage=item.stage,
                status="blocked",
                command=item.command,
                blocked_reason=item.blocked_reason,
            )
            results.append(result)
            if not args.continue_on_error:
                break
            continue
        if item.stage == "index":
            # Even direct index / ledger override needs fresh scope review evidence.
            audit_command = cleanup_command(args, "--audit-agent-assets")
            audit_result = subprocess.run(
                audit_command, cwd=args.root, text=True, capture_output=True, check=False,
            )
            ready, reason = post_apply_index_ready(
                {"success": True}, parse_json_output(audit_result.stdout)
            )
            ready = ready and audit_result.returncode == 0
            scope_error = index_scope_error(args.root, args.scope)
            if scope_error:
                ready, reason = False, scope_error
            results.append(StageResult(
                stage="pre-index-audit", status="ok" if ready else "blocked",
                command=audit_command, returncode=audit_result.returncode,
                stdout=audit_result.stdout, stderr=audit_result.stderr,
                blocked_reason="" if ready else reason if audit_result.returncode == 0 else "audit command failed / 审计命令失败",
            ))
            if not ready:
                results.append(StageResult(
                    stage="index", status="blocked", command=item.command,
                    blocked_reason=reason if audit_result.returncode == 0 else "fresh scope audit did not succeed / 最新范围审计未成功",
                ))
                if not args.continue_on_error:
                    break
                continue
        result = subprocess.run(
            item.command,
            cwd=args.root,
            text=True,
            capture_output=True,
            check=False,
        )
        status = "ok" if result.returncode in item.allow_returncodes else "failed"
        if item.stage == "retrieval-verify" and result.returncode == 3:
            status = "attention"
        results.append(
            StageResult(
                stage=item.stage,
                status=status,
                command=item.command,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )
        )
        if item.stage == "retrieval-verify" and result.returncode == 3 and args.allow_semantic_rerank:
            semantic_command = retrieval_quality_command(args, semantic_rerank="auto")
            semantic_result = subprocess.run(
                semantic_command,
                cwd=args.root,
                text=True,
                capture_output=True,
                check=False,
            )
            semantic_status = "ok" if semantic_result.returncode == 0 else "attention" if semantic_result.returncode == 3 else "failed"
            results.append(
                StageResult(
                    stage="retrieval-semantic-verify",
                    status=semantic_status,
                    command=semantic_command,
                    returncode=semantic_result.returncode,
                    stdout=semantic_result.stdout,
                    stderr=semantic_result.stderr,
                )
            )
            if semantic_status == "failed" and not args.continue_on_error:
                break
        if item.stage == "apply" and status == "ok" and args.execute_decisions and args.after_apply_index == "auto":
            apply_payload = parse_json_output(result.stdout)
            audit_command = cleanup_command(args, "--audit-agent-assets")
            audit_result = subprocess.run(
                audit_command,
                cwd=args.root,
                text=True,
                capture_output=True,
                check=False,
            )
            audit_status = "ok" if audit_result.returncode in {0, 2} else "failed"
            results.append(
                StageResult(
                    stage="post-apply-audit",
                    status=audit_status,
                    command=audit_command,
                    returncode=audit_result.returncode,
                    stdout=audit_result.stdout,
                    stderr=audit_result.stderr,
                )
            )
            if audit_status == "failed":
                if not args.continue_on_error:
                    break
                continue
            ready, reason = post_apply_index_ready(apply_payload, parse_json_output(audit_result.stdout))
            scope_error = index_scope_error(args.root, args.scope)
            if scope_error:
                ready, reason = False, scope_error
            if not ready or audit_result.returncode != 0:
                results.append(
                    StageResult(
                        stage="post-apply-index",
                        status="skipped",
                        command=[],
                        blocked_reason=reason if not ready else "audit command did not succeed / 审计命令未成功",
                    )
                )
                continue
            if not args.second_brain_routine.exists():
                results.append(
                    StageResult(
                        stage="post-apply-index",
                        status="failed",
                        command=[],
                        blocked_reason=f"missing second-brain routine: {display_path(args.second_brain_routine)}",
                    )
                )
                if not args.continue_on_error:
                    break
                continue
            index_command = automatic_index_command(args)
            index_result = subprocess.run(
                index_command,
                cwd=args.root,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                StageResult(
                    stage="post-apply-index",
                    status="ok" if index_result.returncode == 0 else "failed",
                    command=index_command,
                    returncode=index_result.returncode,
                    stdout=index_result.stdout,
                    stderr=index_result.stderr,
                )
            )
            if index_result.returncode != 0 and not args.continue_on_error:
                break
        if status != "ok" and not args.continue_on_error:
            break
    return results


def print_results(results: list[StageResult], json_output: bool) -> None:
    payload = [asdict(item) for item in results]
    if json_output:
        print(json.dumps({"results": payload}, ensure_ascii=False, indent=2))
        return
    for item in results:
        print(f"[{item.status.upper()}] {item.stage}")
        if item.blocked_reason:
            print(f"  reason / 原因: {item.blocked_reason}")
        if item.returncode is not None:
            print(f"  returncode / 返回码: {item.returncode}")
        if item.stdout.strip():
            print(item.stdout.rstrip())
        if item.stderr.strip():
            print(item.stderr.rstrip(), file=sys.stderr)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Agent Asset workspace root / Agent Asset 工作区根目录。")
    parser.add_argument("--scope", default=".", help="Scope path under the workspace root / 工作区根目录下的 scope 路径。")
    parser.add_argument(
        "--cleanup-tool",
        type=Path,
        help="Explicitly trusted custom adapter; defaults only to the bundled mixed-folder adapter, never workspace code / 显式信任的自定义 adapter；默认仅使用随包 mixed-folder adapter，绝不自动执行工作区代码。",
    )
    parser.add_argument(
        "--pipeline",
        choices=sorted(PIPELINES),
        default="review",
        help="Stage bundle to run when --stage is omitted / 未提供 --stage 时运行的 stage bundle。",
    )
    parser.add_argument(
        "--stage",
        action="append",
        help="Specific stages, comma-separated or repeated; overrides --pipeline / 指定 stages，可逗号分隔或重复提供；覆盖 --pipeline。",
    )
    parser.add_argument("--decisions", help="Exported decisions JSON for apply or apply-dry-run / 用于 apply 或 apply-dry-run 的已导出 decisions JSON。")
    parser.add_argument("--workbench-decisions", help="Decisions JSON used only to prefill workbench fields / 仅用于预填 workbench 字段的 decisions JSON。")
    parser.add_argument("--execute-extraction", action="store_true", help="Allow extraction or archive stages to mutate sources / 允许 extraction 或 archive 阶段修改 sources。")
    parser.add_argument("--execute-sync", action="store_true", help="Allow sync to update Agent Assets and manifest state / 允许 sync 更新 Agent Assets 与 manifest state。")
    parser.add_argument("--auto-keep", action="store_true", help="For maintain, auto-keep successful non-PII changes and conditionally refresh the final index / 在 maintain 中自动保留成功的 non-PII changes，并按条件刷新 final index。")
    parser.add_argument("--execute-decisions", action="store_true", help="Allow apply to write the ledger and move delete assets to Trash / 允许 apply 写入 ledger，并把 delete assets 移入 Trash。")
    parser.add_argument(
        "--after-apply-index",
        choices=["auto", "never"],
        default="auto",
        help="After execute-decisions apply, conditionally run asset-manifest indexing when the scope audit is ready / 执行 decisions apply 后，在 scope audit 就绪时按条件运行 asset-manifest indexing。",
    )
    parser.add_argument("--execute-index", action="store_true", help="Allow final SecondBrain asset-manifest indexing / 允许最终 SecondBrain asset-manifest indexing。")
    parser.add_argument(
        "--execute-retrieval-refresh",
        action="store_true",
        help="Allow controlled regeneration of low-signal final repo.agent.md entries / 允许受控重建低信号 final repo.agent.md entries。",
    )
    parser.add_argument("--force-index", action="store_true", help="Pass --force to the second-brain final index build / 向 second-brain final index build 传递 --force。")
    parser.add_argument("--allow-semantic-rerank", action="store_true", help="Opt in to the configured embedding/rerank provider after lexical failure; may send approved text to that provider / 显式允许词法检索失败后使用已配置的 embedding/rerank provider；可能向该提供方发送已批准的文本。")
    parser.add_argument("--strict-audit", action="store_true", help="Treat an audit not-ready return code as a hard failure / 将 audit not-ready 返回码视为硬失败。")
    parser.add_argument("--skip-decision-ledger-check", action="store_true", help="Allow a missing ledger file, but never bypass a fresh scope-readiness audit / 允许缺少 ledger 文件，但不能跳过最新的范围就绪审计。")
    parser.add_argument(
        "--second-brain-routine",
        type=Path,
        default=DEFAULT_SECOND_BRAIN_ROUTINE,
        help="Path to second-brain/scripts/routine_update.py / second-brain/scripts/routine_update.py 的路径。",
    )
    parser.add_argument(
        "--index-out",
        type=Path,
        help=f"SecondBrain asset index output directory; defaults to <root>/{DEFAULT_INDEX_DIR} / SecondBrain asset index 输出目录；默认为 <root>/{DEFAULT_INDEX_DIR}。",
    )
    parser.add_argument(
        "--retrieval-benchmark",
        type=Path,
        help="Strict Top-1 benchmark JSON; defaults to <root>/.cleanup-extracted/retrieval-benchmark.json / Strict Top-1 benchmark JSON；默认为 <root>/.cleanup-extracted/retrieval-benchmark.json。",
    )
    parser.add_argument("--plan-only", action="store_true", help="Print the plan without running commands / 只打印 plan，不运行命令。")
    parser.add_argument("--continue-on-error", action="store_true", help="Continue after blocked or failed stages / 遇到 blocked 或 failed stages 后继续。")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output / 打印机器可读 JSON 输出。")
    parser.add_argument("--self-test", action="store_true", help="Run built-in command-planning tests / 运行内置命令规划测试。")
    args = parser.parse_args(argv)
    args.root = args.root.expanduser().resolve()
    try:
        args.scope = validate_workspace(args.root, args.scope)
    except (ValueError, OSError, RuntimeError) as exc:
        parser.error(f"scope or state path escapes workspace / 范围或状态路径越出工作区: {exc}")
    if args.cleanup_tool is None:
        args.cleanup_tool = default_cleanup_tool(args.root)
    else:
        args.cleanup_tool = args.cleanup_tool.expanduser().resolve()
    args.second_brain_routine = args.second_brain_routine.expanduser().resolve()
    if args.index_out is None:
        args.index_out = args.root / DEFAULT_INDEX_DIR
    else:
        args.index_out = args.index_out.expanduser().resolve()
    if args.retrieval_benchmark is None:
        args.retrieval_benchmark = args.root / ".cleanup-extracted" / "retrieval-benchmark.json"
    else:
        args.retrieval_benchmark = args.retrieval_benchmark.expanduser().resolve()
    return args


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        generic_args = parse_args(["--root", str(root), "--scope", "docs", "--pipeline", "review", "--plan-only"])
        assert generic_args.cleanup_tool == DEFAULT_MIXED_FOLDER_ADAPTER
        generic_plan = build_plan(generic_args)
        assert not generic_plan[0].blocked_reason
        sync_args = parse_args(["--root", str(root), "--pipeline", "maintain", "--plan-only"])
        sync_plan = build_plan(sync_args)
        assert sync_plan[0].blocked_reason.startswith("sync writes")
        sync_args = parse_args(["--root", str(root), "--pipeline", "maintain", "--execute-sync", "--plan-only"])
        sync_plan = build_plan(sync_args)
        assert sync_plan[0].command[-2:] == ["--sync", "--execute"]
        tool = root / "tools" / "cleanup_convert.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        args = parse_args(["--root", str(root), "--scope", "docs", "--pipeline", "review", "--plan-only"])
        plan = build_plan(args)
        assert [item.stage for item in plan] == ["inventory", "suggest", "workbench", "audit"]
        assert plan[0].command[-2:] == ["--scope", "docs"]
        auto_sync_args = parse_args(["--root", str(root), "--pipeline", "maintain", "--execute-sync", "--auto-keep", "--plan-only"])
        auto_sync_plan = build_plan(auto_sync_args)
        assert "--auto-keep" in auto_sync_plan[0].command
        assert not auto_sync_plan[1].blocked_reason
        args = parse_args(["--root", str(root), "--scope", "docs", "--stage", "apply", "--decisions", "docs/asset-decisions.json"])
        plan = build_plan(args)
        assert plan[0].blocked_reason.startswith("apply can move")
        args = parse_args(
            [
                "--root",
                str(root),
                "--scope",
                "docs",
                "--stage",
                "workbench",
                "--workbench-decisions",
                "review.json",
            ]
        )
        plan = build_plan(args)
        assert "--workbench-decisions" in plan[0].command
        args = parse_args(["--root", str(root), "--stage", "index", "--execute-index"])
        plan = build_plan(args)
        assert "missing reviewed decision ledger" in plan[0].blocked_reason
        args = parse_args(["--root", str(root), "--pipeline", "index", "--execute-index"])
        plan = build_plan(args)
        assert plan[0].stage == "audit"
        assert plan[0].allow_returncodes == (0,)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        run_self_test()
        print("asset_pipeline self-test passed / asset_pipeline 自检通过")
        return 0
    try:
        plan = build_plan(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.plan_only:
        print_plan(plan, args.json)
        return 0 if not any(item.blocked_reason for item in plan) else 2
    results = run_plan(args, plan)
    print_results(results, args.json)
    if any(item.status in {"blocked", "failed"} for item in results):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
