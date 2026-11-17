# Importing And Exporting — Getting Cards In Without Breaking Anything

An import is one irreversible action against the whole collection. Two minutes of header discipline prevents an hour of Browse cleanup.

## Text Import (CSV / TSV)

Put the directives at the top of the file and Anki configures the import itself:

```
#separator:tab
#html:true
#notetype:Basic
#deck:Spanish::Vocabulary
#tags column:3
#columns:Front	Back	Tags
```

| Directive | Why it matters |
|---|---|
| `#separator:tab` | Tab survives commas, semicolons and European decimals in your content |
| `#html:true` | Required for `<br>`, `<b>`, images; without it your markup shows as literal text |
| `#notetype:` | Wrong note type = wrong field count = truncated or merged fields |
| `#deck:` | Missing it drops everything into whatever deck was last used — usually `Default` |
| `#tags column:N` | Otherwise the tag column becomes a field |
| `#columns:` | Names the columns so the mapping dialog is pre-filled |

Rules that decide whether the import lands clean:

- A **tab inside a field** ends the field. Strip tabs from source text before writing the file.
- A **raw newline ends the record**. Multi-line answers need `#html:true` plus `<br>`, or the whole field quoted in a CSV dialect Anki understands.
- **Duplicate handling** is chosen in the dialog: *Update existing notes* matches on the FIRST field only and overwrites your edits with no warning; *Preserve existing* skips; *Duplicate* imports anyway. Pick deliberately — the default is the one that overwrites.
- Cloze notes need `#notetype:Cloze` and real `{{c1::…}}` markers; a cloze note with no marker imports as a note that generates **zero cards**.
- Import creates notes, not scheduling: everything arrives as new cards at the end of the new queue. Use Reposition if the order matters.

## Shared Decks And .apkg

- `.apkg` = notes, cards, note types, media, optionally scheduling. Importing one **adds** to your collection; it never replaces it.
- Note types are matched by internal ID: a shared deck usually brings its own copies, so expect new entries in Manage Note Types. Do not "clean them up" until you have confirmed no notes use them.
- Scheduling included in a shared deck is the author's, not yours. For a downloaded study deck this is noise — most are published without it, and if intervals arrive, `Forget` the imported cards to start clean.
- Import first into a scratch profile when the deck is large or unknown, look at it, then import into the real collection.
- Big shared decks arrive fully unsuspended. Suspend everything, then unsuspend by topic tag as you cover material — this single step prevents the classic day-three burnout.

## .colpkg — Different Animal

`.colpkg` is the **whole collection**. Importing one REPLACES your current collection, including decks not in the file. It is a backup/restore format, not a sharing format. Never accept a `.colpkg` from someone else unless you intend to abandon your own collection.

## Migrating From Other Apps

| From | Path | Watch for |
|---|---|---|
| Quizlet | Export as text with custom separators → TSV with the header block above | Rows with images lose them; term/definition ordering may need swapping |
| Memrise | Course export (add-on or manual copy) → TSV | Audio references do not transfer; re-add via `audio_source` |
| SuperMemo | Export to text; scheduling does not translate | Item structure is finer-grained than Anki notes; expect manual splitting |
| Excel / Sheets | Save as UTF-8 TSV, not CSV | Autocorrect, smart quotes, and locale decimal commas corrupt content with no warning |
| Notion / Obsidian | Export markdown, convert Q/A pairs | Markdown emphasis needs converting to HTML with `#html:true` |
| Another Anki profile | `.apkg` with scheduling included | Duplicate note types multiply; merge them after |

Universal step: import 10 rows first, inspect them in Browse, then import the rest.

## Media

- Media lives in the profile's `collection.media` folder, flat, no subfolders. Fields reference bare filenames: `<img src="diagram.png">`, `[sound:word.mp3]`.
- Files copied into that folder are not linked to anything until a field references them. Tools → Check Media lists unused files and missing references — run it after a bulk import.
- Filenames starting with `_` are never treated as unused (that is how fonts and shared assets survive Check Media).
- Media does not travel in a plain `.apkg` export unless "include media" is checked, and never travels in a text export.

## Exporting

| Export | Contains | Use |
|---|---|---|
| `.apkg`, scheduling excluded | Notes, cards, note types, optionally media | Sharing a deck |
| `.apkg`, scheduling included | The above plus intervals and history | Moving your own cards between your profiles |
| `.colpkg` | Everything, including all decks and settings | Your backup before any destructive operation |
| Notes in Plain Text | Field text only | Dedupe checks, spellchecking, review outside Anki |

Export the affected selection before every irreversible operation: Change Note Type, field deletion, Forget on many cards, bulk delete. It takes seconds and is the only undo that survives a restart.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| CSV with commas in the content | Fields split at the wrong places, with no warning | Tab-separated, always |
| Importing without `#deck:` | Cards land in the last-used deck; often `Default` | Always emit the header block |
| "Update existing notes" on a re-import | Overwrites hand-edited notes matching field 1 | Preserve existing, or verify the key first |
| Importing a `.colpkg` from a friend | Replaces your entire collection | Ask for `.apkg` |
| Fixing an import by re-importing | Doubles the damage | Delete by `added:1` and start over |
| Trusting a smart-quote-laden spreadsheet | Typographic characters break `{{type:…}}` matching and search | Export UTF-8, normalize quotes before import |
