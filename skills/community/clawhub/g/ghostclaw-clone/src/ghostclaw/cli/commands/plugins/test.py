from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commands.plugins.base import PluginsCommand, PluginService
import sys

class PluginsTestCommand(PluginsCommand):
    @property
    def name(self) -> str:
        return "plugins test"

    @property
    def description(self) -> str:
        return "Test if a plugin is available and working"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("name", help="Name of the plugin")

    async def execute(self, args: Namespace) -> int:
        print(f"🧪 Testing plugin '{args.name}'...")
        is_available = self.service.test_plugin(args.name)
        if is_available:
            print(f"✅ Plugin '{args.name}' is registered.")
            return 0
        else:
            print(f"❌ Plugin '{args.name}' is not registered.")
            return 1
