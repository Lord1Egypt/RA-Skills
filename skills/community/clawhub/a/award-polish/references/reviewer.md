# Independent review: how to run it and keep it strict

After every batch, and before finishing, start **fresh** subagents as reviewers (2 of them, each scoring on its own, then averaged). Start new ones every time; a reused reviewer remembers its old scores and drifts lenient.

## Running it

- **Who reviews**: two fresh subagents that can read local files, open a headless browser and look at images. When the user stops subagents, the main session reviews itself (see SKILL.md "Subagents").
- **Record the model**: the model and effort of both reviewers go into the batch record and to `calibrate.py --model`. The same version scored by a different model can shift 1 to 3 points across the board (on one content site the reviewer model changed in round 4 and both reviewers said a transition that was always running did not exist). So versions are ranked by item-by-item blind comparison, and absolute scores from different models are not compared.
- **One at a time**: check memory first (macOS `sysctl -n hw.memsize`, Linux `free -g`). At 8GB or less the two reviewers run one after the other; each opens one browser, one page at a time, with a screenshot cap, written into review.json "machine_limits".
- **Check what comes back**: open the reviewer's review.md and scores.json; confirm the format, that both sets were scored and the comparison is filled in; for anything a reviewer "did not see", check whether it exists yourself first (see "When reviewers miss things").

## What reviewers get

- The address to review: a local production build (localhost); ship only after review (they open it and click themselves, not just screenshots).
- **Several versions at once**: build the current version, the best version and the anchor version into subdirectories of one folder (Vite: `--base /a/ --outDir <dir>/a`) and serve them by path (`/a/`, `/b/`) from one static server instead of one port each. For assets with hard-coded absolute paths in `index.html` (fonts, favicon), add a same-named symlink in that folder pointing at one of the builds.
- This version's home and core page screenshots: one set at 1440 and one at 375, one image per screen (`layout_check.py --slices 8`; desktop-only back offices use the project's main widths).
- Anchor set screenshots (blind-labelled A/B, see "Anchor set") and the previous best version's screenshots (blind-labelled C/D, see "Comparing with the best version").
- Frame-by-frame sheets of signature moments: `scripts/record_moment.py` steps a virtual clock and stitches each moment into one sheet (each frame labelled with ms since the action), plus `animations.json` (duration, easing, delay of each animation, View Transition pseudo-elements included) and `motion.json` (from which ms to which ms the picture moves). Static screenshots cannot score motion or micro-interactions, and live screen recordings drop frames on a busy machine, turning smooth animations into jumps, so reviewers always get frame sheets.
- **Looping demos** (idle first-screen demos, auto carousels): the prompt states how long one loop is and when each part starts, and the frames cover a full loop. Reviewers taking two screenshots some time apart will likely catch the start both times and conclude the first screen is static.
- **One sheet per major variant of a signature moment**: when the product has several roles or color themes, record at least 2-3 of them (a reviewer who sees one color assumes every variant looks the same).
- **Sound**: for sites with sound, the level file from `scripts/sound_levels.py` (review.json "sounds"), since reviewers hear nothing in a headless browser.
- **Features using the microphone or camera**: the operating notes give the test browser flags `--use-fake-device-for-media-stream --use-fake-ui-for-media-stream` and grant the page's origin `context.grant_permissions(["microphone"], origin=...)`, so the browser feeds a test tone as the mic.
- The list of **deliberate flaws** in demo props (a test shop deliberately missing sizes): targets the product is meant to find; no deductions. This is the only "design intent" reviewers may be told.
- Looks the user rejected ("rejected looks" in the brief): only used in the part where reviewers suggest redesign directions, so they do not suggest those. It does not affect scores.
- Reference screenshots of award sites in refs/, with each site's name and award.
- The 10 item names, this file's anchors, and the project's "what each score looks like".
- One line of product type and context (e.g. "back-office tool for merchants, hackathon project"), so retention is judged the right way: tools on rechecks, progress and reminders, with no deductions for missing levels or points.
- When the core flow calls a paid API (e.g. running an AI job), give reviewers demo data or a recorded replay to walk through; running it for real needs the user's OK first, because it spends money.

**Never give them**: the dev log, previous scores, or the developer's explanation of design intent. Reviewers see only the finished product, like real jurors and users.

## Review prompts

