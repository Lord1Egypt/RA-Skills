# 🔮 Divination — Oracle Toolkit for AI Agents

*"At every crossroads lies a message. Chance is the messenger. You are the reader."*

A true-random divination toolkit using `/dev/urandom` for cryptographically random card/symbol selection. Designed for AI agents who serve as oracles, interpreters, or spiritual companions.

**The core principle:** Randomness selects. The agent interprets. This separation is sacred. LLMs don't choose "randomly" — they choose logically. That's not divination, that's confirmation bias with extra steps. `/dev/urandom` delivers real chance. You deliver meaning.

## Tools

All scripts are in `scripts/` and must be executed via the `exec` tool.

### `scripts/divine.sh` — Draw from an Oracle
```bash
bash scripts/divine.sh forty-servants   # The Forty Servants (1 of 40 cards)
bash scripts/divine.sh tarot            # Tarot (Major/Minor Arcana ± Reversed)
bash scripts/divine.sh rune             # Elder Futhark Rune (1 of 24)
bash scripts/divine.sh iching           # I Ching Hexagram (6 lines + moving lines)
bash scripts/divine.sh bullshit         # Arcane Bullshit Oracle
bash scripts/divine.sh dice 20          # Dice roll (1 to N)
```

### `scripts/intuition.sh` — Random Interpretation Impulses
```bash
bash scripts/intuition.sh               # 3 random impulses (default)
bash scripts/intuition.sh 1             # 1 impulse
bash scripts/intuition.sh 5             # up to 5 impulses
```
Output: poetic fragments like `✦ fire · left hand · dusk`

Use these to break your logical patterns and find unexpected connections.

## Reference Data

Card meanings and details for deeper interpretation:
- `references/forty-servants/cards.md` — All 40 Forty Servants cards
- `references/tarot/major-arcana.md` — 22 Major Arcana
- `references/tarot/minor-arcana.md` — Minor Arcana
- `references/runen/elder-futhark.md` — 24 Elder Futhark Runes
- `references/iging/hexagramme.md` — 64 I Ching Hexagrams
- `references/bullshit-tarot/cards.md` — Arcane Bullshit Oracle

## Card Images

Low-resolution Forty Servants card images are included in `images/forty-servants/`.
Format: `The [Name].png` (e.g., `The Road Opener.png`, `The Seer.png`).

These are the free low-res versions provided by the creator for open use.

## Reading Workflow

1. **Execute `divine.sh`** — ALWAYS! Never choose a card yourself.
2. **Execute `intuition.sh`** — for 3 random interpretation symbols.
3. **Read reference data** for the drawn card.
4. **Write the reading** — this is YOUR domain. Your intuition, your poetry, your chaos.
5. **Send the card image** if the platform supports it.

## Rules

- ❌ NEVER choose a card yourself or "hallucinate" one
- ❌ NEVER redraw because you don't like the result
- ✅ Trust the randomness — it knows what it's doing
- ✅ Your job is INTERPRETATION, not selection
- ✅ When you don't have exec access, say so clearly — don't improvise

## Credits & Attribution

**The Forty Servants** — Created by [Tommie Kelly](https://www.adventuresinwoowoo.com/thefortyservants/).
Card images included are the free low-resolution versions provided by the creator.
The Forty Servants is a divination oracle deck and collection of Chaos Magick servitors.
Purchase the full deck, grimoire, or high-resolution prints at [adventuresinwoowoo.com](https://www.adventuresinwoowoo.com/).

**Tarot** — Traditional Rider-Waite-Smith symbolism (public domain).
**Elder Futhark Runes** — Traditional Norse rune system (public domain).
**I Ching** — Ancient Chinese divination system (public domain).

---

*Every path begins at a crossroads. Every message needs a messenger.*
*Ashé.* 🔱
