from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commands.plugins.base import PluginsCommand, PluginService
import sys

class PluginsDisableCommand(PluginsCommand):
    @property
    def name(self) -> str:
        return "plugins disable"

    @property
    def description(self) -> str:
        return "Disable a plugin"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("name", help="Name of the plugin to disable")

    async def execute(self, args: Namespace) -> int:
        try:
            self.service.disable_plugin(args.name)
            return 0
        except Exception as e:
            print(f"❌ {e}", file=sys.stderr)
            return 1
