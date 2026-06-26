from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command
from ghostclaw.cli.services import ConfigService
import sys

class InitCommand(Command):
    @property
    def name(self) -> str:
        return "init"

    @property
    def description(self) -> str:
        return "Scaffold local project configuration"

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    async def execute(self, args: Namespace) -> int:
        try:
            ConfigService.init_project(".")
            return 0
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1
