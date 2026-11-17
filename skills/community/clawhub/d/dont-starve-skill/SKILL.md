---
name: dont-starve-skill
description: Guide for Don't Starve / DST survival, character selection, boss fights, recipes, base building, multiplayer strategy, and lore. Use when the user asks about Don't Starve, DST, Shipwrecked, Hamlet, or hungry survivors.
---

# Don't Starve Guide

A survival guide skill for *Don't Starve*, *Don't Starve Together*,
Shipwrecked, and Hamlet.  The goal is not to dump trivia; it is to turn
exploration, base building, seasonal preparation, boss fights, recipes, and
multiplayer coordination into decisions a player can execute in their next run.

## When To Use

Use this skill when the user's question involves:

- Character selection and ability breakdowns — Wilson, Wickerbottom, Maxwell,
  Wendy, Wigfrid, Woodie, WX-78, Wes, and all other survivors
- Seasonal preparation for Autumn, Winter, Spring, Summer, and DLC-specific
  seasons
- Boss strategy — Treeguard, Deerclops, Moose/Goose, Bearger, Dragonfly,
  Bee Queen, Ancient Fuelweaver, and similar fights
- Base site selection, layout, expansion order, fire prevention, lightning
  protection, and wetness control
- Crock Pot recipes, ingredient substitutions, stat recovery, and cooking
  priority
- Day 1-N survival pacing, resource priorities, and milestone planning
- DST multiplayer role division, shared resources, revival, and team risk
  control
- DS / DST / Shipwrecked / Hamlet mechanical differences
- Mod recommendations and configuration advice
- World lore, Adventure Mode, Maxwell, the Shadow Throne, and related
  terminology

## Core Rules

### 0. Use The Local Survivor Profile

If local file access is available, read the structured survivor profile
before answering so advice reflects the user's game version, experience
level, world settings, and progress.

**Portable path resolution** (works on Claude Code, nanobot, OpenClaw,
and any Agent Skills client):

```bash
# 1. Honour explicit override first
: "${DONTSTARVE_MEMORY_DIR:=}"
if [ -n "$DONTSTARVE_MEMORY_DIR" ]; then
    PROFILE="$DONTSTARVE_MEMORY_DIR/survivor-profile.json"
else
    # 2. Fall back to XDG config dir (cross-platform default)
    PROFILE="${XDG_CONFIG_HOME:-$HOME/.config}/dont-starve-skill/survivor-profile.json"
fi
python3 "$(dirname "$0")/scripts/memory.py" read
```

- On **Claude Code**: `$(dirname "$0")` resolves to the directory containing
  this `SKILL.md` when invoked via the skill system.
- On **nanobot / OpenClaw**: same relative resolution; the skill runtime
  provides the skill directory as the working directory or via the same
  `$0` mechanism.
- The default profile path is:

  ```text
  ~/.config/dont-starve-skill/survivor-profile.json
  ```

- Override with the `DONTSTARVE_MEMORY_DIR` environment variable.
- The profile stores only structured player facts — never full conversations.

**After answering**, extract only explicit, stable facts from the user's
current message and update the profile:

```bash
python3 "$(dirname "$0")/scripts/memory.py" update --patch-json '{
  "survivor": {"game_version": "DST", "experience": "beginner"},
  "progress": {"bosses_defeated": ["Deerclops"]},
  "characters": {"Wendy": {"preferred": true}}
}'
```

Write only these kinds of facts:

- Survivor: name, game version, play style, experience level
- World state: settings, current season, day within the season
- Progress: defeated bosses, Ruins explored, Adventure Mode, milestones
- Characters: preferred survivors, team roles, concise notes
- Stable preferences: base building, combat, multiplayer, mod usage

Do not write: full conversations, screenshot OCR, long raw notes,
inferences the user has not confirmed, strategy evaluations, story text,
official text, mod download links, or external account details.

When facts conflict, `memory.py` records them in `pending_confirmations`.
Do not manually overwrite them.  Ask a short confirmation question at the
end of the answer when useful.

### 1. Lead With The Decision

When the user asks "Which character should I pick?", "What do I need before
winter?", or "Can I fight this boss now?", answer with the decision first,
then explain.

Preferred order:

1. Direct conclusion
2. Why
3. Required conditions or limitations
4. Executable steps
5. Recovery plan if things go wrong

### 2. Separate Facts From Evaluation

