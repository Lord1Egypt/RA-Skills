from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commands.plugins.base import PluginsCommand, PluginService
import sys

try:
    from rich.console import Console
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

class PluginsListCommand(PluginsCommand):
    @property
    def name(self) -> str:
        return "plugins list"

    @property
    def description(self) -> str:
        return "List all discovered plugins"

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    async def execute(self, args: Namespace) -> int:
        from ghostclaw.core.adapters.registry import registry

        metadata = self.service.list_plugins()
        if not metadata:
            print("No plugins found.")
            return 0

        if HAS_RICH:
            table = Table(title="Ghostclaw Plugins")
            table.add_column("Name", style="cyan")
            table.add_column("Version", style="magenta")
            table.add_column("Description")
            table.add_column("Type", style="green")

            for meta in metadata:
                p_name = meta.get("name", "unknown")
                p_type = "Built-in" if p_name in registry.internal_plugins else "External"
                table.add_row(
                    p_name,
                    meta.get("version", "unknown"),
                    meta.get("description", ""),
                    p_type
                )
            Console().print(table)
        else:
            print("Name | Version | Description | Type")
            for meta in metadata:
                p_name = meta.get("name")
                p_type = "Built-in" if p_name in registry.internal_plugins else "External"
                print(f"{p_name} | {meta.get('version')} | {meta.get('description')} | {p_type}")

        return 0
