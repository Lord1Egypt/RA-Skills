from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.llm_client import LLMClient
import sys
from pathlib import Path

class DoctorCommand(Command):
    @property
    def name(self) -> str:
        return "doctor"

    @property
    def description(self) -> str:
        return "Run diagnostic checks on environment and plugins"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--ai-provider", help="Provider to test (overrides config)")
        parser.add_argument("--ai-model", help="Model to test (overrides config)")

    async def execute(self, args: Namespace) -> int:
        print("🏥 Ghostclaw Doctor\n")

        # 1. Check Directories
        print("1. Directory Structure")
        gc_dir = Path.cwd() / ".ghostclaw"
        if gc_dir.exists():
            print(f"  ✅ .ghostclaw/ exists at {gc_dir}")
            cache_dir = gc_dir / "cache"
            plugins_dir = gc_dir / "plugins"
            if cache_dir.exists(): print(f"  ✅ Cache dir exists")
            else: print(f"  ⚠️ Cache dir missing (will be created automatically)")
            if plugins_dir.exists(): print(f"  ✅ Plugins dir exists")
            else: print(f"  ⚠️ Plugins dir missing (will be created automatically)")
        else:
            print(f"  ⚠️ .ghostclaw/ directory missing in current path. Run 'ghostclaw init' to scaffold.")
        print()

        # 2. Check Dependencies/Plugins
        print("2. Environment & Plugins")
        from ghostclaw.core.adapters.registry import registry
        registry.register_internal_plugins()
        if gc_dir.exists() and (gc_dir / "plugins").exists():
            registry.load_external_plugins(gc_dir / "plugins")

        validation_results = await registry.validate_all()
        for name, is_valid in validation_results.items():
            status = "✅ available" if is_valid else "❌ unavailable"
            print(f"  • {name}: {status}")
        print()

        # 3. Check LLM Connectivity
        print("3. AI Provider Connectivity")
        cli_overrides = {}
        if args.ai_provider: cli_overrides['ai_provider'] = args.ai_provider
        if args.ai_model: cli_overrides['ai_model'] = args.ai_model

        config = GhostclawConfig.load(".", **cli_overrides)
        client = LLMClient(config, ".")

        print(f"  Testing connection to {config.ai_provider}...")
        if not config.api_key:
            print("  ❌ API Key not found. Set GHOSTCLAW_API_KEY environment variable.")
            return 1
        else:
            success = await client.test_connection()
            if success:
                print(f"  ✅ Connection successful! Model: {client.model}")
                return 0
            else:
                print("  ❌ Connection failed. Check provider configuration or network.")
                return 1
