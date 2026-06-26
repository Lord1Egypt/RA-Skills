import pytest
from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command

class DummyCommand(Command):
    @property
    def name(self) -> str:
        return "dummy"

    @property
    def description(self) -> str:
        return "A dummy command"

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--foo", type=str)

    async def execute(self, args: Namespace) -> int:
        return 0

    def validate(self, args: Namespace) -> None:
        if args.foo == "invalid":
            raise ValueError("Invalid foo")

def test_command_properties():
    cmd = DummyCommand()
    assert cmd.name == "dummy"
    assert cmd.description == "A dummy command"

def test_command_configure_parser():
    cmd = DummyCommand()
    parser = ArgumentParser()
    cmd.configure_parser(parser)
    args = parser.parse_args(["--foo", "bar"])
    assert args.foo == "bar"

@pytest.mark.asyncio
async def test_command_execute():
    cmd = DummyCommand()
    args = Namespace(foo="bar")
    result = await cmd.execute(args)
    assert result == 0

def test_command_validate():
    cmd = DummyCommand()
    args = Namespace(foo="bar")
    cmd.validate(args)

    invalid_args = Namespace(foo="invalid")
    with pytest.raises(ValueError):
        cmd.validate(invalid_args)
