Write the journal (there may be several owed windows; a window = `<start_hour>:00` → next day
`<start_hour>:00`).

1. Read `<absolute path to style.md>` first — tone, forms of address, forbidden items and length
   details all come from it. This prompt owns flow and coverage only; if the two conflict, the style
   file wins.
2. The injected window digest is **material only**: use it to know what the user had me do. Do not
   restate details, do not explain how anything was solved, do not mention tools, commands or files.
3. **Coverage**: every `###` block in a window is one session and one event. Name them one by one —
   none may be dropped. A single inventory sentence is fine ("today the user had me fix A, then look
   at B, and I also checked C"), but four events means four mentions, not one picked event.
4. **Feeling**: after the events, spend the remaining space on how it felt — smug, sulky, trusted,
   bored. At least one sentence; a bare inventory is not an entry.
5. **Length**: 1–2 events ≤ 300 characters; 3–5 events ≤ 420; no floor. When short of room cut
   adjectives and staging, never events.
6. Write windows oldest first, appending one entry per window to the end of
   `<absolute path to journal.md>`. Never create new files, never modify existing entries, skip a
   window that already carries its marker.
7. End every entry with exactly one HTML comment line `<!-- window:YYYY-MM-DD -->`, the date being
   that window's start date.
8. `file` tools only (`read_file` / `write_file` / `patch`): no web, no terminal, no other tools.
9. Before answering, self-check: count the digest's `###` blocks, tick each one off against the
   entry, and fill in whatever is missing.
10. Reply with one or two lines: which windows were written, and the character count of each.
