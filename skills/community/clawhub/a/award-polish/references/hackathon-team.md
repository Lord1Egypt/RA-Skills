# Scenario: hackathons, team work, owning one part

Time is counted in hours (say 36), several people write in one repo, I own one part (say frontend and experience), and judges see a few minutes of demo and a video.

**The bar does not drop: still aim for Awwwards level.** In a hackathon that is itself an edge: everyone codes with AI, features end up similar, and judges remember the best-looking, easiest-to-use few. Only how time is spent changes: design is done before the start, the first version after the start already follows the agreed system, and reviews and polishing follow the team's checkpoints. The roles, schedule and feature-cut line agreed by the user and the team apply as they are.

**Mode**: the team repo exists at the start, but my part starts from zero, so mode 1.

## Find out five things first (from team docs)

Read these from the team docs and write them in the log. This is design setup, so it does not need a question. Do not deploy, publish, delete, or take another destructive or irreversible action without an explicit yes from the user.

- **Which folders are mine**: change only those; others' folders are read-only. Shared contracts (data formats, APIs) are read-only; to change one, stop and tell the user, who raises it in the team chat.
- **The team's schedule and feature-cut line**: polishing batches follow the team's checkpoints (e.g. 16:00, 20:00, Sunday 07:30).
- **Who deploys and how often**: usually backend or integration. I do not deploy; after each team deploy I click through the demo path live.
- **How judges look**: what they see in the live demo, the public link, the demo video and the submission page (e.g. Devpost).
- **The demo path**: which clicks the demo makes in order and what each one should show. This path is the project's signature moment list.

## Global things are agreed with the team in the first 90 minutes

Where design variables live, whether to add dependencies like a motion library, page titles and favicon, the 404 page, .gitignore: these all sit in shared areas of the repo. Raise them in the first 90 minutes together with the shared contracts, write them into the contracts once the team agrees, and follow them without changing them alone.

My own log, brief and `refs/` screenshots stay on my machine, out of the team repo; the baseline is recorded as a commit hash in the log, not a tag.

## Before the start: finish the design

Ask the organizers first what may be prepared before the start. Usually code is written after the start, while design can be done ahead.

- Study references (`reference-study.md`) and write the reference notes and design read.
- Settle the design system: colors, fonts, type scale, layout grid, spacing scale, radius, shadows, motion durations, plus product name, logo and favicon, on one page.
- One design mockup per demo screen, marking how signature moments move. If the rules allow, mockups may be static web pages, rewritten after the start rather than copied into the repo; if not, image mockups only.
- Generate image assets with an image generator the user has authorized: illustrations, empty states, share cards and other large pictures made and picked ahead. Reference sketches and prompts leave the machine. If that generator is out of quota, ask before using another (ChatGPT, Gemini, or Grok in a browser). Do not switch providers silently. After the start only fill gaps; no wholesale replacement.
- One small reviewer critiques the mockups, then the user sees them; **settled only on the user's go-ahead**. Direction changes (a new visual direction) happen only at this step; no direction reviews after the start.
- Anchor set: the version at the first checkpoint after the start becomes the anchor set (see reviewer.md "New projects without an older version") and never changes.

## After the start: the first version already looks good

- First turn the design system into code variables and base components (buttons, cards, tables, status tags), and build every page from them. Pages off the main path automatically get the same quality.
- When others' APIs are not ready, build the interface on mock data that follows the shared contract and swap in the real API later. Mock data lives in my own folder with file names that say it is mock.
- While waiting on APIs, build signature moment motion and all states (loading, success, failure, empty).
- Run the build before merging into main and confirm no one else's files changed.

## Demo props: make them look good, keep the deliberate flaws

Demo props like test shops and sample accounts often keep deliberate flaws (product data missing sizes) so the product has something to find and fix.

- At kickoff, list the deliberate flaws in the log, tell reviewers during self-checks and reviews that they are not problems, and never fix them in passing.
- Props still look polished, like a real shop, so judges believe them.
- Prop pages follow the motion system, but content must not wait for animations to finish, so AI agents and scripts can read the page.
- Prop shops are still scored on the 10 items; the deliberate flaw list goes to reviewers, see `reviewer.md`.

