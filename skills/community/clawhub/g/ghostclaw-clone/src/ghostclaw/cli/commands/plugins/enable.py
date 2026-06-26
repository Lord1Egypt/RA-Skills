from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commands.plugins.base import PluginsCommand, PluginService
import sys

class PluginsEnableCommand(PluginsCommand):
    @property
    def name(self) -> str:
        return "plugins enable"

    @property
    def description(self) -> str:
        return "Enable a plugin"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("name", help="Name of the plugin to enable")

    async def execute(self, args: Namespace) -> int:
        try:
            self.service.enable_plugin(args.name)
            print(f"✅ Enabled plugin '{args.name}'.")
            return 0
        except Exception as e:
            print(f"❌ {e}", file=sys.stderr)
            return 1
