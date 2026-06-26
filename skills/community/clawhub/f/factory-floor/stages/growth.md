# Growth: Post-Revenue Through ~$1M ARR

You have paying customers. The customer factory exists. Now you need to find
its constraint, exploit it, and run the system — not build random features.

---

## If You Don't Have Numbers

Most startups at this stage are flying on instinct and Stripe dashboards.
That's fine for the triage — use the signals table in SKILL.md. But if the
signals are ambiguous, **your first constraint-serving action is to instrument
the funnel.**

Set up tracking for:
- New trials or signups per week
- Activation rate (% who reach the "aha moment")
- Conversion to paid
- Monthly churn

This IS constraint work. You can't exploit a constraint you can't measure.
Use whatever tool you have — a spreadsheet updated weekly is enough. Don't
spend a month building a dashboard. Spend an hour setting up the tracking,
then use it.

---

## Before You Build Anything

This is the check that saves startups from their own instincts.

When a founder says "we need to build feature X," ask first: **"Is the real
problem that not enough people know you exist?"**

Sharp's research across decades of brand data shows that most potential
customers don't know you exist. When your product works (users who try it
stay) but growth is flat, the answer is almost never another feature. It's
**mental availability** — the probability your brand comes to mind when
someone has the problem you solve.

**Run this diagnostic before any growth initiative:**

1. "Do enough of the right people know we exist?" If no → invest in reach,
   content, partnerships, presence where buyers look. Do NOT build another
   feature.
2. "Can they easily find and try/buy us?" If no → fix distribution, signup
   friction, pricing transparency, marketplace presence.
3. "Are we distinctive enough to be remembered?" If no → invest in brand
   assets (visual identity, tone, tagline), not features.

**This isn't binary.** You may have awareness in one channel and be invisible
in others. You may be known to one segment but not the one that matters most.
The question isn't just "do people know us?" but "do the right people know
us, on the right channels, associated with the right struggling moments?"

Map your Category Entry Points — the 3-5 struggling moments that trigger
buying behavior. For each one, ask: "Would someone in this situation think
of us?" Gaps are where you invest in awareness. Use the 5-minute canvas
(see `stages/pre-revenue.md`) after every conversation to keep this map
current.

**The exception: features that ARE distribution.** Some features directly
serve acquisition — integrations that get you listed in a partner's
marketplace, viral sharing mechanics, embeddable widgets, API access that
turns customers into channels. The test: "Will this feature bring us new
visitors who wouldn't have found us otherwise?" If yes, it's distribution
wearing a feature hat. Build it.

Read `references/pillar-sharp.md` for the full framework, including the
laws of brand growth and CEP mapping.

### Brand Building vs. Activation: Know the Difference

When the constraint is awareness, you're doing **brand building**. When the
constraint is conversion, you're doing **activation**. These are different
types of work with different metrics and different time horizons. Don't
confuse them.

**Brand building (long-term):**
- Builds mental availability over time
- Effects take months to materialize
- Measure: reach, brand awareness, CEP coverage
- Examples: content that educates, thought leadership, sponsorships, PR

**Sales activation (short-term):**
- Converts existing demand into action
- Effects visible within days/weeks
- Measure: clicks, demos booked, trials started, conversions
- Examples: "book a demo" ads, retargeting, promos, direct outreach

**The budget rule (Binet & Field):** For established brands, ~60% brand
building, ~40% activation. For early startups, the ratio shifts toward
activation (you need revenue now), but don't go 100% activation. Even
10-20% brand investment builds memory structures that make future activation
cheaper.

**Why this matters:** Founders who run 100% activation see short-term
metrics that look fine. But they're harvesting demand without replenishing
it. Long-term growth stalls. When you finally try brand building, it takes
months to show up — and by then, you've burned runway on activation that
kept getting more expensive.

When awareness is the constraint, measure reach, not clicks. You're building
memory structures, not harvesting demand. Different work, different metrics.

See `references/pillar-ritson.md` for the full long vs. short framework.

### The Awareness Cadence (when awareness is the constraint)

**Weekly (5 min during the constraint review):**

1. **Did we publish/distribute anything this week?** One piece of content,
   one outreach batch, one partnership touchpoint — something that puts the
   brand in front of people who don't know you yet. If the answer is no,
   that's a problem.

2. **Which CEPs did we cover?** Each piece of content should map to a
   specific CEP. Track which CEPs you're covering — rotate through your
   top 5-7.

