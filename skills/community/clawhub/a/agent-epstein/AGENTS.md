# AGENTS.md — AgentEpstein

Working notes for whoever (human or agent) touches this skill. Read
`SKILL.md` for what it does; this file is for how it is worked on.

## Run it

```bash
python scripts/bootstrap.py        # FIRST. Prints the interpreter to use.
```

`bootstrap.py` creates the venv, installs deps, and verifies imports. Read
the `interpreter:` line it prints and use that exact path for everything
else — a bare `python` resolves to a system interpreter with no playwright
and fails with an import error that points nowhere useful.

```bash
PY=<the interpreter bootstrap printed>
$PY tests/test_harvest.py                 # 63 tests, offline, ~0.4s
HARVEST_CONTACT=you@example.com \
HARVEST_LIVE=1 $PY tests/test_harvest.py # adds one live testbooru run
```

`HARVEST_CONTACT` is **required**. There is no default and the harvester
exits rather than send a placeholder UA — Danbooru and e621 ban clients
without a contact address, and a fake one gets an IP banned rather than a
request refused.

A venv created by `uv` has no `pip` at all. `bootstrap.py` handles that
(uv → ensurepip → pip order); do not assume `pip` exists when debugging.

## Constraints — do not break these

- **Safety filters in `normalize.py` are code, not flags.** The underage
  and banned tag sets and the 512px/20KB floors apply on every path that
  writes an image, including `--download-only`. No bypass flag, ever. If
  the user wants them changed they edit that file deliberately.
- **Never type, request, store or accept a password, 2FA or verification
  code.** Open a window, tell the human, wait for them.
- **Never close a browser you did not open.** `Browser.__exit__`
  disconnects on CDP attach; that is the user's window with their tabs in
  it. The same applies to a browser we *did* open but handed over
  mid-run: the ChatGPT login gate sets `br.keep_open = True` so the window
  it tells the user to sign into survives the exit that follows the
  prompt. Without it `__exit__` called `ctx.close()` and the gate could
  never be satisfied — reported as "u closed the browser how do i login".
- **Never flip the user's account-level ChatGPT training setting.** Point
  at it; they change it. It governs all their data, not one batch.
- **Keep the attribution columns** — `page_url`, `file_url`, `artist`,
  `tags`. Stripping them turns a research artifact into a rights problem.

## When something breaks: diagnose, then fix — do not just report

ChatGPT is a moving target, and this skill drives its UI. It broke twice in
one session in ways that all *looked* fine from the console. So:

**A claim in this file that the code works is a claim about a specific
version of someone else's UI, and it expires without warning.** If a
reported success is contradicted by the screen, the screen is right.

When a step in this project breaks:

1. **Reproduce and observe before theorising.** Open the page, screenshot
   it, dump the DOM. Do not infer why it failed from a stack trace.
2. **Derive selectors from a case that is known to work, never guess.**
   A guess that looks plausible costs a full round trip and can report
   success while doing nothing. Two of the three worst bugs here were
   "plausible selector" bugs.
3. **Never let an unmeasurable check read as success.** If a
   measurement fails, report *unknown* and exit non-zero. Laundering
   `-1` into "probably fine" is how a message with no attachment was
   reported as `1/1 sent`.
4. **Fix it, then leave a note where the next reader will hit it.** Each
   comment in this codebase that sounds defensive exists because someone
   lost time to that exact failure. Add one for the new one.
5. **Add a test that fails before the fix and passes after.** The suite
   exists to stop a "fixed" bug from being reintroduced.

Prefer fixing in `scripts/` over adding a flag. Prefer a new candidate at
the *front* of an existing selector tuple over replacing the old one —
Free and Plus accounts render differently and both must keep working.

Known-likely-failure list, in the order it tends to break:

- ChatGPT composer markup (attachment preview, send control, login
  marker). Check both a Free and a Plus account if you can.
- `article` / `[data-message-author-role]` do not exist on ChatGPT turns;
  do not reintroduce selectors that rely on them.
- Cloudflare clearance expiring mid-run → the browser silently degrades to
  HTML where JSON was expected. `--probe` before blaming the parser.
- X DOM: `[data-testid="tweet"]` and the media `img` selectors move.
- Sites dropping fields from their JSON (`file_url`, `md5`, `rating`).
  Records must degrade, not crash.

## Verified working, with the evidence

Do not re-litigate these. Each was checked against a live service, not
inferred, because several plausible-looking things here are broken.

