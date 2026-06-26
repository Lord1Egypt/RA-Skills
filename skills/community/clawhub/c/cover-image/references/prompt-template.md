# Prompt Template

Use this structure for `prompts/cover.md`:

```markdown
[one-sentence topic]

Create a cover image for an article about: <topic>.
Primary concept: <subject / metaphor / scene>.

Composition type: <type>.
Visual focus: <main visual element>.
Aspect ratio: <aspect>.

Color palette: <palette>.
Rendering style: <rendering>.
Mood: <mood>.
Language: <zh|en|ja|ko>.

Text treatment: <text>.
If text is needed, reserve clean title space and avoid dense tiny text.

Avoid: low contrast clutter, awkward anatomy, unreadable small text, watermarks, distorted hands.
```

Additional rules:

- If the user provides a title, add a line such as `Title to place: "<title>"`, but still emphasize reserved title space.
- If the image contains text, add a line such as `Title language: "<zh|en|ja|ko>"` or an equivalent instruction.
- If reference images exist, describe exactly what should be borrowed from them instead of just saying "see attachment".
- If the content is abstract, prefer `conceptual` or `metaphor`.
