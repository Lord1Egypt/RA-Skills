# Approval: the page, the reply, and what a yes covers

## Why a page and a plain reply

Clients approve on their phone, between other things. They won't log in to a tool, and a yes in a
chat thread ("all good!") doesn't say which version of which clip it covers. The page shows every
clip of one episode as it will go out, numbered, and the client answers in plain words by any
channel: email, chat, text. The agency keeps the record of exactly what that page showed.

## The page

`approve.py <batch.json>` checks the batch first: a batch with errors gets no page. The page is one
small HTML file that works with no scripts, opened from an email attachment on iPhone or Android:

- "Page N" at the top: every page of an episode gets the next number, and the reply names it;
- every clip as "Clip 1", "Clip 2"...: its cover picture linked to the clip, its length, its hook,
  why it was picked;
- each platform's caption and the YouTube title, exactly as they will be posted, plus the YouTube
  privacy and made-for-kids answers and the tags;
- when: "Planned around Wed 07 Oct, 18:00 New York time (EDT)" in the client's time zone, or
  "Already scheduled for ... Reply '2: skip' to stop it" for a clip that is already with WoopSocial;
- anything to know: a sponsor segment (it goes out labelled as paid), "Your brand" for a clip that
  promotes the client's own business, possible music, a no-go topic the agency reviewed, the year
  the episode was recorded (`episode.recorded`);
- TikTok's choices, which TikTok asks the account owner to make: who can see the posts (only the
  audiences the account offers), and comments, duets and stitches on or off. Nothing is chosen in
  advance; "only me" isn't offered for a paid partnership. A choice from an earlier page is shown
  and still holds unless the reply has a new TikTok line;
- the approval rule in plain words, with an absolute deadline when silence counts (below);
- the reply to copy, in a box: `Page 2, Example Mission Talks ep-007`, then `1:`, `2:`, `3:`,
  `TikTok:` and `Name:`, plus a "Reply by email" link that opens the client's mail app with it
  filled in. When scripts run, optional Yes, Change and Skip buttons fill the same reply in; nothing
  depends on them.

### How the clips reach the client

The page doesn't carry the videos, so it stays small enough to attach anywhere. Pick one:

- **Default:** the page links `../clips/clip-01.mp4` and so on. Send the page with the clip files
  (attach them, or share the episode folder). On a phone, a linked file only opens when it came with
  the page, so for phones a shared folder link is better:
- **`--clips-url https://...`:** the link of a shared folder (Google Drive, Dropbox, the agency's
  own storage) holding the clip files under the same names. Each cover picture links to its clip
  there. Share the folder with the approvers only.
