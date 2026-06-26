from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commands.plugins.base import PluginsCommand, PluginService
import sys

class PluginsScaffoldCommand(PluginsCommand):
    @property
    def name(self) -> str:
        return "plugins scaffold"

    @property
    def description(self) -> str:
        return "Generate a boilerplate adapter"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("name", help="Name of the new plugin")

    async def execute(self, args: Namespace) -> int:
        try:
            target = self.service.scaffold_plugin(args.name)
            name = args.name.lower().replace("-", "_")
            print(f"🏗️ Scaffolded plugin '{name}' at {target}")
            print(f"💡 Edit {target / '__init__.py'} to add your logic.")
            return 0
        except FileExistsError as e:
            print(f"⚠️ {e}")
            return 0
        except Exception as e:
            print(f"❌ Failed to scaffold plugin: {e}", file=sys.stderr)
            return 1
