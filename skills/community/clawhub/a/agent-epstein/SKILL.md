---
name: AgentEpstein
description: >-
  Harvest image datasets from art sites (Danbooru, yande.re, e621, Safebooru,
  Konachan, Gelbooru, X, Pixiv) into a folder a LoRA or fine-tune reads
  directly. Routes each source over plain HTTP or a real browser to get past
  bot walls, verifies X and Pixiv candidates by actually looking at them, and
  keeps artist/page/tag provenance on every row. Use for: building a dataset
  or reference set from a tag, ship, fandom or artist; collecting images for
  LoRA training; or scraping a site that 403s a normal client.
version: 0.2.0
author: OpenClaw Agent
license: MIT
platforms: [linux, macos, windows]
metadata: {"openclaw": {"tags": ["datasets", "images", "scraping", "playwright", "booru", "training", "lora"], "requires": {"commands": ["python3"], "env": ["HARVEST_CONTACT", "DANBOORU_LOGIN", "DANBOORU_API_KEY", "GELBOORU_API_KEY", "GELBOORU_USER_ID", "HF_TOKEN"]}}}
---

# Art Dataset Harvest

Collects images plus their tag metadata from art sites into a dataset
folder a trainer can read directly. Drives a **real browser** so that
bot-walled and logged-in-only sites work, and drops to a **plain HTTP API**
whenever that is actually open. Never types a password itself.

## When to Use

- "Build me a dataset of <query> art from danbooru / yande.re / e621"
- "Harvest images from this artist / this tag on X or Pixiv"
- "Collect reference images for a LoRA / fine-tune"
- "That site blocks curl — get the images anyway"

Don't use for: one-off image downloads (just fetch the URL), text or
video corpora, or anything where the user has not confirmed they have the
right to use the images.

## Loose tagging: why X and Pixiv need a different approach

On a booru `yuri` is a **tag**: ask and you get exactly that. X and Pixiv
have no such guarantee — people post under a ship tag, a fandom hashtag,
or nothing at all. Four mechanisms compensate, and you need all four.

1. **A ranked query plan** (`scripts/queries.py`). One intent becomes an
   ordered list, most precise first — user-supplied ship tags, generated
   character pairs, fandom plus a term meaning two women, then generic
   terms held back. `--aggressive` adds hashtag-compounded forms.
2. **Relaxation.** X ANDs every term, so one extra word can zero out a
   search. A dry query is walked back toward looser forms rather than
   treated as absence.
3. **An adaptive driver** (`scripts/search.py`) that watches yield and
   stops when more scrolling is not worth it, instead of re-issuing dead
   queries.
4. **Visual verification** (`scripts/vision_filter.py`). Search terms are
   never evidence. Candidates from a loosely-tagged source are checked by
   actually looking at them.

Mechanisms 1-3 are described in full under **Loose tagging: why X and
Pixiv need a different approach** below.

## Logins: X will refuse an automated browser

Two things bite here, and they look like separate bugs but are one:

1. **A Playwright launch uses its OWN profile directory.** The user's
   everyday browser being logged in means nothing — the automated browser
   is signed out, every time.
2. **X actively refuses logins from an automated browser.** A correct
   login still bounces to `x.com/i/jf/onboarding/web?...&mode=login`, so
   even a successful sign-in produces a logged-out session.

Both are solved by **driving the user's real browser** instead of
launching one:

```bash
# terminal 1 — opens a real browser on a debug port; log in there by hand
python {baseDir}/scripts/start_browser.py --port 9222 --url https://x.com/home

# terminal 2 — attach to it
python {baseDir}/scripts/harvest.py --sources twitter --cdp http://localhost:9222 ...
```

The browser must be started with `--remote-debugging-port`; `start_browser.py`
does that and verifies the port answers before claiming success. Never close
a browser you attached to — it is the user's window. `Browser.__exit__`
already respects that.

**Detecting login state must require POSITIVE evidence.** Absence of a
login-wall marker is not proof of a session: X redirects an unauthenticated
visit through onboarding URLs that match no marker, so a naive check
reports success on a logged-out page. `logged_in_markers` exist for this —
a session is only confirmed when one of them is present. Marker sets live
on the source class (`login_url_markers`, `login_dom_markers`,
`logged_in_markers`), not hardcoded in the orchestrator.

