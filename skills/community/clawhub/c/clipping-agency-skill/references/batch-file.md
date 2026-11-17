# The episode batch: clients/<client-id>/episodes/<episode-id>/batch.json

`sources.py start` writes the skeleton. The agent fills in the episode facts and the clips. Every
path is from the episode folder. A batch must sit inside the folder of the client it names.

```json
{
 "client": "example-mission-talks",
 "episode": {
  "id": "ep-007",
  "title": "Episode 7: two days before launch",
  "recorded": "1969",
  "published": "2026-11-06T12:00:00Z",
  "source": "source.mp4",
  "transcript": "work/transcript.json",
  "guests": ["The mission commander", "The command module pilot"],
  "guest_release": "on_file",
  "sponsor_segments": [{"start": 1210.0, "end": 1265.5, "sponsor": "Acme"}],
  "music": [[0, 12.5]]
 },
 "clips": [
  {"id": "01", "start": 0.7, "end": 39.9,
   "why": "The question everyone asked, answered straight. Stands alone.",
   "hook": "Were the first words on the Moon scripted?",
   "title": "Were the first words on the Moon scripted? (1969)",
   "tags": ["apollo 11", "moon landing"],
   "captions": {"TIKTOK": "...", "INSTAGRAM": "...", "YOUTUBE": "..."},
   "reframe": "center", "focus_x": 0.5, "fillers": true, "hook_at": "top", "logo_at": "high-right"}
 ]
}
```

## The episode

| Field | What it is |
|---|---|
| `id` | lowercase letters, digits, single dashes: names the folder and the page |
| `recorded` | when it was recorded, as the client should read it ("1969", "March 2025"): shown on the page, so an old statement is never mistaken for news |
| `published` | clips are never scheduled before it (set `"not_before_published": false` to allow) |
| `source` | the episode's video file |
| `guests`, `guest_release` | `on_file`, `not_needed`, `missing` or `unknown`. With guests and no release on file (and no contract clause in the client file), the batch can't go to the client |
| `sponsor_segments` | where a sponsor read sits, in seconds of the episode. A clip that overlaps one must say it is paid in every caption (`#ad`, "Sponsored by ...", "Paid partnership with ..."), goes out with TikTok's paid partnership label, and lists the Instagram and YouTube labels to set in the apps |
| `music` | `[start, end]` stretches you know hold music. Clips overlapping them get a possible-music warning |

## A clip

| Field | What it is |
|---|---|
| `id` | `01`, `02`... (becomes `clip-01.mp4`) |
| `start`, `end` | seconds of the episode |
| `why` | one sentence for the client: why this moment (it stands alone, opens on the point, what it gives the viewer) |
| `hook` | the text on screen for the first seconds; 8 words or fewer, true to the clip |
| `captions` | one per platform of the client: `TIKTOK`, `INSTAGRAM` (5 hashtags at most), `YOUTUBE` (the description) |
| `title`, `tags` | YouTube's title (100 characters, no `<` or `>`) and tags |
| `promotes_client_business` | `true` when the clip promotes the client's own product or business: TikTok's "Your brand" label |
| `no_go_reviewed` | why a clip that mentions a no-go word is still fine; the client reads it on the page |
| `reframe` | `auto`, `face`, `center`, `fit` (whole frame on a blurred copy: wide shots, screen shares), `split` (two people: `speakers`, two `{"x", "y", "w", "h"}` boxes in source pixels, shown one above the other), `stack` (streams: `facecam` box over the gameplay) |
| `focus_x`, `zoom` | crop position 0 to 1 and punch-in 1.0 to 2.0 |
| `shots` | `[[source second, focus_x], ...]`: where the camera cuts, re-aim the crop. From each second on, the crop sits at that focus_x (a wide shot, then a close-up) |
| `track` | `[[source second, focus_x], ...]`: where the camera moves (a pan or a zoom), the crop slides from one point to the next, so the speaker stays in frame through the move |
| `hook_at` | `"top"` puts the hook box just under the app's top bar instead of the default spot, when the default would cover a face in the first seconds |
| `logo_at` | where the client's logo sits: `top-left`, `top-right`, `high-left`, `high-right`, `bottom-left`, `bottom-right`, or `none`. Look at the first seconds and keep it off faces |
| `cut`, `fillers`, `snap` | remove stretches inside the clip and "um"s; snap to sentence edges. With estimated word times (a subtitle file without word timing) fillers stay in, so no cut lands mid-word |
| `tighten` | off unless set to `true`: shortens pauses inside the clip. Only with real word times, and a pause is only cut where the sound is quiet, so a word the transcript timed wrong is never cut |
| `file` | a clip the agency cut itself: the file, plus `start` and `end` of the source it uses, so every check still runs |

Anything that changes what the client sees (the file, a caption, the title, the tags) changes the
clip's fingerprint, and an earlier yes no longer counts for it. Changing the times, hook or framing
after cutting is an error until `make_clips.py` cuts it again. The `why` and these notes can change
freely.

## What the scripts add next to it

- `work/transcript.json`, `transcript.txt`, `peaks.txt`: from `transcribe.py`. The transcript also
  keeps sound cues from caption files (`[MUSIC]`, `(LAUGHTER)`) and the loudness of every second,
  which `check_clips.py` reads for the music hint.
- `clips/`: the clips, a cover frame each, `contact-sheet.jpg`, `manifest.json` (each clip's
  fingerprint, the source ranges it uses, the names the dictionary fixed, the brand it used).
- `approval/approve-<episode>.html`, `approvals.json`: the page and the record of every page, reply
  and decision.
- `schedule.md`, `requests/`, `media.json`: the schedule and what is sent to WoopSocial.
