"""
Debug command implementation.
"""

import sys
import asyncio
from pathlib import Path
from argparse import ArgumentParser, Namespace

from ghostclaw.cli.commander import Command
from ghostclaw.cli.services import AnalyzerService
from .console import GhostclawDebugConsole


class DebugCommand(Command):
    """
    Interactive debugger for ghostclaw analysis.
    """

    @property
    def name(self) -> str:
        return "debug"

    @property
    def description(self) -> str:
        return "Interactive debugger for analysis (development only)"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("repo_path", nargs="?", default=".", help="Path to repository")
        parser.add_argument(
            "--break-at",
            choices=['start', 'config', 'files', 'metrics', 'adapters', 'stack', 'pre-synth', 'post-synth', 'end'],
            default='pre-synth',
            help="Phase to break at (default: pre-synth)"
        )
        parser.add_argument(
            "--readonly",
            action="store_true",
            help="Prevent mutation of any state (safe for exploration)"
        )
        parser.add_argument(
            "--no-cache",
            action="store_true",
            help="Disable caching for fresh analysis"
        )
        parser.add_argument(
            "--concurrency-limit",
            type=int,
            help="Override concurrency limit"
        )

    def validate(self, args: Namespace) -> None:
        if not Path(args.repo_path).is_dir():
            print(f"Error: directory not found: {args.repo_path}", file=sys.stderr)
            sys.exit(1)

        import os
        debug_enabled = os.environ.get('GHOSTCLAW_DEBUG', '').lower() in ('1', 'true', 'yes')
        try:
            import json
            global_cfg_path = Path.home() / ".ghostclaw" / "ghostclaw.json"
            if global_cfg_path.exists():
                with open(global_cfg_path) as f:
                    data = json.load(f)
                    if data.get('debug_enabled'):
                        debug_enabled = True
        except:
            pass

        if not debug_enabled:
            print(
                "\x1b[31m❌ Debug mode is disabled.\x1b[0m\n"
                "   Set GHOSTCLAW_DEBUG=1 environment variable, or add\n"
                "   'debug_enabled': true to ~/.ghostclaw/ghostclaw.json\n"
                "   Debug mode is for development only and exposes internal state.\n",
                file=sys.stderr
            )
            sys.exit(1)

    async def execute(self, args: Namespace) -> int:
        """Run the interactive debugger."""
        self.validate(args)

        print("\x1b[36m[Debug] Starting analysis with breakpoint at: \x1b[33m" + args.break_at + "\x1b[0m")
        print("\x1b[90mPress Ctrl+C to abort at any time.\x1b[0m\n")

        cli_overrides = {}
        if args.no_cache:
            cli_overrides['use_cache'] = False
        if args.concurrency_limit is not None:
            cli_overrides['concurrency_limit'] = args.concurrency_limit

        service = AnalyzerService(
            repo_path=args.repo_path,
            config_overrides=cli_overrides,
            use_cache=not args.no_cache,
            benchmark=False,
            json_output=True
        )

        debug_ctx = {
            'service': service,
            'repo_path': args.repo_path,
            'breakpoints': set([args.break_at]),
            'readonly': args.readonly,
            'config': None,
            'files': [],
            'metrics': {},
            'adapter_results': [],
            'stack_result': {},
            'issues': [],
            'ghosts': [],
            'coupling_metrics': {},
            'import_edges': [],
        }

        original_run = service.run

        async def instrumented_run():
            try:
                report = await original_run()
                debug_ctx['report'] = report
                debug_ctx['vibe_score'] = report.get('vibe_score')
                debug_ctx['issues'] = report.get('issues', [])
                debug_ctx['ghosts'] = report.get('architectural_ghosts', [])
                debug_ctx['coupling_metrics'] = report.get('coupling_metrics', {})
                debug_ctx['import_edges'] = []
                debug_ctx['final'] = True
                return report
            except Exception as e:
                debug_ctx['error'] = e
                raise

        service.run = instrumented_run

        try:
            loop = asyncio.get_event_loop()
            report = loop.run_until_complete(service.run())
        except Exception as e:
            print(f"\x1b[31mError during analysis: {e}\x1b[0m")
            debug_ctx['error'] = e
            print("\nEntering REPL to inspect partial state...")
            debug_ctx['final'] = False

        console = GhostclawDebugConsole(debug_ctx)
        try:
            console.cmdloop()
        except KeyboardInterrupt:
            print("\n\n\x1b[33mDebug session ended.\x1b[0m")
            return 1 if debug_ctx.get('error') else 0

        if debug_ctx.get('error'):
            return 1
        return 0
