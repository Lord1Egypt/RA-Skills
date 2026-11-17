# Polish brief (not committed; read before every batch; add anything new the user asks for)

## 1. Goal
- One line: real users find it easy to use, good-looking, smooth and worth coming back to; it holds up next to the reference award sites.
- Mode: <1 new site / 2 redesign>; scenario: <none / hackathon or team work (read hackathon-team.md)>
- Core concept: <one sentence, what only this product has>
- Design brief: page type <> · audience <> · mood words <2-4> · references <URLs or product names> · avoid <clichés you do not want>
- Baseline: <commit or tag the user approved; no AI score overrides it>
- Floor: <domain, theme, fonts, dashes, search fields and other user and project constraints; core flow works; existing features do not regress>
- Real deadline: <date, time, time zone; how long the wrap-up takes>
- User checkpoints: <looks at side-by-sides and replies / looks without replying / does not look, choices left to you> (no direction-level redesigns when the user does not look)
- Shipping: <which branch push ships, who approves; for deploy-first, the link>

## 2. Rejected looks (looks the user turned down; review suggestions and direction reviews avoid them)
- <look> (<when, in which side-by-side it was rejected>)

## 3. Decided not to do (strike it when reviewers raise it again without a new reason)
- <item>: <reason>

## 4. What each batch does
- Read this brief and the latest full list in the log → strike items in the two sections above → fix everything in one go (fatal → experience → polish, one commit per change) → self-check → 2 independent reviewers → calibrate verdict → record → next batch
- Project-specific to-dos: <the top few from the reference gap list>

## 5. How to check
- Widths: <375,768,1024,1280,1440 / back office: 1280,1440,1920 + 1280x720>
- Key elements in the first screen: <name=selector, one or two per page; y values measured at kickoff>
- Machine limits: <memory; at 8GB or less one browser job at a time>
- Reviewer model: <recorded each batch>
- Commands and options: <skill dir>/references/scripts.md
- Anchor set: <screenshot folder>, reference scores: <anchor.json path>; review config: <review.json path>
- What each score looks like: <where that section is in the log, same as review.json>
- Signature moments: <each listed, marked not started / needs polish / done>
- Deliberate flaws (demo props): <"none" if none>

## 6. What to record
- Log location: <ITERATION_LOG.md or a local path>
- One entry per batch: batch N · list size · what changed (with commits) · not done and why · reviewer model · calibrated scores · side-by-side verdict · signature moment status

## 7. When to stop
- Finish: latest independent review has all 10 items at 9+; every signature moment done; holds up next to the references; two batches in a row with nothing obvious to improve
- Stop early: hard deadline / the user says stop / the live site is broken and rollback does not save it
- Stuck, keep going: park a problem unsolved for 3 batches; three reviews in the same band means a direction review (when the user does not look at images, and in hackathons, redo the cheapest-looking screen instead); when the user does not look at images and 3 batches tie, wrap up
