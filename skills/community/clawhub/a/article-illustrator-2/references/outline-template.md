# Outline Template

To support automatic Markdown insertion, `outline.md` should follow at least this structure:

```markdown
**Series Reference**: references/series-reference.png
**Series Anchors**:
- <overall palette / brand colors>
- <repeating subject / product / presenter / diagram vocabulary>
- <shared composition rules and annotation style>

## Illustration 1
**Position**: after-heading: Background
**Purpose**: Explain the background and context with a structural diagram
**Visual Content**: A clean framework visual showing the problem source, actors, and goal
**Continuity Anchors**:
- <what must stay visually consistent: palette, device, product, presenter, diagram style, framing>
**Filename**: 01-framework-context.png

## Illustration 2
**Position**: after-heading: Method
**Purpose**: Explain the execution steps with a flow diagram
**Visual Content**: A 3-step process showing input, processing, and output
**Filename**: 02-flowchart-method.png
```

## Supported `Position` Values

- `after-heading: <heading>`: insert after the matching Markdown heading
- `before-heading: <heading>`: insert before the matching Markdown heading
- `after-text: <snippet>`: insert after the first matching text snippet
- `end`: insert at the end of the article

## Recommendations

- Prefer `after-heading` because it is the most stable option.
- The heading text must match the article exactly.
- `Filename` should be just the image filename, not an absolute path.
- `Purpose` or `Visual Content` is used as the image alt text when possible.
- Use `Series Reference` plus `Series Anchors` for global visual consistency across the article.
- Use `Continuity Anchors` when a later illustration must preserve the same subject, device, UI state, product look, or diagram language.
