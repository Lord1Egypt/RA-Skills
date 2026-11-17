# Organization — Decks, Tags, And Keeping A Collection Sane

Decks control **scheduling scope**; tags control **selection**. Every structure mistake comes from using one for the other's job.

## The Rule

**Make a deck when the cards need different settings or a different daily limit. Make a tag for everything else.**

Because deck options are presets applied per deck, a deck is a scheduling container that happens to look like a folder. Two subjects studied on identical settings do not need two decks — they need two tags and one deck.

| Want | Use |
|---|---|
| Different new/day or steps for this material | Deck (with its own preset) |
| Study this subject alone today | Tag + filtered deck |
| Pause a subject | Deck with a preset at new = 0, or suspend by tag |
| Track source, chapter, difficulty, lecture | Tags |
| Keep exam material separate from hobby material | Deck (different intensity) |
| Anything else | Tag |

## Deck Structure

- **Two levels, rarely three.** `Spanish::Vocabulary`, `Med::Pharm`. Depth costs navigation, and per-deck limits multiply confusingly at depth.
- Renaming a deck to `Parent::Child` moves it — that is the only "move" operation, and it is safe.
- **Deleting a deck deletes its cards.** To empty a deck without losing cards, move them out in Browse first (Change Deck), then delete.
- The `Default` deck cannot be deleted, only emptied; a collection with cards sitting in Default usually has an import whose `#deck:` header was missing.
- Deck descriptions (deck options → Description) are the right home for "how I study this deck" notes — they show on the deck's study screen and survive device changes.

## Tag Taxonomy

Use hierarchical tags (`::`) so one tree collapses in the sidebar instead of a hundred flat tags:

```
source::first-aid          content::cardio::arrhythmia        status::rewrite
source::lecture-14         content::pharm::antibiotics        status::leech
```

Three axes cover almost every collection:

- **content** — what the card is about. The axis you filter by when studying.
- **source** — where it came from. The axis you use to delete or unsuspend in bulk when a book or lecture is superseded.
- **status** — what you intend to do with it: `rewrite`, `high-yield`, `exam::june`, `paused`. Transient by design; clear them when the intent is discharged.

Rules that keep it usable: singular or plural, pick one and never mix. No spaces (Anki splits tags on whitespace). If you have never filtered by a tag, delete it — Browse → sidebar → Find & Replace on tags handles renames across the collection in one action.

## Duplicates

- Anki's Find Duplicates (Browse → Notes) matches the **first field, exact text** — nothing else. Rephrased duplicates are invisible to it.
- Semantic duplicates come from carding the same material twice, months apart; the tell is two cards with the same answer and different phrasing. Search by the answer text, not the question.
- Resolution: keep the note with review history (usually the older one), move any unique content from the loser into the keeper's Extra field, then delete.
- Prevention beats cleanup — dedupe at generation time.

## Splitting And Merging

Split when: the material needs different daily limits or steps; one part is exam-bound and the rest is not; the deck exceeds what you can meaningfully audit in one Browse view. Do not split for tidiness — that is what tags are for.

Merge when: two decks share a preset and you never study them separately; a subdeck holds fewer cards than its own daily limit; the hierarchy has levels you always expand.

Both operations are the same mechanic: select in Browse → Change Deck. Review history follows the cards.

## Maintenance Cadence

| Cadence | Action | Trigger to act |
|---|---|---|
| Weekly | Review `tag:leech` and the `status::rewrite` queue | More than a handful accumulated |
| Weekly | Glance at Future Due | A rising slope means cutting new cards now, not later |
| Monthly | Audit suspended cards | Suspended for a month = decide: fix, unsuspend, or delete |
| Monthly | Delete never-failed trivia (`prop:reps>8` with no lapses) | Reviews spent on cards that teach nothing |
| Quarterly | Tag audit; delete unused tags | The sidebar has entries you do not recognize |
| Quarterly | Verify a backup restores | You have never tested one |
| Per exam | Retag high-yield, adjust limits, plan capacity | A date exists |

## Sharing A Deck

- Export as `.apkg` with scheduling **excluded** — your intervals are meaningless to anyone else and leak your study history.
- Strip personal fields (source notes, mnemonics tied to your life) and check media licensing before publishing; images from textbooks are the usual copyright problem.
- Clear `status::` tags: they are your intent, not the recipient's.
- Include a note type that is self-contained (fonts and CSS in the note type), otherwise the deck renders wrong on their machine.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| A deck per lecture | Dozens of decks, each with its own limit interacting with the parent's | One subject deck, `source::lecture-14` tags |
| Deleting a deck to remove it from the list | Takes the cards and their history with it | Move cards out first, then delete |
| Tags with spaces | Anki splits them into several tags with no warning | `high-yield`, not `high yield` |
| Reorganizing instead of studying | Structure work feels productive and moves no card into memory | Timebox it to the maintenance cadence above |
| One preset for a 10k-card collection | Vocabulary and reasoning cards need different limits and steps | Split presets by material type |