The template `templates/REVIEW_PROMPT.md` is shared by every project; do not write another. Project specifics go in `review.json` (copied from `templates/review.json` into the project's work directory, filled once at kickoff, then only fields like "signature_moments" and "rejected_looks" change), and each round `review_prompt.py` generates the prompts and blind mapping (usage in `scripts.md`). Reviewers write the full answer to `rN/review.md` and save the final JSON block as `rN/scores.json`.

What the prompt asks for (the template has it all; change rules there): click through the core flow at phone and desktop width before looking at screenshots; score 10 items by the anchors, with evidence for every 9 and above; caps only for serious problems; the 3 cheapest-looking spots, a complete issue list (tagged fatal, experience, polish), "what would add 1 point" per item, structural reasons and a redesign direction; item-by-item C/D comparison; the four Awwwards items on the real jury scale; JSON at the end.

## One ruler: the anchor set (every review)

Reviewers disagree, so the same site scores 62 one time and 68 the next and progress disappears. The fix works like exam marking: give reviewers an anchor set first.
- **Anchor set**: a fixed set of screenshots of an older version's home and core pages (one set at 1440, one at 375) in `refs/anchor/`, with reference scores (10 items, `anchor.json`). Never changed afterwards.
- **Every review scores the anchor set and the current version**, without knowing which is which. Then each item is corrected by "anchor reference score minus this reviewer's anchor score". If the anchor's typography reference is 7 and this reviewer gave 6, they run 1 point strict, so their current typography score gets +1.
- **Write down what each score looks like for every item**: once at kickoff, stored in the log and review.json, passed verbatim into every prompt and never changed: what 6, 7, 8 and 9 look like for each item, pointing at references ("this site's typography is a 9 because…"), so every reviewer uses the same ruler.
- Only calibrated scores go in the log and count, computed with `calibrate.py` (usage in `scripts.md`; it warns when reviewers differ by 3+ points on an item).
- **New projects without an older version**: when the first version is complete, take one-image-per-screen shots with `layout_check.py --slices 8` as the anchor set, and have 2 more reviewers score **only these screenshots**; their average becomes the reference score. Calibration starts with the next review.
- **Redesigns**: at kickoff, take one-image-per-screen shots of the current live site as the anchor set, scored the same way by 2 reviewers looking only at these screenshots; until the user picks an approved version, it is also the temporary baseline.
- Once fixed, the anchor set never changes, or scores stop being comparable. The next polish round keeps the same anchor set so both rounds compare directly.
- **Reference scores must come from reviewers looking at the same material**: the anchor set is screenshots, so the reference scores come from reviewers scoring those screenshots, never from elsewhere (such as a score given while browsing the live site). (Tested; see lessons.md.)
- **One image per screen**: full-page screenshots get shrunk to two or three hundred pixels wide and nothing is readable.
- **Screenshots cannot show motion or micro-interactions**: by default `calibrate.py` treats the anchor as screenshots and does not calibrate motion, micro-interactions, usability or retention. To calibrate those too, keep the anchor version as a local build that opens (e.g. on another port), have reviewers click it like the current version, and pass `--live-anchor`.
- `calibrate.py` limits each correction to ±1 by default and warns when calibration moves an item by 1 or more; check that the anchor set is shown under the same conditions as before.

## Comparing with the best version: blind comparison and verdicts

Absolute scores of different batches come from different reviewers and often differ by three points (on a content site, one direction's batch 5 scored 3.5 below batch 4 in absolute terms, while both reviewers comparing the two side by side found 8 items better and 0 worse, and 7 better and 1 worse). One reviewer comparing two versions directly is more reliable than two sets of reviewers' absolute scores, so "does this version count" is decided by the blind comparison:
- When there is a previous best version, generate prompts with `--best <its screenshot folder>`. Reviewers get sets C and D (this version and the best version, unlabelled) and pick the better one or "tie" per item.
- When the best version only exists as screenshots, only typography, whitespace, hierarchy, color, responsive and originality are compared; motion, micro-interactions, usability and retention count as changed only when both rounds used the same reviewer model and calibrated scores differ by 1 or more. When the best version also opens (another port), pass `--live-best <url>` to compare all ten.
- `calibrate.py` marks each item "better / tie / worse / split / worse (all reviewers)" by vote and gives a verdict:
  - Any item every reviewer judged better in the best version: **revert** those items. Edit this batch's changes that touched them back to the best version's look, as a new commit on top; keep the rest; the best version stays.
  - More "better" than "worse": **new best version**; `--save` stores it as the new best.json; worse and split items go first in the next batch.
  - Equal: **tie**; this version becomes the base of the next batch; the best version stays.
  - More "worse": edit the worse items back to the best version's look; the best version stays.
- Absolute scores are still printed: when both rounds used the same model and the scores differ by 3+ in the opposite direction of the verdict, the script warns; read both reviewers' reasons before deciding and note it in the log.
- Every new best version keeps its one-image-per-screen set as `best/` (needed for next round's C/D); delete the older set.

## When reviewers miss things

When a reviewer says an animation, transition or feedback "does not exist", do not rush to add it. This happened twice: on a content site, the View Transition from card to detail page was always running and the reviewer only saw a page fade; on a generator prototype, the generation animation was smooth but the screen recording dropped frames and the reviewer thought it cut straight over. What to do:
- Check locally with `document.getAnimations()` or `record_moment.py` whether it exists and what it looks like.
- If it exists, add that moment's frame sheet to the next round's signature moment material and note "missed by reviewer, no change" in the log.
- Only if it does not exist, or is too faint to see (say a 100ms fade), is it a problem for the list.
- When a reviewer says "no audio feedback", check the level file first: levels in the file mean the reviewer could not hear it, so add the file to the next round's material; only zeros in the file are a problem.

## Talking to reviewers

- Reviews are one-way: reviewers score, point out problems and suggest; the developer fixes. No arguing scores, no explaining design intent to get a higher score.
- **Clarify**: when feedback is unclear or there are several ways to fix it, start a fresh small reviewer subagent and ask only that one thing. It gives no total score and does not see the dev log.
- **Choosing options**: for subjective choices like fonts, colors and layouts, do not try them one by one until satisfied. Make 2-4 candidates, screenshot them in the same spot at the same width, let a small reviewer pick one by this file's standards with a reason, and go with its pick.
- Small reviewers' conclusions go in the log. Formal scores still come from the independent review once per batch.

## Direction review (when scores are stuck)

Normal reviews list concrete problems and only bring local patches; the developer always fixes small problems first and structural changes never get their turn. So when three reviews in a row stay in the same band (say 62-67), stop patching and run a direction review:

1. Start a fresh subagent as "art director", with the brief's "rejected looks" in its prompt, answering only three things:
   - The structural reasons the score is stuck (visual concept, layout system, type system, image language, motion language, information architecture), at most 3, no small problems.
   - 2 clearly different redesign directions, both avoiding the rejected looks: a one-line visual concept, type, color, layout grid, image style, motion principles, what the first screen looks like, each with 1-2 reference sites.
   - Which direction is more likely to bring all 10 items to 9+ (an average SOTD), and why.
2. Build a first screen plus one middle section of each direction on a branch, and let a small reviewer pick one A/B.
3. **Show the picked direction to the user first**: before, the user's baseline and the new direction in three columns (`side_by_side.py --urls` with three addresses), home and key pages, 1440 and 375. Continue only if the user picks it; if the user rejects it, add its look to "rejected looks" and go back to polishing the baseline. If the user does not look at images or does not want questions, skip direction reviews (see SKILL.md "Score stuck").
4. Roll the picked direction out across the site on a branch, features and data untouched, fixing only fatal problems meanwhile.
5. Score the current best version and the redesign with the same review standard (blind comparison as usual); merge only if the redesign is clearly better (better on most items in the blind comparison, no item judged worse by every reviewer, and 5+ points higher in absolute score), otherwise drop it. Before merging and shipping, show the user the three columns once more.
6. Give the redesign a deadline that leaves time for polishing and release afterwards. Main always keeps the current best version.

## Using review results

**Reviews exist to make changes raise scores; a change that raises nothing was wasted.** To make sure:
- Average two reviewers so one reviewer's bias does not drown real progress.
- Judge progress by the blind comparison ("Comparing with the best version"); absolute scores only count with the same reviewer model.
- Reviewers check the previous list item by item: what improved, what did not, and whether anything else broke.
- Each batch does "what would add 1 point" and the structural changes that fit within the baseline look first, small problems after.

- Only independent, calibrated, averaged scores go in the log, marked "independent review" with the model. Self-scores take no part and are never compared with review scores.
- The full list from reviewers, minus items in "rejected looks" and "decided not to do", is the next batch's to-do; fatal and experience problems first, "what would add 1 point" right after.
- "All 10 items at 9 or above" in the finish conditions must come from **the latest independent review**. Self-scores reaching it do not count.
- If you think a reviewer is wrong, write the reason in the log; the next review scores just as strictly, and you never rerun with a more lenient prompt.
