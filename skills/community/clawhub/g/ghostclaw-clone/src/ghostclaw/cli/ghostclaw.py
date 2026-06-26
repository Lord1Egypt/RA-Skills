#!/usr/bin/env python3
"""
Ghostclaw CLI — command-line interface for the architectural analyzer.
"""

import sys
import os
import json
import argparse
import subprocess
import logging
import datetime
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv
from ghostclaw.core.analyzer import CodebaseAnalyzer
from ghostclaw.core.cache import LocalCache
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.llm_client import LLMClient
from ghostclaw.core.agent import GhostAgent, AgentEvent
from ghostclaw.cli import __version__
import asyncio

from ghostclaw.cli.commander import registry

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.status import Status
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

load_dotenv()

def setup_logging(verbose: bool = False):
    """Configure global logging for the CLI."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    level = logging.DEBUG if verbose else logging.INFO
    
    handlers = [logging.StreamHandler(sys.stderr)]
    if verbose:
        handlers.append(logging.FileHandler("ghostclaw.log"))

    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )

def generate_markdown_report(report: Dict) -> str:
    from ghostclaw.cli.formatters import MarkdownFormatter
    return MarkdownFormatter().format(report)

def detect_github_remote(repo_path: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            if "github.com" in url:
                return url
    except Exception:
        pass
    return None

def create_github_pr(repo_path: str, report_file: Path, title: str, body: str):
    from ghostclaw.cli.services import PRService
    import asyncio
    asyncio.run(PRService(repo_path).create_pr(report_file, title, body))

def print_report(report: Dict):
    from ghostclaw.cli.formatters import TerminalFormatter
    TerminalFormatter().print_to_terminal(report)

def update_ghostclaw():
    from ghostclaw.cli.commands.update import UpdateCommand
    import asyncio
    asyncio.run(UpdateCommand().execute(argparse.Namespace()))

def legacy_main(args: argparse.Namespace) -> int:
    """Fallback legacy code for commands not yet migrated."""
    if args.command == "update":
        update_ghostclaw()
        return 0

    if args.command == "plugins":
        import shutil
        from ghostclaw.core.adapters.registry import registry as plugin_registry
        plugin_registry.register_internal_plugins()

        local_plugins = Path.cwd() / ".ghostclaw" / "plugins"
        if local_plugins.exists():
            plugin_registry.load_external_plugins(local_plugins)

        if args.plugin_command == "list":
            metadata = plugin_registry.get_plugin_metadata()
            if not metadata:
                print("No plugins found.")
            else:
                if HAS_RICH:
                    from rich.table import Table
                    table = Table(title="Ghostclaw Plugins")
                    table.add_column("Name", style="cyan")
                    table.add_column("Version", style="magenta")
                    table.add_column("Description")
                    table.add_column("Type", style="green")
                    for meta in metadata:
                        name = meta.get("name", "unknown")
                        p_type = "Built-in" if name in plugin_registry.internal_plugins else "External"
                        table.add_row(name, meta.get("version", "unknown"), meta.get("description", ""), p_type)
                    Console().print(table)
                else:
                    print("Name | Version | Description | Type")
                    for meta in metadata:
                        name = meta.get("name")
                        p_type = "Built-in" if name in plugin_registry.internal_plugins else "External"
                        print(f"{name} | {meta.get('version')} | {meta.get('description')} | {p_type}")
            return 0
        else:
            print(f"Warning: Plugin subcommand {args.plugin_command} not available in legacy mode. Please check command installation.", file=sys.stderr)
            return 1

    if args.command == "bridge":
        from ghostclaw.core.bridge import GhostBridge
        async def _run_bridge():
            bridge = GhostBridge()
            await bridge.run()
        try:
            asyncio.run(_run_bridge())
        except KeyboardInterrupt:
            pass
        return 0

    if args.command == "doctor":
        async def _run_doctor():
            print("🏥 Ghostclaw Doctor\n")
            print("1. Directory Structure")
            gc_dir = Path.cwd() / ".ghostclaw"
            if gc_dir.exists():
                print(f"  ✅ .ghostclaw/ exists at {gc_dir}")
                if (gc_dir / "cache").exists(): print(f"  ✅ Cache dir exists")
                else: print(f"  ⚠️ Cache dir missing (will be created automatically)")
                if (gc_dir / "plugins").exists(): print(f"  ✅ Plugins dir exists")
                else: print(f"  ⚠️ Plugins dir missing (will be created automatically)")
            else:
                print(f"  ⚠️ .ghostclaw/ directory missing in current path. Run 'ghostclaw init' to scaffold.")
            print("\n2. Environment & Plugins")
            from ghostclaw.core.adapters.registry import registry as plugin_registry
            plugin_registry.register_internal_plugins()
            if gc_dir.exists() and (gc_dir / "plugins").exists():
                plugin_registry.load_external_plugins(gc_dir / "plugins")
            validation_results = await plugin_registry.validate_all()
            for name, is_valid in validation_results.items():
                status = "✅ available" if is_valid else "❌ unavailable"
                print(f"  • {name}: {status}")
            print("\n3. AI Provider Connectivity")
            cli_overrides = {}
            if getattr(args, 'ai_provider', None): cli_overrides['ai_provider'] = args.ai_provider
            if getattr(args, 'ai_model', None): cli_overrides['ai_model'] = args.ai_model
            config = GhostclawConfig.load(".", **cli_overrides)
            client = LLMClient(config, ".")
            print(f"  Testing connection to {config.ai_provider}...")
            if not config.api_key:
                print("  ❌ API Key not found. Set GHOSTCLAW_API_KEY environment variable.")
            else:
                success = await client.test_connection()
                if success:
                    print(f"  ✅ Connection successful! Model: {client.model}")
                else:
                    print("  ❌ Connection failed. Check provider configuration or network.")
        asyncio.run(_run_doctor())
        return 0

    if args.command == "init":
        from ghostclaw.cli.services import ConfigService
        ConfigService.init_project()
        return 0

    if args.command == "test":
        if args.llm:
            async def _run_test():
                cli_overrides = {}
                if args.ai_provider: cli_overrides['ai_provider'] = args.ai_provider
                if args.ai_model: cli_overrides['ai_model'] = args.ai_model
                config = GhostclawConfig.load(".", **cli_overrides)
                client = LLMClient(config, ".")
                print(f"🔍 Testing LLM Connection ({config.ai_provider})...")
                success = await client.test_connection()
                if success:
                    print("✅ Connection successful!")
                    models = await client.list_models()
                    for m in models: print(f"  • {m}")
                else:
                    print("❌ Connection failed. Check your API key and provider settings.")
            asyncio.run(_run_test())
        return 0

    if args.command == "analyze":
        # Call the new service code via AnalyzeCommand just for legacy stub
        from ghostclaw.cli.commands.analyze import AnalyzeCommand
        return asyncio.run(AnalyzeCommand().execute(args))

    return 1

def main():
    parser = argparse.ArgumentParser(description="Ghostclaw CLI — Architectural Analyzer")
    parser.add_argument("--version", action="version", version=f"Ghostclaw {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Auto-discover commands
    registry.auto_discover()

    # Track the plugins parser specially to add subcommands
    plugins_parser = None
    plugins_subparsers = None

    # Store command instances created during configuration
    cmd_instances = {}
    top_level_commands = set()

    # Build parser from registry
    for cmd_cls in registry.all():
        cmd = cmd_cls()
        cmd_instances[cmd.name] = cmd

        # Track top-level command name (e.g., "plugins" from "plugins list")
        top_level = cmd.name.split(" ")[0]
        top_level_commands.add(top_level)

        # Handle "plugins xxx" subcommands specially
        if cmd.name.startswith("plugins "):
            if not plugins_parser:
                plugins_parser = subparsers.add_parser("plugins", help="Manage architectural adapters/plugins")
                plugins_subparsers = plugins_parser.add_subparsers(dest="plugin_command", help="Plugin sub-commands")

            subcommand_name = cmd.name.split(" ", 1)[1]
            subparser = plugins_subparsers.add_parser(subcommand_name, help=cmd.description)
            cmd.configure_parser(subparser)
        else:
            subparser = subparsers.add_parser(cmd.name, help=cmd.description)
            cmd.configure_parser(subparser)

    # Pre-parse handling: directory shortcut and unknown command fallback
    if len(sys.argv) > 1:
        raw = sys.argv[1]
        # Only apply shortcut/fallback for non-option arguments (skip flags like --help)
        if not raw.startswith('-') and raw not in top_level_commands:
            if os.path.isdir(raw):
                sys.argv.insert(1, "analyze")
            else:
                print("Warning: Using legacy CLI mode...", file=sys.stderr)
                legacy_ns = argparse.Namespace(command=raw)
                exit_code = legacy_main(legacy_ns)
                sys.exit(exit_code)
                return exit_code

    args = parser.parse_args()

    # Setup global logging
    setup_logging(verbose=getattr(args, "verbose", False))

    if not args.command:
        parser.print_help()
        return 1

    # Determine command name
    cmd_name = args.command
    if cmd_name == "plugins" and getattr(args, "plugin_command", None):
        cmd_name = f"plugins {args.plugin_command}"

    # Try modular command first, using the instances created during parser setup
    cmd = cmd_instances.get(cmd_name)
    if not cmd:
        cmd_cls = registry.get(cmd_name)
        if cmd_cls:
            cmd = cmd_cls()

    if cmd:
        exit_code = asyncio.run(cmd.execute(args))
        return exit_code

    # LEGACY: Fall back to monolithic code
    print("Warning: Using legacy CLI mode...", file=sys.stderr)
    exit_code = legacy_main(args)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