- **X search, end to end.** `SearchDriver` recovered 2 images from the
  single query `wuwa denrika art` — which returns 0 on its own — by
  relaxing to `wuwa denrika`, which returns 5.
- **ChatGPT attach and send**, on both Free and Plus tiers, which render
  different markup. Checked twice per batch: a composer preview must
  appear after attaching, and the delivered count is a page-wide image
  delta taken after the send.
- **ChatGPT upload over CDP, end to end.** 60 images, 6 batches, 43
  confirmed delivered and 17 dropped by the account cap — reported from
  the measured count, not from the send succeeding. See the CDP section
  above for the launch-and-attach recipe.
- **Shipping Wiki lookups.** `Category:<Fandom>/Ships/Femslash` returns
  real pairings — 138 for Genshin Impact.
- **Danbooru past Cloudflare** and its hotlink-protected CDN, alongside
  e621, safebooru and testbooru on plain HTTP, in one 12/12 run.
- **The rating ceiling actually bites.** `--tags yuri` on yandere + e621
  found 10 and kept 1 at `general`; `--rating any` kept all 10.
- **Merging, not clobbering:** a second harvest into the same `--out`
  merges rather than overwrites, and `rejected.jsonl` does not duplicate
  across resumes.

## Getting real ship names: the Shipping Wiki

Do not invent pairings by combining character names. Fans use portmanteau
ship names — `Jinhli`, `Byler`, `Destiel`, `Klance` — and those names are
what people actually tag their art with. Searching `"jinhsi changli"` finds
less than searching `"Jinhli"`.

**Look them up before running a harvest.** This is your job, not the
script's: the skill deliberately does not scrape wikis, because it has web
access and can read a page faster and more reliably than a scraper can.

Base URL: `https://shipping.fandom.com/wiki/`

**Prefer the per-fandom femslash category.** It is the single most useful
URL here, because it is already filtered to the pairings this skill wants:

```
https://shipping.fandom.com/wiki/Category:<Fandom>/Ships/Femslash
```

Verified: `Category:Genshin_Impact/Ships/Femslash` returns 138 pairings.

| I have | Fetch |
|---|---|
| a series, want its femslash ships | `.../wiki/Category:<Fandom>/Ships/Femslash` |
| a series, want everything | `.../wiki/<Series_Name>` (spaces → `_`) |
| a character | `.../wiki/<Character_Name>` |
| every femslash ship on the site | `.../wiki/Category:Ships/Femslash` |
| the fandom is unknown | `.../wiki/Fandoms_A-B` (…`_N-R`, `_S-Z`) |

**Do not fetch the series page to get ships.** It is enormous — the
Genshin page is ~290KB because it lists 170 het and 103 slash pairings
alongside the 138 femslash ones. Go straight to the Femslash category.
The series page is only worth fetching for the "Popular Ships" box, which
is a short handful of names.

**Gotchas that cost a wasted round trip:**

- Page names do not always match the series name. Several carry a
  `(Fandom)` suffix — `Harry Potter (Fandom)`, `Sonic the Hedgehog
  (Fandom)`. If a fetch 404s, retry with the suffix before concluding the
  fandom is absent. Many fandoms simply are not there; newer games often
  are not.
- If the series page has no ship list, fetch the two character pages
  instead — character pages list their pairings.
- **Read the character pair, not just the ship name**, and keep only pairs
  that could be the content the user wants. For yuri art that means
  femslash pairs; drop the M/M and het entries. The category page gives
  you ship names, not genders — a femslash category entry is reliable, but
  cross-check anything ambiguous against the pairing description.
- A fandom's own wiki (`wutheringwaves.fandom.com`) usually has a better
  and more current pairing list than the Shipping Wiki does. Try it when
  the Shipping Wiki has nothing.

Then pass what you found as `--ship-tags`, verbatim:

```bash
python scripts/harvest.py --sources twitter \
    --ship-tags "Jinhli,Changli" --chars "jinhsi,changli" --aggressive ...
```

Tell the user which pairings you found and where they came from, so a bad
lookup is visible rather than silently narrowing the search.

## Never block on stdin

The user is in a chat client talking to an agent. They cannot see a
terminal prompt. Every login gate prints a block marked
`NEEDS HUMAN LOGIN — relay this to the user verbatim` and **exits 2**;
the agent relays it and re-runs with `--logged-in`. `--logged-in` verifies
the session by polling for positive DOM evidence rather than trusting the
claim. Do not "improve" this by adding a blocking `input()` — an earlier
revision did and it hung until timeout, then reported a state
indistinguishable from "the user never signed in".

