# Scaling: $1M+ ARR or 10+ People

The frameworks still apply. But at this size, the constraint is often not a
funnel step — it's a decision-making pattern, a coordination failure, or
a model that worked at $500K but breaks at $5M.

---

## Policy Constraints

At 10+ people, the bottleneck is often not a resource but a **policy** —
a decision-making pattern that throttles the system:

- A VP who overrides sprint priorities with pet projects.
- A process that requires three approvals before anything ships.
- OKRs that reward local metrics (leads generated, features shipped)
  instead of system throughput (happy paying customers created).
- A "no one ships without full test coverage" rule applied uniformly
  to experiments and production code alike.
- An unwritten rule that only one person can approve customer-facing
  changes.

**How to spot a policy constraint:** The triage points to a funnel step
(say, activation), but fixing that step doesn't move throughput. Or the
constraint keeps shifting back and forth — you fix acquisition, it moves
to activation, you fix activation, it moves back to acquisition. That
oscillation usually means the real constraint is above both: a policy
that prevents the team from sustaining focus.

**How to fix it:** Name the policy. Make it visible. Ask: "If we removed
this policy, what would break?" If the answer is "nothing," remove it.
If the answer is "something important," find the minimum version of the
policy that protects what matters without throttling throughput.

Policy constraints are the hardest to fix because they feel like
"how we do things." They're defended by habit, not logic.

---

## Before You Build: The Awareness Check at Scale

The same check from `stages/growth.md` applies here — but the failure mode
is different. At scale, companies expand into **new segments** where they
have zero mental availability. The product works in segment A, so the team
assumes it will sell in segment B. But segment B has never heard of you,
associates your brand with different (or zero) Category Entry Points, and
can't find you in their usual channels.

**Run this diagnostic before any growth initiative or segment expansion:**

1. "Do the right people in the target segment know we exist?" If not →
   invest in reach and CEP coverage for that segment before building
   segment-specific features.
2. "Can they find and buy us through their usual channels?" If not → fix
   physical availability (directories, marketplaces, integrations, pricing
   transparency) for that segment.
3. "Are we distinctive enough that they'll remember us?" If not → ensure
   brand assets are consistent across new channels.

**At scale, also check:** "Are we associated with the right CEPs for this
new segment?" Re-run the CEP mapping exercise (see `references/pillar-sharp.md`)
for each new segment. The struggling moments that drive your current customers
may not match the new audience. Map before you build.

**Quarterly awareness review (1 hour, strategic):**

1. **Full CEP mapping exercise.** Re-score coverage per segment, add new
   CEPs from JTBD data, retire stale ones.
2. **Full physical availability audit.** Re-score every dimension, especially
   for new segments.
3. **Reach trend.** Plot monthly unique reach across all channels for the
   last 3 months. Flat or declining despite consistent publishing means
   channel saturation or CEP-market mismatch.
4. **Competitive association check.** For your top 3 CEPs per segment,
   search the way a buyer would. Gaps are where you invest.

---

## Multi-Team Constraint Work

With multiple teams, constraint identification becomes two layers:

### Team-level triage

Each team runs their own triage: "What's blocking our throughput?" A
product team might have an engineering constraint. A sales team might
have a pipeline constraint. A CS team might have an onboarding constraint.

### Company-level triage

Roll the team-level answers up: "Which team's constraint is the
system constraint?" The system constraint is the one that limits how
fast the entire company creates happy paying customers.

If the product team's engineering constraint is limiting activation,
and activation is the company constraint, then engineering IS the system
constraint. Every other team subordinates to it.

If the sales team's pipeline constraint is limiting acquisition, but
the company constraint is actually retention (customers are churning
faster than you acquire them), then sales is a non-constraint. Their
pipeline problem doesn't limit system throughput. Fix retention first.

### The weekly review becomes two layers

1. **Team-level** (each team, 10 min): What's blocking our throughput?
   Are we feeding the company constraint? Where is our work piling up?
2. **Company-level** (leadership, 25 min): Which team is at the system
   constraint? Are all other teams subordinating? Has the company
   constraint shifted?

Use the Full Review format for the company-level review. See the
"Full Weekly Review" section below.

---

## Hiring as Elevation

"Elevate" means invest. At this stage, that usually means hire. The
rules:

### When to hire

Only after exploiting and subordinating. If you haven't squeezed maximum
output from the constraint with existing resources, and you haven't
redirected non-constraint capacity to help, hiring is premature. You'll
add headcount to a broken system.

### Where to hire

**At the constraint. Never at a non-constraint.** A senior hire at the
bottleneck pays for themselves in throughput. A hire at a non-constraint
adds cost without adding output.

If the company constraint is activation and your onboarding team is at
capacity after exploiting and subordinating, hire an onboarding specialist.
Don't hire another engineer because "engineering is always useful."

### Sequencing

The constraint will shift after the new hire is productive. Plan for it:

