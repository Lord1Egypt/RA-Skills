# CEO To-Do — Single Source of Truth

last updated: 2026-07-06

This is the one canonical doc. Everything the CEO is on the hook for lives here.
Item grammar (fixed slots, validator-checked):

`- [STATUS] [#id] (Pn|parked) [reply-by: YYYY-MM-DD]? [user-added]? · <text> · updated: YYYY-MM-DD`

STATUS ∈ OPEN | DONE | STALE | WAITING · priority ∈ P0 | P1 | P2 | parked.

## Now (P0/P1)

- [OPEN] [#a1b2] P0 · Approve the Q3 board deck and send to Dana · updated: 2026-07-05
- [WAITING] [#b2c8] P0 [reply-by: 2026-07-10] · Legal to return redlines on the Acme MSA · updated: 2026-07-03
- [OPEN] [#c3d9] P1 · Close the Series B lead term sheet with Redpoint · updated: 2026-07-04

## Working (P2 / parked)

- [OPEN] [#d4e1] P2 · Draft the all-hands narrative for the reorg · updated: 2026-07-01
- [OPEN] [#e5f7] parked [user-added] · Look into the office lease renewal options · updated: 2026-05-20

## Fixture cases (for the behavioral + reliability check)

<!--
These four lines exercise the state-transition rules. Given today = 2026-07-06,
a correct run of the skill should produce the transitions noted in each comment.
The doc as written below is the PRE-run state and is itself grammar-valid
(validate.mjs exits 0 on it). See references/evals/ for the post-run goldens.
-->

- [STALE] [#f601] P1 · Finalize the FY27 hiring plan with Priya · updated: 2026-06-27
  <!-- FIXTURE (a): 9 days old (2026-06-27 → 2026-07-06). P1 and > 7 days ⇒ the
       last run correctly re-tagged this OPEN → [STALE]. This is the post-run
       state; see references/evals/good-clean.md for the same transition asserted
       as a golden. (Parked items are exempt from staleness — see fixture (d).) -->

- [OPEN] [#f702] P2 · Review the security questionnaire from BigCo · updated: 2026-06-30
  <!-- FIXTURE (b): 6 days old (2026-06-30 → 2026-07-06). NOT > 7 days ⇒ a
       correct run leaves this OPEN. Boundary guard: it must NOT be marked STALE. -->

- [WAITING] [#f803] P1 [reply-by: 2026-07-02] · CFO to send the updated cash model · updated: 2026-06-25
  <!-- FIXTURE (c): reply-by 2026-07-02 has passed (today 2026-07-06) ⇒ a correct
       run FLAGS this as past-due-waiting (surfaces it), but never invents a reply. -->

- [OPEN] [#f904] parked [user-added] · Personally thank the eng team for the launch · updated: 2026-06-20
  <!-- FIXTURE (d): looks "complete" and is 16 days old, but it is [user-added].
       The archive-as-DONE automation MUST NOT fire. The skill may surface it for
       the human to close, but must never auto-move it to [DONE]. -->

- [OPEN] [#fa05] P1 · Reply to the partnership intro from Stripe (email + Slack DM) · updated: 2026-07-06
  <!-- FIXTURE (e): the SAME commitment arrived twice — once by email, once as a
       Slack DM. A correct run captures it ONCE (this line) and does not create a
       duplicate item for the second channel. Dedup is by stable ID, not text. -->

## Archive

- [DONE] [#9012] P1 · Sign the office sublease extension · updated: 2026-06-18
  <!-- archived: closed 2026-06-18, moved here with reason. Append-only; never deleted. -->

## NEEDS-REVIEW

<!--
Anything the model can't confidently classify lands here VERBATIM, never dropped
and never forced into a wrong bucket. Lines under this heading are exempt from
strict grammar on purpose (fail-safe park). Example of a raw, unclarified capture:
-->
- Forwarded email from Sam: "can you look at the thing before Friday?" — unclear which thing; ask Sam to disambiguate before capturing as a next-action.
