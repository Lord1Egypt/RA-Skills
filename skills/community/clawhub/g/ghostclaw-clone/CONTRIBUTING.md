# Contributing to Ghostclaw

Thank you for your interest in contributing to Ghostclaw!

## Adding a new command

Ghostclaw's CLI is built using a modular Commander architecture. Adding a new command is designed to be simple and require no changes to central files like the main CLI script.

### 1. Create a Command Class

Create a new `.py` file inside `src/ghostclaw/cli/commands/` and define a class that inherits from `ghostclaw.cli.commander.Command`.

```python
from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command

class MyCommand(Command):
    @property
    def name(self) -> str:
        return "my-command"

    @property
    def description(self) -> str:
        return "Does something cool."

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--cool-flag", action="store_true")

    async def execute(self, args: Namespace) -> int:
        print("Cool things happening.")
        return 0
```

### 2. Auto-Discovery

You don't need to manually register your command! The CLI uses an auto-discovery registry that scans `src/ghostclaw/cli/commands/` for any subclasses of `Command`. When you run `ghostclaw`, it will be automatically available.

### 3. Architecture Best Practices

- **Keep `execute` Thin:** For non-trivial operations, create a Service class in `src/ghostclaw/cli/services/`.
- **Use Formatters:** For formatting reports or complex console outputs, utilize classes in `src/ghostclaw/cli/formatters/`.
- **Unit Tests:** Add a test file for your command in `tests/unit/cli/commands/`.

For complete details, see [docs/COMMAND_DEVELOPMENT.md](docs/COMMAND_DEVELOPMENT.md).
