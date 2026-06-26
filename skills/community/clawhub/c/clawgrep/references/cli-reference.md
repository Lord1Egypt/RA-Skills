# CLI Reference

## All flags

| Flag | Default | Description |
|------|---------|-------------|
| `-k`, `--top-k` | 5 | Number of results to return |
| `-B`, `--before-context` | 0 | Lines of context before match |
| `-A`, `--after-context` | 0 | Lines of context after match |
| `-C`, `--context` | 0 | Lines before and after match |
| `--min-score` | none | Minimum score threshold (0.0–1.0) |
| `--semantic-weight` | 0.7 | Embedding similarity weight (0.0–1.0) |
| `--keyword-weight` | 0.3 | Keyword match weight (0.0–1.0) |
| `--path-boost` | 1.0 | Boost for path/filename matches (0.0 disables) |
| `--reindex` | false | Force re-embedding all files |
| `--no-cache` | false | Skip cache reads/writes |
| `--cache-dir` | platform default | Custom cache directory |
| `--no-gitignore` | false | Don't respect .gitignore |
| `--ignore-file` | none | Additional ignore file (repeatable) |
| `--no-recursive` | false | Don't recurse into subdirectories |
| `-l` | — | Print only matching filenames |
| `-c` | — | Print match count per file |
| `-q` | — | Quiet; exit 0 if any match |
| `--no-color` | false | Disable coloured output |
| `--show-score` | false | Append relevance score to each line |
| `--verbose` | false | Print diagnostics to stderr |
| `-i` | — | Accepted, ignored (always case-insensitive) |

## Grep compatibility

These grep flags work identically in clawgrep:

| Flag | Behavior |
|------|----------|
| `-l` | Print only filenames of matching files |
| `-c` | Print match count per file |
| `-q` | Quiet mode — exit 0 if match, 1 if not |
| `-B N` | N lines of context before match |
| `-A N` | N lines of context after match |
| `-C N` | N lines of context before and after |
| `-i` | Accepted for compatibility (always case-insensitive) |

Output format (`file:line:text`), exit codes (0/1/2), and context line
separators all match grep. Any parser that reads grep output can read clawgrep
output.

Key differences from grep:

- Results are ranked by relevance, not printed in file order.
- Default is semantic + keyword hybrid search, not regex matching.
- First run downloads a small ONNX embedding model (~30 MB) from Hugging Face
  and builds an embedding index (takes a few seconds). Subsequent runs reuse
  the cached model and embeddings and are fully offline.
- Model weights and embedding cache share the same directory. The default
  location is platform-specific: `~/.cache/clawgrep/` on Linux,
  `~/Library/Caches/clawgrep/` on macOS, `AppData\Local\clawgrep\` on Windows.
  Use `--cache-dir`, `CLAWGREP_CACHE_DIR`, or the config file to override.
- Always case-insensitive. `-i` is accepted but has no effect.

## Environment variables

| Variable | Description |
|----------|-------------|
| `CLAWGREP_CONFIG` | Path to config file (default: `~/.clawgrep.toml`) |
| `CLAWGREP_CACHE_DIR` | Cache directory (overrides platform default) |
| `CLAWGREP_VERBOSE` | Set to `1` to enable verbose output |
| `NO_COLOR` | Disable coloured output (any value) |

Precedence for cache directory: `--cache-dir` flag > config file `cache_dir` > `CLAWGREP_CACHE_DIR` env var > default.

## Configuration file

Settings can be pre-configured in `~/.clawgrep.toml` so commands stay simple.
Set the `CLAWGREP_CONFIG` environment variable to use a different path.

```toml
semantic_weight = 0.7
keyword_weight = 0.3
top_k = 10
min_score = 0.3
path_boost = 1.5
cache_dir = "/tmp/clawgrep-cache"
```

All fields are optional. Precedence: CLI flags > config file > environment variables.

Pre-configuring this file is recommended so that search commands only need a
query and path.

## Performance

- First search builds an embedding index. Subsequent searches reuse cached
  embeddings and are fast.
- Only changed files (by mtime/size) are re-embedded on subsequent runs.
- Multiple processes can share the same cache safely.
- Use `--no-cache` for one-off searches on throwaway content.
- Use `--reindex` if results seem stale after file changes.

## Logging

Set `RUST_LOG` to control debug output:

```bash
RUST_LOG=clawgrep=debug clawgrep "query" .
```

Logs go to stderr.
