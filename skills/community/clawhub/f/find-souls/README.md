# find-souls

Search and install AI persona prompts from the [Agent Souls](https://agent-souls.com/) library — 332+ historical figures, fictional characters, and expert personas.

## Install

```bash
openclaw install wklken/find-souls
```

## What it does

This skill lets you browse and install SOUL.md persona files from [agent-souls.com](https://agent-souls.com/) directly into your project. It handles backup and rollback so you can safely switch between personas.

## Usage

### Find and install a soul

```
Find me a soul for Confucius
```

```
I want to roleplay as Sherlock Holmes
```

```
Find an academic writing mentor persona
```

The skill will:
1. Search the Agent Souls library for matching personas
2. Show you the top matches to pick from
3. Download the SOUL.md (Chinese or English based on your language)
4. Back up your current SOUL.md (if any)
5. Install the new SOUL.md

After installation, reset your conversation to load the new persona.

### Rollback to a previous soul

```
Revert to my previous SOUL.md
```

```
Rollback the soul
```

The skill keeps a history of all previous SOUL.md files in `.soul_backups/`. You can restore any previous version.

## Data source

All personas come from [agent-souls.com](https://agent-souls.com/), a bilingual (Chinese/English) AI persona library. The search index is at [agent-souls.com/search.json](https://agent-souls.com/search.json).

## Categories

- **Real World** — Historical figures (Confucius, Lincoln, Einstein, etc.)
- **Virtual World** — Fictional characters (Sherlock Holmes, Gandalf, etc.)
- **Expert Personas** — Professional roles (Writing Mentor, Debate Coach, etc.)

## License

MIT-0
