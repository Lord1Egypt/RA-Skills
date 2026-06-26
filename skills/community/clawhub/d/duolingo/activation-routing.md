# AGENTS Routing Rules

Use this file when the user explicitly wants AGENTS auto-routing.
If not requested, keep duolingo manual and user-invocable.

## Router Block Template

Provide this block for the user to paste into AGENTS:

```markdown
## Duolingo Router

When user asks to learn, practice, quiz, review, or improve any topic listed in `~/duolingo/router/topics.md`, activate `duolingo`.

Examples:
- "help me learn english"
- "practice cooking fundamentals"
- "quiz me on finance terms"

If multiple topics match, ask which track to run now and keep other tracks queued.
```

## Topic Registration Format

Store in `~/duolingo/router/topics.md`:

```markdown
- topic: english
  triggers: english, grammar, vocabulary, speaking

- topic: cooking
  triggers: cooking, recipes, kitchen skills, food prep
```

## Sync Rules

- If a topic is added or removed, update both `topics.md` and AGENTS router block.
- Keep one router block only; avoid duplicates in AGENTS.
- Router changes must not overwrite unrelated AGENTS rules.
- Never auto-write AGENTS from this skill.
