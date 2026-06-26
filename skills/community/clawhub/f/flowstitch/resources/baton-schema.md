# Baton File Schema

The baton file (`.stitch/next-prompt.md`) is the relay mechanism between build loop iterations.
It tells the next agent what page to build.

## Format

```markdown
---
page: <filename-without-extension>
---
<Full Stitch prompt — must include DESIGN SYSTEM block>
```

## Fields

### Frontmatter (YAML)

| Field | Type | Required | Description |
|:---|:---|:---|:---|
| `page` | string | Yes | Output filename without `.html` (e.g., `about`, `contact`) |

### Body (Markdown)

The body is the complete Stitch prompt. Must include:

1. **One-line description** with vibe/atmosphere keywords
2. **DESIGN SYSTEM block** — copied verbatim from `.stitch/DESIGN.md` Section 6
3. **Page Structure** — numbered list of sections with descriptions

## Example

```markdown
---
page: about
---
A warm, artisanal about page telling the story of Oakwood Furniture Co.

**DESIGN SYSTEM (REQUIRED):**
- Platform: Web, Desktop-first
- Theme: Light, minimal, photography-first
- Background: Warm barely-there cream (#FCFAFA)
- Surface: Crisp very light gray (#F5F5F5) for cards
- Primary Accent: Deep muted teal-navy (#294056) for buttons and links
- Text Primary: Charcoal near-black (#2C2C2C) for headlines
- Text Secondary: Soft warm gray (#6B6B6B) for body copy
- Font: Modern sans-serif (Manrope or similar)
- Buttons: Subtly rounded corners (8px), comfortable padding
- Cards: Gently rounded (12px), whisper-soft shadow on hover
- Layout: Centered content, max-width container, generous whitespace

**Page Structure:**
1. **Header:** Navigation with logo, Shop, Collections, About (active), Contact
2. **Hero Section:** "Our Story" headline, warm founder photo, brief mission statement
3. **Craftsmanship Section:** Three columns: materials, process, sustainability
4. **Team Section:** Founder profile cards with photos and bios
5. **Footer:** Links, social icons, copyright
```

## Validation Checklist

Before completing a build loop iteration, verify your baton:

- [ ] `page` frontmatter field exists and is a valid filename (lowercase, no spaces)
- [ ] Body includes the full DESIGN SYSTEM block from `.stitch/DESIGN.md` Section 6
- [ ] Page described is NOT already in `.stitch/SITE.md` sitemap (Section 4)
- [ ] Page structure is specific with numbered sections
- [ ] One-line vibe description is present at the top

## Common Mistakes

- ❌ Missing `page` frontmatter → loop has no filename target
- ❌ Omitting DESIGN SYSTEM block → inconsistent visual language
- ❌ Copying a page already in the sitemap → wasted iteration
- ❌ Vague page structure → poor generation quality
- ❌ Writing the baton AFTER marking task complete → loop breaks
