# Example: one NASA clip to TikTok, Reels and Shorts

A 14-second vertical clip about why astronauts exercise in space, cross-posted to three accounts:
TikTok and Instagram Reels (both `@example.orbit`) through WoopSocial, YouTube Shorts by hand (the free plan covers 2
accounts, so this is what a first run looks like).

| File | What it is |
|---|---|
| `clips/microgravity.mp4` | the video (see [CREDITS](CREDITS.md)) |
| `covers/microgravity-sheet.jpg` | 12 frames to pick a cover from, made by `cover.py` |
| `covers/microgravity.jpg`, `covers/microgravity-grid.jpg` | the cover, and how it looks full screen and in the profile grid |
| `covers/microgravity.json` | which video and which second the cover came from (12.2 s), for the plan and the by-hand page |
| `crosspost.json` | the job: accounts, settings, answers, a text per platform |
| `plan.html`, `plan.md` | every post as it will go out, made by `plan.py` |
| `requests/microgravity.json` | the one WoopSocial request: a child per account, each with its own text |
| `by-hand/microgravity/shorts.md` | the YouTube page: title, description, tags, settings, cover frame and numbered steps |

The account IDs start with `example-` (made up; `plan.py` accepts these, and refuses placeholders such as `<id>` or `your-...`) and the media IDs are not filled in; nothing here was posted.

NASA footage is free to reuse; in the job it counts as a file you have the right to post (`own_video: true`), and every text credits it.

The plan pages say when they were planned (Thu 12 Nov 2026); the "(in 61 days 12 h)" next to the
time counts from then.

To run it yourself, copy this folder somewhere else first (the skill's own folder is replaced on
every update, so nothing is written into it), then from the copy, with `<skill>` the folder the
skill is installed in:

```bash
python3 <skill>/scripts/check_video.py clips/microgravity.mp4
python3 <skill>/scripts/cover.py clips/microgravity.mp4 --at 12.2
python3 <skill>/scripts/plan.py crosspost.json
```

The time in `crosspost.json` must be in the future; change `when` if `plan.py` says it has passed.
