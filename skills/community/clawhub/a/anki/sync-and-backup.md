# Sync And Backup — Not Losing Years Of Reviews

Sync is replication, not backup: it copies deletions and corruption to every device just as faithfully as it copies your reviews. The two mechanisms are separate and you need both.

## How Sync Actually Works

- AnkiWeb holds a copy of the collection. Normal sync sends the changes since your last sync in both directions and merges them.
- **Media syncs separately** from cards, in its own pass. "Syncing media" continuing after the card sync finished is normal on large collections; let it run.
- A sync happens on close (if configured) and on demand. The discipline that prevents every conflict: **sync at the start and the end of every session, on every device.**
- Reviews done offline are merged normally when the device reconnects — as long as no full sync intervened.

## The Upload-Or-Download Prompt

Anki asks this when the two sides can no longer be merged. Whatever you pick, **the other side's unsynced work is destroyed**.

Causes, in rough order of frequency: restoring from a backup, importing a `.colpkg`, schema-level changes (note type surgery, deleting fields or templates), switching schedulers, an add-on writing directly to the collection, and a client too old for the server's schema.

Decision procedure:

1. Stop. Do not press either button yet.
2. On every other device, note whether reviews were done since its last sync. Sync any device that CAN still sync normally first.
3. Identify the device holding the work you cannot recreate.
4. From that device: **Upload** (push it to AnkiWeb). From every other device: **Download**.
5. Export a `.colpkg` from the winning device before pressing anything.

"One-way sync required" mid-session with reviews pending on two devices means one side's reviews are lost. That is the whole reason for the sync-at-both-ends habit.

## Backups

- Anki keeps automatic backups inside the profile folder (`backups/`), on a rolling daily/weekly/monthly schedule configurable in Preferences. They are local: a dead disk takes them with it.
- Restore via File → Switch Profile → Open Backup, or by importing the `.colpkg`. Restoring always triggers the upload-or-download prompt afterwards — restore on the device you will Upload from.
- **Your real backup is a `.colpkg` you copy off the machine** (cloud drive, external disk) on a cadence you can name. Monthly is enough for most; weekly during an exam term.
- Test one restore per quarter — open it in a scratch profile and verify the card count. An untested backup is a belief, not a backup.
- Profile folder locations: `~/.local/share/Anki2/` (Linux), `~/Library/Application Support/Anki2/` (macOS), `%APPDATA%\Anki2\` (Windows). Never sync that folder with Dropbox/iCloud while Anki is running — concurrent writes to the collection database are the classic corruption cause.

## Multiple Devices

- Same AnkiWeb account everywhere; the desktop is the editing device, mobile clients are for reviewing.
- Add-ons run on the desktop only. Cards that depend on an add-on's rendering will look wrong or broken on mobile.
- AnkiDroid and AnkiMobile ship their own scheduler implementations; keep clients reasonably current, since an old client plus a new collection schema forces a full sync.
- Reviewing on two devices without syncing between them is the only way to lose reviews in normal use. Sync before you open the phone.

## Integrity Checks

| Tool | What it does | When |
|---|---|---|
| Tools → Check Database | Rebuilds indexes, fixes counts, clears invalid card states | Counts look wrong, the app misbehaves, or before reporting a bug |
| Tools → Check Media | Lists missing references and unused files | After a bulk import or a media cleanup |
| Tools → Empty Cards | Finds cards whose front renders empty | After note-type or template changes |
| Restore from backup | Rolls the collection back | Corruption Check Database cannot fix, or a destructive mistake |

Check Database is safe and non-destructive to content — but it may report deleted invalid cards, which is a signal to look at what created them, not something to ignore.

## Corruption Recovery

1. Do not sync. A corrupted collection uploaded to AnkiWeb propagates to every device.
2. Copy the whole profile folder somewhere safe, as-is.
3. Try Check Database.
4. If that fails, restore the most recent backup that predates the problem, verify the card count and a few decks, then Upload from that device.
5. Reviews between the backup and the failure are gone. That gap is exactly the value of an off-machine `.colpkg` cadence.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Treating AnkiWeb as the backup | It mirrors deletions and corruption within seconds | Off-machine `.colpkg` copies |
| Cloud-syncing the Anki2 folder | Two processes writing one SQLite file = corruption | Use AnkiWeb for sync, cloud only for exported `.colpkg` files |
| Pressing Download to make the prompt go away | Silently discards whatever that device had | Run the five-step decision procedure |
| Note-type surgery on the phone-heavy device | Forces a full sync from the device with the least work | Do structural edits on the desktop, then sync immediately |
| Skipping the end-of-session sync | Tomorrow's device starts from stale state and conflicts | Sync at both ends, every session |
| Deleting the `backups/` folder to save space | Removes the only local recovery path | Reduce the retention counts in Preferences instead |
