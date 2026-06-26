"""
CodebaseAnalyzer facade — orchestrates stack detection, metrics, and stack-specific analysis.
"""

import datetime
import asyncio
import json
import logging
from pathlib import Path
from typing import Optional

from ghostclaw.core.detector import find_files, find_files_parallel
from ghostclaw.core.validator import RuleValidator
from ghostclaw.core.cache import LocalCache, compute_fingerprint
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.models import ArchitectureReport
from ghostclaw.core import git_utils

from .metrics import MetricCollector
from .stacks import StackAnalyzer
from .scoring import VibeScorer
from .discovery import get_index
from .run import FingerprintedRun

logger = logging.getLogger("ghostclaw.analyzer")


class CodebaseAnalyzer:
    """Main analyzer class that coordinates the full analysis pipeline."""

    def __init__(self, validator: RuleValidator = None, cache: LocalCache = None):
        self.validator = validator or RuleValidator()
        self.cache = cache
        self.progress_cb = None

    @staticmethod
    def _find_base_report(repo_path: Path, base_ref: str = "HEAD~1") -> Optional[dict]:
        """Legacy synchronous base report discovery (DEPRECATED)."""
        reports_dir = repo_path / ".ghostclaw" / "storage" / "reports"
        if not reports_dir.exists():
            return None

        try:
            import subprocess

            result = subprocess.run(
                ["git", "-C", str(repo_path), "rev-parse", base_ref],
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
            base_sha = result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            base_sha = None

        json_files = list(reports_dir.glob("*.json"))
        if not json_files:
            return None

        if base_sha:
            for path in json_files:
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    if (
                        data.get("metadata", {}).get("vcs", {}).get("commit")
                        == base_sha
                    ):
                        return data
                except Exception:
                    continue

        latest = max(json_files, key=lambda p: p.stat().st_mtime)
        try:
            return json.loads(latest.read_text(encoding="utf-8"))
        except Exception:
            return None

    async def _find_base_report_async(self, repo_path: Path, base_ref: str = "HEAD~1") -> Optional[dict]:
        """Find the base report for delta context using indexed discovery."""
        try:
            # 1. Resolve base_ref to SHA
            executor = git_utils.AsyncGitExecutor(repo_path)
            returncode, stdout, _ = await executor.run_git(["rev-parse", base_ref])
            if returncode != 0:
                return None
            base_sha = stdout.strip()

            # 2. Use indexed discovery
            index = await get_index(repo_path)
            return await index.find_by_commit(base_sha)
        except Exception as e:
            logger.warning("Failed to find base report for %s: %s", base_ref, e)
            return None

    async def analyze(
        self,
        root: str,
        use_cache: bool = True,
        config: Optional[GhostclawConfig] = None,
    ) -> ArchitectureReport:
        """Perform a complete architectural analysis of a codebase."""
        root_path = Path(root)
        config = config or GhostclawConfig()

        delta_mode = getattr(config, "delta_mode", False)
        delta_base_ref = getattr(config, "delta_base_ref", None) or "HEAD~1"

        fingerprint = None
        if use_cache and self.cache is not None:
            # Use async version of get_current_sha to avoid blocking
            current_sha = await git_utils.get_current_sha_async(root_path)
            base_fingerprint = compute_fingerprint(root_path, git_sha=current_sha)
            delta_suffix = (
                f":delta={delta_mode}:base={delta_base_ref}" if delta_mode else ""
            )
            config_suffix = f":ai={config.use_ai}:pyscn={config.use_pyscn}:codeindex={config.use_ai_codeindex}{delta_suffix}"

            # Include orchestrator/routing settings in fingerprint
            # Determine effective orchestrator enabled state
            orch_enabled = False
            if getattr(config, 'orchestrate', None) is not None:
                orch_enabled = config.orchestrate
            elif getattr(config, 'orchestrator', None) is not None:
                orch_enabled = config.orchestrator.enabled
            config_suffix += f":orch_enabled={orch_enabled}"

            if orch_enabled:
                orch_cfg = config.orchestrator
                # Include key orchestrator parameters that affect plugin selection/planning
                config_suffix += f":orch_llm={orch_cfg.use_llm}"
                config_suffix += f":orch_max_plugins={orch_cfg.max_plugins}"
                config_suffix += f":orch_vec_w={orch_cfg.vector_weight}"
                config_suffix += f":orch_heur_w={orch_cfg.heuristics_weight}"
                config_suffix += f":orch_hist={orch_cfg.plugin_history_lookback}"
                config_suffix += f":orch_cache={orch_cfg.enable_plan_cache}"

            # Include plugin filter (if any)
            if getattr(config, 'plugins_enabled', None):
                sorted_plugins = sorted(config.plugins_enabled)
                config_suffix += f":plugins={','.join(sorted_plugins)}"

            fingerprint = base_fingerprint + config_suffix

            cached_data = await asyncio.to_thread(self.cache.get, fingerprint)
            if cached_data is not None:
                cached_data.setdefault("metadata", {})["cache_hit"] = True
                return ArchitectureReport(**cached_data)

        # 1. Detect stack
        stack = await StackAnalyzer.detect(root)
        analyzer_instance = StackAnalyzer.get_analyzer_instance(stack)
        extensions = analyzer_instance.get_extensions() if analyzer_instance else []

        # 2. Find relevant files
        if self.progress_cb:
            self.progress_cb("Scanning files")
        diff_result = None
        changed_rel_paths = []

        if delta_mode:
            # v0.2.0-alpha: Use DiffCache
            from ghostclaw.core.diff_cache import diff_cache

            current_sha = await git_utils.get_current_sha_async(root_path)
            cached_diff = diff_cache.get(str(root_path), delta_base_ref, current_sha)
            if cached_diff:
                diff_result = cached_diff
            else:
                diff_result = await git_utils.get_git_diff_async(
                    delta_base_ref, root_path
                )
                # Cache it!
                diff_cache.set(str(root_path), delta_base_ref, current_sha, diff_result)

            changed_rel_paths = diff_result.files_changed
            files = [
                str(root_path / r)
                for r in changed_rel_paths
                if (root_path / r).exists()
                and (not extensions or (root_path / r).suffix in extensions)
            ]
        else:
            if extensions:
                if config.parallel_enabled:
                    files = await find_files_parallel(
                        root, extensions, config.concurrency_limit
                    )
                else:
                    files = await asyncio.to_thread(find_files, root, extensions)
            else:
                files = []

        # 3. Compute base metrics
        threshold = (
            analyzer_instance.get_large_file_threshold() if analyzer_instance else 300
        )
        total_lines, line_counts, large_files = await asyncio.to_thread(
            MetricCollector.collect_metrics, files, threshold
        )

        total_files = len(files)
        avg_lines = sum(line_counts) / total_files if total_files > 0 else 0
        base_metrics = {
            "total_files": total_files,
            "total_lines": total_lines,
            "large_file_count": len(large_files),
            "average_lines": avg_lines,
            "vibe_score": 100,
        }

        # 4. Standardized Tool Ingestion via Adapters
        from ghostclaw.core.adapters.registry import PluginRegistry

        # Create a fresh registry for this analysis to avoid global state mutations and races
        registry = PluginRegistry()
        self.registry = registry  # expose for later use (e.g., save_report)
        registry.register_internal_plugins()
        if (root_path / ".ghostclaw" / "plugins").exists():
            registry.load_external_plugins(root_path / ".ghostclaw" / "plugins")

        # Compute enabled_plugins as a local variable (do not mutate global state)
        enabled_plugins: Optional[Set[str]] = None
        if config.orchestrator.enabled:
            enabled_plugins = {"orchestrator"}
        elif config.plugins_enabled is not None:
            enabled_plugins = set(config.plugins_enabled)
        elif config.use_qmd:
            enabled_plugins = None  # All plugins enabled including qmd
        else:
            from ghostclaw.core.adapters.registry import INTERNAL_PLUGINS

            enabled_plugins = (
                set(INTERNAL_PLUGINS) | set(registry.external_plugins)
            ) - {"qmd"}

        if config.use_qmd and enabled_plugins is not None:
            enabled_plugins.add("sqlite")
            enabled_plugins.add("qmd")

        # Pass filter to registry via instance attribute (safe: this registry is local to this analysis)
        registry.enabled_plugins = enabled_plugins

        if self.progress_cb:
            self.progress_cb("Running adapters")
        adapter_results = await registry.run_analysis(root, files, config)
        errors = list(getattr(registry, "errors", []))

        issues, ghosts, flags, coupling_metrics, symbol_index = [], [], [], {}, ""
        for res in adapter_results:
            issues.extend(res.get("issues", []))
            ghosts.extend(res.get("architectural_ghosts", []))
            flags.extend(res.get("red_flags", []))
            coupling_metrics.update(res.get("coupling_metrics", {}))
            if "symbol_index" in res:
                symbol_index += res["symbol_index"] + "\n"

        # 5. Legacy Stack-specific analysis and Rule validation
        stack_result = await StackAnalyzer.analyze_stack(
            stack, root, files, base_metrics
        )
        issues.extend(stack_result.get("issues", []))
        ghosts.extend(stack_result.get("architectural_ghosts", []))
        flags.extend(stack_result.get("red_flags", []))
        coupling_metrics.update(stack_result.get("coupling_metrics", {}))
        import_edges = stack_result.get("import_edges", [])

        try:
            report_with_rules = await asyncio.to_thread(
                self.validator.validate,
                stack,
                {
                    "issues": issues,
                    "architectural_ghosts": ghosts,
                    "red_flags": flags,
                    "coupling_metrics": coupling_metrics,
                    "import_edges": import_edges,
                    "files": files,
                    "files_analyzed": total_files,
                    "total_lines": total_lines,
                    "stack": stack,
                    **base_metrics,
                },
            )
            issues, ghosts, flags = (
                report_with_rules["issues"],
                report_with_rules["architectural_ghosts"],
                report_with_rules["red_flags"],
            )
        except Exception as e:
            issues.append(f"Rule validation failed: {str(e)}")

        # 6. Final vibe score
        context_data = {
            "metrics": base_metrics,
            "issues": issues,
            "ghosts": ghosts,
            "flags": flags,
            "stack": stack,
            "files": files,
            "coupling_metrics": coupling_metrics,
        }
        multi_score = await VibeScorer.compute_score(context_data, registry=registry)
        vibe_score = multi_score.overall

        # 7. Metadata and AI Prompt
        try:
            from ghostclaw.cli import __version__
        except ImportError:
            __version__ = "unknown"

        # Initialize base metadata
        metadata = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
            .replace(tzinfo=None)
            .isoformat()
            + "Z",
            "analyzer": "ghostclaw-async",
            "version": __version__,
            "adapters_active": [m["name"] for m in registry.get_plugin_metadata()],
            "pyscn_integrated": registry.pm.get_plugin("pyscn") is not None,
            "ai_codeindex_integrated": registry.pm.get_plugin("ai-codeindex") is not None,
        }

        # Add VCS info
        try:
            metadata["vcs"] = {
                "commit": git_utils.get_current_sha(root_path),
                "branch": git_utils.get_current_branch(root_path),
                "dirty": git_utils.has_uncommitted_changes(root_path),
            }
        except Exception:
            pass

        # Add delta info
        if delta_mode:
            metadata["delta"] = {
                "mode": True,
                "base_ref": delta_base_ref,
                "diff": diff_result.raw_diff if diff_result else "",
                "files_changed": changed_rel_paths,
            }

        report_data = {
            "repo_path": str(root_path),
            "vibe_score": vibe_score,
            "vibe_detailed": multi_score.to_dict(),
            "stack": stack,
            "files_analyzed": total_files,
            "total_lines": total_lines,
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": flags,
            "coupling_metrics": coupling_metrics,
            "errors": errors,
            "metadata": metadata,
        }
        # (Removed redundant blocks as they are integrated above)

        if config.use_ai:
            from ghostclaw.core.context_builder import ContextBuilder

            context_builder = ContextBuilder()
            if delta_mode:
                base_report = await self._find_base_report_async(root_path, base_ref=delta_base_ref)
                report_data["ai_prompt"] = context_builder.build_delta_prompt(
                    base_metrics,
                    issues,
                    ghosts,
                    flags,
                    diff_result.raw_diff if diff_result else "",
                    base_report,
                )
            else:
                report_data["ai_prompt"] = context_builder.build_prompt(
                    base_metrics,
                    issues,
                    ghosts,
                    flags,
                    coupling_metrics,
                    import_edges,
                    config.patch,
                    symbol_index,
                )

        if fingerprint and use_cache and self.cache:
            # Create a fingerprinted run for fast comparison in storage layer
            fp_run = FingerprintedRun.from_report(report_data)
            
            # Use explicit dict to satisfy type checkers
            meta_dict = report_data.get("metadata", {})
            if isinstance(meta_dict, dict):
                meta_dict["hashes"] = {
                    "issue_hash": fp_run.issue_hash,
                    "ghost_hash": fp_run.ghost_hash,
                    "flag_hash": fp_run.flag_hash,
                    "metrics_hash": fp_run.metrics_hash,
                }
            await asyncio.to_thread(self.cache.set, fingerprint, report_data)

        return ArchitectureReport(**report_data)
