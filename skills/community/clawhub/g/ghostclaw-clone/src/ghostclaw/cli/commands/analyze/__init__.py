"""
Analyze command implementation.
"""

import sys
import json
import datetime
import pdb
from pathlib import Path
from typing import Dict, Any, Optional
from argparse import ArgumentParser, Namespace

from ghostclaw.cli.commander import Command
from ghostclaw.cli.services import AnalyzerService, PRService
from ghostclaw.cli.formatters import MarkdownFormatter, TerminalFormatter, JSONFormatter
from .utils import detect_github_remote, estimate_repo_file_count


class AnalyzeCommand(Command):
    """
    Command to analyze codebase architecture.
    """

    @property
    def name(self) -> str:
        return "analyze"

    @property
    def description(self) -> str:
        return "Analyze codebase architecture"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("repo_path", nargs="?", default=".", help="Path to the repository to analyze")
        parser.add_argument("--json", action="store_true", help="Output raw JSON")
        parser.add_argument("--no-write-report", action="store_true", help="Skip writing the .md report file")
        parser.add_argument("--create-pr", action="store_true", help="Automatically create a GitHub PR with the report")
        parser.add_argument("--pr-title", help="Custom PR title")
        parser.add_argument("--pr-body", help="Custom PR body")

        # Delta-Context Mode
        parser.add_argument("--delta", action="store_true", help="Enable delta-context analysis (PR-style review on diffs)")
        parser.add_argument("--base", dest="delta_base_ref", default=None, help="Git reference to diff against")
        parser.add_argument("--delta-summary", action="store_true", help="Print diff statistics")

        # QMD backend
        parser.add_argument("--use-qmd", action="store_true", help="Use QMD backend")
        parser.add_argument("--embedding-backend", choices=["sentence-transformers", "fastembed", "openai"], help="Embedding backend")

        # Caching options
        parser.add_argument("--no-cache", action="store_true", help="Disable result caching")
        parser.add_argument("--cache-dir", type=Path, help="Custom cache directory")
        parser.add_argument("--cache-ttl", type=int, default=7, help="Cache TTL in days")
        parser.add_argument("--cache-stats", action="store_true", help="Show cache statistics")

        # Parallel processing
        parser.add_argument("--no-parallel", action="store_true", help="Disable parallel file scanning")
        parser.add_argument("--concurrency-limit", type=int, help="Max concurrent operations")

        # AI options
        parser.add_argument("--use-ai", action="store_true", help="Enable AI synthesis")
        parser.add_argument("--no-ai", action="store_true", help="Explicitly disable AI synthesis")
        parser.add_argument("--ai-provider", help="AI Provider")
        parser.add_argument("--ai-model", help="Specific LLM model")
        parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
        parser.add_argument("--verbose", action="store_true", help="Verbose mode")
        parser.add_argument("--patch", action="store_true", help="Enable patch suggestions")

        # Engine Integrations
        parser.add_argument("--pyscn", action="store_true", help="Enable PySCN integration")
        parser.add_argument("--no-pyscn", action="store_true", help="Explicitly disable PySCN integration")
        parser.add_argument("--ai-codeindex", action="store_true", help="Enable AI-CodeIndex integration")
        parser.add_argument("--no-ai-codeindex", action="store_true", help="Explicitly disable AI-CodeIndex integration")

        # Orchestrator
        orchestrator_group = parser.add_mutually_exclusive_group()
        orchestrator_group.add_argument("--orchestrate", action="store_true", help="Enable orchestrator routing")
        orchestrator_group.add_argument("--no-orchestrate", action="store_true", help="Disable orchestrator routing")

        # Orchestrator options
        parser.add_argument("--orchestrate-llm", action="store_true", help="Enable LLM-based planning in orchestrator")
        parser.add_argument("--orchestrate-plan-only", action="store_true", help="Generate plan but do not execute plugins (debug/validation)")
        parser.add_argument("--orchestrate-max", type=int, help="Maximum number of plugins to run (overrides config)")
        parser.add_argument("--orchestrate-llm-model", type=str, help="LLM model to use for orchestrator planning (overrides config)")
        parser.add_argument("--orchestrate-concurrency", type=int, help="Concurrency limit for orchestrator plugin execution (overrides config)")

        # Orchestrator caching (mutually exclusive)
        orchestrate_cache_group = parser.add_mutually_exclusive_group()
        orchestrate_cache_group.add_argument("--orchestrate-cache", action="store_true", help="Enable plan caching in orchestrator")
        orchestrate_cache_group.add_argument("--no-orchestrate-cache", action="store_true", help="Disable plan caching in orchestrator")

        # Reliability
        parser.add_argument("--strict", action="store_true", help="Treat adapter errors as fatal")

        # Observability
        parser.add_argument("--benchmark", action="store_true", help="Print performance timings")
        parser.add_argument("--pdb", action="store_true", help="Drop into pdb on error")
        parser.add_argument("--show-tokens", action="store_true", help="Show token usage")

    def validate(self, args: Namespace) -> None:
        if not Path(args.repo_path).is_dir():
            print(f"Error: directory not found: {args.repo_path}", file=sys.stderr)
            sys.exit(1)

    async def execute(self, args: Namespace) -> int:
        self.validate(args)
        try:
            return await self._execute_impl(args)
        except Exception as e:
            if args.pdb:
                print("\n\x1b[31m⚠️  Debugger enabled. Entering pdb post-mortem session.\x1b[0m", file=sys.stderr)
                import traceback
                tb = sys.exc_info()[2]
                pdb.post_mortem(tb)
            else:
                print(str(e), file=sys.stderr)
            return 1

    async def _execute_impl(self, args: Namespace) -> int:
        cli_overrides = self._build_cli_overrides(args)
        self._handle_parallel_warning(args, cli_overrides)

        report, service = await self._run_analysis(args.repo_path, cli_overrides, args)

        if getattr(args, 'delta_summary', False): self._print_delta_summary(report)
        self._format_and_print_report(report, args)

        report_file_path = None
        if not args.no_write_report:
            report_file_path = await self._write_report(report, args)

        if args.create_pr:
            await self._handle_pr_creation(report, report_file_path, args.repo_path, args)

        self._print_auxiliary_info(report, service, args)
        if args.strict and report.get('errors'):
            print(f"\n\x1b[31m❌ Analysis failed due to {len(report['errors'])} adapter error(s) (--strict mode).\x1b[0m", file=sys.stderr)
            return 1
        return 0

    def _build_cli_overrides(self, args: Namespace) -> Dict[str, Any]:
        overrides: Dict[str, Any] = {}
        if args.use_ai: overrides['use_ai'] = True
        elif args.no_ai: overrides['use_ai'] = False
        if args.ai_provider: overrides['ai_provider'] = args.ai_provider
        if args.ai_model: overrides['ai_model'] = args.ai_model
        if args.dry_run: overrides['dry_run'] = True
        if args.verbose: overrides['verbose'] = True
        if args.patch: overrides['patch'] = True
        if args.delta: overrides['delta_mode'] = True
        if args.delta_base_ref is not None: overrides['delta_base_ref'] = args.delta_base_ref
        if args.use_qmd: overrides['use_qmd'] = True
        if getattr(args, 'embedding_backend', None): overrides['embedding_backend'] = args.embedding_backend
        if args.pyscn: overrides['use_pyscn'] = True
        elif args.no_pyscn: overrides['use_pyscn'] = False
        if args.ai_codeindex: overrides['use_ai_codeindex'] = True
        elif args.no_ai_codeindex: overrides['use_ai_codeindex'] = False

        # Orchestrator flags
        if args.orchestrate or args.no_orchestrate:
            overrides['orchestrate'] = args.orchestrate

        # Orchestrator options
        if args.orchestrate_llm:
            overrides['orchestrator'] = overrides.get('orchestrator', {})
            overrides['orchestrator']['use_llm'] = True
        if args.orchestrate_plan_only:
            overrides['orchestrator'] = overrides.get('orchestrator', {})
            overrides['orchestrator']['plan_only'] = True
        if args.orchestrate_max is not None:
            overrides['orchestrator'] = overrides.get('orchestrator', {})
            overrides['orchestrator']['max_plugins'] = args.orchestrate_max
        if args.orchestrate_llm_model:
            overrides['orchestrator'] = overrides.get('orchestrator', {})
            overrides['orchestrator']['llm_model'] = args.orchestrate_llm_model
        if args.orchestrate_concurrency is not None:
            overrides['orchestrator'] = overrides.get('orchestrator', {})
            overrides['orchestrator']['max_concurrent_plugins'] = args.orchestrate_concurrency
            overrides['orchestrator']['concurrency_limit'] = args.orchestrate_concurrency
        if args.orchestrate_cache:
            overrides['orchestrator'] = overrides.get('orchestrator', {})
            overrides['orchestrator']['enable_plan_cache'] = True
        if args.no_orchestrate_cache:
            overrides['orchestrator'] = overrides.get('orchestrator', {})
            overrides['orchestrator']['enable_plan_cache'] = False

        if args.no_parallel: overrides['parallel_enabled'] = False
        if args.concurrency_limit is not None: overrides['concurrency_limit'] = args.concurrency_limit
        return overrides

    def _handle_parallel_warning(self, args: Namespace, overrides: Dict[str, Any]) -> None:
        if not args.no_parallel: return
        LARGE_REPO_THRESHOLD = 5000
        file_count = estimate_repo_file_count(args.repo_path)
        if file_count > LARGE_REPO_THRESHOLD:
            overrides['parallel_enabled'] = True
            print(f"⚡ Auto-enabling parallel processing (~{file_count} files).", file=sys.stderr)
        else:
            print("⚠️  WARNING: --no-parallel is ~300× slower.", file=sys.stderr)

    async def _run_analysis(self, repo_path: str, cli_overrides: Dict[str, Any], args: Namespace):
        service = AnalyzerService(
            repo_path=repo_path,
            config_overrides=cli_overrides,
            use_cache=not args.no_cache,
            cache_dir=args.cache_dir,
            cache_ttl=args.cache_ttl,
            json_output=args.json,
            benchmark=args.benchmark
        )
        report = await service.run()
        return report, service

    def _print_delta_summary(self, report: Dict[str, Any]) -> None:
        delta = report.get("metadata", {}).get("delta", {})
        if not delta.get("mode"): return
        diff_text = delta.get("diff", "")
        if not diff_text: return
        files_changed = len(delta.get("files_changed", []))
        insertions = sum(1 for l in diff_text.splitlines() if l.startswith("+") and not l.startswith("+++"))
        deletions = sum(1 for l in diff_text.splitlines() if l.startswith("-") and not l.startswith("---"))
        print(f"\n=== Delta Summary ===\nFiles: {files_changed}, +{insertions}, -{deletions}", file=sys.stderr)

    def _format_and_print_report(self, report: Dict[str, Any], args: Namespace) -> None:
        if args.json: print(JSONFormatter().format(report))
        else: TerminalFormatter().print_to_terminal(report)

    async def _write_report(self, report: Dict[str, Any], args: Namespace) -> Optional[Path]:
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        repo_path = Path(args.repo_path)
        is_delta = report.get("metadata", {}).get("delta", {}).get("mode", False)
        filename = f"ARCHITECTURE-DELTA-{now}.md" if is_delta else f"ARCHITECTURE-REPORT-{now}.md"

        report_dir = repo_path if args.create_pr else (repo_path / ".ghostclaw" / "storage" / "reports")
        report_dir.mkdir(parents=True, exist_ok=True)

        if not args.create_pr:
            gitignore_path = repo_path / '.gitignore'
            if gitignore_path.exists():
                content = gitignore_path.read_text(encoding='utf-8')
                if '.ghostclaw' not in content and '.ghostclaw/' not in content:
                    newline = '\n' if not content.endswith('\n') else ''
                    with open(gitignore_path, 'a', encoding='utf-8') as f:
                        f.write(f'{newline}# Added by Ghostclaw\n.ghostclaw/\n')

        report_file_path = report_dir / filename
        try:
            report_file_path.write_text(MarkdownFormatter().format(report), encoding='utf-8')
            print(f"📝 Report written to: {report_file_path.absolute()}", file=sys.stderr)
            report_file_path.with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            return report_file_path
        except Exception as e:
            print(f"Error writing report: {e}", file=sys.stderr)
            return None

    async def _handle_pr_creation(self, report: Dict[str, Any], report_path: Optional[Path], repo_path: str, args: Namespace) -> None:
        if not report_path: return
        title = args.pr_title or f"🏰 Architecture Report - {datetime.datetime.now().strftime('%Y-%m-%d')}"
        body = args.pr_body or f"Ghostclaw review. Vibe Score: {report['vibe_score']}/100"
        pr_service = PRService(repo_path)
        try:
            await pr_service.create_pr(report_path, title, body)
        except Exception: pass
        finally:
            try:
                report_path.unlink(missing_ok=True)
                report_path.with_suffix('.json').unlink(missing_ok=True)
            except: pass

    def _print_auxiliary_info(self, report: Dict[str, Any], service, args: Namespace) -> None:
        info_file = sys.stderr if args.json else sys.stdout
        if args.benchmark and getattr(service, 'timings', None):
            print("\n=== Benchmark Results ===", file=sys.stderr)
            for p, d in sorted(service.timings.items()): print(f"{p:20} {d:>8.3f}s", file=sys.stderr)
        if getattr(args, 'show_tokens', False):
            tokens = report.get('metadata', {}).get('tokens', {})
            print(f"\n=== Token Usage ===\nTotal: {tokens.get('total', 0)}", file=sys.stderr)
        if getattr(args, 'cache_stats', False) and getattr(service, 'cache', None):
            stats = service.cache.info()
            print(f"\n=== Cache Statistics ===\nCache: {stats.get('cache_dir')}\nentries: {stats.get('entries')}", file=info_file)
        remote_url = detect_github_remote(args.repo_path)
        if remote_url and not args.create_pr:
            print(f"💡 Tip: Use --create-pr to upload findings.", file=info_file)
