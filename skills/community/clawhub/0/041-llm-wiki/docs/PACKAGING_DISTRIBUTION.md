# Packaging & Distribution Decisions (uv tool install)

> Status: current decision record. Documents why llm-wiki is distributed as a
> `uv tool install` package from the git remote rather than from PyPI, and the
> constraints that shaped the packaging layout.
>
> Introduced on branch `feat/uv-tool-install` (2026-07-27). Not yet merged to
> `main`.

## Goal

Let a user install and start a knowledge base with one command, **without
manually running `git clone`**, while keeping the project a plain-text,
git-native wiki.

Target user experience:

```bash
uv tool install git+https://github.com/Nemo4110/llm-wiki.git
llm-wiki init my-kb
cd my-kb
llm-wiki status
```

## Decisions

### 1. Distribute via `uv tool install` from the git remote, not PyPI

`uv tool install git+https://github.com/Nemo4110/llm-wiki.git` satisfies the
"no manual clone" goal: uv fetches and builds the package in the background and
exposes the `llm-wiki` executable on `PATH`. Upgrades are `uv tool upgrade
llm-wiki`, which re-fetches the default branch.

**Why not PyPI (attempted first):** `uv publish` of a clean `1.2.0` wheel was
rejected with `400 The name 'llm-wiki' is too similar to an existing project`.
This is PyPI's name-confusion protection, which can trigger even when the exact
name returns 404 (it guards against near-name squatting). Rather than squat a
near-name (`llm-wiki-skill`, `llm_wiki`, `llm-kb` were probed), the decision
was to keep the project name `llm-wiki` and install straight from the git
remote.

**Consequence:** the package is not on PyPI today. If a PyPI release is wanted
later, the project name in `pyproject.toml` must change to a non-conflicting
one; the console script name (`llm-wiki`) can stay as-is. A PyPI token was
supplied for the attempt and is no longer needed for the chosen path.

### 2. Keep the `src.llm_wiki` on-disk layout; map it to `llm_wiki` at build time

The import package stays `src/llm_wiki/` in the repository. `pyproject.toml`
uses hatchling with `packages = ["src/llm_wiki"]`, which maps the on-disk
directory to the importable top-level package `llm_wiki` in the wheel. No
source files move, so existing `from src.llm_wiki...` imports in
`scripts/agent-bridge.py` and `tests/` keep working unchanged.

- Console entry point: `llm-wiki = "llm_wiki.commands:cli"`.
- Version is dynamic, read from `src/llm_wiki/__init__.py`.
- Runtime dependencies mirror `src/requirements.txt`; `pytest` moved to the
  `dev` extra and the PDF fallback readers (`pdfplumber`, `pdfminer.six`) to a
  `pdf` extra so a default install stays lean.

### 3. Ship scaffold templates inside the wheel; add `llm-wiki init`

A tool installed without a checkout has no project skeleton, so the knowledge
base scaffold must ship in the wheel. `src/llm_wiki/templates/` holds
`AGENTS.md`, `config.yaml.example`, `sources-README.md`, and
`page_template.md`; because it lives under `src/llm_wiki/`, it is included in
the wheel automatically (no separate `force-include`, which would collide with
the `packages` mapping).

`llm-wiki init <dir>` (implemented in `src/llm_wiki/init_cmd.py`, registered in
`commands.py`) materializes `wiki/`, `sources/`, `AGENTS.md`, `CLAUDE.md`,
`config.yaml.example`, `assets/`, and `log.md` via `importlib.resources`. The
CLI group (`cli()`) resolves the wiki root lazily so `init` runs in an
uninitialized directory; all other subcommands still require a root.

### 4. `CLAUDE.md` is a real file in scaffolds, a symlink in the repo

In the repository, `CLAUDE.md` is a relative symlink to `AGENTS.md` (git mode
`120000`) so every agent entry point stays byte-identical. A scaffolded
knowledge base instead gets a small **real** `CLAUDE.md` that points the agent
at `AGENTS.md`. Reasons:

- Windows cannot create symlinks without Developer Mode / elevated privileges,
  so `llm-wiki init` cannot rely on symlink creation on a user's machine.
- `find_wiki_root()` only needs a file named `CLAUDE.md` to exist as its
  sentinel; a pointer file satisfies that and degrades gracefully.

> Note: when this worktree was checked out on Windows with `core.symlinks
> = false`, the repo's own `CLAUDE.md` was materialized as a plain file and a
> test failed. Restoring the symlink (`git config core.symlinks true` then
> `git checkout -- CLAUDE.md`) fixed it. The committed object remains mode
> `120000`; this is a local-checkout concern, not a history change.

### 5. `agent-bridge.py` accepts both installed and source layouts

The interpreter probe was broadened from "can import `src.llm_wiki`" to "can
import either `llm_wiki` (installed by `uv tool install`) or `src.llm_wiki`
(source checkout)". This keeps the bridge usable both for developers in a
checkout and for agents operating against a tool-installed environment.

## Verification performed (2026-07-27)

- `uv build` produces a clean `llm_wiki-1.2.0` sdist + wheel: no
  `__pycache__/` or `.pyc`, templates and `entry_points.txt` present.
- Installed into an isolated venv and into `uv tool` (local dir), then ran
  `llm-wiki init`, `status`, and `lint` in a fresh directory; `find_wiki_root`
  resolves correctly from a subdirectory.
- Real end-to-end: `uv tool install
  git+https://github.com/Nemo4110/llm-wiki.git@feat/uv-tool-install` installed
  the executable and ran `init` + `status` with no manual clone.
- Full pytest suite: 121 passed, 3 skipped.
- Test tool and temp dirs were uninstalled/removed after verification.

## Open items

- **Merge to `main`**: deferred. Until merged, the install command needs the
  branch suffix `@feat/uv-tool-install`; the README's plain
  `git+https://...` form takes effect only after merge.
- Optional: record this distribution choice in `ROADMAP.md` when the branch is
  merged.
