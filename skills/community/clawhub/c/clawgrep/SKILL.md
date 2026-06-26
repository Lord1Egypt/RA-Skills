---
name: clawgrep
description: >
  Grep-like CLI with hybrid semantic and keyword search.
  Combines semantic embedding search with keyword matching for high-quality code and document retrieval.
  Use when searching for content where the exact wording is unknown,
  or when grep misses results across large codebases or folders.
  Useful for recursively searching large collections of markdown
  files, like memories. Output is grep-compatible for easy parsing.
compatibility: >
  Requires the clawgrep binary on PATH. Works on Linux, macOS, and Windows.
  No API keys needed. On first run, downloads a small ONNX embedding model
  (~30 MB) from Hugging Face and caches it locally. Subsequent runs are
  fully offline. Install via cargo, npm, or pip.
license: MIT OR Apache-2.0
metadata:
  version: "0.1"
  author: Schonhoffer
  repository: https://github.com/Schonhoffer/clawgrep
  homepage: https://github.com/Schonhoffer/clawgrep
---

# clawgrep

Semantic + keyword file search. Output is grep-compatible. Runs fully locally. On first run, automatically downloads a small ONNX embedding model (~30 MB) from Hugging Face and caches it in the local cache directory. After that, all searches are offline.

## Check availability

```bash
clawgrep --version
```

If not found, install from the [open-source repository](https://github.com/Schonhoffer/clawgrep) using any of these methods (only one needed):

```bash
cargo install clawgrep        # Rust (recommended)
npm install -g clawgrep        # Node.js
pip install clawgrep           # Python
```

## Basic usage

```bash
clawgrep --no-color "query" <path>
```

Always pass `--no-color` when parsing output programmatically.

### Search a workspace

```bash
clawgrep --no-color "previous discussion about auth flow" ./memory
```

### Output format

Grep-compatible, one result per line, ranked by relevance (best first):

```
$ clawgrep --no-color "previous discussion about auth flow" ./memory
memory/2025-06-12-auth-design.md:8:Decided to use OAuth2 with PKCE for all client auth.
memory/2025-06-12-auth-design.md:14:Token refresh should be transparent to the user.
memory/2025-06-10-planning.md:3:Auth flow is the top priority for the sprint.
memory/archive/2025-05-session-notes.md:42:Discussed moving auth to a separate service.
memory/archive/2025-05-session-notes.md:87:Need to revisit token expiry policy.
```

Each line is `file:line:text`. Context lines (from `-C`) use `-` as the
separator instead: `file-line-text`.

### Exit codes

| Code | Meaning |
|------|---------|
| `0`  | Match found |
| `1`  | No match |
| `2`  | Error |

Same as grep. Use `-q` for existence checks without output.

## Choosing search mode

Default weights: 70% semantic, 30% keyword.

**Concept search** (don't know exact wording):

```bash
clawgrep --no-color "decision about migration strategy" ./memory
```

**Exact identifier search** (note IDs, tags, serial numbers):

```bash
clawgrep --no-color --keyword-weight 0.8 --semantic-weight 0.2 "PROJ-1042" ./memory
```

## Key flags

| Flag | Purpose |
|------|---------|
| `-k N` | Number of results (default: 5) |
| `-C N` | Context lines before and after |
| `-l` | Print only matching filenames |
| `-q` | Quiet; just set exit code |
| `--show-score` | Append relevance score |
| `--path-boost N` | Boost filename matches (>1.0 = higher) |
| `--min-score N` | Filter low-relevance results (0.0–1.0) |

See [CLI reference](references/cli-reference.md) for all flags.

## Best practices

1. Use `--no-color` always when parsing output.
2. Keep `-k` small (3–5) to reduce output. Increase only when needed.
3. Check exit codes instead of parsing stdout when possible.
4. Let the cache persist — don't use `--no-cache` unless searching throwaway
   content. First run indexes; subsequent runs are fast.
5. Search the narrowest relevant directory, not the whole filesystem.

## References (advanced, usually not needed)

The information above should be sufficient for normal use. Only load these if
you run into problems or need flags not listed above:

- [CLI reference](references/cli-reference.md) — all flags, config file format, grep compatibility
- [Examples](references/examples.md) — more input/output examples for edge cases