`harvest.py` runs a **preflight session check** for any source with
`needs_login` and asks before spending queries. Without it, a logged-out X
silently returns zero results and the run reports "found 0" — which reads
as "no art exists" rather than "you are not signed in."

## X quality: engagement beats keywords

Search terms on X say nothing about quality. `--min-likes N` pushes
`min_faves:N` into the search URL (server-side, so junk never reaches the
page) and re-checks the like count on each card. Low-engagement posts are
overwhelmingly reposts, screenshots, memes and unrelated chatter. In
testing this was the single highest-value filter on that site.

## Loose tagging: why X and Pixiv need a different approach

On a booru `yuri` is a **tag**, so asking for it returns exactly that. X
and Pixiv have no such guarantee — people post under a ship tag, a fandom
hashtag, or nothing at all. Three mechanisms compensate, and you need all
three.

### 1. A ranked plan, not one query (`scripts/queries.py`)

`plan()` returns candidates ordered by expected yield, most precise first:

| kind | example | why |
|---|---|---|
| `ship_tag` | `Jinhli` | a pairing name you supplied, used **verbatim** |
| `ship` | `raiden x yae` | a named pairing is almost always fanart of those two |
| `hashtag` | `#Jinhsi #Changli` | aggressive mode; hashtag posts are disproportionately actual fanart |
| `fandom` | `wuthering waves yuri` | fandom plus a term meaning two women |
| `generic` | `yuri` | last resort — lots of results, almost none survive verification |

`--ship-tags "Jinhli,Changli"` beats anything generated, and is never
rewritten: `Jinhli` and `jinhsi changli` are not the same search.
`--aggressive` adds the hashtag-compounded forms.

### 2. Relaxation, because X ANDs its terms (`scripts/queries.py`)

This is measured, not theoretical. On a live session:

```
"wuwa denrika"      ->  5 results
"wuwa denrika art"  ->  0 results      <- one extra word, everything gone
```

So when a query returns nothing, `relax()` walks looser forms rather than
treating it as absence: drop search-boilerplate words (`art`, `fanart`,
`pic`), then trailing words, then hashtags alone, then each term on its
own. `wuwa denrika art` → `wuwa denrika` on the first step.

3. **An adaptive driver that watches yield** (`scripts/search.py`)

`SearchDriver` runs the plan as a feedback loop and decides when to stop:

- a query that yields → move on, keep the rank
- a query that is dry → **relax it and retry before abandoning it**
- three consecutive dry queries → stop; the tail is dry, not the site
- yield decaying well below the best run → stop scrolling for nothing

It dedupes across queries, so a post appearing under three queries is
stored once, and it never decides what content is *acceptable* — that
stays with the vision filter. It only decides where to look next.

Verified live: a plan containing **only** `wuwa denrika art` recovered 2
images by relaxing to `wuwa denrika`.

```bash
python {baseDir}/scripts/harvest.py --sources twitter \
    --ship-tags "Jinhli" --chars "jinhsi,changli" --aggressive \
    --min-likes 500 --vision-gate --pool 30 --out ./ds \
    --cdp http://localhost:9222
```

The run prints what it tried, what came back dry, and why it stopped.
Report that — "found 0" with no explanation is the failure mode this
replaces.

### 4. Visual verification (`scripts/vision_filter.py`)

Search terms are not evidence, however well-ranked. Every candidate from a
loosely-tagged source has to be checked by actually looking at it and
asking how many female-presenting characters are visible and whether two of
them are depicted as a couple.

The default backend is `worklist`, which is the right one in an agent
context and needs no API key: the script emits a list of image paths, **the
agent looks at them with its own vision tool**, then writes verdicts back
and applies them. `openai` and `ollama` backends exist for unattended runs.

## The correct flow for X and Pixiv

Boorus have strict tags; X and Pixiv do not. **A search hit there is not
evidence of content.** Collecting and downloading the first N results
produces group collabs, solo portraits and meme screenshots that all
matched the query.

Use the gate — verify before download:

```bash
harvest.py --sources twitter --fandom "wuthering waves" \
    --chars "jinhsi,changli,yinlin" --min-likes 500 \
    --vision-gate --pool 30 --out ./ds --cdp http://localhost:9222
#   -> queues vision_worklist.json, downloads NOTHING

vision_filter.py --dataset ./ds --backend worklist
#   -> the agent looks at each candidate, writes verdicts.json

vision_filter.py --dataset ./ds --apply verdicts.json --drop
harvest.py --dataset ./ds --download-only    # fetch only the survivors
```

