# Script usage

Set `S` to the `scripts` directory inside the skill directory before the commands below.
SKILL.md explains where that directory is, under "Where the scripts are".
All browser scripts use headless Python Playwright.
On an 8GB machine, run one at a time.

**Steps files** (shared by layout_check states, record_moment, and sound_levels)
are a JSON array, one action per item:
`{"click": selector}`, `{"hover": selector}`, `{"fill": selector, "value": text}`,
`{"press": "Enter"}`, `{"scroll": pixels}`, `{"js": code}`, `{"wait": ms}`,
`{"wait_for": selector}`.
Clicks go to the first visible match.

## Layout check: layout_check.py

```bash
python3 $S/layout_check.py URL \
  --widths 375,768,1024,1280,1440 \
  --out DIR \
  [--keep name=selector] \
  [--states states.json] \
  [--slices 8] \
  [--forbid "—,–"] \
  [--clock 2026-11-09T12:30]
```

- Takes a full-page screenshot at each width and checks horizontal overflow,
  elements off screen, clipped outlines and shadows, truncated text, h1 over
  2 lines, console errors, broken images, and failed requests (analytics and
  ad requests ignored). Writes `report.json`.
- `--keep` measures key elements in the first screen. Outside the first
  screen, or covered by a banner or overlay, fails. It prints a y-value table
  per width. Run pages with different key elements separately. For laptop
  screens add `--widths 1536 --height 864` and `--widths 1280 --height 800`.
- `--states` checks states after interaction. Each item is
  `{"name", "url", "steps"}`. The script clicks there at every width and
  checks again.
- `--slices 8` writes one image per screen, for reviewers and the anchor set.
  `--forbid` lists strings that must not appear. `--clock` freezes the clock
  so greetings and opening hours give the same result every run.
- Three report-only fields do not fail the run: `smallTargets` (hit area under
  44px, counting absolutely positioned `::before` / `::after`, phone widths
  only), `smallVisible` (visible size under 44px with a big enough hit area),
  `smallText` (rendered size, ancestor scaling included, under 12px). On
  scaled canvases all three count as failures.
- Every `clipped` entry carries `over` (pixels past the edge) and `kind`.
  `shadow` means only the outline or shadow crosses, usually invisible at a
  few pixels. `box` means the element itself crosses, including intentionally
  cropped images. Elements under a zero-opacity ancestor and 1px
  screen-reader text are skipped.
- Check every reported item. For anything you call a false positive, write one
  line why. A whole interface inside a frame that scrolls sideways is only
  checked at its design width.

## Site assets: asset_check.py

`python3 $S/asset_check.py SITE_DIR [--skip subdir]`

No browser. Checks that every local file referenced by each HTML and CSS file
(`src`, `srcset`, `href`, `poster`, `url()`) exists on disk. Exit code 1 if
anything is missing. The layout check only covers pages it opened. This covers
the whole site in seconds.

## Review snapshot: snapshot.py

```bash
python3 $S/snapshot.py REPO SITE_DIR SNAPSHOT_DIR \
  [--ref HEAD] \
  [--overwrite] \
  [--link path-in-snapshot=real-path] \
  [--skip subdir]
```

Exports from a commit only (`git archive`), then runs asset_check. The
uncommitted-files check runs for every `--ref`, not only `HEAD`. Large files
kept out of git are symlinked in with `--link`. Projects with a build step
build from a clean checkout instead.

The archive is extracted into a fresh temporary directory and then moved to
`SNAPSHOT_DIR`. That path must not already exist. It must not overlap the
repo, the home directory, or the filesystem root, and it must not be a
symlink. The tool does not follow symlinks. Pass an absolute path outside
those places, for example under the system temp directory, that does not
exist yet.

`--overwrite` replaces a directory only when it contains the marker file
`.award-polish-snapshot` written by an earlier run of this tool. Any other
existing directory is left untouched.

## Signature moment frames: record_moment.py

`python3 $S/record_moment.py URL --steps steps.json --out DIR --every 40 [--phone]`

Add `"frames": 800` (milliseconds to record) to the step to record, and
optionally `"name"`. A virtual clock drives JS and CSS animations, so a busy
machine drops no frames. Writes `contact-NN.png` (each frame labelled in ms),
`animations.json` (duration, easing, delay, View Transition pseudo-elements
included), and `motion.json` (from which ms to which ms the picture moves).
Warns when the last frame is still moving, meaning `frames` is too short.

## Sound levels: sound_levels.py

`python3 $S/sound_levels.py URL --steps steps.json --out levels.json [--phone] [--fake-mic]`

