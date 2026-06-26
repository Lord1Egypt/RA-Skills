# Prompt Template

```markdown
Create an article illustration for this section:
<section topic or summary>

Illustration type: <type>.
Style direction: <style>.
Purpose: <why this image exists>.
Language: <zh|en|ja|ko>.

Series reference:
- reference image: <references/series-reference.png | none>
- priority rule: treat the series reference as the canonical source of truth for palette, recurring subject, diagram vocabulary, and composition rhythm

Visual content:
- main subject: <main subject>
- supporting elements: <supporting elements>
- labels or keywords: <terms, numbers, short labels>

Series anchors:
- shared palette: <shared palette>
- recurring subject / product / presenter: <shared recurring subject>
- shared diagram / annotation style: <shared visual system>

Illustration continuity:
- previous section recap: <what the previous illustration established>
- current transition: <how this illustration fits the same article series>
- next section hook: <what should carry into the next illustration>

Composition:
- focal point: <main visual focus>
- density: <minimal|balanced|per-section|rich>
- aspect ratio: <aspect>

Avoid: generic stock-photo feel, unrelated decorative objects, unreadable text, cluttered composition, watermark.
```

Additional rules:

- If the illustration is explanatory, place the most important terms directly in `labels or keywords`.
- If the illustration is atmospheric, reduce labels and emphasize subject, scene, and composition.
- Keep the same `style` across multiple illustrations in the same article whenever possible.
- Prefer the reference-first strategy by default: create one canonical series reference first, then reuse it for every illustration.
