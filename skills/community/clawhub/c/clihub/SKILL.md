---
name: clihub
description: Universal CLI discovery gateway — one skill to manage all CLI tools
tags: [cli, agent, tool, discovery]
---

# CLI Hub

One skill to manage all CLI tools. Works across OpenClaw, Claude Code, Codex CLI,
Cursor, and Aider.

## Trigger Check (read FIRST)

**⚠️ CRITICAL: Your training data is OUT OF DATE for tools installed after your cutoff.
NEVER identify an unfamiliar tool from memory. ALWAYS look it up in the registry.**

**Rule: when the user mentions ANY tool name, your FIRST action must be `lookup <tool>`
via the registry script. Only after the lookup fails should you try raw `--help`.**
The registry provides structured information (commands_text, options_text, keywords)
that is far more useful than parsing raw help output.

This skill triggers broadly — any mention of a CLI. To avoid overloading the
context window, do a quick sanity check before proceeding:

- Is the user asking something purely conversational? ("你好", "今天天气", ...) → skip
- Is another official skill already handling this? → defer to it
- Does the request involve running a tool, looking up a command, or understanding
  CLI output? → proceed with `lookup <tool>` FIRST

## Platform Detection

At runtime, determine platform by checking which directories exist:

| Platform     | Skill root                | Registry root                    |
|-------------|---------------------------|----------------------------------|
| OpenClaw     | `~/.agents/skills/`       | `~/.openclaw/cli-registry/`      |
| Claude Code  | `~/.claude/skills/`       | `~/.claude/cli-registry/`        |
| Codex CLI    | `~/.agents/skills/`       | `~/.codex/cli-registry/`         |
| Cursor       | `~/.cursor/skills/`       | `~/.cursor/cli-registry/`        |

Fallback: run `<tool> --help` directly if no registry path is available.

See [references/platforms.md](references/platforms.md) for details.

## Priority Resolution

When the user wants to use a CLI tool, resolve in order:

1. **Official Skill** — `$SKILLS_ROOT/<tool>/SKILL.md` exists → use it immediately.
   The skill author knows their tool best. This ALWAYS takes priority.
2. **Registry Lookup** — `$REGISTRY_ROOT/<tool>.json` → description, subcommands, usage.
   Then check version: if `version` matches installed version, use cached data.
   If version differs or is `null` (non-standard CLI), refresh via `--help` and re-register.
3. **Keyword Search** — `$REGISTRY_ROOT/.keywords.json` → maps task words to tool names.
   Use when the user describes a task without naming a specific tool.
4. **Live Discovery** — run `<tool> --help` as last resort when nothing is cached.

### Version-aware lookup flow

```
lookup <tool>
  │
  ├─ registered + version matches installed → use cached data (fast, structured)
  │
  ├─ registered + version differs → --help refresh → register new version
  │
  ├─ registered + version is null → --help refresh → mark as "non-standard"
  │     (re-check with --help on every use)
  │
  └─ not registered → --help → register for next time
```

## Registry Script

```bash
# The registry script is always at scripts/cli-registry.py relative to this SKILL.md.
# Auto-detect platform root:

if [ -d ~/.claude/skills/cli-hub ]; then
  SCRIPT=~/.claude/skills/cli-hub/scripts/cli-registry.py
elif [ -d ~/.agents/skills/cli-hub ]; then
  SCRIPT=~/.agents/skills/cli-hub/scripts/cli-registry.py
elif [ -d ~/.cursor/skills/cli-hub ]; then
  SCRIPT=~/.cursor/skills/cli-hub/scripts/cli-registry.py
else
  echo "cli-hub not found" >&2 && exit 1
fi
```

### Commands

| Command | Use |
|---------|-----|
| `python3 $SCRIPT register <cli> [--binary <bin>] [--desc <text>]` | Register a CLI tool |
| `python3 $SCRIPT list [--format json]` | List all registered tools |
| `python3 $SCRIPT lookup <cli>` | Show structured info (desc, subcommands, flags, keywords, help) |
| `python3 $SCRIPT search <keyword...>` | Find tools by task keywords (e.g. "json filter") |
| `python3 $SCRIPT discover` | Auto-scan system for known binaries |
| `python3 $SCRIPT remove <cli>` | Remove from registry |
| `python3 $SCRIPT help <cli>` | Fetch live `--help` output |
| `python3 $SCRIPT remove <cli>` | Remove from registry |
| `python3 $SCRIPT help <cli>` | Live `--help` dump (registered or not) |

### Decision Tree