1. Before hiring, ask: "When this hire breaks the current constraint,
   where will the constraint move next?"
2. Start subordination planning for the new constraint before the hire
   starts.
3. Don't hire for two constraints simultaneously. Break one at a time.
   Parallel hiring at different constraints means neither gets enough
   support during onboarding.

### The role description test

Every job description should name the constraint it serves: "This role
exists to increase [throughput metric] by [doing what] at the [specific
constraint]." If you can't write that sentence, you don't know why
you're hiring.

---

## Multi-Quarter Strategic Initiatives

The 2-week GOLEAN cycle is the tactical layer. Some constraint work
takes months: moving upmarket, rebuilding onboarding for enterprise,
launching in a new geography.

### How to run them

1. **Set a GOLEAN goal for each cycle** that serves the larger initiative.
   "This cycle: reduce enterprise onboarding from 6 weeks to 4 weeks by
   automating data import." Not "work on enterprise onboarding."

2. **Track with the fever chart at the project level.** Break the
   initiative into milestones. For each: % of work done vs. % of buffer
   consumed. See the Buffer Management section below.

3. **The weekly review asks two questions about the initiative:**
   "What % of the initiative is done? What % of our buffer is consumed?"
   If buffer is outpacing completion, act — cut scope, add resources from
   non-constraints, remove blockers.

4. **Don't let the initiative become a WIP black hole.** If the
   initiative has been "in progress" for 3 months with no measurable
   throughput improvement, it's inventory. Either break it into smaller
   shipped increments or kill it.

### The strategic constraint test

Before committing to a multi-quarter initiative, ask: "Is this work on
the current constraint, or are we investing in a future constraint?" Both
are valid, but they have different urgency. Current-constraint work gets
priority. Future-constraint work gets a smaller allocation and a longer
buffer.

---

## Business Model Constraints

Sometimes the constraint isn't a funnel step — it's the model.

**Re-run the napkin test annually.** The math that worked at $500K ARR
may not work at $5M:

- The addressable market at your current price point may be saturating.
- Customer acquisition costs may be rising faster than lifetime value.
- Your best segment may be fully penetrated while adjacent segments
  don't convert as well.

If Required Customers > Addressable Market at your current pricing, the
fix is the model, not the funnel. Options:

- **Move upmarket.** Charge more per customer. Fewer customers needed,
  but longer sales cycles, more onboarding complexity.
- **Expand the product.** Serve adjacent jobs for existing customers
  (expansion revenue). The most capital-efficient growth at this stage.
- **Change the pricing model.** Usage-based, seat-based, outcome-based.
  Different models attract different segments.

This is a strategic decision, not a tactical one. Don't try to solve it
in a GOLEAN cycle. Use the napkin test to diagnose, then plan the model
change as a multi-quarter initiative.

---

## Buffer Management and Estimation at Scale

At this size, you have external commitments (customer launch dates, board
reporting, partner timelines) that demand honest estimation.

### Critical Chain Project Management (CCPM)

The full method, for initiatives with external commitments:

1. **Get focused estimates** (50% confidence) for each task. "How long
   with no interruptions?"
