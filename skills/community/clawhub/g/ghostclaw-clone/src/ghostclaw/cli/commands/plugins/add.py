from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commands.plugins.base import PluginsCommand, PluginService
import sys

class PluginsAddCommand(PluginsCommand):
    @property
    def name(self) -> str:
        return "plugins add"

    @property
    def description(self) -> str:
        return "Install an external plugin from a local path"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("source", help="Path to the plugin directory or file")

    async def execute(self, args: Namespace) -> int:
        try:
            target = self.service.add_plugin(args.source)
            print(f"✅ Installed plugin '{args.source}' to {target}")
            return 0
        except Exception as e:
            print(f"❌ Failed to install plugin: {e}", file=sys.stderr)
            return 1
