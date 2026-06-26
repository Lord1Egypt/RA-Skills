# CLI Architecture

Ghostclaw's CLI has been migrated from a single monolithic file to a modular **Commander Pattern** architecture. This document explains how the CLI is structured and how commands are executed.

## Overview

The CLI is separated into four distinct layers:

1.  **Commander Framework:** Defines the `Command` base interface and the `CommandRegistry` for auto-discovery.
2.  **Commands:** The concrete implementations of each command (e.g., `analyze`, `init`, `doctor`). These classes define their arguments and orchestrate execution.
3.  **Services:** Reusable business logic separated from argument parsing. These services can be called directly by other interfaces (e.g., the MCP bridge or other plugins).
4.  **Formatters:** Responsible for taking output data (like a report dictionary) and formatting it into different representations (Markdown, JSON, Terminal).

## Directory Structure

```
src/ghostclaw/cli/
├── commander/        # Command framework (base, registry)
├── commands/         # All command implementations (analyze, init, etc.)
│   └── plugins/      # Subcommands for the `plugins` group
├── formatters/       # Output formatters (terminal, JSON, markdown)
└── services/         # Reusable business logic (analyzer, config, plugins)
```

## The Request Lifecycle

1.  **Initialization:** The main entry point `ghostclaw.py` calls `registry.auto_discover()`. This scans `ghostclaw.cli.commands` and registers all subclasses of `Command`.
2.  **Parsing:** `argparse` subparsers are built dynamically based on the registered commands' `name` and `description` properties. Each command adds its specific arguments via `configure_parser()`.
3.  **Execution:** Once arguments are parsed, the dispatcher uses the command name to retrieve the correct `Command` instance from the registry and calls its `execute(args)` method.
4.  **Service Invocation:** The command invokes the appropriate service(s) to perform the actual business logic.
5.  **Formatting & Output:** If output is needed, the command uses a formatter to render the result to the console or a file.
6.  **Dual-Mode Fallback:** For backward compatibility, if a command isn't found in the registry, the CLI falls back to the legacy code path.

## Design Principles

-   **Separation of Concerns:** CLI argument parsing should not be mixed with core business logic.
-   **Testability:** Commands, services, and formatters can be tested in isolation without spawning full subprocesses.
-   **Extensibility:** Adding a new command is as simple as creating a new subclass of `Command` in the `commands/` directory. No changes to the main parser are required.
