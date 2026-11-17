# Note Types — Fields, Templates, And Styling

A **note** holds fields; a **card** is one rendering of that note through a template. One note can produce several cards; editing the note changes every card it produces. Every "why did my card disappear / duplicate / show blank" question resolves inside this model.

## The Model In Four Lines

- Note type = field list + card templates + CSS. It is shared by every note using it; editing it edits all of them.
- Card templates decide how many cards a note generates. Adding a template to a note type generates a new card for every existing note (with a fresh review history).
- **Deleting a field or a template deletes its content and its cards' review history, permanently.** Backup first, and expect a one-way sync afterwards.
- A card whose front side renders empty is not generated. That is a feature — it powers optional cards (below), not a bug.

## Field Design

| Field | Purpose | Notes |
|---|---|---|
| Front / Text | The question or the cloze sentence | Must be the sort field on most types; duplicate detection uses field 1 only |
| Back / Extra | The answer, or the cloze note's context | Extra is shown on every cloze card of the note — put shared context here, never a second fact |
| Source | Chapter, page, URL | Lets you repair a card years later; keep it off the question side |
| Hint | Optional cue shown on demand | Rendered with `{{hint:Hint}}` — collapsed until clicked |
| Mnemonic / Notes | Memory hook and personal commentary | Answer side only |
| Tags | Not a field | Tags live on the note, outside the field list |

Renaming a field is safe and rewrites templates automatically. Reordering is safe. Deleting is not. Add fields freely — an empty field costs nothing and a missing one costs a re-import.

## Template Syntax Worth Knowing

```html
{{Front}}                     <!-- field substitution -->
{{FrontSide}}                 <!-- on the back: reprints the question, so you see what you answered -->
{{type:Back}}                 <!-- typing box; shows a red/green diff after answering -->
{{hint:Hint}}                 <!-- click-to-reveal cue -->
{{cloze:Text}}                <!-- required on cloze note types, on BOTH sides -->
{{text:Front}}                <!-- strips HTML — useful when a field carries pasted formatting -->
{{#Reverse}} … {{/Reverse}}   <!-- render only if the field is non-empty -->
{{^Reverse}} … {{/Reverse}}   <!-- render only if the field IS empty -->
```

- **Optional reverse card**: put `{{#Reverse}}{{Back}}{{/Reverse}}` as the second template's front. Fill the `Reverse` field only on the vocabulary that deserves a production card, and the reverse cards exist only for those notes.
- `{{type:…}}` compares literally: accents, capitalization and trailing spaces count. That is the point for spelling, and a nuisance for prose — use it on short exact answers only.
- Cloze templates cannot be mixed with regular templates on the same note type; a cloze note type has exactly one template.

## Styling That Matters

```css
.card { font-size: 22px; text-align: center; }         /* one place, all clients */
.cloze { font-weight: bold; color: #2b6cb0; }
.nightMode .cloze { color: #7fb3ff; }                   /* dark mode needs its own contrast */
img { max-width: 100%; height: auto; }                  /* stops phone-breaking images */
```

- Styling is per note type and syncs to every device. Per-card colour lives in the field content as HTML, not in the CSS.
- Test on the smallest screen you study on: a table that fits a desktop card becomes a horizontal scroll on a phone, and cards you cannot read on the bus stop getting reviewed.
- Night mode is not automatic for hard-coded colours. Every custom colour needs a `.nightMode` counterpart or it will be unreadable half the time.
- Fonts referenced in CSS must exist on each device; ship the font as `_font.ttf` in the media folder (files starting with `_` are never deleted by Check Media) or fall back to a system stack.

## Math And Code On Cards

- MathJax delimiters (`\(…\)` inline, `\[…\]` display) render client-side and stay editable; LaTeX image generation needs a local LaTeX install and breaks sync of the generated images across devices. Default to MathJax.
- Code blocks: wrap in `<pre><code>` and set `white-space: pre-wrap` in the CSS, or every snippet becomes one line. Syntax highlighting requires an add-on at edit time but stores plain HTML, so it survives on mobile.

## Changing Note Types Safely

1. Export the affected notes (Notes → Export, include scheduling) before touching anything.
2. Browse → select notes → Change Note Type, then map fields explicitly. Any field mapped to "Nothing" is discarded with no warning.
3. Card templates map too: mapping a template to "Nothing" deletes those cards and their history.
4. After the change, Tools → Empty Cards to clear cards whose front no longer renders. Read the list before confirming — an unexpectedly long list means a mapping was wrong.
5. The next sync after a note-type change is often a full upload; do it from the device holding the truth.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Editing the shipped Basic type to fit one deck | Every deck using Basic changes with it | Clone it (Tools → Manage Note Types → Add: clone) and edit the clone |
| Deleting a field to "clean up" | Content and history are gone, unrecoverable outside a backup | Empty the field, or hide it in the template |
| Putting a second fact in Extra on a cloze note | Extra shows on every sibling card, leaking the answer | New note |
| Using `{{type:…}}` on long answers | Punctuation mismatches fail cards you actually knew | Reserve typing for short exact strings |
| Hard-coded white background | Unreadable in night mode on the phone | Use `.nightMode` rules |
| Ten near-identical note types | Every template fix must be repeated ten times | One type with optional fields and conditional templates |
