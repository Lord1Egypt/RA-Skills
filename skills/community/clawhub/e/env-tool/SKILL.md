---
name: env-tool
description: Display, set, and manage environment variables in shell sessions. Use when inspecting or modifying the runtime environment.
---

# Environment Variable Manager

View and control environment variables available to shell processes. Supports listing all variables, querying specific values, and temporary variable assignment.

## Usage

```bash
env-tool [options]
```

## Common Operations

- List all environment variables with values
- Show value of a specific variable (e.g. PATH, HOME, USER)
- Check if a variable is set without showing its value
- Run a command with modified environment

## Examples

```bash
# List all environment variables
env-tool

# Show a specific variable
env-tool | grep PATH

# Check variable exists
env-tool | grep ^HOME=
```