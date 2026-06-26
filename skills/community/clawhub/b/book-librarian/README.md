# Book Librarian Skill for OpenClaw

A personal reading companion that manages your book library, wishlist, and recommends what to read next based on your mood and taste.

## What It Does

- **Track your books** — Separate library (owned) and wishlist (wanted) with CSV-based storage
- **Smart recommendations** — Always suggests unread books you already own first, then wishlist, then new discoveries
- **Mood-based picks** — Match your current mood to your reading profile for tailored suggestions
- **No spoilers** — Hooks and premises only, never plot reveals
- **Taste learning** — Tracks your reactions to refine future recommendations

## File Structure

```
books/
├── books_library.csv    # Owned books (Read: Y/blank, Title, Author)
└── books_wishlist.csv   # Wanted books (Title, Author)

memory/
└── library.md           # Taste profile, mood map, reading notes
```

## How to Use

Add this skill to your OpenClaw workspace, then simply ask:

- *"What should I read next?"*
- *"Recommend a horror book"*
- *"I just finished Dune"* → marks as read + logs your thoughts
- *"Add The Hobbit to my wishlist"*
- *"I bought The Martian"* → moves from wishlist to library

## Recommendation Logic

```
Library (unread) → Wishlist → New discoveries
```

The skill always checks what you already own before suggesting new purchases. This keeps your unread pile from growing while your wishlist shrinks.

## Setup

1. Copy the skill files to `~/.openclaw/workspace/skills/book-librarian/`
2. The skill will **ask before creating anything** — no files are created without permission
3. On first use, it creates `books/` directory, CSVs, and `memory/library.md` from the included template
4. Optionally fill in your taste profile and mood map during setup, or let it learn over time

## Template Files

- `templates/library.md` — starter template for new users. Copied to `memory/library.md` on first setup. Keeps the SKILL.md context smaller.

## Example Taste Profile (library.md)

```markdown
## Taste Profile
- Fiction: 80%, Non-fiction: 20%
- Preferred genres: horror, sci-fi, literary fiction
- Avoids: romance, self-help

## Mood Map
- stressed → comfort horror (King, atmospheric)
- curious → hard sci-fi (Le Guin, Clarke)
- nostalgic → classics (Dickens, Austen)
- adventurous → epic fantasy (Tolkien, Sanderson)
```

## License

Apache License 2.0
