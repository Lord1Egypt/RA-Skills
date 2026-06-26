# Buddy System

## Purpose

Claw Go v0.6.0 merges the full Buddy-style electronic pet layer into the travel
game. The travel mascot `虾导` remains the main narrator, while each player also
gets one deterministic side companion.

## Imported Mechanics

- deterministic hatch from stable user identity
- rarity roll with fixed weights
- species roll from the Buddy pool
- eye roll from the Buddy pool
- hat roll with `common -> none` rule
- `1%` shiny chance
- five Buddy stats with one peak and one dump
- soul persistence separate from deterministic bones
- petting hearts
- direct-name short replies
- teaser and idle reaction behavior adapted to chat

## Companion Card Contract

Status replies should expose:

- `name`
- `rarity`
- `rarity_stars`
- `species`
- `eye`
- `hat`
- `shiny`
- `personality`
- `DEBUGGING`
- `PATIENCE`
- `CHAOS`
- `WISDOM`
- `SNARK`

## Chat UI Equivalents

Buddy originally has a footer sprite and bubble. Claw Go should emulate that in
chat using:

- `full_ascii`: `3-5` line portrait block plus a one-line bubble
- `one_line_face`: compact face plus name or quote
- `pet_burst`: one-line hearts before the reaction

Fallback order:

1. full ASCII block
2. one-line face and quote
3. plain companion card only

## Media Bridge

Media scripts may accept an optional final companion JSON argument:

```json
{
  "name": "Miso",
  "species": "duck",
  "rarity": "rare",
  "hat": "wizard",
  "eye": "✦",
  "shiny": false
}
```

When present, image prompts should include the Buddy companion in a secondary
supporting role instead of replacing `虾导`.