Taps the WebAudio output with a probe (test browser only) and records each
step's peak level (0 silent, 1 full scale) and played media files. Steps may
add `"label"` and `"listen"` (ms to listen, default 700). `wait` and
`wait_for` only wait and are not measured. The browser creates audio on the
first click, so start with a warm-up click. `--fake-mic` feeds a test tone as
the microphone with permission granted.

## Review prompts: review_prompt.py

```bash
python3 $S/review_prompt.py \
  --config review.json \
  --anchor-shots ANCHOR_SCREENSHOTS \
  --current CURRENT_SCREENSHOTS \
  --round ROUND_DIR \
  [--best BEST_SCREENSHOTS] \
  [--live-best BEST_URL] \
  [--reviewers N]
```

Copies the screenshot sets into the round directory under names that do not
reveal their source, randomly assigns A/B and C/D per reviewer, and writes
the prompts and the mapping `blind.json`. By default, `--reviewers` is 2 and
the two-reviewer workflow uses `prompt-r1.md` and `prompt-r2.md`. Counts below
2 are rejected. For higher counts, the script writes one prompt per reviewer,
from `prompt-r1.md` through `prompt-rN.md`. The config is copied from
`templates/review.json`. The template is
`templates/REVIEW_PROMPT.md`, and review rules change only there.

## Scoring: calibrate.py

```bash
python3 $S/calibrate.py \
  --round ROUND_DIR \
  --anchor anchor.json \
  --model "MODEL EFFORT" \
  [--best best.json] \
  [--save best.json] \
  [--live-anchor]
```

Finds the anchor set via `blind.json`, calibrates each item (at most ±1 by
default; with screenshots only, motion, micro-interactions, usability, and
retention are not calibrated unless `--live-anchor`), averages, decides by
the C/D blind comparison, and prints a last line ready for the log. `--save`
writes `best.json` only on "new best version". **Keep the algorithm fixed
within a round**: copy the script into the project's work directory at
kickoff and use that copy for the whole round.

## Before/after: side_by_side.py

```bash
python3 $S/side_by_side.py \
  --urls "Before=URL" "After=URL" \
  [third column] \
  --pages / KEY_PAGE \
  --widths 1440,375 \
  --out DIR \
  [--dismiss BANNER_CLOSE] \
  [--clock ...] \
  [--full]
```

Each column gets a fresh browser context. The same page and width are
screenshotted and stitched with labels. URLs may include a subpath
(`http://localhost:8790/a/`). To stitch existing images:
`side_by_side.py img1 img2 --labels Before,After --out x.png`.

## Search fields: seo_keep.py

`python3 $S/seo_keep.py --base LIVE_URL --new LOCAL_URL --pages PAGE [more pages] [--sitemap N] [--files /robots.txt /sitemap.xml] [--dump refs/seo-baseline.json]`

Compares title, description, canonical, hreflang, robots, structured data
types, H1, lang, and share card fields page by page. Any difference exits
with code 1. `--dump` saves the base fields as the search baseline. The path is
relative and must stay inside the repo or the working directory. Absolute
paths and `..` are refused.

## Wait for release: wait_live.py

`python3 $S/wait_live.py URL --has NEW_TEXT [--gone OLD_TEXT] [--timeout 1500]`

Opens the page with a fresh `?v=` each round and checks the page plus the
stylesheets and scripts it references, so a CDN still serving old CSS is
caught. `NEW_TEXT` is a string only the new version has.

## Split commits: split_commits.py

For when polish changes piled up in the working tree. The normal way is to
commit each change right away. This optional helper splits that pile into one
reviewable commit each. The split is a JSON file:

```json
{
  "ctx": {"styles.css": 1},
  "items": [
    {"name": "hero", "msg": "commit message", "hunks": {"src/site.js": ["keyword"], "pages/*/index.html": ["keyword"]}},
    {"name": "palette", "msg": "...", "files": ["assets/raw"]},
    {"name": "stamps", "msg": "...", "files": ["pages"], "only": "?v="}
  ]
}
```

- `hunks`: a hunk belongs to this item when any added or removed line contains
  a keyword. Paths with `*` are globbed. `files`: whole files or directories
  for this item.
- `only`: after staging, every added or removed line must contain this string,
  otherwise the commit is refused. Put site-wide changes like asset
  fingerprints last and guard them with it.
- `ctx`: context lines, default 3. Use 1 when changes are a line or two apart.
  Never 0. When part of a zero-context diff is staged, git apply places later
  hunks at stale line numbers.
- `python3 $S/split_commits.py REPO split.json plan` lists hunks with no owner
  or two owners. Adjust keywords until everything is clear, then
  `run [--dry] [--items a,b] [--sign "Co-Authored-By: ..."]` commits item by
  item. Paths in the split stay inside the repo. Pick keywords that belong to
  one item only. A class name several items share puts a hunk in two items.
