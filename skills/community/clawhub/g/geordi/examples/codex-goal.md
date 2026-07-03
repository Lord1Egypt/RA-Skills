# Example Codex goal

Goal: Add a small CSV export path to an existing reports page.

Install and run:

```bash
geordi init --goal "Add CSV export to reports" --mode codex
geordi mission add "Implement CSV export helper and button" --accept "npm test" --scope "Reports page and export helper only."
geordi run --mode codex
```

If your shared agent rules live outside the default `~/.agents/AGENTS.md` path:

```bash
GEORDI_AGENTS_FILE=/path/to/AGENTS.md geordi run --mode codex
```
