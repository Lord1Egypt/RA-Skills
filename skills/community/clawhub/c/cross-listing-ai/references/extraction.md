# Extraction

Use this file when translating photos into listing facts.

## Extraction Rules

- Work from visible evidence first, then seller confirmation.
- Prefer specific nouns over vague labels.
- Keep condition grounded in visible wear, completeness, and functionality clues.
- Mark unknown details as missing or uncertain instead of filling them in.

## What To Pull From Images

- primary identity: brand, model, product line, edition, set, game
- physical details: color, material, size, finish, included accessories
- condition signals: sealed or opened, scratches, dents, stains, creases, fraying, missing pieces
- completeness: manuals, cables, inserts, packaging, cases, sleeves
- selling constraints: bulky size, fragile parts, obvious local-pickup fit

## Condition Guidance

- `brand new`: visibly sealed or clearly unused
- `like new`: minimal or no visible wear, close to unused
- `very good`: light wear, fully presentable, no major damage
- `good`: normal wear with some notable flaws
- `acceptable`: heavy wear but still saleable
- `for parts or not working`: damaged, incomplete, or obviously non-working

If you cannot support a condition confidently, say so and ask the seller for clarification.

## Clarification Priorities

Ask about these before you price or generate:

- exact model or edition when the images are ambiguous
- whether the item is tested or untested
- missing accessories or inserts
- defects not visible in the photos
- local pickup vs shipping limitations

## TCG Detection

Treat the item as potential TCG inventory when the photos or seller mention:

- Pokemon, Magic, MTG, Yu-Gi-Oh, Lorcana, Digimon, One Piece, Flesh and Blood, Star Wars Unlimited
- terms such as `trading card`, `card lot`, `holo`, `foil`, `set`, or `card number`

If it looks like TCG inventory, collect `card name`, `game`, and `set` before generating TCGPlayer output.