## Order: main path first, one standard for every page

Order decides what comes first, not how good it gets:

1. The demo path runs reliably: every step clickable with a result, ten runs out of ten. Protect this first.
2. Every screen on the demo path: judges understand "what happened and why" within 10 seconds, at award-level polish.
3. What judges see clicking the public link themselves: the home page's first look, no login, empty states that guide.
4. Other pages: same system and components, so quality follows; polish them when time allows.

## Waiting screens while AI runs (common in AI products)

AI agents, generation and retrieval take seconds to tens of seconds, and that wait is itself a signature moment:

- More than a spinner. Show step by step what the AI is doing (where it went, what it read, what it decided), read from the run log. A hard-coded animation does not count.
- Show elapsed time; past the expected time, say so, so nobody thinks it froze.
- When results vary between runs, honestly show "succeeded X of Y times", not only the successful run.
- Separate evidence from AI guesses visually: evidence (which field is missing, which page) is the main element; the AI's explanation is marked as a guess and secondary.
- Charts, metric cards and comparisons follow the dataviz skill's method.

## Interface and widths

- **Back offices are desktop only**: main widths 1280, 1440, 1920, plus 1280x720 for projectors. 375 and 768 are only checked not to break and stay readable; no phone-specific version.
- **No onboarding popup**: someone presents live and a popup interrupts. For judges clicking the link themselves, a small "walk me through" entry in a corner that starts only when clicked.
- **Projector check**: large enough type and strong enough contrast; light gray text disappears on projectors.

## The demo must survive the room

- **One-click reset**: one button restores the demo data to the opening state so the next judges can see it.
- **Offline backup**: key images and fonts bundled locally; a full demo video ready to play if something fails.
- **No login, no permission prompts**: the public link works on open.

## The demo video is part of the work

Judges often watch the video before the live demo. Make it to signature-moment standard:

- Same storyline as the 90-second pitch; the first 5 seconds say what the product is.
- Real screen recordings with steady mouse movement; speed up long waits and label them "sped up".
- Captions so it works muted; end on the product name and link.

## How the loop runs

- **One checkpoint is one batch**: between checkpoints keep working with quick self-checks only (build passes, one screenshot per changed page at the main widths, no console errors, demo path clicks through); at checkpoints run the full self-check, reviews, and screenshots for the user.
- **Every checkpoint**: demo path clicked through and screenshotted at the main widths, no console errors, whatever the detail checklist can already check, 2 independent reviewers averaged, side-by-side with the previous best version.
- **Once a night**: Lighthouse and a keyboard walk-through, blind test (whenever there is a guide entry).
- **Before the last checkpoint**: every check in `polish-checklist.md`.
- **Reviewers walk the flow** on demo data or a recorded replay, never running the AI for real; running it needs the user's OK first because it spends money. The replay mode (playing back the log of one real run) is itself part of the dev plan; agree in the first 90 minutes who builds it.
- **User checkpoints**: at each checkpoint send before/after shots of key screens to the user (usually also a teammate) and continue without waiting. When something feels off: fix small things right away; for "ugly" or "wrong direction", follow SKILL.md and line up several versions for the user to pick. Only finalizing the mockups and changing the baseline wait for the user's go-ahead. If the live site breaks, tell the teammate who deploys to roll back first.
- **Score stuck**: no direction reviews after the start. A small reviewer picks the cheapest-looking screen, it is redone within the same design system, and compared side by side with the current one.
- **The goal stays**: all 10 items at 9, every signature moment done, holding up next to the references.
- **When to stop**: at the team's "no new features" time, stop polishing regardless of scores and only fix problems. If it did not reach 9, write down honestly where it falls short.
- **Finally**: once the team has deployed, click through the demo path live from the start, keep a recording, and add this event's problems to your local copy of `lessons.md`.

## For tools and back-office products

- Add references: still study award sites, plus a few widely praised tool and back-office UIs, see `reference-study.md` "For tools and back-office products". The ruler stays Awwwards.
- Judge retention as a tool: whether users want to come back to recheck, whether there is progress and reminders, whether results can be shared, without consumer tricks like levels and points. Say so in the review prompt.
