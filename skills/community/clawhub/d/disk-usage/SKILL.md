---
name: disk-usage
version: 1.0.0
description: >-
  Show disk usage of a directory or file in human-readable format.
  Use when the user wants to know how much space a folder or file takes.
allowed-tools: Bash(du:*)
metadata: >-
  {"openclaw":{"emoji":"💾","requires":{"bins":["du"],"env":[]},"install":[]}}
---

# Disk Usage

Show how much disk space a directory or file uses with a single command.

## Usage

```bash
du -sh <PATH>
```

**Arguments:**
| # | Name | Description |
|---|------|-------------|
| 1 | PATH | Path to file or directory to measure |

## Example

```bash
du -sh /home/user/projects
```

**Output:**
```
1.2G	/home/user/projects
```

Format: `SIZE	PATH`

## Success / Failure

- **Success**: One line with human-readable size and path (exit code 0)
- **Failure**: Error message (exit code non-zero, e.g. path not found)
