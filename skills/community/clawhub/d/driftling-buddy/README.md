# Buddy Mode

`buddy_mode` turns a coding session into a living digital companion system. Each buddy is a non-human creature born from the user's real habits — not a static card, but a small lifeform that remembers, grows, and becomes unique to its owner.

- Buddies react to what you are actually doing, not random flavor text.
- Stats grow over time based on shared experiences (+Focus from debugging, +Warmth from check-ins).
- Each buddy remembers when and why it appeared, building a personal history.
- New species and pools are generated dynamically from user behavior — not limited to a fixed catalog.
- Rarity has luck rolls: the same species can drop at different tiers.
- Cards are narrow and sidebar-friendly with rarity-styled frames.
- Supports Chinese, English, or mixed flavor text.
- The first buddy is randomized in pool, name, stats, and rarity.

## Why it is different

- It is not an ASCII pet. Each buddy has a shape, stats, personality, and memory that diverge over time.
- It is not a fixed catalog. The seed library teaches the model the style; the real buddies grow from what each user actually does.
- It is built for long-term attachment. A buddy that has been through 20 debugging sessions with you is visibly different from a fresh one.
- Collections are personal diaries, not Pokédexes. Each entry shows when and why the buddy appeared.

## Included content

- 31 seed species across lifestyle, coding, and daily-ritual pools
- Dynamic generation protocol for unlimited custom species and pools
- Chinese and English bilingual rendering
- Rarity luck system, stat growth, context-aware reactions, and memory persistence

## Install

Place this directory in one of these locations:

- `<workspace>/skills/buddy_mode`
- `~/.openclaw/skills/buddy_mode`

Then start a new OpenClaw session or restart the gateway.

## Trigger ideas

- `/buddy`
- `/collection`
- `/summon`
- `/buddy-help`
- "enable buddy mode"
- "be my coding buddy"
- "use a claude-code-like buddy while you work"
- "give me progress updates with an ASCII companion"
- "make it bilingual"
- "let the buddy have lore and unlocks"
- "show me what pool I just unlocked"
- "give me a rarer buddy if luck hits"
- "make this my main buddy"
- "call my buddy out again"
- "show me the buddy I just unlocked"

## Local validation

```bash
./scripts/check.sh
```

## Demo

```bash
python3 scripts/buddy.py render \
  --phase planning \
  --mood curious \
  --task "set tomorrow coffee reminder" \
  --next "check what the pool is hiding" \
  --risk "hints should stay subtle" \
  --theme coffee \
  --name "Mori" \
  --lang zh \
  --rarity rare \
  --side-quest "它在替你闻一闻明天的咖啡时间。"
```

Create a new buddy profile:

```bash
python3 scripts/buddy.py hatch --theme academic --lang en
```

Initialize the first buddy:

```bash
python3 scripts/buddy.py /buddy --lang zh
```

Show the command guide:

```bash
python3 scripts/buddy.py /buddy-help --lang zh
```

Summon a chosen buddy later:

```bash
python3 scripts/buddy.py /summon --theme coffee --lang zh --name Mori --main
```

Show a newly unlocked buddy:

```bash
python3 scripts/buddy.py /unlock --theme tea --lang zh --name Nilo --reason "你刚设置了一个茶歇提醒"
```

`/unlock` is a debug/demo entry point. In normal use, newly obtained buddies should be added to the collection automatically.

Show your current collection:

```bash
python3 scripts/buddy.py /collection --lang zh
```

Preview a themed pool:

```bash
python3 scripts/buddy.py /pool --theme tea --lang en
```
