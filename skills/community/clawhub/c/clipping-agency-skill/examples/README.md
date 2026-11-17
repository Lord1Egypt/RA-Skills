# Example: two made-up clients on NASA archive footage

**EXAMPLE ONLY.** "Example Orbit Podcast" and "Example Mission Talks" are invented clients. Their
episodes are short excerpts of two public-domain Apollo 11 videos from NASA's archive (see
[CREDITS](CREDITS.md)). The accounts, post ids, approvers, links and every number are made up;
nothing here was posted.

Every file was made by the skill's scripts, in the order the skill runs them, on a fixed clock
(`AGENCY_NOW`) so the dates read like a real month.

## The two clients

| | Example Orbit Podcast | Example Mission Talks |
|---|---|---|
| Client file | [`client.json`](agency/clients/example-orbit-podcast/client.json), [`checklist.md`](agency/clients/example-orbit-podcast/checklist.md) | [`client.json`](agency/clients/example-mission-talks/client.json), [`checklist.md`](agency/clients/example-mission-talks/checklist.md) |
| Time zone | America/Chicago | America/New_York |
| Approval rule | silence means hold | silence for 48 h counts as a yes, agreed in writing |
| End card | yes | none |
| Accounts | TikTok, Reels and Shorts connected | TikTok and Shorts connected, Instagram posted by hand |
| Episode | [`ep-012`](agency/clients/example-orbit-podcast/episodes/ep-012/): three clips, approved by reply, live, and the October report | [`ep-007`](agency/clients/example-mission-talks/episodes/ep-007/): one clip changed on request, a second page, scheduled |

## Example Orbit Podcast, episode 12

1. [`batch.json`](agency/clients/example-orbit-podcast/episodes/ep-012/batch.json): three moments
   with the reason for each, hooks, captions per platform, YouTube titles. Clip 2 re-aims the crop
   when the camera cuts to another shot (`shots`).
2. [`clips/`](agency/clients/example-orbit-podcast/episodes/ep-012/clips/): the cut clips,
   [`contact-sheet.jpg`](agency/clients/example-orbit-podcast/episodes/ep-012/clips/contact-sheet.jpg),
   and `listen.json`, what the edge check heard in each clip's first and last seconds.
3. [`approval/approve-ep-012.html`](agency/clients/example-orbit-podcast/episodes/ep-012/approval/approve-ep-012.html):
   page 1, the page the client opens on their phone.
4. [`reply-from-client.txt`](agency/clients/example-orbit-podcast/episodes/ep-012/reply-from-client.txt):
   the client's plain reply, applied with `approve.py --apply --received` into
   [`approvals.json`](agency/clients/example-orbit-podcast/episodes/ep-012/approvals.json).
5. [`schedule.md`](agency/clients/example-orbit-podcast/episodes/ep-012/schedule.md): the clips
   at the client's times, then `--media`, `--check` and `--posted` for each request.
6. [`after-posting/`](agency/clients/example-orbit-podcast/episodes/ep-012/after-posting/): saved
   post statuses and the month's saved analytics (made-up numbers).
7. [`reports/2026-10.html`](agency/clients/example-orbit-podcast/reports/2026-10.html) and
   [`.md`](agency/clients/example-orbit-podcast/reports/2026-10.md): the October report for the
   client, with the agency's words from [`notes/2026-10.md`](agency/clients/example-orbit-podcast/notes/2026-10.md);
   [`2026-10-agency.md`](agency/clients/example-orbit-podcast/reports/2026-10-agency.md) is what
   the agency chases, never sent.

## Example Mission Talks, episode 7

1. Page 1 went out; the client approved clips 1 and 2 and asked for a change to clip 3
   ([`reply-from-client.txt`](agency/clients/example-mission-talks/episodes/ep-007/reply-from-client.txt)).
2. Clip 3 got a new hook and was cut again. Its old decision no longer counted, so page 2 went out,
   with the 48-hour deadline printed as a New York date and time. No reply came by then, so clip 3
   went ahead on silence, recorded as that and never as "approved"; clips 1 and 2 kept their yes
   because they hadn't changed ([`approvals.json`](agency/clients/example-mission-talks/episodes/ep-007/approvals.json),
   [`approval/approve-ep-007.html`](agency/clients/example-mission-talks/episodes/ep-007/approval/approve-ep-007.html)).
3. [`schedule.md`](agency/clients/example-mission-talks/episodes/ep-007/schedule.md): TikTok and
   YouTube through WoopSocial, Instagram listed to post by hand.

[`agency/ledger.json`](agency/ledger.json) is the agency's ledger for both clients: every clip file,
account and post.

## Run it yourself

From this folder, with the example's own ledger:

```bash
export CLIPPING_AGENCY_LEDGER="$PWD/agency/ledger.json"
cd agency
python3 ../../scripts/client.py list
python3 ../../scripts/approve.py clients/example-mission-talks/episodes/ep-007/batch.json --status
python3 ../../scripts/status.py
```

(Windows PowerShell: `$env:CLIPPING_AGENCY_LEDGER = "$PWD\agency\ledger.json"`.)

To cut the clips again, download the two NASA files listed in [CREDITS](CREDITS.md), cut the listed
stretches into one `source.mp4` per episode folder, and run `make_clips.py <batch.json> --width 360`.
Cutting again changes the files, so their earlier approvals stop counting: that is the point of the
check. Work on a copy of this folder.
