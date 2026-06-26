# Command Development Guide

This guide explains how to create new commands or modify existing ones using Ghostclaw's modular CLI architecture.

## Adding a New Command

Adding a new command involves creating a new class that inherits from the `Command` base class and placing it in the `ghostclaw.cli.commands` package. The CLI's auto-discovery mechanism will automatically detect and register it.

### Step 1: Create a Command Class

Create a new file in `src/ghostclaw/cli/commands/` (e.g., `mycommand.py`).

```python
from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command
import sys

class MyCommand(Command):
    @property
    def name(self) -> str:
        return "mycommand"

    @property
    def description(self) -> str:
        return "Description of what my command does"

    def configure_parser(self, parser: ArgumentParser) -> None:
        # Add your arguments here
        parser.add_argument("--myflag", action="store_true", help="My custom flag")

    async def execute(self, args: Namespace) -> int:
        # Validate arguments if necessary
        self.validate(args)

        # Execute business logic (ideally via a Service)
        if args.myflag:
            print("Flag is set!", file=sys.stdout)
        else:
            print("Running my command...", file=sys.stdout)

        # Return an exit code (0 for success, non-zero for error)
        return 0

    def validate(self, args: Namespace) -> None:
        # Optional validation logic
        pass
```

### Step 2: Use Services and Formatters

Keep your `execute` method thin. Business logic should reside in the `services/` directory, and output formatting should use the `formatters/` directory.

- **Services**: e.g., `AnalyzerService`, `ConfigService`. These classes should handle all logic and return data structures.
- **Formatters**: e.g., `TerminalFormatter`, `JSONFormatter`. These classes should take data and format it.

### Step 3: Run the CLI

Since the registry uses auto-discovery, your command will be immediately available.

```bash
ghostclaw mycommand --help
```

## Adding a Subcommand

Subcommands (like `plugins list` or `plugins add`) follow a slightly different pattern. The dispatcher currently expects commands in the format `group subcommand`.

If you are adding a subcommand to an existing group (e.g., `plugins`), place the file in the corresponding subfolder (`src/ghostclaw/cli/commands/plugins/`). Ensure the `name` property reflects the full path:

```python
class MyPluginCommand(PluginsCommand):
    @property
    def name(self) -> str:
        return "plugins mynewcommand"
```

## Best Practices

- Always return an integer exit code from `execute`.
- Use `sys.stdout` for regular output and `sys.stderr` for errors or debugging information.
- Use `asyncio` for I/O bound operations. All `execute` methods must be `async`.
- Provide meaningful help strings in `configure_parser`.
- Write unit tests for your command in `tests/unit/cli/commands/`.
