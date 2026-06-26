"""CLI command: ghostclaw qmd migrate — Manage QMD embedding migration."""

import argparse
import asyncio
from pathlib import Path

from ghostclaw.core.qmd_store import QMDMemoryStore
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.cli.commander import Command


class QMDMigrateCommand(Command):
    """Manage QMD legacy data migration (embedding backfill)."""

    @property
    def name(self) -> str:
        return "qmd-migrate"

    @property
    def description(self) -> str:
        return "Show migration status and manage background embedding backfill for QMD"

    def configure_parser(self, parser: argparse.ArgumentParser):
        # Store parser for later use in execute (e.g., print_help)
        self.parser = parser

        subparsers = parser.add_subparsers(dest="subcommand", help="Migration actions")

        # status
        status_parser = subparsers.add_parser("status", help="Show migration progress")

        # stop
        stop_parser = subparsers.add_parser("stop", help="Stop running migration")

        # trigger (manual)
        trigger_parser = subparsers.add_parser("trigger", help="Manually trigger migration")
        trigger_parser.add_argument(
            "--batch-size",
            type=int,
            default=None,
            help="Override batch size for this run"
        )

        parser.add_argument(
            "--repo",
            type=Path,
            default=Path.cwd(),
            help="Repository path (default: current directory)",
        )

    async def execute(self, args) -> int:
        repo_path = args.repo or Path.cwd()
        subcmd = getattr(args, 'subcommand', 'status')

        try:
            cfg = GhostclawConfig.load(repo_path)
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            return 1

        if not getattr(cfg, 'use_qmd', False):
            print("⚠️  QMD is not enabled (use_qmd=false)")
            return 1

        db_path = repo_path / ".ghostclaw" / "storage" / "qmd" / "ghostclaw.db"
        if not db_path.exists():
            print(f"⚠️  QMD database not found at {db_path}")
            print("Run an analysis first: ghostclaw analyze . --use-qmd")
            return 1

        # Initialize store with config (but don't start auto migration if we're just checking status)
        # Temporarily disable auto_migrate to avoid double-start if just checking status
        original_auto_migrate = getattr(cfg, 'auto_migrate', True)
        if subcmd == 'status':
            # Pass auto_migrate=False to prevent auto-start when we just want status
            store = QMDMemoryStore(
                db_path=db_path,
                use_enhanced=True,
                embedding_backend=getattr(cfg, 'embedding_backend', 'fastembed'),
                ai_buff_enabled=getattr(cfg, 'ai_buff_enabled', False),
                prefetch_enabled=getattr(cfg, 'prefetch_enabled', True),
                prefetch_window=getattr(cfg, 'prefetch_window', 2),
                prefetch_hours=getattr(cfg, 'prefetch_hours', 24),
                prefetch_vibe_delta=getattr(cfg, 'prefetch_vibe_delta', 10),
                prefetch_stack_count=getattr(cfg, 'prefetch_stack_count', 5),
                auto_migrate=False,  # don't auto-start when checking status
            )
        else:
            store = QMDMemoryStore(
                db_path=db_path,
                use_enhanced=True,
                embedding_backend=getattr(cfg, 'embedding_backend', 'fastembed'),
                ai_buff_enabled=getattr(cfg, 'ai_buff_enabled', False),
                prefetch_enabled=getattr(cfg, 'prefetch_enabled', True),
                prefetch_window=getattr(cfg, 'prefetch_window', 2),
                prefetch_hours=getattr(cfg, 'prefetch_hours', 24),
                prefetch_vibe_delta=getattr(cfg, 'prefetch_vibe_delta', 10),
                prefetch_stack_count=getattr(cfg, 'prefetch_stack_count', 5),
                auto_migrate=original_auto_migrate,
            )

        # Handle subcommands
        if subcmd == 'status':
            stats = store.get_stats()
            mig_stats = stats.get('migration')
            if not mig_stats:
                print("✅ Migration not enabled or not required")
                return 0

            print("=== QMD Migration Status ===")
            print(f"Enabled: {mig_stats.get('enabled', 'unknown')}")
            print(f"Running: {mig_stats.get('running', False)}")
            print(f"Triggered: {mig_stats.get('triggered', 0)}")
            print(f"Completed: {mig_stats.get('completed', 0)}")
            print(f"Errors: {mig_stats.get('errors', 0)}")
            if mig_stats.get('last_error'):
                print(f"Last error: {mig_stats['last_error']}")
            if mig_stats.get('started_at'):
                print(f"Started: {mig_stats['started_at']}")
            if mig_stats.get('completed_at'):
                print(f"Completed: {mig_stats['completed_at']}")
            return 0

        elif subcmd == 'stop':
            if store.backfill_manager:
                store.backfill_manager.stop()
                print("🛑 Migration stop requested")
                return 0
            else:
                print("⚠️  No migration running")
                return 1

        elif subcmd == 'trigger':
            if not store.backfill_manager:
                print("⚠️  Migration manager not available (auto_migrate disabled?)")
                return 1
            # Manual trigger: start background if not running
            if store.backfill_manager._running:
                print("⚠️  Migration already running")
                return 0
            task = await store.backfill_manager.start_background()
            if task:
                print("🚀 Migration triggered manually")
                return 0
            else:
                print("✅ No migration needed")
                return 0

        else:
            self.parser.print_help()
            return 1
