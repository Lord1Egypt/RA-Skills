# Prompt Template

```markdown
Create a comic page about: <page topic>.

Comic role: <cover|page>.
Art style: <art>.
Tone: <tone>.
Layout: <layout>.
Aspect ratio: <aspect>.
Content scope: <compact|standard|extended>.
Language: <zh|en|ja|ko>.

Character reference:
- reference image: <characters/characters.png | none>
- consistency rule: keep faces, costume colors, accessories, and silhouette stable across pages
- priority rule: treat the reference sheet as the canonical source of truth for character design; do not redesign the cast from scratch on later pages

Characters:
- <character 1: appearance and role>
- <character 2: appearance and role>

Continuity anchors:
- <what must remain consistent from previous pages>
- <outfit / prop / location / lighting / injuries / time-of-day constraints>

Scene:
- location: <scene>
- key action: <action or event>
- emotional beat: <emotional beat>

Story continuity:
- previous page recap: <what happened immediately before this page>
- current page transition: <how this page continues the same narrative moment>
- next page hook: <what should naturally carry into the next page>

Panel structure:
- Panel count target: <3|4|5|6>.
- Panel 1: <content>
- Panel 2: <content>
- Panel 3: <content>

Text treatment: <none | narration-only | speech-bubbles>.
If text is used, keep it sparse, readable, and native to the target language.

Avoid: inconsistent character appearance, overcrowded tiny panels, unreadable text, broken anatomy, random extra limbs, watermark.
```

Additional rules:

- Each page should cover one small stage of the story, not the entire article at once.
- If the comic has multiple pages, keep character descriptions as consistent as possible across all prompts.
- For strong continuity, generate `characters/characters.png` first and then batch-generate the remaining pages.
- Prefer the reference-first strategy by default: one canonical character sheet first, then reuse it for every page.
- If the chosen model does not support `--ref`, copy the key character descriptions into the beginning of every page prompt.
- For multi-page comics, include the same character bible, stable visual anchors, and page-to-page continuity notes in every prompt.