Measured on a real run: **15 candidates, 4 genuinely yuri.** One of the
rejects was a Facebook meme screenshot of a real photograph.

## Interactive setup

`scripts/wizard.py` asks instead of making the user memorise flags —
sources, query, fandom/characters, count, **rating ceiling**, minimum
likes, output path, verify-first, and whether to attach to their browser.
It prints the resulting commands, or runs them with `--run`. It invokes
`sys.executable`, not a bare `python`, so the run lands in the same
interpreter that has Playwright installed.

## The routing rule (the core idea)

Two transports, one normalized output:

| Transport | When | Why |
|---|---|---|
| plain HTTP API | the site answers `/posts.json`-style endpoints to a normal client | fastest, no browser, no memory cost |
| real browser | bot wall (Cloudflare), login wall, or JS-only UI | plain HTTP gets a 403 challenge page and dies |

`auto` sources are **probed** with one cheap request. Open → API. Closed →
browser. If a source passes the probe but then fails mid-run (a TLS
reset, a challenge that appears under load), the harvester **downgrades to
the browser** rather than losing the source.

The browser is not just a fallback for scraping HTML: once it holds the
site's clearance cookies it is used as an **authenticated HTTP client**, so
a Cloudflare-gated booru is still harvested through its own clean JSON API
instead of fragile DOM scraping. Only X and Pixiv genuinely need DOM/DOM-
adjacent work, because they have no public API.

## Prerequisites

**If you are an agent: do this yourself, do not ask the user to.**
Run `scripts/bootstrap.py` first. It is idempotent, it prints the
interpreter path to use, and it needs nothing from the user:

```bash
python {baseDir}/scripts/bootstrap.py
```

It creates the virtualenv (outside the skill folder, so it is never
published), installs the requirements, and verifies the imports actually
work. **Read the `interpreter:` line it prints and use that exact path for
every subsequent command.** A bare `python` resolves to a system
interpreter with no playwright installed, which fails with a confusing
import error rather than anything that points at the cause.

Use `--check` to report status without changing anything, and
`--browser` to also install bundled Chromium (only needed for offline
use — the default `--channel msedge` uses your installed Edge, which has
the better bot-wall pass rate).

If you would rather do it by hand, or bootstrap is unavailable:

```bash
python3 -m venv ~/.cache/art-harvest/venv
~/.cache/art-harvest/venv/bin/pip install -r {baseDir}/scripts/requirements.txt
~/.cache/art-harvest/venv/bin/python -m playwright install chromium
```

On Windows substitute `Scripts/` for `bin/` and `.exe` for none. Note the
venv may have been created by `uv`, in which case it has no `pip` at all —
use `uv pip install --python <venv-python> -r requirements.txt`.

Also required:

**Required:**

- Python 3.10 or newer (built and verified on 3.14; Playwright's bundled
  Chromium is what actually renders the pages).
- `HARVEST_CONTACT` — an email address you actually read. Danbooru and
  e621 ban clients that send no contact info, and a placeholder string
  such as `set YOUR_EMAIL` gets an IP banned rather than a request
  refused. Every API request carries it; the harvester exits rather than
  send an unidentifiable UA.

```bash
export HARVEST_CONTACT="you@example.com"   # bash
$env:HARVEST_CONTACT = "you@example.com"    # PowerShell
```

Optional, and they meaningfully change what you get:

- `DANBOORU_LOGIN` + `DANBOORU_API_KEY` — anonymous users only see a
  fraction of main-site Danbooru results; logged-in search is much wider.
- `GELBOORU_API_KEY` + `GELBOORU_USER_ID` — Gelbooru's API 401s without
  them.
- `HF_TOKEN` — only for publishing.

Nothing here reads a credentials file. Keys come from the environment.

## FIRST: ask the user before running anything

**Do not run a command until the user has answered these.** Use your own
question mechanism — the user is in a chat client and cannot see a
terminal prompt, so `wizard.py` is for a human at a keyboard, not for you.

**Offer every option below, including the ones that need a login.** Do not
present a shortlist of the easy sources: an agent that only offers
`yandere`/`e621`/`safebooru` quietly makes X and Pixiv look unavailable, and
those two are the only sources with art that never reaches a booru at all.