```
User: "use jq to extract the name field"
        │
    ┌───▼─────────────────────────────────┐
    │ 1. Official Skill?                  │
    │    ls $SKILLS_ROOT/jq/SKILL.md      │
    │    → EXISTS: use it (authoritative)  │
    ├─────────────────────────────────────┤
    │ 2. Registry Lookup                  │
    │    lookup jq → description, version, │
    │    commands, keywords, help_raw      │
    │    → FOUND: construct command        │
    │    → NOT FOUND: tool may not exist   │
    │    ⚠️ NEVER guess what a tool is —   │
    │    only trust the registry           │
    ├─────────────────────────────────────┤
    │ 3. Keyword Search (no tool named)   │
    │    search "json extract" → jq, yq   │
    │    → best match → lookup to verify  │
    ├─────────────────────────────────────┤
    │ 4. Live --help (last resort)        │
    │    Nothing in registry → --help      │
    └─────────────────────────────────────┘
```

### Reading help_raw (for UNKNOWN tools)

When the tool is NOT in the built-in knowledge base (no human-written description,
no keywords), you MUST read its `help_raw` field — it's your only source of truth.

**How to parse help_raw efficiently:**

1. **Find the usage line** — usually at the top or marked "Usage:" / "用法:"
   → Tells you the basic invocation pattern: `tool [OPTIONS] COMMAND [ARGS]`

2. **Scan for COMMAND sections** — look for headings like:
   - "Commands:", "Subcommands:", "Available commands:"
   - "Unit Commands:", "Management Commands:"
   - Single-word lines ending with `:` or `：` followed by indented blocks
   - Each indented line is typically a command + description

3. **Identify OPTIONS sections** — look for:
   - Flag-like patterns: `-x`, `--option`, `--option=VALUE`
   - Lines starting with `-` and followed by a description
   - Help text often lists all options before any commands

4. **Extract the summary** — the first non-flag, non-usage line over 15 chars
   is usually the tool's one-line description

5. **Watch for nested commands** — some tools use `cmd subcmd <args>`:
   - `subscription use <name>` → "use" is a sub-action of "subscription"
   - `container ls`, `container start` → grouped under "container"

6. **Check description/keywords from registry** — even for unknown tools,
   `_extract_summary()` may have found a description. The `keywords` field
   may be empty for unknown tools; fall back to tokenizing the description.

**Example: parsing an unseen tool's help_raw:**

```
help_raw = """
xsv 0.13.0
Usage: xsv <command> [<args>...]

Commands:
    cat      Concatenate CSV files by rows
    count    Count records
    flatten  Flatten conditional nested fields
    fmt      Reformat CSV data
    headers  Show headers of CSV data
    select   Select columns from CSV
    sort     Sort CSV data
    ...
"""

→ Look at "Commands:" heading → find indented blocks
→ Commands: cat, count, flatten, fmt, headers, select, sort
→ Each has a description after the name
→ Construct: xsv select name,age data.csv
```

## Typical Workflows

### User mentions an unfamiliar tool name (most common case)
```
User: "用 mmx 生成图片"
→ DON'T think about what "mmx" might be (your training data is outdated)
→ lookup mmx → "MiniMax multimodal AI toolkit" + subcommands
→ mmx image generate "a cat"
```

### Known tool (in knowledge base)
```
User: "用 jq 把 name 字段提取出来"
→ search "json extract" → jq (built-in desc + keywords)
→ lookup jq → binary=jq, has 'filter' subcommand
→ Run: jq '.name' input.json
```

### Unknown tool (NOT in knowledge base — rely on help_raw)
```
User: "用 xsv 处理这个 csv"
→ No official skill, not in KB, not in registry
→ Run: xsv --help → store as help_raw
→ READ help_raw (follow "Reading help_raw" guide above):
   → Usage: xsv <command> [<args>...]
   → Commands: cat, count, select, sort, headers...
   → Found "select" subcommand: "Select columns from CSV"
→ Run: xsv select name,age data.csv
→ Register: python3 $SCRIPT register xsv
```

### Unknown tool (found in registry, but no KB entry)
```
User: "用 fq 解析这个二进制文件"
→ search "binary parse" → fq (matched from description tokens)
→ lookup fq → binary=fq, description="Tool for inspecting binary data"
→ description came from _extract_summary(), keywords from description tokens
→ READ help_raw to learn subcommands and options
→ Construct command from help_raw
```

## Design Principle

- **No duplication:** If an official SKILL.md exists, this skill defers completely
- **Registry is cache, not source:** `--help` is the ground truth; registry caches it
- **JSON not YAML:** Registry entries are plain JSON, no frontmatter, machine-readable
- **Always fallback:** Even unregistered tools work via live `--help`