3. **Reach check.** How many *new* people saw us this week? Not engagement
   — reach (unique views, impressions, new subscribers). The trend matters
   more than the number. Flat reach with consistent publishing means you
   need a new channel.

**Monthly (20 min):**

1. **CEP coverage review.** Which CEPs have you addressed in the last 4
   weeks? If two or more high-frequency CEPs have had zero coverage,
   prioritize them next month.

2. **Channel diversity check.** If you're on fewer than 3 channels, you're
   under-diversified. Add one new channel per quarter until you're at 4-5.

3. **Distinctiveness audit.** Review the last month's content side by side.
   Does it look and sound like your brand? Distinctiveness compounds only
   through consistency.

4. **Physical availability spot-check.** Pick one item from the physical
   availability audit and verify it's still healthy. Rotate quarterly.

**Content cadence guidelines:**

| Team size | Minimum weekly output | Channel target |
|---|---|---|
| Solo founder | 1 piece (short-form) | 2 channels |
| 2-3 people | 2 pieces (1 short + 1 long or outreach batch) | 3 channels |
| 4-5 people | 3 pieces (mix of short, long, and partnerships) | 4 channels |

The key behavior is **never going dark.** A week with no output is a week
where memory structures decay. Consistency matters more than quality of
any individual piece.

---

## The System: Goldratt + Maurya

### Goldratt's Five Focusing Steps

1. **Identify** the constraint. Where does work pile up? Where do downstream
   stages starve?

2. **Exploit** the constraint. Squeeze maximum output without spending money.
   If sales is the constraint, the founder sells — no admin, no code reviews.
   If engineering is the constraint, pre-package every spec so the developer
   never waits.

3. **Subordinate** everything else. Non-constraints serve the constraint,
   even when that means they look idle. Idle capacity at a non-constraint
   is buffer, not waste.

4. **Elevate** the constraint. Only after exploiting and subordinating,
   invest real resources (hire, buy tools, outsource).

5. **Repeat.** After elevating, the constraint moves. Never let inertia
   become the constraint.

**What each role does, based on the current constraint:**

| Current constraint | Founder | Developer | Support/CS |
|---|---|---|---|
| Sales/Pipeline | 100% selling. Nothing else. | Build sales tools, demo flow, landing pages. | Case studies, FAQs, onboarding materials. |
| Engineering | Write specs, do QA, handle support to shield the dev. | Protected focus. One task at a time. | QA, bug reports, documentation, workarounds. |
| Onboarding | Help with onboarding calls. Pause selling if queue is full. | Build onboarding automation, setup wizards. | Protected focus on activating customers. |
| Awareness | Content, outreach, partnerships, speaking. | SEO pages, integrations directory, API docs. | Testimonials, case studies, social proof. |

### The Customer Factory (Maurya)

Every business is a **customer factory** — a system that takes in unaware
visitors and turns them into happy customers:

```
Acquisition → Activation → Revenue → Retention → Referral
```

Each step has a conversion rate. The step with the lowest rate relative to
your goal is your constraint. Fix that one. Ignore the others until it moves.

The factory is linear, but growth has loops. Retained customers refer new
ones. Content attracts users who generate data that improves the product
that attracts more users. When you find a reinforcing loop, invest in it —
a small improvement at any point in the loop accelerates the whole cycle.

**Throughput** = the rate at which you create happy paying customers. Not
signups, not pageviews — happy customers who achieve their desired outcome
and pay you for it.

**Key rules:**

- **Throughput > Activity.** Measure deals closed, customers activated —
  not hours worked or tasks in progress.
- **WIP is inventory, and inventory is liability.** A half-built feature
  consumes resources and generates zero revenue.
- **"Stop starting, start finishing."** Nobody begins new work until current
  work is done. If blocked, help someone else finish theirs.
- **Local optimization ≠ global optimization.** Marketing generating more
  leads while activation is broken = pouring water through a sieve.

---

## The Execution Loop: GOLEAN

Identifying the constraint tells you *where* to focus. GOLEAN tells you
*how to run the sprint*. Use it as a 2-week cycle:

1. **Go** — State the constraint. Set a goal with four numbers: **target**
   (where you want to be), **baseline** (where you are now), **trend**
   (which direction it's moving), and **timeframe** (this cycle). Example:
   "Increase trial signups from 200/mo (baseline, flat trend) to 280/mo
   by end of cycle." Not "work on acquisition."

2. **Observe** — Measure the constraint's current performance. What are the
   numbers right now? What does the funnel look like? Baseline before you act.

3. **Learn** — Run 1-2 focused experiments that target the constraint. Not
   five. Not a roadmap. One or two bets, sized to complete within the cycle.

4. **Evaluate** — Did throughput increase? Not "did we ship the thing" — did
   the constraint actually move? Check the numbers, not the activity log.

5. **Analyze** — What worked? What didn't? Systemize what worked so you
   don't lose it. Kill what didn't so you don't repeat it.

6. **Next** — If the constraint broke (throughput increased and the
   bottleneck visibly shifted), identify the new constraint. If not, run
   another experiment on the same one. Return to Go.

**Cycle length:** 2 weeks. Fast enough to learn, slow enough to execute
meaningfully. If 2 weeks feels too long, shorten to 1 week but never run
more than 2 experiments per cycle.

---

## Managing Projects Against the Constraint

### Check your team's state first

Before planning the sprint, ask: **what state is the team in?**

- **Falling behind** — backlog grows every week, morale dropping. Reduce
  scope or add capacity before doing anything else.
- **Treading water** — critical work gets done but nothing improves. Reduce
  WIP, consolidate effort, finish things. The fix is focus, not more work.
- **Repaying debt** — momentum is building, compound improvements emerging.
  Protect this time. Don't interrupt with new priorities.
- **Innovating** — low debt, high morale, new value being created. Maintain
  slack. Prevent over-commitment.

Most startup teams oscillate between the first two states. Every time you
add WIP or change priorities mid-sprint, you push the team back toward
treading water.

### Break priorities into constraint-sized tasks

After the weekly review produces your top 3 priorities, break each one into
tasks that can be completed in 1-3 days. Every task should pass the
constraint test: **"Does completing this task directly increase throughput
at the constraint?"** If the answer is "indirectly" or "eventually," it's
backlog.

**Sizing rule:** If a task will take longer than 3 days, it's too big.
Split it. Big tasks become WIP. WIP becomes inventory.

**Start from the epicenter.** Build the thing it cannot function without
first. A blog page starts with the post, not the sidebar. An onboarding
flow starts with the aha moment, not the welcome email.

### WIP limits are non-negotiable

Set your WIP limit to team size. A three-person team has 3 slots for
in-progress work. That's it. Nobody starts new work until a slot opens.
If you're blocked, help someone else finish theirs. In simulations, teams
with strong WIP limits finished **200x more projects** than teams without
them (Larson).

When a founder says "but we need to get ahead on X," the answer is: "X is
not the constraint. Starting X now increases WIP, extends lead time on
constraint work, and slows throughput. X waits."

This is Goldratt's **Drum-Buffer-Rope** in practice: the constraint sets
the pace (drum), a buffer of ready work sits in front of it, and the rope
ties new work intake to the constraint's consumption rate. Nobody starts
new work faster than the constraint can absorb it.

### Feed the constraint buffer

Maintain 2-3 tasks that are fully specified, unblocked, and ready to pull.
The person or process at the constraint should never wait for their next
piece of work. If the buffer drops below 2, refilling it is the team's
top priority.

**Who fills the buffer?** Non-constraint team members. Spec work, gather
requirements, prepare assets, remove blockers — whatever the constraint
needs to stay at full speed.

### Track throughput, not activity

The board should answer one question at a glance: **"Are we creating happy
paying customers faster than last week?"**

Track these weekly:
- **Throughput metric:** The number that measures output at the constraint
  (trials generated, customers activated, deals closed — depends on where
  the constraint is).
- **Cycle time:** How long tasks spend in progress. If cycle time is
  growing, WIP is creeping up.
- **Buffer health:** How many ready items sit before the constraint. If
  it's consistently empty, the constraint is starving.

Don't track vanity metrics (tasks completed, story points burned, hours
logged). They measure motion, not progress.

### Handle blockers by severity

- **Constraint blocker:** Drop everything. Clear it now. Every hour the
  constraint is blocked is an hour of lost throughput for the entire company.
- **Non-constraint blocker:** Note it, move on. Work on something else that
  feeds the constraint.

### Respect the delay

Most constraint work has a feedback delay. A content strategy takes 4-8
weeks to show up in acquisition. An onboarding improvement takes 2-3
cohorts to show up in activation. Set a minimum evaluation window (usually
one GOLEAN cycle) and don't judge results before it closes.

