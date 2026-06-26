# Run layout — one directory per lookbook, never share

**Every lookbook generation lives in its own dedicated directory.** No cross-lookbook reads, no reused images, no mixed picks/configs. The convention exists because an agent that reuses files across lookbooks ships mismatched imagery — last week's try-on photos with this week's product list — and the customer can't tell from the rendered HTML that anything's wrong.

This doc is short on purpose. The canonical layout, the hard rules, and the marker file that lets the build script enforce isolation.

## Canonical layout

Every run is rooted at:

```
~/.buck-mason-stylist/runs/<lookbook_id>/
```

`<lookbook_id>` is unique by construction — `<YYYY-MM-DD>-<short-slug>` (e.g., `2026-05-09-mellow-la`, `2026-05-16-weekly`). Two runs **never** share a `lookbook_id`. If the customer asks for "another LA mellow weekend lookbook today," that's a NEW id like `2026-05-23-mellow-la-2`.

Inside each run directory:

```
~/.buck-mason-stylist/runs/<lookbook_id>/
├── config.json                  # build-html-lookbook.py inputs (title, looks meta, page_url)
├── picks.json                   # resolved SKUs + variants (per piece, per look)
├── candidates.json              # OPTIONAL — output of discover-weekly-candidates.py
├── looks/                       # gpt-image-2 outputs (Premium tier only)
│   ├── .lookbook_id             # marker file: contains the lookbook_id string
│   ├── look1.png
│   └── look2.png
├── deploy/                      # build-html-lookbook.py output
│   ├── .lookbook_id             # marker, written by the build script
│   ├── index.html
│   ├── look1.jpg
│   ├── look2.jpg
│   ├── og.jpg
│   └── thumb-<id>.jpg
└── summary.md                   # headless-mode run summary
```

## Hard rules

1. **Each lookbook gets a fresh run directory.** `mkdir -p ~/.buck-mason-stylist/runs/<lookbook_id>/{looks,deploy}` at the start of the run; never operate inside an existing run dir for a different lookbook.

2. **Reference photos come from `profile.md → reference_photos[]` only.** They are absolute paths the agent reads each time. **Never** consume reference photos from `~/.buck-mason-stylist/runs/<other_id>/` — that's other-lookbook state. Even if the photos look right.

3. **Try-on PNGs are per-lookbook artifacts and never carry across runs.** A new lookbook regenerates them via gpt-image-2 (or skips to the Editorial tier when the OpenAI key is missing). If the agent finds a `looks/look1.png` already in the new run dir, that's only valid when its sibling `looks/.lookbook_id` matches the current `<lookbook_id>` — see the marker convention below. Otherwise the file is from a botched prior run and should be deleted, not consumed.

4. **The only cross-lookbook state is `~/.buck-mason-stylist/wishlist.jsonl`.** Read it for dedup (newsletter / re-propose check) and append to it after a successful run. Nothing else crosses run boundaries.

5. **Each Cloudflare Pages project is one-to-one with a permanent `lookbook_id`.** See `references/hosting-options.md` § "URL stability." `--no-overwrite` on `scripts/deploy-lookbook.sh` enforces this for production runs.

6. **Run dirs are append-only within a run.** Never mutate a closed run dir to fix something — generate a new lookbook with a new id and let the customer reach for the latest.

## The `.lookbook_id` marker

A one-line text file containing the run's `<lookbook_id>` string, written into both `looks/` and `deploy/` subdirectories. Purpose: let downstream scripts verify they're consuming THIS run's artifacts and not stale ones from a prior run that happens to be in the same parent dir.

**Who writes it:**

- `looks/.lookbook_id` — written by the gpt-image-2 generation step (or whoever places try-on PNGs in `looks/`). The agent's image-gen orchestrator writes the marker after the last `look<N>.png` lands.
- `deploy/.lookbook_id` — written by `scripts/build-html-lookbook.py` on successful build.

**Who reads it:**

- `scripts/build-html-lookbook.py` — refuses to consume `--look-images <dir>` if `<dir>/.lookbook_id` exists and doesn't match the config's `lookbook_id`. Missing marker = warning, not abort (manual / curated images may not have one).
- `scripts/deploy-lookbook.sh` — reads `<deploy-dir>/.lookbook_id` and uses it (when set) to derive the project name pattern, so the URL stability guarantee composes cleanly.

**What "doesn't match" looks like in practice:**

```
$ python3 scripts/build-html-lookbook.py \
    --config 2026-05-16-weekly/config.json \
    --picks  2026-05-16-weekly/picks.json \
    --look-images 2026-05-09-mellow-la/looks/ \   # ← oops, wrong run
    --out    2026-05-16-weekly/deploy/

error: --look-images directory has .lookbook_id "2026-05-09-mellow-la"
       but the config is for "2026-05-16-weekly".
       Either generate fresh look images for this lookbook (Premium tier),
       skip them with --no-tryon (Editorial tier), or fix the path.
```

That's the failure mode the marker prevents. Without it, the build proceeds silently and ships mismatched imagery.

## Quick checklist before a new run

The agent walks this in order at the top of every lookbook generation:

- [ ] Pick a unique `lookbook_id` (`<YYYY-MM-DD>-<slug>`). Verify it's not already a directory under `~/.buck-mason-stylist/runs/`.
- [ ] `mkdir -p ~/.buck-mason-stylist/runs/<lookbook_id>/{looks,deploy}`.
- [ ] Reference photos from `profile.md` only; absolute paths, freshly resolved.
- [ ] `runs/<other_id>/` directories are read-only background — never `cp` or symlink into the new run.
- [ ] The wishlist (`~/.buck-mason-stylist/wishlist.jsonl`) is the only acceptable cross-run read.

## Composition with other docs

- `references/headless-mode.md` § "Recurring weekly newsletter" — the canonical invocation already uses `runs/<lookbook_id>/` paths; this doc is the why.
- `references/hosting-options.md` § "URL stability" — the matching guarantee on the deploy side: per-lookbook directory + per-lookbook Pages project = permanent URL the customer can revisit.
- `scripts/build-html-lookbook.py` — enforces the marker check.
- `scripts/deploy-lookbook.sh` — composes with the marker via `--no-overwrite` for production runs.