2. **Use focused estimates as task durations.** Do NOT add safety to tasks.
3. **Identify the critical chain** — the longest dependent sequence,
   including resource dependencies (same person can't do two tasks at once).
4. **Buffer = critical chain × 0.4.** Place at the end of the project.
   A 30-day chain gets a 12-day buffer. Commit date = day 42.
5. **Schedule tasks as late as possible.** Reduces WIP, prevents premature
   work.
6. **Run the relay race.** When a task finishes, the next person starts
   immediately — not on the scheduled date. Early finishes propagate.

The 0.4 multiplier works for almost everything. It's the default. For
initiatives where you need statistical backing (regulated work, board-level
commitments), also get safe estimates (80-90% confidence) for each task —
this enables RSEM. See `references/estimation.md` for RSEM, calibration
exercises, and other buffer sizing methods.

### The fever chart

Track weekly: % of critical chain completed vs. % of project buffer
consumed.

- **Green (buffer < 1/3 consumed):** On track. Don't fill slack with
  scope creep.
- **Yellow (buffer 1/3 to 2/3 consumed):** Plan a recovery option. Being
  in yellow is normal — the buffer is doing its job.
- **Red (buffer > 2/3 consumed):** Act now. Cut scope to minimum viable
  delivery. Redirect non-constraint capacity to help. Remove blockers.
  Communicate risk to stakeholders with a revised range.

### Communicating timelines

**To customers and stakeholders:** Never give a point estimate. "We expect
to deliver between [aggressive date] and [buffer end date]." If using
cycle time data: "50% chance by [date A], 85% chance by [date B]."

**To the board:** Use throughput metrics. "We shipped X initiatives serving
the constraint. Cycle time for customer-facing work is Y days. We're in
green/yellow/red on the current initiative."

**To the team:** Buffer status and constraint, not individual task
deadlines. "We've consumed 40% of buffer with 60% of work done — we're
healthy. Keep the relay race going."

### Cycle time measurement

After 3+ weeks of data, stop estimating and start measuring. Track how
long tasks take from start to done:

- **Median:** 50% of tasks complete in this time or less.
- **85th percentile:** Use this for external commitments.

This replaces estimation with measurement. It's the most accurate method
for ongoing work.

See `references/estimation.md` for PERT, Monte Carlo forecasting, the
cone of uncertainty, and why estimates structurally fail.

---

## When the Constraint Shifts

This is the hardest moment operationally. At scale, the stakes are
higher — the team has built process, muscle memory, and identity around
the old constraint.

1. **Name it explicitly.** "Our constraint has moved from X to Y.
   Starting now, everything serves Y."

2. **Reassign subordination roles.** At 10+ people, this means updating
   team-level priorities, not just individual roles. The principle:
   every team that is NOT at the constraint serves the team that IS.
   Non-constraint teams feed the buffer, remove blockers, and absorb
   overflow — even if that means they look underutilized.

3. **Don't abandon the old constraint.** The systems that fixed it
   (content calendar, outreach cadence, onboarding automation) go on
   autopilot. Monitor weekly. Don't let it regress.

4. **Expect resistance.** At scale, resistance is louder. Teams built
   KPIs around the old constraint. Dashboards measure the old thing.
   Headcount was justified by the old diagnosis. The founder needs to
   re-align the narrative, not just the board.

5. **Update everything in the same meeting.** Buffer columns, WIP tags,
   constraint labels, team assignments, GOLEAN goals. Don't let tools
   lag behind decisions.

6. **Watch for the oscillation pattern.** If the constraint keeps
   bouncing between two steps (acquisition → activation → acquisition),
   look for a policy constraint sitting above both. The oscillation
   usually means neither step is the real constraint.

---

## Worked Example: The Hidden Policy Constraint

**DataPipe — data integration SaaS, 15 people, $2.1M ARR, stuck for
6 months.**

The founder asks: "We're stuck at $2.1M. Activation is the problem —
enterprise customers take 6 weeks to onboard. We need to hire 2 more
onboarding specialists."

**Step 1: Triage.**

| Question | Answer |
|---|---|
| Enough people finding you? | Yes — 80 enterprise trials/month from partnerships and content. |
| Do signups reach the aha moment? | Slowly. Median time-to-value is 6 weeks. Only 40% activate within 90 days. |
| Do activated users pay? | Yes — 70% convert, $2K/mo average. |
| Do paying customers stay? | Yes — 92% annual retention. |
| Is the team finishing things? | No. 4 engineers split across 6 projects. Onboarding backlog growing. |

**Step 2: Dig deeper.** The triage says activation. But why is onboarding
taking 6 weeks?

Interview the onboarding team: "What blocks you?" Three answers:
1. Custom data connectors — each enterprise needs 2-3 connectors that
   don't exist yet. Engineering builds them ad-hoc.
2. Security reviews — each enterprise requires a security questionnaire.
   Only the CTO can complete them, and he's also the lead architect.
3. The VP of Product keeps pulling engineers off connector work to build
   "strategic features" for the roadmap.

**Step 3: Identify the real constraint.** The activation problem is real,
but it's caused by a **policy constraint**: the VP of Product controls
the engineering sprint and prioritizes features over onboarding
infrastructure. The CTO being the only person who can do security reviews
is a secondary constraint — a bus factor of 1 is a throughput ceiling.
Document it, pair on it, or automate it.

**Step 4: Exploit the policy constraint.**

- The founder takes sprint prioritization away from the VP of Product
  for this quarter. All engineering serves activation until onboarding
  time drops below 3 weeks.
- Two engineers move full-time to building a self-serve connector
  framework (so enterprise customers can configure their own, instead
  of waiting for custom builds).
- The CTO documents the security review process and trains the CS lead
  to handle standard questionnaires. CTO only handles non-standard ones.

**Step 5: Subordinate.**

- The VP of Product's roadmap features go on ice. They're inventory.
- The two engineers still on other projects consolidate to one project
  each (WIP discipline).
- The CS team pre-packages onboarding materials for the top 10 most
  common data sources.

**Step 6: Don't hire yet.** The founder wanted 2 onboarding hires.
Answer: "First, exploit. If the connector framework and security review
delegation cut onboarding to 3 weeks and the activation rate climbs
above 60%, you may not need the hires. If it doesn't, then hire — at
the constraint (onboarding), not at engineering."

**What happened:** After one quarter, median onboarding dropped from
6 weeks to 2.5 weeks. Activation rate went from 40% to 65%. The
constraint shifted to acquisition — now that onboarding was fast,
they could handle more enterprise trials than they were generating.
The VP of Product's roadmap features were revisited then, and half
were cut because JTBD data showed customers didn't need them.

---

## The Full Weekly Review (25 minutes)

See `references/weekly-review.md` — Scaling section. Run it now.
