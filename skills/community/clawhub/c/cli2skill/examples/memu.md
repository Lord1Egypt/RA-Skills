---
name: memu
description: Agent skill for memu CLI
user-invocable: false
allowed-tools: Bash(python C:/Users/Administrator/scripts/memu-cli.py *)
---

# memu

## Commands

```bash
python C:/Users/Administrator/scripts/memu-cli.py search
python C:/Users/Administrator/scripts/memu-cli.py query
python C:/Users/Administrator/scripts/memu-cli.py add
python C:/Users/Administrator/scripts/memu-cli.py categories
```

### search
Semantic search
- `-h, --help`: show this help message and exit

### query
Search + categories
- `-h, --help`: show this help message and exit

### add
Memorize content
- `-h, --help`: show this help message and exit

### categories
List categories
- `-h, --help`: show this help message and exit
- `--all`: Include inactive

## Options

- `-h, --help`: show this help message and exit

## When to use
- Agent skill for memu CLI
- Available commands: `search`, `query`, `add`, `categories`
