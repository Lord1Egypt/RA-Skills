# Mode 1: Creating a new website

Goal: design the first version to award standard, then polish from that level.

## Step 0: deploy first or not

By default do not deploy first; go to step 1. When the user or the situation needs a link up front (a pitch, a client who wants to look), ship a viewable version as fast as possible:

- Fix the hosting and the **final domain** (it cannot change later), scaffold, make a viewable home page (product name, one-line positioning, one or two core blocks), deploy right away.
- Confirm the live URL returns 200 with `curl -sI`, then actually open it in a browser.
- With a deadline: give the user the link on its own line and continue after they submit. Without one, just keep going.
- If deployment is stuck for more than 15 minutes, stop and tell the user which step it is stuck on and what you need from them (a login, a permission).

## Step 1: read the brief, set the product structure

- Break the brief into: target users and pains, the core flow (the main path from arrival to done), required features, and where we can stand out.
- Write a design brief (format borrowed from the taste skill): page type, the product in one sentence, audience (concrete adjectives), 2-4 mood words (e.g. "restrained, editorial, clean"), references (real URLs or product names), and **what to avoid** (name the AI clichés you do not want: purple gradients, three identical cards, a centered huge headline on a dark background).
- Put the feature list in the log for acceptance item by item. Features are the passing line: all of them, all clickable.
- For work shown to reviewers (timed take-homes, portfolios), design so one reviewer can walk the whole flow alone: one-click demo, role switching, a guide.

## Step 2: study award sites, set the design direction

- Pick references following `reference-study.md`.
- Then write in the log:
  - A one-sentence design read: page type, audience, mood, which design language it leans toward.
  - The three dial values (when design-taste-frontend is installed), each with a reason.
  - 3-5 techniques borrowed from references and where each is used.
  - Signature moments: 4-6 from the core flow.
  - Image plan: what goes in each spot and where it comes from (generate whatever can be generated).
  - Spacing scale, accent color, radius, fonts.
  - Layout grid: columns, gutters, max content width; type scale (e.g. 1.25x per step) and how many levels from heading to body; how Latin and CJK fonts pair if both are used.
  - Brand: product name, logo or wordmark, favicon. If missing, settle them now (an image generator can make logo candidates for a small review to pick).
- **Make 2-3 clearly different directions**: for each, a high-fidelity mockup of the first screen plus one signature moment (generated images or a clickable static mockup) with a one-line visual concept. A small review picks against the references, then the directions go side by side to the user; code starts only after the user picks. Direction is the hardest thing to change later (one clickable prototype sat at 62-67 points for 38 batches, and this was the root), so time spent here pays off most.

## Step 3: build it right the first time

- Build the full site in the chosen direction: every feature on the list (only your part in team work), signature moments with designed motion and feedback from the first version.
- When to ship: `release.md`.

## Step 4: acceptance

Write Pass or Fail for each item in the log:

- Every feature, with where on the page it can be seen.
- Design rule check (with design-taste-frontend installed, run its Pre-Flight Check, Pass or Fail with a reason each). Plus three written checks:
  - Dash check: no dashes anywhere on the page (`layout_check.py --forbid` with the em dash U+2014 and en dash U+2013).
  - Layout repetition check: list each section's layout type; each type at most once, at least 4 types across 8 sections.
  - First-screen check: heading lines (2 at most), subheading length, main button visible without scrolling.
- Any Fail means this step is not done.
- Layout check at five widths.
- Two independent reviewers score the 10 items (`reviewer.md`), and the anchor set is fixed per reviewer.md "New projects without an older version".
- Local production build: no console errors, all images load, core flow clicks through. Verify again live after release.

Fix any Fail and rerun acceptance. When everything passes, enter the shared iteration loop in SKILL.md.
