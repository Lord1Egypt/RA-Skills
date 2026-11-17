# Worked examples (adapted from the source essay)

These double as regression cases: the skill should produce plans like these.

## 1. Crash fixing → crash-free (Altitude + setup)
- **Asked:** fix this crash.
- **Ambitious:** keep the app crash-free.
- **Setup first:** the agent can fetch crash reports, map each app version to a git commit, and reach Windows, macOS and Linux machines to reproduce and verify fixes on its own.
- **Judge:** the crash rate per release from the crash reporter, plus a reproduction before and after each fix.

## 2. Quarterly business review deck (Altitude ladder)
- **Rung 1:** give the model all the data you can and ask what changed this quarter, why, and what to do about it. Do not just refresh the numbers in the template.
- **Rung 2:** pick the three most urgent decisions and draft directions with arguments for and against each.
- **Rung 3:** the review exists so leadership catches problems early and moves money and people. Design a better mechanism than a quarterly deck, use the company's own history to show it would have caught issues sooner, and run it beside the current review for a quarter.
- **Judge:** a historical backtest (lead time gained on known past problems) and the parallel run.

## 3. Churn analysis (Depth)
- Use real instruments: a database and statistical models, not markdown tables.
- **Challenge the belief:** "churn is an onboarding problem". Try to reproduce it from the raw event data.
- **New knowledge:** simulate customers from a year of logs, find the earliest churn signal nobody knows about yet, and show it predicts on data the model has not seen.
- **Judge:** held-out predictive performance against a stated baseline.

## 4. Page load 10 s → 5 s (unreasonable target)
- **Asked floor:** 5 s. **Ambitious target:** 200 ms, treated as solvable.
- **Judge:** a profiler trace and repeated lab measurements on fixed hardware and network, reporting p50 and p95.
- **If 200 ms is missed:** report the real number, what each approach bought, and the remaining bottleneck. Do not rename 5 s as the goal.

## 5. Range crew for the QBR
- **Verbs:** get busy people to believe a cause-and-effect story and decide under uncertainty, in 30 minutes.
- **Crew:** an analyst (causal analysis), a journalist (finding the story and checking sources), an editor (cutting to the decision), a motion and audio designer if it will be presented, a short seller (attacking the thesis the way they research a short position), and a forensic accountant (reconciling the numbers).
- **Rule:** each member contributes a method, not a voice.

## 6. When not to escalate (our addition)
- "Fix the typo in README line 3." → `AS-ASKED`.
- "Just give me a quick bash one-liner to count lines." → `AS-ASKED`.
- "Production is down, roll back now." → `AS-ASKED`. Propose a post-incident ambitious follow-up only after the rollback is done.
