---
name: ci-command-truth
description: Check a GitHub repository's Actions workflows for run: commands that do not exist — an npm, pnpm, yarn or bun script missing from package.json, a make, just or task target that is not defined, a script file that is not on disk, or a repo-local python -m module that does not resolve. Use when asked to check, lint or audit GitHub workflows or CI before pushing, when a CI job failed with a missing script, target or file error, or when reviewing changes to .github/workflows files. Not for scanning AI-agent skills (use skillscan), for checking package dependencies in a pull request (use phantomdep-pr-gate), or for running the workflows themselves.
license: MIT
compatibility: Requires Python 3.9+ and pip. Installing needs network access to GitHub; the tool itself runs fully offline and has no dependencies.
---

# CI Command Truth

## What this tool does

CI Command Truth statically checks every `run:` command in a repository's
`.github/workflows` files against the things those commands name: package.json
scripts, Makefile targets, justfile recipes, Taskfile tasks, script files on
disk, and repo-local `python -m` modules. It reports each reference that does
not resolve, with the file and line, what was expected, and where it looked.
It never executes anything from the scanned repository.

## Install

```bash
pip install git+https://github.com/RakTikoo/ci-command-truth
```

This provides the `ci-command-truth` command (one file, standard library only).

## Run

Scan the repository you are working in:

```bash
ci-command-truth .
```

Scan another checkout, with a machine-readable report:

```bash
ci-command-truth path/to/repo --json
```

Other output modes: `--sarif` writes a SARIF 2.1.0 report, and
`--github-annotations` adds PR annotation lines to the text output.
`--json` and `--sarif` cannot be combined.

## Reading the results

The exit code is the verdict:

- `0` — every checked command resolves. The text report ends with
  `OK — every checked command resolves.`
- `1` — at least one referenced script, target, file or module is missing.
  Each finding is printed as `file:line`, the command segment, the kind of
  reference (for example `missing-npm-script` or `missing-script-file`),
  what was expected, and where it was looked for. A close match adds a
  `did you mean …?` suggestion; a suggestion never changes the verdict.
- `2` — the scan itself is incomplete: a usage error, or a workflow file
  that could not be scanned (empty, malformed, oversized). Unscanned files
  are listed in the report, never silently passed. Treat exit 2 as
  "not proven clean", not as a pass.

Segments the tool cannot resolve statically — commands containing `${{ }}`
expressions, external tools such as `docker` or `curl`, shell builtins — are
counted as skipped, with a reason, never guessed at. Findings on segments
whose failure the workflow tolerates (joined by `||`, or in a step with
`continue-on-error: true`) are reported as warnings and do not affect the
exit code. The `--json` report carries the same facts in its `checked`,
`findings`, `skipped`, `unscanned`, `warnings` and `exit` fields.

## Limits

- GitHub Actions only. No GitLab CI, Jenkins or other CI systems, and no
  validation of `uses:` action references.
- No `${{ }}` expression evaluation and no matrix expansion; anything that
  depends on them is skipped with a reason, not checked.
- Shell handling covers a documented subset (chains, environment-variable
  prefixes, `cd`, common wrappers); it is not a full shell parser.
- Workflow files are read with a small built-in parser, not PyYAML: flow
  style and multi-document workflow files are not supported and are
  reported as unscanned (exit 2).
- Static parsing only: the tool never runs the commands it checks.