### Estimate time honestly

Most estimates fail because safety padding gets baked into each task, then
consumed by procrastination and scope creep. The fix: **strip safety from
individual tasks and pool it into a project buffer.**

**The quick protocol:**
1. Get the **focused estimate** for each task — "How long with no
   interruptions?" (50% confidence.)
2. Use the focused estimate as the task duration.
3. Add up the longest dependent chain of tasks. That's the critical chain.
4. **Buffer = critical chain × 0.4.** Add this to the end.
5. The buffer end date is the only date you commit to externally.

That's it. A 20-day chain gets an 8-day buffer. Commit date = day 28.
Don't overthink the multiplier. 0.4 works for almost everything — it's
aggressive enough to keep urgency but safe enough to absorb real surprises.

To build this skill over time, use the two-question split (focused + safe
estimate) from `references/estimation.md` — it trains you to see estimates
as ranges, not points.

**When to estimate vs. measure vs. time-box:**

| Situation | Method |
|---|---|
| Novel work, external commitment | Focused estimates + pooled buffer |
| Ongoing work with 3+ weeks of data | Cycle time measurement (median and 85th percentile) |
| Experiments, learning, customer discovery | Time-box at 2 weeks (GOLEAN cycle) |
| Quick internal sizing | T-shirt: S (hours), M (1-2 days), L (3-5 days). XL = break it down. |

**The two-question filter:** Before estimating anything, ask "Is this work
on the constraint?" If yes, estimate carefully. If no, T-shirt size it.

See `references/estimation.md` for why pooled buffers work, calibration
exercises, and alternative sizing methods for edge cases.

### Monitor with the fever chart

Track two numbers weekly: **% of work completed** vs. **% of buffer
consumed.**

- **Green (buffer < 1/3 consumed):** On track. Don't fill the slack with
  scope creep.
- **Yellow (buffer 1/3 to 2/3 consumed):** Plan a recovery option. The
  buffer is doing its job.
- **Red (buffer > 2/3 consumed):** Act now. Fix time and budget, flex
  scope. Cut features to fit the deadline. Redirect non-constraint
  capacity to help.

### Run the relay race

When someone finishes a task, the next person starts **immediately** — not
on the scheduled date. Early finishes evaporate in traditional project
management. In the relay race, they propagate forward.

### Communicate timelines honestly

Never give a point estimate externally. Always give a range.

**To a customer or stakeholder:** "We expect to deliver between [focused
estimate date] and [buffer end date]." The buffer end date is the only
commitment.

**To the team:** Communicate buffer status, not individual task deadlines.
"We've consumed 40% of buffer with 60% of work done — we're healthy."

**If someone demands a single date:** Give the buffer end date. That's
what the buffer is for.

---

## JTBD in the Weekly Rhythm

JTBD is not a one-time research project. It's a weekly habit.

**After every conversation:** Fill in the 5-minute canvas (see
`stages/pre-revenue.md`). Every sales call, demo, support ticket, and
churn conversation is JTBD data.

**During the weekly review:** Review the week's canvases. Do the forces
match your constraint diagnosis? Three canvases showing the same anxiety
might mean your highest-leverage move isn't a feature — it's a guarantee,
a testimonial, or a simpler onboarding. Update the running pattern: which
pushes, pulls, anxieties, and habits keep appearing?

**Monthly:** Review all canvases. Have your assumptions about the forces
changed? Should your messaging change? Should your constraint diagnosis
change?

**Mine what you already have:** Lost deal notes, churn conversations,
and support tickets already contain JTBD data. For lost deals: "What did
you go with instead?" For churned customers: "What are you using now?"

---

## Worked Example: Growth Stall

**ConvoAI — AI meeting summaries, B2B SaaS, 8-person team, $40K MRR.**

The founder asks: "Growth has stalled for 3 months. We think we need Slack
integration and CRM sync to compete. What should we work on?"

**Step 1: Triage.**

| Question | Answer |
|---|---|
| Enough people finding you? | ~200 trials/month, mostly from one viral blog post 6 months ago. Pipeline is thin. |
| Do signups reach the aha moment? | Yes — 60% activate within the first week. |
| Do activated users pay? | Yes — 35% convert to paid. |
| Do paying customers stay? | Yes — 90% monthly retention. |
| Is the team finishing things? | Mostly, though 2 engineers are split across 3 projects. |

