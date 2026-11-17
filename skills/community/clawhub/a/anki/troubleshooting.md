# Troubleshooting — Symptom To Cause In The Application

This file is for when Anki itself does something you did not ask for. "My memory is not working" — low retention, leech piles, a backlog — is a different chain; SKILL.md Quick Reference routes it. Each chain here is ordered by probability; every step is a check, not a guess.

## The Universal First Three

1. **What does the screen say, exactly?** Deck counts (new/learning/due), the exact error text, the client and version. Most reports resolve on the counts alone.
2. **Tools → Check Database.** Fixes wrong counts and invalid card states, and is safe for content.
3. **Restart with add-ons disabled** (hold Shift while launching on desktop). If the symptom vanishes, it is an add-on, and you have saved yourself the rest of the chain.

## Cards Are Due But Nothing Appears

1. **Daily limits reached** — the deck list shows the capped numbers, not the real ones. Check the preset's new and review limits, and remember the v3 scheduler applies the limits of the deck you clicked, parent included.
2. **Studying a subdeck under a limited parent** — study from the parent, or raise the parent's limit for today only.
3. **Buried siblings** — burying hides a card until tomorrow. Unbury from the deck's gear menu if you need it now.
4. **Suspended** — suspended cards never appear anywhere. Check `is:suspended` in Browse; large shared decks arrive with thousands suspended, or with none.
5. **Cards live in a filtered deck** — they are unavailable to their home deck until it is emptied.
6. **Timezone / next-day-starts-at** — if your day rolls over at 4am and it is 2am, the cards are correctly not due yet.
7. Still nothing: `is:due` in Browse. If Browse finds them and the deck screen does not, it is a limit (step 1), not a bug.

## Imported Notes Produced No Cards

1. Cloze note type with no `{{c1::…}}` in the text — the single most common cause.
2. Wrong note type selected: the fields mapped to a template whose front renders empty.
3. Everything landed in `Default` because `#deck:` was missing — check `added:1` in Browse.
4. Duplicate handling set to "Preserve existing": the notes matched field 1 and were skipped. The import summary reports the skip count; read it.
5. Tools → Empty Cards lists notes whose templates render nothing — the fix is the template or the field content, not a re-import.

## Media Missing Or Broken

1. Desktop shows it, phone does not → media sync has not finished; force a sync and wait for the media pass.
2. Neither shows it → Tools → Check Media. Missing files are listed by name; they were never copied into `collection.media`.
3. Images broke after editing on another device → filenames with spaces, accents, or subfolder paths. Rename to plain ASCII, flat.
4. Audio silent on desktop only → the field holds `[sound:x.mp3]` correctly but the codec is unsupported; convert to mp3 or ogg.
5. Everything is missing after an import → the `.apkg` was exported without media.

## Sync Refuses Or Loops

1. Read the exact message. "One-way sync required" → do not press either button yet. Sync every device that still syncs normally, identify the device holding work you cannot recreate, export a `.colpkg` from it, then Upload from that one and Download on every other. Whatever you pick, the other side's unsynced work is destroyed.
2. Auth failures after a password change → log out and back in on every client.
3. Sync stalls at media forever → a huge media folder syncs slowly on first run; check whether progress is advancing at all before intervening.
4. Repeated conflicts between two devices → the sync-at-both-ends habit is missing, not a bug.
5. Client too old for the server schema → update the client; old mobile clients are the usual holdout.

## The App Is Slow

1. **Browse slow** → an unbounded search across a large collection; add a `deck:` or `added:` term.
2. **Reviews slow to appear** → heavy card templates: giant images, MathJax on every card, or an add-on rendering hook.
3. **Startup slow** → add-ons; test with Shift-launch.
4. **Everything slow, all clients** → collection size plus a filesystem it is syncing on; move the profile off cloud-synced folders.
5. **Slow only on the phone** → images not downscaled. Card images should be sized for the phone, not the textbook scan.

## Counts, Decks, Or Cards Look Wrong

- Counts wrong but cards present → Check Database.
- A deck vanished → it was renamed into another deck's hierarchy (renaming with `::` moves it) or deleted with its cards. Check the deck list for a new child, then a backup.
- Duplicate cards after syncing two devices → the same import ran twice, once per device. Delete by `added:N` on one side.
- Card count changed after a note-type edit → templates were added or removed; Empty Cards reports what disappeared.
- Review history gone for a card → `Forget` with "reset repetition count", a Change Note Type that dropped a template, or a restored backup predating the reviews.

## After An Upgrade

1. Add-ons are the first suspect; disable all, confirm, then re-enable in halves.
2. A one-way sync prompt after a major version bump is expected once — Upload from the device with the work.
3. Deck options moved rather than disappeared: the settings from older versions live under the same presets with new grouping.
4. Never upgrade the desktop mid-exam-term without a fresh `.colpkg` and a check that your mobile client is compatible.

## When You Are Truly Stuck

Reproduce in a new profile (File → Switch Profile → Add): import one `.apkg` of the affected deck and try the action there. If it works in the clean profile, the cause is your add-ons or your collection state, not Anki — and you now know which half to bisect.
