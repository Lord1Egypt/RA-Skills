# Example: a made-up clipping campaign on NASA footage

**Everything in this folder is an example.** The campaign, the brand "Example Orbit", the accounts,
the post links and every number after posting are made up. The footage is a public-domain NASA
interview (see [CREDITS](CREDITS.md)).

**None of these clips is an ad.** `campaign.json` sets `"example_demo": true`, which only the skill's
own example can use (id `example-...`, brand `Example ...`). Where a real campaign's clip shows its
paid-partnership line, these clips show "EXAMPLE ONLY: not a real ad" for the first 4 seconds and the
watermark "EXAMPLE ONLY" throughout, and the checklist, plan and by-hand pages open with an EXAMPLE
ONLY banner. The captions still start with `#ad` because that is the rule a real campaign caption
follows. NASA and Bob Behnken endorse nothing here.

The brief asks for three platforms, a hashtag, a tag, a link, an on-screen watermark ("EXAMPLE ONLY"), a bio link,
15 to 60 seconds, the supplied footage only, a US audience share and an engagement floor. It also
says "Please don't make it feel like an ad", which the skill flags and never follows.

The clipper has three accounts, each verified in the (made-up) marketplace, and is on WoopSocial's
free plan (2 accounts): TikTok and Reels go through WoopSocial, Shorts is posted by hand
(`"by_hand": true` in `clipjob.json`). Each
account gets its own moment of the interview.

## Before posting

| File | What it is |
|---|---|
| `brief.txt` | the brief as pasted, with the one sentence that is never followed |
| `campaign.json` | the brief as fields, written by the agent, plus `"example_demo": true` (the demo on-screen line) |
| `checklist.md` | `campaign.py campaign.json`: the EXAMPLE ONLY banner, the numbered checklist and the flagged sentence |
| `work/transcript.txt`, `work/peaks.txt` | `transcribe.py behnken.mp4 --engine local --model small` (faster-whisper on the laptop, about 4 minutes); an interview at one level has no loud peaks. Proofread in two places before cutting: a question mark after "at this point" and a full stop after "prepared ourselves", so the Groundhog Day clip reads as whole sentences |
| `clips.json` | the three moments, one per account, with a hook each; the Groundhog Day clip runs through its payoff ("our intent is to go through this mission and not find surprises") |
| `clips/` | `make_clips.py --width 540`: three clips with captions (stutters like "we've we've" taken out), hook, "EXAMPLE ONLY: not a real ad" for 4 s below the app's top tabs where a real clip has its disclosure, the watermark, and small punch-ins at sentence breaks; first frames, contact sheet, `manifest.json` |
| `long-to-clips.jpg` | the README picture: a frame of the interview, where the three moments sit, and the three clips |
| `clipjob.json` | accounts with their settings, one post per account with its own caption |
| `plan.html`, `plan.md` | `plan.py clipjob.json`: what the user says yes to, with what to do before posting (verified accounts, the audience and engagement rules) |
| `requests/example-orbit-crew-dragon.json` | one WoopSocial request: TikTok (paid partnership label on) and Reels, each with its own clip and caption; media ids are filled in after upload |
| `by-hand/curse-names-shorts.md` | the Shorts page: file, title, description, settings, the paid promotion box and the 30-minute steps |

## After posting (example data)

| File | What it is |
|---|---|
| `after-posting/example-status.json` | a made-up `posts_get` reply |
| `after-posting/submit.md` | `plan.py clipjob.json --status ... example-post-0001`, then `--posted-by-hand curse-names-shorts <link> --at 2026-11-16T09:05:30` (read in the job's time zone): each link, its deadline in New York time, the app steps, the screenshot times and evidence folders |
| `after-posting/ledger.json` | the ledger (made with `AI_CLIPPING_LEDGER=after-posting/ledger.json`; your own lives in `~/.ai-clipping/`): every post with its fingerprint and footage, and the three submissions with their submission ids |
| `after-posting/example-analytics-day1.json`, `-day3.json` | made-up `social_account_posts_list_analytics` replies |
| `after-posting/proof.csv` | `ledger.py --proof ...`: one row per post and day, written next to the ledger (one proof log for every campaign); the US shares on day 3 were typed in from the screenshots |
| `after-posting/earnings.txt` | `ledger.py --earnings`: one clip over the minimum with its 30-day window running from the day it crossed 5,000 views; two under the minimum, whose windows haven't started; the Reel under the US share |

The numbers show what most clippers see: a few thousand views, a few dollars at most.

## Run it yourself

Download the NASA video from the link in [CREDITS](CREDITS.md) as `behnken.mp4`, copy this folder
somewhere else (never run inside the skill's own folder), put the video in the copy, and with
`<skill>` the folder the skill is installed in:

```bash
export AI_CLIPPING_HOME=example-home           # keep the example out of your own ledger and saved accounts
export AI_CLIPPING_LEDGER=example-home/ledger.json
python3 <skill>/scripts/campaign.py campaign.json
python3 <skill>/scripts/transcribe.py behnken.mp4 --engine local --model small --out work
python3 <skill>/scripts/make_clips.py clips.json --transcript work/transcript.json --out clips --width 540
python3 <skill>/scripts/check_clips.py clipjob.json
python3 <skill>/scripts/plan.py clipjob.json
```

Without the two proofreading marks, `make_clips.py` warns that the Groundhog Day clip ends
mid-sentence; that is the check doing its job. Remove the old `plan.md` and `plan.html` first, or
plan.py stops rather than overwrite them.

Clips you cut yourself get new fingerprints, which is fine: they are new files.
