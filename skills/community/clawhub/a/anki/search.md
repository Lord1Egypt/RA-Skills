# Search — Finding, Filtering, And Bulk-Editing Cards

Browse's search bar is the collection's query language. Every bulk fix in this skill — rewriting leeches, resetting ease, unsuspending a lecture, building an exam deck — starts with a search that selects exactly the right cards.

## Syntax Core

| Query | Selects |
|---|---|
| `deck:Spanish` | That deck and its subdecks |
| `deck:Spanish -deck:Spanish::Verbs` | The deck minus one subdeck |
| `"deck:Med School"` | Deck names with spaces — quote the whole term |
| `tag:content::cardio::*` | A tag branch, including children |
| `-tag:*` | Notes with no tags at all |
| `note:Basic` / `card:2` | By note type / by template ordinal (the reverse card) |
| `front:*ACE*` | Substring inside a named field (`field:` needs the exact field name) |
| `is:due is:new is:learn is:review is:suspended is:buried` | Queue state |
| `prop:ivl>=21` | Mature cards (Anki's own maturity definition) |
| `prop:due<=3` | Due within three days (negative numbers = overdue) |
| `prop:lapses>3` / `prop:reps>8` | Failure- and exposure-count filters |
| `prop:ease<2.0` | The SM-2 ease-hell screen — wider than the 130-180% core band on purpose, so cards on the way down are caught |
| `prop:s>=100` / `prop:d>0.8` / `prop:r<0.9` | FSRS stability, difficulty, current retrievability |
| `rated:7:1` | Answered Again in the last 7 days (`:1`=Again … `:4`=Easy) |
| `introduced:30` / `added:7` / `edited:7` | First studied / added / edited in the last N days |
| `flag:1` | Flagged cards (1-7, per-card and never synced to notes) |
| `re:^What` / `w:run` | Regex / whole-word match |
| `preset:Vocabulary` | Every card whose deck uses that options preset |

Combining: space = AND, `or` = OR, `-` = NOT, parentheses group. `deck:Med (tag:high-yield or prop:lapses>3) -is:suspended` is the shape of most useful queries.

Two gotchas that waste the most time: search matches the **HTML-stripped** text, so a word broken by `<b>` tags will still match but a word split across fields will not; and `deck:` matches subdecks while `tag:` does not match children unless you add `::*`.

## Recipes

```
tag:leech -is:suspended                     # today's rewrite queue
prop:ivl>=21 rated:31:1                     # mature cards that failed this month — the real problem list
is:new added:1 -deck:Default                # what today's import actually created
prop:reps>8 -prop:lapses>0                  # never-failed cards: deletion candidates
is:suspended edited:180                     # suspended and forgotten about
introduced:21 is:due                        # cards too young to survive an exam
deck:Med tag:source::lecture-14 is:suspended  # a lecture ready to unsuspend
"note:Basic (and reversed card)" card:2     # every reverse card, for a bulk cull
-is:suspended -is:new prop:d>0.9            # FSRS's hardest live cards
```

## Bulk Operations From The Browser

Select all (Ctrl/Cmd-A) after a search, then:

| Operation | Effect | Reversible |
|---|---|---|
| Suspend / Unsuspend | Removes from or returns to the queue | Yes |
| Change Deck | Moves cards, history intact | Yes |
| Add/Remove Tags, Find & Replace | Note-level edits across the selection | Via undo, in-session |
| Reposition | Reorders new cards' introduction | Yes, by repositioning again |
| Set Due Date | Forces a due date; `3-7` picks randomly in that range, a trailing `!` also rewrites the interval | Only from a backup |
| Forget | Back to new; "restore original position" and "reset repetition count" decide how much history dies | No |
| Delete Notes | Removes notes, cards, and history | No |

Undo covers one action at a time and only in the current session. Anything in the "no" column: export the selection first.

## Filtered Decks

A filtered deck temporarily borrows cards matching a search, then returns them.

- **Reschedule ON** (default) is the normal choice: answers count and intervals update as usual — a filtered deck is just a different order of studying.
- **Reschedule OFF** means the session does not affect scheduling — a cram/preview mode. Use it the night before an exam; never as a daily habit, or you study without teaching the scheduler anything.
- Build order and limit matter: `order: oldest seen first` for a backlog, `order: relative overdueness` for triage, `random` for interleaving practice.
- Second filter slot exists for two-tier priority (high-yield first, then everything else).
- Cards in a filtered deck are unavailable to their home deck until the filtered deck is emptied or deleted. Deleting a filtered deck returns cards home safely — it never deletes cards.
- `is:due` inside a filtered deck's search is usually wrong for cram: it excludes exactly the cards you have not learned yet.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `tag:cardio` expecting children | Hierarchical children are separate tag strings | `tag:cardio::*` or `tag:cardio*` |
| Deck names with spaces unquoted | Anki reads the second word as a new term | Quote the whole term: `"deck:Med School"` |
| Set Due Date to clear a backlog | Hides the debt and corrupts the review history the model learns from | Cap reviews and burn down |
| Forget instead of Set Due Date | Throws away all history to solve a scheduling annoyance | Set Due Date, or fix the card |
| Building a filtered deck with Reschedule OFF for daily study | Days of reviews teach the scheduler nothing | Reschedule ON except for deliberate cram |
| Leaving a filtered deck sitting for weeks | Its cards are invisible to the home deck's counts and limits | Empty it when the session ends |