**Diagnosis:** Activation, Revenue, and Retention are healthy. Acquisition
is the constraint. Almost no one is entering the funnel.

**Step 2: Run the "Before You Build" check.**

Users who try ConvoAI love it. Retention is 90%. The product works.
Building Slack integration and CRM sync is optimizing a non-constraint.
It will not move the $40K MRR number.

**Step 3: Exploit the constraint.**

The founder redirects effort to distribution with existing resources:

- Founder spends mornings on outreach, partnerships, and content instead
  of product reviews.
- One engineer moves from CRM sync to building SEO landing pages and an
  integrations directory.
- The CS person collects testimonials and case studies.
- The two engineers on 3 projects drop to 1 project each — finishing >
  starting.

**Step 4: Subordinate.**

Slack integration and CRM sync go on ice. They'll matter later when
acquisition is no longer the bottleneck. Right now they're inventory.

**Step 5: What changes.**

The team's weekly review metric shifts from "features shipped" to "new
trials generated." When trials climb from 200/month to 500/month and the
funnel backs up at activation or revenue, the constraint has moved.

---

## Worked Example: The Constraint Shifts

**ConvoAI — 3 months later. Trials now at 500/month.**

The acquisition work paid off: SEO pages, partnerships, and founder-led
content tripled top-of-funnel. But the weekly review reveals a new problem.

| Metric | Before | Now |
|---|---|---|
| Trials/month | 200 | 500 |
| Activation rate | 60% | 35% |
| Activated → Paid | 35% | 34% |
| Retention | 90% | 88% |

Activation has dropped from 60% to 35%. The new users from SEO and
partnerships are less hand-held than the old ones — they don't get the
"aha moment" without help, and there's no concierge capacity for 500
trials a month.

**The constraint has moved from Acquisition to Activation.**

**Step 1: Name it explicitly.** The founder says in the weekly review:
"Our constraint has moved from acquisition to activation. Starting now,
everything serves activation."

**Step 2: Reassign subordination roles.**

| Role | Was doing (acquisition) | Now doing (activation) |
|---|---|---|
| Founder | Content, outreach, partnerships | Onboarding calls for high-value trials. Pause outreach if queue is full. |
| Engineer A | SEO pages, integrations directory | In-app onboarding wizard, setup health check. |
| Engineer B | Landing page experiments | Fix the 3 drop-off points in trial-to-active flow. |
| CS person | Testimonials, case studies | Protected focus: activate every trial. Track time-to-value. |

**Step 3: Don't abandon acquisition.** The SEO pages and partnerships
that tripled trials don't need daily attention anymore. Put the content
calendar on autopilot (1 post/week, scheduled). Monitor trials weekly —
if they start declining, investigate, but don't redirect capacity back
unless they drop below 400.

**Step 4: Set the new GOLEAN goal.** "Increase activation rate from 35%
(baseline, declining trend) to 50% by end of cycle." Two experiments:
(a) an in-app setup wizard that guides new users to their first meeting
summary in under 3 minutes, (b) a triggered email sequence for users who
sign up but don't import their first meeting within 24 hours.

**Step 5: Update the board.** Buffer column now feeds activation work.
WIP tags shift. The throughput metric changes from "trials generated" to
"users activated."

---

## The Weekly Constraint Review (10 minutes)

See `references/weekly-review.md` — Growth section. Run it now.

---

## Applying This to Tools

This framework is tool-agnostic. When setting up your tool:

- The board should show where work piles up (the constraint is visible).
- Every task should be taggable by which constraint it serves.
- WIP limits should be visible in column/section names.
- Weekly review metrics should be accessible in under 2 minutes.
- A "buffer" stage before the constraint — 2-3 ready items so the
  bottleneck never starves.

These principles apply to Linear, Asana, Notion, Monday, Trello, Jira,
GitHub Projects, a whiteboard with sticky notes.

---

## When to Graduate

You're ready for `stages/scaling.md` when:

- You have 10+ people, or multiple workstreams across teams.
- $1M+ ARR (or equivalent traction for your model).
- The constraint keeps showing up as a **coordination problem** rather
  than a capacity problem — priorities conflict across teams, people
  disagree on the diagnosis, or the triage points to a funnel step but
  fixing it doesn't move throughput.

Until then, stay here. This stage's tools handle most startups through
product-market fit and early scaling.
