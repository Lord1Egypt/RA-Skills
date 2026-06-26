from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commands.plugins.base import PluginsCommand, PluginService
import sys

class PluginsRemoveCommand(PluginsCommand):
    @property
    def name(self) -> str:
        return "plugins remove"

    @property
    def description(self) -> str:
        return "Remove an external plugin"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("name", help="Name of the plugin to remove")

    async def execute(self, args: Namespace) -> int:
        try:
            target = self.service.remove_plugin(args.name)
            print(f"🗑️ Removed plugin '{args.name}' from {target}")
            return 0
        except ValueError as e:
            print(f"🚫 {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"❌ Failed to remove plugin: {e}", file=sys.stderr)
            return 1
