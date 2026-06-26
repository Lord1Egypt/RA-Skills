import pytest
from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command
from ghostclaw.cli.commander import CommandRegistry

class Cmd1(Command):
    @property
    def name(self): return "cmd1"
    @property
    def description(self): return "Command 1"
    def configure_parser(self, parser): pass
    async def execute(self, args): return 0

class Cmd2(Command):
    @property
    def name(self): return "cmd2"
    @property
    def description(self): return "Command 2"
    def configure_parser(self, parser): pass
    async def execute(self, args): return 0

def test_registry_registration():
    registry = CommandRegistry()
    registry.register(Cmd1)

    assert registry.get("cmd1") is Cmd1
    assert registry.get("cmd2") is None

def test_registry_all():
    registry = CommandRegistry()
    registry.register(Cmd1)
    registry.register(Cmd2)

    all_cmds = registry.all()
    assert len(all_cmds) == 2
    assert Cmd1 in all_cmds
    assert Cmd2 in all_cmds

def test_registry_invalid_registration():
    registry = CommandRegistry()
    with pytest.raises(TypeError):
        registry.register(object)

def test_auto_discover(mocker):
    registry = CommandRegistry()
    registry.auto_discover()

    analyze_cmd = registry.get("analyze")
    assert analyze_cmd is not None
    assert analyze_cmd.__name__ == "AnalyzeCommand"
