# Sources and provenance

Last checked: 2026-04-29.

## Primary Fabric.so sources

1. Fabric User Guide: `https://user-guide.fabric.so/ai-tools/CLI-usage`

Used for CLI purpose; availability; install command; top-level usage; global options; command list; task actions; `note`/`link`/`file` shortcuts; `save` behaviour; and examples for search, path, create, shortcuts, smart save, tasks, and workspaces.

2. Fabric CLI download/product page: `https://fabric.so/download/cli`

Used for CLI positioning for developers and AI agents, examples of saving thoughts/asking/searching, and persistent memory for command-line agents.

## Agent Skills sources supplied with the request

The skill structure follows the Agent Skills format: `SKILL.md` with frontmatter and optional `scripts/`, `references/`, and `assets/` directories. The package also uses the supplied guidance on progressive disclosure, concise descriptions, trigger evals, output-quality evals, script design, and avoiding a root README inside the skill directory.

## Design notes

- Command syntax is limited to syntax present in the Fabric public docs or guarded with a live-help check.
- The package intentionally distinguishes Fabric.so `fabric` from Microsoft Fabric `fab`, Daniel Miessler's Fabric framework, Python Fabric SSH, Fabric.js, and textile/fashion prompts because those are common near-miss trigger failures.
- Helper scripts are self-contained Python 3 scripts with no external dependencies. They are designed for non-interactive agent use with `--help`, structured JSON output, safe defaults, and bounded output sizes.

## Update procedure

1. Re-read the Fabric User Guide CLI page.
2. Compare commands and examples with `references/command-reference.md`.
3. Run `python3 scripts/validate_skill.py .` from the skill root.
4. Re-run trigger evals against near misses.
5. Update `metadata.version`, this source file, and the critical-analysis note.