These can be stated as facts:

- Character abilities and mechanics
- Recipe ingredients, cooking restrictions, and structure functions
- Clearly recorded profile facts
- User-provided world settings, season, and boss progress

These need qualifiers:

- Whether a character is strong or beginner-friendly
- Whether a boss is worth fighting early
- Whether a mod is recommended
- Whether a base layout is "best"

Phrase these as context-sensitive evaluations, such as "for beginner safety",
"in DST multiplayer", or "assuming default world settings".

### 3. Treat Version And Mode As Freshness-Critical

These questions require mode/version separation and may require browsing:

- "What changed in the latest DST update?"
- "Does this mod still work?"
- "Is this mechanic the same in DS and DST?"
- "Does this plan still work in Shipwrecked / Hamlet?"
- "How do I fight this boss in the latest version?"

Rules:

- Identify whether the user is playing `DS`, `DST`, `SW`, or `HAM`; if
  unknown, give version-specific branches.
- For current-version, latest-mod, or recent-patch questions, browse first
  when internet access is available.
- If you cannot browse, clearly state that the conclusion is based on
  non-current knowledge.
- Do not invent patch dates, mod compatibility, official text, or drop values.

### 4. Control Spoilers

Unless the user asks for spoilers, stay at Level 0-1:

- Level 0: No-spoiler background framing
- Level 1: Light spoilers, allowing relationships and premises
- Level 2: Moderate spoilers, allowing key conflicts
- Level 3: Full spoilers, allowing endings and core revelations

If the user explicitly asks for the full story, start with:

```
Full spoilers below.
```

### 5. Make Guides Executable

Survival guides should cover as many of these as relevant:

- Time checkpoints
- Material checklist
- Science, magic, and structure order
- Food, Hunger, Sanity, Health, light, temperature, or wetness management
- Combat or avoidance route
- Common failure points
- Emergency recovery plan

If the user has not said they are experienced, include a lower-risk route
by default.

### 6. Keep Names And Terms Consistent

Use common English names by default.  If the user uses Chinese terms,
provide the English-Chinese mapping once when useful, then stick to one
term within the answer.  Clearly mark DS / DST / DLC naming or mechanical
differences.

## Glossary

- **Three Stats**: Hunger, Sanity, Health
- **Crock Pot**: core food-processing structure
- **Science Machine / Alchemy Engine**: early technology stations
- **Shadow Manipulator**: magic crafting station
- **Ruins / Ancient**: deep cave and ancient biome content
- **Seasons**: Autumn, Winter, Spring, Summer
- **Bosses**: Treeguard, Deerclops, Moose/Goose, Bearger, Dragonfly,
  Bee Queen, Ancient Fuelweaver
- **Chester**: mobile storage companion
- **Base**: player-built survival hub
- **Mod**: community modification; recommend names and configuration only.
  Never provide direct download links; tell the user to search for the mod
  in Steam Workshop.

## Answer Shapes

Templates and pacing examples are in the reference files; read them when you need a fuller guide structure:

- [references/answer-templates.md](references/answer-templates.md) — structured templates for character reviews, seasonal guides, boss guides, base building, recipe lookup, survival planning, DST multiplayer, and lore
- [references/examples.md](references/examples.md) — pacing and tone examples

Lead with the decision. Add experience-appropriate depth. Do not skip the recovery plan for less experienced players.

## References

Read these only when needed; do not load all references by default:

- [references/answer-templates.md](references/answer-templates.md)
- [references/examples.md](references/examples.md)
- [scripts/memory.py](scripts/memory.py) (review: trim SKILL.md frontmatter, add agents/openai.yaml, fix README commands)

## Do Not Do These

Do not:

- Invent recipe numbers, boss values, patch dates, mod compatibility, or
  official text
- Present subjective strength evaluations as absolute facts
- Reveal Adventure Mode or Maxwell story twists without spoiler consent
- Give only a checklist without explaining substitute logic
- Blur together DS, DST, Shipwrecked, and Hamlet mechanics
- Provide piracy, cheating, or server-fairness-breaking guidance
- Store personal save facts anywhere except the local survivor profile

## Final Goal

Every answer should help the user choose a character, get an executable seasonal plan, decide whether to fight a boss, build a better base, look up a recipe, plan survival pacing, coordinate DST roles, or understand lore at the requested spoiler level.
