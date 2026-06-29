# jiangsier-skill-codewiki

> An AI-Agent–friendly Bash workflow that clones a Git repository and
> generates a structured wiki from it using the `codewiki` CLI.

`scripts/codewiki.sh` is a small, dependency-light Bash script designed to be invoked
either directly from a terminal or programmatically by an external AI agent
(see `SKILL.md`). Given a repository and an optional output directory and
set of instructions, it will:

1. Clone the repository (or pull the latest changes if it's already cloned).
2. Run `codewiki generate` inside the repo to produce a wiki under
   `<output>/<repo>/wiki`.
3. *(Optional)* Render that wiki into a static **MkDocs** and/or **VitePress**
   site via the sibling `scripts/render_docs.sh`, and optionally serve the
   result over HTTP for local preview.

> **Dependency note**
> This skill is a thin orchestration wrapper around
> [CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki). The actual wiki
> generation is performed by the `codewiki` CLI provided by that project, so
> you must install CodeWiki before using this script. Rendering additionally
> requires `python3` (MkDocs) and/or `node` + `npm` (VitePress); the
> per-renderer dependencies are installed automatically into isolated
> sandboxes at render time — no manual `pip install` or `npm install`.

## Features

- **Agent-friendly.** Predictable flags, structured `--help`, stable exit
  codes, and an accompanying `SKILL.md` so AI agents can parse, confirm, and
  invoke it without guessing.
- **Dual-format repository parsing.** Accepts the shorthand `group/repo`
  (expanded to `https://github.com/group/repo.git`) or a full `https://` /
  `git@` clone URL.
- **Dynamic instruction handling.** Optional `-i/--instructions` text is
  forwarded verbatim to `codewiki generate` with correct quoting — spaces,
  quotes, and shell metacharacters are preserved.
- **Optional rendering pipeline.** `--render <mkdocs|vitepress|both>` turns
  the generated Markdown into static sites under `<output>/<repo>/mkdocs`
  and/or `<output>/<repo>/vitepress`. `--serve [PORT]` previews them over
  HTTP.
- **Idempotent re-runs.** If the target directory already contains a clone,
  the script runs `git pull --ff-only` instead of re-cloning.
- **Strict dependency checks.** Fails fast with a clear message if `git` or
  `codewiki` are missing (render-time tools are checked only when their
  stack is requested).
- **Shallow by default.** Uses `git clone --depth 1` to keep clones fast and
  small — sufficient when only the working tree is needed.

## Installation & prerequisites

| Requirement    | Purpose                                          | Install                                                                          |
|----------------|--------------------------------------------------|----------------------------------------------------------------------------------|
| Bash ≥ 4       | Script runtime (arrays, `[[ ]]`)                 | System default on macOS / Linux                                                  |
| Git            | Clone / pull repositories                        | https://git-scm.com/                                                             |
| `codewiki`     | Wiki generator invoked by the script             | [FSoft-AI4Code/CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki) — install per their README |
| `python3` ≥3.9 | MkDocs renderer (only when `--render` uses mkdocs or both) | https://www.python.org/downloads/                                       |
| `node` ≥18 + `npm` | VitePress renderer (only when `--render` uses vitepress or both) | https://nodejs.org/                                              |

Make the script executable:

```bash
chmod +x scripts/codewiki.sh scripts/render_docs.sh
```

(Optional) Add the `scripts/` directory to your `PATH` so the script can be called as `codewiki.sh`
from anywhere.

## Usage

### Direct CLI invocation

```bash
# Shorthand repo, default output dir (.):
./scripts/codewiki.sh -r anthropics/claude-code

# Full HTTPS URL with custom output dir:
./scripts/codewiki.sh -r https://github.com/foo/bar.git -o ./work/bar

# SSH URL with instructions:
./scripts/codewiki.sh -r git@github.com:foo/bar.git \
              -o ./out \
              -i "Focus on the auth module; skip vendored code."

# Generate + render both stacks, then preview over HTTP on port 3000:
./scripts/codewiki.sh -r foo/bar --render both --serve 3000

# Render MkDocs only (no preview server):
./scripts/codewiki.sh -r foo/bar --render mkdocs

# Show help:
./scripts/codewiki.sh -h
```

### As an AI-Agent skill

Copy `SKILL.md` (and the script) into your agent's skill directory (e.g.
`~/.claude/skills/codewiki/`). The agent will then be able to respond to
`/codewiki <user input>` by parsing the request, showing a structured
confirmation overview, and — only after the user confirms — invoking the
script.

## Configuration & parameters

| Flag / option               | Required | Description                                                                       | Default |
|-----------------------------|----------|-----------------------------------------------------------------------------------|---------|
| `-r, --repository <repo>`   | yes      | Repository in shorthand `group/repo` form, or a full `https://` / `git@` URL.      | —       |
| `-o, --output <dir>`        | no       | Destination directory. Created with `mkdir -p` if missing.                         | `.`     |
| `-i, --instructions <text>`| no       | Free-form instructions passed verbatim to `codewiki generate --instructions`.     | (none)  |
| `--render <stack>`          | no       | Render the generated wiki via `render_docs.sh`. `<stack>` ∈ `mkdocs`, `vitepress`, `both`. | (skip) |
| `--serve [PORT]`             | no       | After rendering, serve the built site(s) over HTTP. Requires `--render`. Default port `8000`; with `--render both`, MkDocs uses `PORT` and VitePress uses `PORT+1`. | (none) |
| `-h, --help`                | —        | Print help and exit.                                                              | —       |

## Output layout

```
<output>/
└── <repo>/
    ├── (.git)              # shallow clone of the source repository
    ├── wiki/               # codewiki output — Markdown + metadata
    ├── mkdocs/site/        # MkDocs static site (only with --render mkdocs|both)
    └── vitepress/site/     # VitePress static site (only with --render vitepress|both)
```

## Exit codes

| Code | Meaning                |
|------|------------------------|
| 0    | Success                |
| 1    | Usage error            |
| 2    | Missing dependency     |
| 3    | Clone / pull failure   |
| 4    | codewiki failure       |
| 5    | Render failure         |

## Acknowledgements

This project depends on **[CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki)**
by [FSoft-AI4Code](https://github.com/FSoft-AI4Code) for the underlying
documentation generation engine. Please direct upstream bugs and feature
requests to that repository; this wrapper only handles cloning and invocation.

## License

See [LICENSE](LICENSE).