- **`--embed`:** puts the clips inside the page, for a short batch under 15 MB in total (bigger is
  refused: mail apps and phones don't open pages that size).

Limits, said plainly: an attachment opened in a mail app can't always play a linked video, and some
mail apps strip the "Reply by email" link. The reply box works everywhere: the client can always
copy it, or type the same lines.

## The reply

A plain reply like any of these works:

```
Page 2, Example Mission Talks ep-007
1: yes
2: change: start on the second sentence
3: skip
TikTok: followers, comments on, duets off, stitches on
Name: Jordan Example
```

```
page 2: 1 yes, 2 change: start later, 3 skip
```

```
Page 1
1) Yes 2) Yes 3) No
```

The same lines typed with a bullet in front, in bold, with a curly quote or a non-breaking space
from a mail app, or with the change note on the next line, read the same.

`approve.py <batch.json> --apply reply.txt [--received "2026-11-09 14:12"]`:

- reads the reply in any encoding a mail app saves (UTF-8, UTF-16, Windows-1252) and ignores quoted
  lines (`> ...`) and everything below "On ... wrote:" from the message it answers;
- finds the page from "Page N" (or `--page N`). With more than one page and none named, it stops and
  asks. **A reply to an older page is refused** once a newer page was sent: an older page's answers
  never overwrite newer ones. A newer page that was made but never sent doesn't block it; the output
  says to make that page again;
- reads one answer per clip number: yes, ok, approve, no changes; change, edit, revise (with what to
  change after the colon or on the next line: a change with no note is refused); skip, no, drop,
  don't post, not this one. "All yes" approves every clip, but only when nothing else in the reply
  hedges, skips, changes or names a clip;
- **safety over convenience: anything it can't read one way is refused, and nothing is recorded.**
  It prints every line with what it understood, and says why. Refused, for example: `All yes but
  skip 3`, `Yes to all apart from number 2`, `1: yes but change the caption`, `2 maybe`, a clip
  named in words ("clip two"), a number the page doesn't have, a clip answered twice. Confirm with
  the client what they meant, then apply their clear answer;
- refuses a reply that leaves a clip on the page without an answer (a clip that already has a
  decision on record from an earlier page counts as answered). `--partial` records the answers
  given; the others wait for an answer;
- **any reply to a page, even one refused or partial, ends approval on silence for that page**:
  nothing on it goes out without an answer after that;
- takes who replied from the `Name:` or `From:` line, or `--by`, and refuses anyone who isn't one
  of the client's approvers. The record says which of the two it was;
- records when the client sent the reply (`--received`, or the `Date:` line of a saved email)
  apart from when it was applied. Without either, the time is unknown, and the monthly report says
  so instead of using the time it was applied;
- refuses a reply that changes nothing (every answer in it is already the decision on record;
  `--again` records it once more on purpose), so a client who changes their mind back is always
  recorded, and says which earlier decisions it changed;
- records the TikTok line only when it gives all four answers (audience, comments, duets,
  stitches) and the audience is one the account offers. Anything less records no TikTok choice:
  TikTok waits and the other platforms go;
- removes any send request written before it (`requests/`), so nothing written for the old state
  can be sent.

**A no for a clip that is already scheduled:** the post is marked `cancel_requested`, a delete
request is written (`requests/cancel-<postId>.json`), and the output says `CANCEL NOW: post X`. This
happens even when the clip was edited after the page was made. Run `posts_delete` with that postId at
once, then `schedule.py <batch> --cancelled X`. `status.py` and `schedule.md` show the cancel until it
is recorded, and `schedule.py --status` never clears it while the post hasn't gone out.
`posts_delete` works only while every account of the post is still NOT_STARTED; a quick delete can
even stop a post sent to publish now. Once any part is live, WoopSocial answers POST_NOT_DELETABLE:
`schedule.py --status` then says LIVE, NOT CANCELLED, and the post has to be removed in the app on
that account. Tell the client the same day.

## What a yes covers

A decision counts only while the clip is exactly what the client decided on: the clip file and every
word posted with it (each caption, the title, the tags, the "Your brand" flag). Re-cut a clip, edit
a caption, change the title or the tags, and its earlier decision no longer counts: `schedule.py`
leaves it out, `--check` and `--posted` refuse its request. Make a new page; clips that didn't
change say "You approved this clip on page 1" and keep their yes.

## Approval on silence

Only with `approval.rule: "auto_after_hours"`, the hours, and where and when the client agreed in
writing. The rule is stored on each page when it is made: changing `client.json` later never
changes a page already sent (a page made under "hold" stays hold; make a new page to use a new
rule).

The page prints an absolute deadline in the client's time zone: "If we haven't heard from you by
Wed 11 Nov, 09:00 New York time (EST)". It is the time the page was made plus the agreed hours,
rounded up to the hour. Silence counts from the later of that deadline and the agreed hours after
the page was marked sent (`--sent`), so a page sent late never gives the client less time than
agreed. Make the page on the day you send it.

After that, each clip of the page the client didn't answer counts as approved, recorded as "no reply
by the deadline on page N, as agreed in writing". Pages and reports never call it "you approved":
the next page says "No reply by <deadline>, so this clip went ahead as agreed in writing", and the
report counts those clips apart. It never covers a clip marked change or skip, a clip changed after
the page was sent, or TikTok's settings.