1. **Which sources?** Offer the full list, grouped by whether they need a
   login:

   - *No login, plain HTTP:* `yandere`, `e621`, `safebooru`, `testbooru`
   - *No login, browser (bot wall):* `danbooru`, `konachan`, `gelbooru`
     (Gelbooru's API also 401s without `GELBOORU_API_KEY` + `GELBOORU_USER_ID`)
   - **Needs a human login:** **`twitter` (X)**, **`pixiv`**

   If they name a fandom, `yandere` is the best first choice: it is open and
   it indexes Danbooru's tag vocabulary, so character-tag queries work there
   while `danbooru` itself is usually behind Cloudflare. But X and Pixiv
   reach posts no booru has indexed, so offer them explicitly.

2. **What query or tags?** For a fandom, ask for the fandom plus characters
   (`--fandom "wuthering waves" --chars "jinhsi,changli"`).
3. **Roughly how many images?**
4. **Safe results only, or everything?** Map to a `--rating` ceiling —
   `general` (default), `sensitive`, `questionable`, `explicit`, or `any`.
   Expect *very* low yields at the safe default: a `--tags yuri` run on
   yandere + e621 found 10 and kept 1, because `yuri` there is mostly
   questionable or explicit.
5. **Where should the output go?**
6. **What is it for?** Offer these explicitly — the answer changes what you do
   next, not just the rights conversation:

   - **Train a local LoRA / fine-tune** — the dataset is already shaped for
     it (`images/` + `metadata.jsonl` with a `caption` per row).
   - **Upload it to ChatGPT / OpenAI** — see the ChatGPT section below for
     what that does and does not actually do, and for the account-level
     training setting they must change themselves.
   - **Publish the dataset** (HuggingFace) — read Rights below first; this
     is the one that puts other artists' work in public.
   - **Personal reference or study.**

7. **If X or Pixiv is in scope:** ask whether they have specific ship tags to
   use verbatim, or whether pairings should be generated from a character
   list. Then ask whether they are signed in, because these two cannot work
   without a session — see Logins below for the two-step handshake.

   If they have no specific pairings, **look them up yourself** rather than
   inventing them. Fans tag art with portmanteau ship names — `Jinhli`,
   `Byler`, `Klance` — and those names find more art than combining the
   character names yourself.

   Go straight to `https://shipping.fandom.com/wiki/Category:<Fandom>/Ships/Femslash`,
   which is already filtered to femslash pairings. Do not fetch the series
   page for ships; it is ~290KB and lists every het and slash pairing too.
   `AGENTS.md` has the full lookup table and the gotchas, including the
   `(Fandom)` page-name suffix. Tell the user what you found and where it
   came from.

State their answers back to them, then proceed. The rest of this document
assumes that happened.

## How to Run

```bash
# 1. See which transport each source will use right now
python {baseDir}/scripts/harvest.py --probe --sources danbooru,yandere,e621

# 2. Harvest
python {baseDir}/scripts/harvest.py \
    --sources danbooru,yandere,safebooru,e621 \
    --tags "yuri" --limit 40 --out ./dataset

# 2b. Loose-tagging sites: fan out queries, then verify visually
python {baseDir}/scripts/harvest.py --sources twitter,pixiv \
    --fandom "genshin impact" --chars "raiden,yae" \
    --limit 30 --out ./dataset_x --vision

# 3. Verify what the loosely-tagged images actually contain
python {baseDir}/scripts/vision_filter.py --dataset ./dataset_x --backend worklist
#    ...agent looks at each image in vision_worklist.json, writes verdicts...
python {baseDir}/scripts/vision_filter.py --dataset ./dataset_x \
    --apply verdicts.json --drop

# 4. Package it (writes README card) or publish it
python {baseDir}/scripts/publish.py --dataset ./dataset --mode local
python {baseDir}/scripts/publish.py --dataset ./dataset --mode hf --repo you/yuri-art
```

Sources: `danbooru`, `testbooru`, `yandere`, `konachan`, `safebooru`,
`gelbooru`, `e621`, `twitter`, `pixiv`.

Useful flags: `--headed` (show the browser — needed for logins, and bot
walls clear far more reliably with a visible window), `--channel msedge`
(use an installed real browser instead of bundled Chromium; best pass
rate), `--dry-run` (list without downloading), `--rating` (decide safe
vs everything — see below), `--pages N` (paginate), `--delay 2` (slow
down).

### Deciding safe results or all of them

`--rating` is a **ceiling**, not an exact match:

| Value | Keeps |
|---|---|
| `general` | **default.** safe art only |
| `sensitive` | general + suggestive |
| `questionable` | the above + more |
| `explicit` | everything the site has |
| `any` | no rating limit |

`--rating general` is the default on purpose: asking for explicit art
should be something you type, not something you get by not choosing.

Two things worth knowing before you trust a "safe" run:

- **A source that reports no rating is not asserting its art is safe.**
  Rows with no rating pass any ceiling, because refusing them would empty
  the dataset from every source that omits the field. Run
  `--show-rating-breakdown` and it tells you how many rows that was. If
  the count is not zero, a rating ceiling did not actually constrain
  those rows — use the vision pass instead.
- **`--rating any` still cannot re-admit hard-excluded content.** The
  underage and banned tag filters are separate and unconditional.

`--show-rating-breakdown` prints what the ceiling cost you, kept versus
excluded per band, so "the source had nothing else" is distinguishable
from "the ceiling discarded 400 rows".

## Procedure

1. **Confirm scope and rights with the user.** Which site, which query,
   roughly how many, and whether it is for personal study or for
   something they intend to publish. Do not skip this — see Rights below.
   *Done when: you can state the target sites, the query, and the
   intended use back to them.*

2. **Probe.** Run `--probe` for the chosen sources.
   *Done when: you know which sources are on the API path and which need
   the browser.*

3. **Trial run small.** `--limit 5 --dry-run`, then a real `--limit 5`.
   *Done when: images are actually on disk and `metadata.jsonl` is
   non-empty and parseable.*

4. **Scale up.** Raise `--limit` / `--pages`, keep `--delay` at 1s or more.
   *Done when: the count in `manifest.json` matches the number of files in
   `images/`.*

5. **Report** the count, the per-source breakdown from `manifest.json`,
   and anything in `rejected.jsonl` worth the user knowing.
   *Done when: the user has the folder path and the totals.*

## Logins

**The person using this skill is talking to an agent, not sitting at the
terminal running the script.** So nothing ever prompts on stdin, and
nothing ever blocks waiting for a keystroke. A question printed to a
terminal is a question the user cannot see.

When a source needs a session the harvester opens a **visible** window,
prints a block marked `NEEDS HUMAN LOGIN — relay this to the user
verbatim`, and **exits 2**. The agent copies that into the conversation,
the user signs in and says so in their own client, and the agent re-runs
with `--logged-in`:

```
==================================================================
  TWITTER: NEEDS HUMAN LOGIN
==================================================================
  A browser window is open. Ask the user to sign in at:
    https://x.com/login

  Relay this to the user:
    "A twitter browser window is open at https://x.com/login.
     Please sign in there yourself, including any 2FA or captcha.
     I can't type your password for you. Tell me when you're done"

  Then re-run this harvest with --logged-in, which skips this gate
  and verifies the session before spending any queries.
==================================================================
```

`--logged-in` does not take the claim on trust. It polls for positive DOM
evidence — the `logged_in_markers` on the source class — before spending a
single query, and says so plainly if no session is detectable. This
matters because a logged-out X returns zero results and the run reports
"found 0", which reads as "no such art exists" when the truth is "you
were never signed in".

The skill never asks for, accepts, stores, or types a password, 2FA code,
or verification code. See the CDP section above for why X additionally
needs to be driven through the user's own browser.

`--no-wait` is deprecated and ignored; it exists only so older command
lines still parse.

## Rights, and what "upload for training" can actually mean

Two things to get straight, because the user's mental model is usually
wrong here:

**1. There is no "upload art to ChatGPT so it trains on it."** Consumer
app uploads are not a training intake. The OpenAI API does not train on
customer data unless the customer explicitly opts in. A file sitting in an
account reaches no training pipeline. What actually feeds training is a
*published dataset* that a fine-tune / LoRA run reads — which is why
`publish.py --mode hf` is the real path and `--mode openai-files` is only
remote storage under 30-day abuse-monitoring retention, with every image
classified on submission.

**2. Harvesting is not licensing.** Every image stays the copyright of its
artist. The metadata keeps `page_url`, `file_url`, `artist` and `tags`
precisely so attribution survives — never strip those columns. Republishing
scraped art is a decision individual artists are entitled to object to;
say so plainly rather than presenting a dataset as risk-free. Respect each
site's terms, keep request rates low, and don't republish what a site
explicitly forbids.

### "Just upload it to ChatGPT and let it train on it"

Get the mechanics right, because the intuition is wrong in one direction
and right in another:

- **The ChatGPT web upload is not a training intake you control.** There
  is no button that says "train on this." On a personal account with
  `Improve the model for everyone` enabled, attached files **are eligible**
  to be used to train OpenAI's models — so images can reach the corpus,
  but probabilistically ("may be used"), with no per-file confirmation and
  no artifact returned. OpenAI's own disclosure that agents posted
  user-provided images from training-eligible conversations confirms
  uploads do reach the pipeline.
- **`Improve the model for everyone` is a permission switch, not a
  training trigger.** Turning it ON means your content *may* be used to
  train their models — data flowing out, not a model coming back. On by
  default on personal Free/Plus/Pro; off by default on
  Business/Enterprise/Edu. Temporary chats are excluded; Codex has a
  separate setting; leaving feedback can pull a conversation in even when
  training is off.
- **The Terms do not prohibit automating your own account's input.** The
  prohibition is on *"automatically or programmatically extract data or
  Output"* — extraction, not upload. Don't cite that clause as a bar to
  this.
- **What the Terms do say is a rights warranty:** *"You represent and
  warrant that you have all rights, licenses, and permissions needed to
  provide Input to our Services."* Uploading third-party artwork makes
  that representation. It is the user's call to make about their own
  account — state it once, then respect their decision.

**Never flip a user's account-level training setting on their behalf.**
That changes what happens to *all* their data, not just this batch. Point
at the setting; let them change it.

**What actually trains a model on this art** is a local LoRA / fine-tune
against an open image model. This dataset is already shaped for it:
`images/` plus `metadata.jsonl` with a `caption` per row is the standard
input for kohya-ss / diffusers LoRA training. That works offline, with no
upload and nothing to ban.

### Uploading to the ChatGPT web UI

`scripts/chatgpt_web.py` drives a logged-in browser session to attach
images to a chat and send them.

```bash
python {baseDir}/scripts/chatgpt_web.py --inspect          # dump selectors
python {baseDir}/scripts/chatgpt_web.py --dataset ./ds --dry-run
python {baseDir}/scripts/chatgpt_web.py --dataset ./ds --batch 20 \
    --message "here you go"
```

- Opens `chatgpt.com` in a visible window. **If not signed in, it stops
  and waits** for the human to log in, including 2FA. Nothing is ever
  typed for them. The session persists in
  `~/.cache/art-dataset-harvest/profiles/chatgpt`.
- **Login is two steps, because the person using this skill is talking to
  an agent, not sitting at a terminal.** The script prints a block marked
  `NEEDS HUMAN LOGIN — relay this to the user verbatim`, then exits 2. The
  agent copies that into the conversation, the user signs in and says so in
  their own client, and the agent re-runs with `--logged-in`. Nothing ever
  blocks on stdin, because the user cannot see stdin. `--logged-in` does
  not trust the claim: it polls for positive DOM evidence (the composer)
  before uploading anything, so "I signed in" cannot become a silent
  failure.
- Chunks the dataset into batches of **10**, matching ChatGPT's attachment
  cap, and starts a fresh chat per batch.
- **`--dry-run`** attaches and types but does not click send — use this first.

### The attachment cap is silent, and the script accounts for it

Verified on a Free account: submitting 4 images produced a message with
**2** in it. No error, no warning, no failed send. The cap is per message,
and what gets dropped is decided server-side after the message is accepted.

So the script does not treat a successful send as success. After each
send it counts the images **in the message that was actually posted**
(`sent_image_count()`) and reports the difference:

```
submitted 4 file(s):
  submitted 10 file(s):
images in the posted message: 2/4 submitted
2 image(s) were dropped — account limit.
```

Anything that did not land is listed by filename and, with `--retry-until`,
re-sent on a schedule.

**Do not add a pre-send acceptance count.** There is no composer preview
element to count: an attached image renders no chip, so any pre-send
measurement reads 0 and will be misread as a failed upload. That mistake
was made during development and briefly marked a working feature broken.
Acceptance is only observable after the send.

**`--retry-until` is opt-in and off by default.** It accepts `HH:MM`,
`+90m`, `2 hours`, or an ISO timestamp, and an unparseable value is refused
rather than silently becoming "retry forever". Hammering an account that
just said no can look like abuse, and a plan cap may never lift at all, so
retrying is the user's decision to make, not the script's.

Do not describe this as "training ChatGPT on the images." It uploads
files into eligible conversations; whether they are used is OpenAI's
decision and is unverifiable from outside.

### Verified against both account tiers

The attach and send path has been exercised for real, on **Free and on
Plus**, because they render differently and both have to work.

Findings worth keeping, because each breaks silently rather than loudly:

- **The send control differs by account.** Free exposes
  `[data-testid="send-button"]` on a `<div>`. Plus has no testid at all:
  it is a real `<button type="submit" aria-label="Send">` that only mounts
  once there is something to send. A selector that only handles one of
  them silently falls through to a guess.
- **`#prompt-textarea` is not always present.** It exists on a Free
  conversation view but not on a fresh new-chat page. The contenteditable
  ProseMirror div is present in both and is the reliable session marker.
- **There are several file inputs, and some only mount later.**
  `#upload-photos` / `#upload-media` appear after clicking "Add files and
  more", so selecting them by name breaks on a fresh page. Match
  `input[type="file"]`.
- **`set_input_files` works.** Clicking the plus menu or synthesising a
  paste is unnecessary; both were tried and neither is needed.
- **An attached image renders as a `data:` URL preview** in the composer,
  which makes a pre-send check possible.
- **The account cap is silent.** A Free account took 2 of 4 images with no
  error and a normal-looking message.

### How delivery is verified, and why

There is **no stable selector for a ChatGPT turn** — every ancestor of an
uploaded image is a bare `<div>` with no `data-testid`, no
`data-message-id`, and no role. So the check does not scope to "the last
message". Instead it measures a **delta**: content images before the send
minus content images after, with avatars filtered out by src.

Two rules make that trustworthy, and both were learned by breaking them:

1. **Take the baseline BEFORE attaching.** Taken after, it already
   includes the composer's own preview, the delta comes out ~0, and a
   perfectly good upload is reported as a total failure.
2. **An unmeasurable result is never a success.** If the count cannot be
   read, the script reports *unconfirmed* and exits `5`. Laundering a
   failed measurement into a pass is how a message with nothing attached
   was reported as `1/1 sent`.

Because the check is a page-wide image delta, it cannot distinguish "the
cap dropped it" from "the upload failed". Both mean an image is missing;
open the conversation to tell them apart.

Re-run with `--inspect` if markup drifts; `--file-input` / `--composer` /
`--send-button` override anything.

### Attaching to a browser you already have open

`--cdp http://localhost:PORT` attaches instead of launching. Needed when
the profile is already held by a running browser, which otherwise fails
with *"Opening in existing browser session"*. The attached window is never
closed — it is the user's.

Note that attaching uses **whatever tab is already open**. Open a fresh
new-chat tab first, or the batch is appended to an unrelated conversation.

## Safety rules — not configurable

`scripts/normalize.py` filters every item, before download and regardless
of `--rating`:

- any tag matching the underage set (`loli`, `shota`, `child`, `toddler`,
  `aged_down`, ...) is dropped and logged to `rejected.jsonl`
- a banned set (guro, snuff, bestiality, necrophilia, scat, ...) is dropped
- downloads under 512px on either side or under 20KB are rejected as
  thumbnails or corrupt files

These are code, not flags. Do not add a bypass flag when a user asks for
one — if they want them changed, they edit `normalize.py` deliberately.

The filters run on **every** path that can put an image on disk, not just
at harvest time. `--download-only` re-applies them to whatever is already
in `metadata.jsonl` before fetching anything, because that file is
editable and mergeable — it can hold rows written by an older version of
this script, or by hand. `--rating` narrows results; it can never widen
them past the hard excludes.

`rejected.jsonl` records `page_url`, `artist` and the full tag string for
excluded items. That is a local audit trail and is **never published**:
`publish.py` uploads `images/`, `metadata.jsonl`, `manifest.json` and
`README.md` only. Republishing the provenance of rejected content would
defeat the point of rejecting it.

`--rating` is separate from these and **does not widen** them. It can only
narrow further. `--rating any` means "no rating ceiling", not "no
filtering".

## What lands on disk

```
dataset/
  images/              one file per row
  metadata.jsonl       one JSON object per image
  manifest.json        query, per-source counts, transports used
  rejected.jsonl       what was filtered and why  (audit trail)
  vision_worklist.json images awaiting visual verification (x/pixiv only)
  README.md            dataset card with provenance
```

Each row carries `file_name` (dataset-relative path) and `caption`
(space-joined tags), so HuggingFace `imagefolder` and most caption-
conditioned trainers read the folder as-is.

## Pitfalls

- **Cloudflare is the norm, not the exception.** Danbooru, Konachan and
  Gelbooru all 403 a plain client with `Cf-Mitigated: challenge`. That is
  expected; the probe reports it and the browser handles it.
- **`testbooru.donmai.us` is the Danbooru schema with no Cloudflare.**
  Use it to validate a new parser before hammering the real site.
- **Pixiv originals 403 without a Referer.** The harvester routes
  pixiv downloads through the browser context for this reason; don't
  "simplify" that away.
- **A transient TLS reset is not a bot wall.** `http_json` retries
  transport errors but treats 401/403/429 as definitive. Keep that
  distinction — conflating them sends healthy sources onto the slow path.
- **`--channel msedge` beats bundled Chromium** for passing bot walls and
  is the default; pass `--channel ""` to force bundled Chromium.
- **Not every probe failure means the browser will work.** Gelbooru's
  `/index.php?page=post` is HTML, so the browser yields HTML, not JSON.
  That source needs API credentials; login alone will not fix it.
- **e621 and Danbooru require a real User-Agent with contact info.**
  Default library UAs get banned, and so does a placeholder address.
  `HARVEST_CONTACT` is required; the harvester refuses to run without it.
- **`--download-only` re-applies the safety filters.** `metadata.jsonl` is
  an ordinary editable file. Do not "optimize" that path by skipping
  `filter_rows()` — the filters must hold at the moment bytes hit disk.
- **`rejected.jsonl` is append-deduped, not appended blindly.** Resuming
  a gated dataset will re-fail the same rows; merging is keyed on record
  identity so the audit trail does not grow N copies of one failure.
- **Never trust a query term as evidence on X or Pixiv.** A search for
  `yuri` there returns solo portraits, group shots and unrelated art. Run
  `vision_filter.py` and only keep images that survive it. Reporting an
  unverified harvest as "yuri art" is wrong, not merely imprecise.
- **The vision `worklist` backend is two steps, not one.** Emitting the
  worklist verifies nothing; the images are only filtered after verdicts
  are applied with `--apply`. Skipping the second step silently keeps every
  candidate, including the ones that failed the look.
- **`--drop` is required to actually remove failures.** Without it,
  verdicts are recorded but nothing leaves `metadata.jsonl` — deliberate,
  so a bad batch of verdicts is recoverable.

## Verification

The test suite runs offline and needs no network:

```bash
python {baseDir}/tests/test_harvest.py -v
```

It covers the safety filters on every code path, the rejected-row dedupe,
manifest writing for both the gated and downloaded shapes, the
`--out`/`--dataset` alias, the publish allowlist, the UA requirement, the
ranked query plans, relaxation, the rating ceiling, and the ChatGPT limit handling.

To check a folder that already exists — the four checks below, run for you:

```bash
python {baseDir}/tests/verify_dataset.py ./dataset
```

One test hits the network and is skipped unless asked for:

```bash
HARVEST_LIVE=1 python {baseDir}/tests/test_harvest.py -v
```

That one is the four checks below, executed against `testbooru`, which is
the Danbooru schema with no Cloudflare — validate a new parser there
before touching the real site.

```bash
python {baseDir}/scripts/harvest.py --sources testbooru --tags yuri --limit 3 \
    --out /tmp/verify
```

Then check all four, and say what you found:

1. `images/` holds 3 non-empty files
2. `metadata.jsonl` has 3 lines, each valid JSON with a `file_name` that
   exists on disk
3. `manifest.json` `total_images` equals the file count in `images/`
4. no row exceeds the `--rating` ceiling (`unknown` excepted, and
   `--show-rating-breakdown` says how many that was), and `rejected.jsonl`
   explains the rest

A run that writes rows but no images, or images but no rows, is a failure
— not a partial success.