## ChatGPT: attach over CDP, do not launch and hand over

**The login gate is not usable as written.** It prints the prompt and
exits, and `keep_open` does not save it: the process exiting tears down
the Playwright transport, and the browser dies with it regardless of what
`__exit__` was told to do. Observed twice — "u closed the browser how do
i login". `keep_open` is correct but it is not the fix; do not credit it
with being the fix.

Launch the browser yourself, detached, and attach to it. A browser owned
by neither script survives both scripts exiting.

```bash
# 1. Launch detached. No --wait: it blocks, and killing the parent that
#    spawned Edge takes Edge with it (observed: no port, no process).
"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.cache/art-dataset-harvest/profiles/cdp" \
  --no-first-run --no-default-browser-check https://chatgpt.com/ &

# 2. The user signs in in that window. Nothing is typed for them.
# 3. Attach. --logged-in still verifies a real session before uploading.
python scripts/chatgpt_web.py --dataset <ABSOLUTE PATH> \
  --cdp http://localhost:9222 --logged-in --batch 10
```

Gotchas that each cost a round trip:

- **`--dataset` resolves against cwd**, so `denia-yuri` run from the repo
  root fails with "no metadata.jsonl" when the dataset lives elsewhere.
  Always pass an absolute path.
- **`start_browser.py --browser` wants a binary path, not a channel
  name.** `--browser msedge` exits with "no such browser: msedge".
- **Default CDP port is 9222.** Probing 9223 finds nothing and looks
  like the browser failed to start.
- **Confirm the session instead of asking twice.** Attach over CDP, read
  `#prompt-textarea`, and report what tier is signed in. Asking the user
  to confirm a login that already happened wastes their time.

Verified end to end: 60 images, 6 batches, **43 confirmed delivered,
17 silently dropped by the account cap** — including explicit-rated
images, so the drops were count-based, not a content refusal. Re-run the
remainder with a smaller `--batch`.

## Verify before claiming

Every claim in `SKILL.md` about a working code path was checked against a
live session, because several plausible-looking things are quietly broken:

- The ChatGPT **send button is a `<div>`**, not a `<button>`. A selector
  written as `button[data-testid="send-button"]` matches nothing and
  raises *after* images are attached and the message typed.
- `[data-testid="profile-button"]` and `#history` **do not exist** on
  current ChatGPT markup. `#prompt-textarea` is the reliable session
  marker.
- There are **five file inputs** on the ChatGPT composer; two only mount
  after clicking "Add files and more". Match `input[type="file"]`.
- A **capped account drops attachments silently.** A Free account sent 2
  of 4 images with no error and a successful-looking message. The send
  succeeding is not evidence the images arrived.
- **There is no composer preview element to count.** An earlier revision
  counted "attachment chips", always got zero, and concluded attaching was
  broken — on a feature that works. Measure acceptance *after* the send
  with `sent_image_count()`. A test now asserts those helpers stay deleted.
- **Danbooru and e621 403 a plain client** (Cloudflare) and **Gelbooru
  401s** without credentials. `yandere` is open and indexes Danbooru's tag
  vocabulary, so it is the best booru for character-tag queries when the
  main sites are walled.
- **A venv may have no `pip`.** Built by `uv`? `pip list` then fails and a
  pip-based dependency check reports everything MISSING on a healthy
  environment. Ask the interpreter to import the module instead.
- **Default arguments bind once.** `def f(root=VENV)` ignores a later
  `VENV = other`, so a test that reassigns it silently checks the original
  directory. Resolve module state at call time.

When a path is unverified, `SKILL.md` says so. Keep that honest — several
"known limitations" listed in an earlier handoff turned out to be either
already fixed or never true.

## Style

Comments explain *why*, especially why a non-obvious thing is done the
odd way. Several exist to stop a future reader from "simplifying" a fix
back into a bug; each one names the bug it prevents.

No comments that restate the code. No emojis. British-leaning spelling in
prose.

## Still outstanding

- **`--mode lora`.** Emit a ready-to-run LoRA config from
  `metadata.jsonl`: base model, caption format, resolution buckets, steps,
  learning rate. This is the piece that turns a dataset into a model, and
  it is the last thing between this skill and its actual purpose.