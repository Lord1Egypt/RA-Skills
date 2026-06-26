from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.llm_client import LLMClient
import sys

class TestCommand(Command):
    @property
    def name(self) -> str:
        return "test"

    @property
    def description(self) -> str:
        return "Run diagnostic tests"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--llm", action="store_true", help="Test LLM connectivity and list available models")
        parser.add_argument("--ai-provider", help="Provider to test (overrides config)")
        parser.add_argument("--ai-model", help="Model to test (overrides config)")

    async def execute(self, args: Namespace) -> int:
        if args.llm:
            cli_overrides = {}
            if args.ai_provider: cli_overrides['ai_provider'] = args.ai_provider
            if args.ai_model: cli_overrides['ai_model'] = args.ai_model

            config = GhostclawConfig.load(".", **cli_overrides)
            client = LLMClient(config, ".")

            print(f"🔍 Testing LLM Connection ({config.ai_provider})...")
            success = await client.test_connection()
            if success:
                print("✅ Connection successful!")
                print("\nFetching available models...")
                models = await client.list_models()
                for m in models:
                    print(f"  • {m}")
                return 0
            else:
                print("❌ Connection failed. Check your API key and provider settings.")
                return 1
        else:
            print("Usage: ghostclaw test --llm", file=sys.stderr)
            return 1
