# Portability Notes

This skill package is authored for ClawHub/OpenClaw packaging flow first.

## Porting to other systems

### ChatGPT custom GPT / instruction use
- Use the operating rules from `SKILL.md`.
- Preserve the mode-selection rules.
- Preserve the exact output contract: plugin zip separate from critique file.
- Keep the default fallback to minimal native tool plugin generation.

### Claude or other markdown-based skill systems
- Reduce frontmatter to only the fields that platform accepts.
- Keep the body instructions focused on plugin-mode selection, minimum publishable contract, and separate critique output.
- If the platform does not support multi-file skills, collapse the essential rules into one markdown file and treat `templates/` and `examples/` as reference material outside the upload.

## Important boundary

Portability changes should adapt **container format**, not the core logic.

The core logic to preserve is:
- explicit plugin modes
- bounded inference
- minimum publishable contract
- separate critique file
- conservative default to native tool plugin
