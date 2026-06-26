from abc import ABC
from ghostclaw.cli.commander import Command
from ghostclaw.cli.services import PluginService

class PluginsCommand(Command, ABC):
    """
    Base class for plugin subcommands.
    """
    def __init__(self):
        super().__init__()
        self.service = PluginService()
