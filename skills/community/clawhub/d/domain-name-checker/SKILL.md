---
name: domain-name-checker
description: "Check domain availability and brainstorm names. Checks .com/.net/.org/.io/.ai/.co/.app/.dev and more. Suggests alternatives when taken. No API key required."
version: 1.0.1
metadata:
  openclaw:
    emoji: "🌐"
  requires:
    bins:
      - python3
  optionalEnv:
    - OPENROUTER_API_KEY
  homepage: https://github.com/eagerbots/domain-name-checker
---

# domain-name-checker

Check domain availability and brainstorm domain names.

## Trigger phrases

- "Is [domain] available?"
- "Check if [name].com is taken"
- "Find me a domain for [idea]"
- "Brainstorm domain names for [project]"
- "What domains are available for [keyword]?"

## How to use

**Skill directory**: The script is at `<skill_dir>/scripts/check.py`.

### Check a specific name across TLDs

When the user asks to check if a domain or name is available, extract the name (without TLD unless they specified one) and run:

```bash
python <skill_dir>/scripts/check.py <name>
```

Examples:
- "Is eagerbots available?" → `python <skill_dir>/scripts/check.py eagerbots`
- "Check openclaw.ai" → `python <skill_dir>/scripts/check.py openclaw.ai`
- "Check eagerbots and clawbay" → `python <skill_dir>/scripts/check.py eagerbots clawbay`

### Brainstorm names from a description

When the user asks to brainstorm domain names or find a domain for an idea/project, run:

```bash
python <skill_dir>/scripts/check.py --brainstorm "<description>"
```

Requires `OPENROUTER_API_KEY` env var. If not set, inform the user and fall back to checking a name they suggest manually.

### Display output

Display the script output as-is — Rich handles the terminal formatting (tables, colors). If running in a non-TTY context, pipe output through `cat` to strip ANSI if needed.

## Notes

- DNS check timeout: 3 seconds per domain
- Unknown = DNS timed out or inconclusive; not necessarily available
- Registration links go to Namecheap search
