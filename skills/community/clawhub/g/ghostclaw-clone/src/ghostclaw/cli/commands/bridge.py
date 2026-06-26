from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command
from ghostclaw.core.bridge import GhostBridge
import sys

class BridgeCommand(Command):
    @property
    def name(self) -> str:
        return "bridge"

    @property
    def description(self) -> str:
        return "Start the JSON-RPC 2.0 bridge server"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--verbose", action="store_true", help="Enable verbose file logging (ghostclaw.log)")

    async def execute(self, args: Namespace) -> int:
        try:
            bridge = GhostBridge()
            await bridge.run()
            return 0
        except KeyboardInterrupt:
            return 130
        except Exception as e:
            print(f"Bridge error: {e}", file=sys.stderr)
            return 1
