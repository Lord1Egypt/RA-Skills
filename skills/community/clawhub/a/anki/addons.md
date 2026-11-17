# Add-ons — What To Install, What Broke, What Is Already Built In

Add-ons are arbitrary Python running inside your collection. They are the leading cause of "Anki broke after the update" and of crashes that look like corruption. Install few, know what each one does, and keep a `.colpkg` from before any add-on that writes to cards.

## Already Built In — Do Not Install These

Installing an obsolete add-on for a feature that shipped is the most common self-inflicted breakage.

| Feature | Built in since | Old add-on now redundant |
|---|---|---|
| FSRS scheduling | `anki >=23.10` | FSRS4Anki scheduler script |
| Image Occlusion note type | `anki >=23.10` | Image Occlusion Enhanced |
| True Retention table in Stats | `anki >=24.11` | True Retention add-on |
| Hierarchical tags with `::` | Long-standing | Hierarchical Tags |
| Night mode / dark theme | Long-standing | Night Mode |
| v3 scheduler and display-order controls | Long-standing | Various queue-order add-ons |

Before installing anything, search the built-in deck options and Browse for the feature. The gap between "the guide I read" and your version is usually the whole reason the add-on is being suggested.

## Categories Worth An Add-on

| Need | What to look for | Notes |
|---|---|---|
| Programmatic access from other tools | AnkiConnect | The de-facto API used by sentence miners, dictionary popups, and scripts; runs a local HTTP server while Anki is open — treat it as an open port and do not run it on shared machines |
| Text-to-speech on cards | A TTS add-on such as AwesomeTTS/HyperTTS | Generate audio into media files, do not depend on runtime TTS: mobile clients cannot run the add-on |
| Extra scheduling helpers on top of FSRS | FSRS Helper-style utilities | Only after plain FSRS has been optimized; helpers on unoptimized parameters solve nothing |
| Consistency tracking / heatmap | Review Heatmap | Motivation tooling; zero effect on scheduling |
| Browser power tools | Advanced Browser-style column and search extensions | Useful during a large cleanup, removable afterwards |
| Editor conveniences | Frozen fields, field-fill helpers | Saves real time during bulk manual entry |

Everything else: try two weeks without it first.

## The Risk Model

- An add-on can modify notes, cards, scheduling and the database. One that writes to the collection can force a full sync (the Upload-or-Download prompt) and can corrupt it — export a `.colpkg` before its first run.
- Add-ons are pinned to Anki versions. A major upgrade disables or breaks incompatible ones; the add-on manager flags them, but a broken hook can still crash startup.
- **Add-ons do not exist on AnkiMobile or AnkiDroid.** Anything an add-on generates at review time (audio, rendering, popups) is missing on the phone; anything it bakes into fields survives everywhere. Prefer add-ons that write to fields.
- Paid ecosystems (subscription note types and deck platforms, common in medicine) tie your collection's rendering to a vendor. Fine while you subscribe; export a plain-note-type copy before you stop.

## The Upgrade Drill

1. Export a `.colpkg` before upgrading Anki.
2. Upgrade, then launch with add-ons disabled (hold Shift) and confirm the collection is fine.
3. Launch normally. If it crashes or misbehaves, Tools → Add-ons → disable all, then re-enable in halves until the culprit appears.
4. Update the survivors from the add-on manager, and delete anything whose feature is now built in (table above).
5. Never do this the week before an exam. Freeze the setup; upgrade after.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Installing ten add-ons at once | No way to bisect the one that breaks startup | One at a time, use each for a week |
| Depending on an add-on for card rendering | Cards look broken on every mobile client | Bake results into fields |
| Copying an add-on's config from a forum post | Configs assume that person's collection and version | Read the add-on's own config description |
| Leaving AnkiConnect enabled by default | An open local API into your collection | Enable it for the workflow that needs it |
| Skipping the backup because "it is just an add-on" | Add-ons write to the collection database | `.colpkg` first, always |
| Chasing a scheduling add-on to fix retention | Scheduling is rarely the cause | Fix grading and card quality first |
