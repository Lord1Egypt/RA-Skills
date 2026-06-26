# Factory Floor

[![npm](https://img.shields.io/npm/v/@swiftner/factory-floor)](https://www.npmjs.com/package/@swiftner/factory-floor)

A startup coach that turns Claude into a thinking partner for prioritization and execution. It won't tell you what to do — it'll ask the questions you're avoiding.

Works with **Claude Code**, **Claude Desktop**, **OpenAI Codex**, and any agent that supports the [open agent skills standard](https://agentskills.io).

### Claude Code

```bash
npx @swiftner/factory-floor
```

Installs to `~/.claude/skills/factory-floor/`. Triggers automatically when you talk about priorities, bottlenecks, what to build, or why growth is flat.

### OpenAI Codex

```bash
npx @swiftner/factory-floor
```

Installs to `~/.codex/skills/factory-floor/`. Codex picks it up automatically — trigger with `/skills` or `$` to mention it directly, or just describe your problem and it will activate implicitly.

Or install via ClawHub:

```bash
clawhub install factory-floor
```

### Claude Desktop

1. Open Claude Desktop and create a new **Project**
2. Set the contents of [`SKILL.md`](SKILL.md) as the project's **Custom Instructions**
3. Upload these files as **Project Knowledge**:
   - `stages/pre-revenue.md`
   - `stages/restart.md`
   - `stages/growth.md`
   - `stages/scaling.md`
   - `references/intake.md`
   - `references/misdiagnoses.md`
   - `references/coaching-patterns.md`
4. Optionally upload reference files for deeper dives:
   - `references/jtbd.md`
   - `references/pillar-goldratt.md`
   - `references/pillar-maurya.md`
   - `references/pillar-sharp.md`
   - `references/pillar-ritson.md`
   - `references/pillar-strategy.md`
   - `references/estimation.md`

Start a conversation in that project and Claude will run the triage and route to the right stage — the same way the skill works in Claude Code.

## What it does

You say "should we build Slack integration?" and instead of a pros-and-cons list, you get:

- *"What's your retention like — do people who try it stay?"*
- *"Where are new trials coming from? Is that number growing?"*
- *"If retention is 90% but trials are flat... is the real problem that not enough people know you exist?"*
- *"Would Slack integration bring you new customers — or is it a feature for people who already use you?"*

It asks, you decide. Three areas where founders consistently fool themselves:

**You're building when you should be selling.** The product works — users who find it stay. But nobody's finding it. You don't need features. You need to exist in more people's heads.

**You're doing five things and finishing none.** Each parallel project costs ~20% in context-switching. With five in flight, you're losing three-quarters of your capacity to the act of juggling.

**You're optimizing the wrong thing.** Marketing is generating leads but onboarding can't absorb them. You just created inventory, not progress. The system has one bottleneck — everything else is either serving it or wasting time.

## It adapts to your stage

A quick triage loads the right playbook:

| Stage | What it covers |
|---|---|
| **[Pre-revenue](stages/pre-revenue.md)** | No customers yet? Don't build. Five tests before you write code. Napkin math. The Mafia Offer. A worked example of killing a bad idea in 20 minutes. |
| **[Restart](stages/restart.md)** | Had customers, lost them. Forensics first — product failure, fit failure, or sales execution failure? Churned customer interviews. Restart sequence. |
| **[Growth](stages/growth.md)** | Have customers, small team. Find the constraint, exploit it, run the system. GOLEAN sprints, WIP limits, brand building vs. activation. Two worked examples. |
| **[Scaling](stages/scaling.md)** | $100K+ MRR or 10+ people. Policy constraints, multi-team coordination, hiring as elevation, buffer management, timeline communication. |

## The six frameworks

Each covers a different blind spot:

**Jobs To Be Done** — Why customers buy (and don't). The four forces behind every deal: push, pull, anxiety, habit. Switch interviews, a 5-minute post-conversation canvas, opportunity scoring. ([Reference](references/jtbd.md))

**Theory of Constraints** (Goldratt) — Your startup has exactly one bottleneck. Find it, squeeze it, subordinate everything else. Triage, role-by-constraint table, WIP discipline. ([Reference](references/pillar-goldratt.md))

**Customer Factory** (Maurya) — Acquisition → Activation → Revenue → Retention → Referral. Which step is broken? GOLEAN cycles, napkin test, Mafia Offer. ([Reference](references/pillar-maurya.md))

**How Brands Grow** (Sharp) — Growth comes from reaching non-buyers, not delighting power users. CEP mapping, physical availability audit, reach over frequency. ([Reference](references/pillar-sharp.md))

**Marketing Strategy Discipline** (Ritson) — Diagnosis before strategy, strategy before tactics. STP, positioning as 2-3 associations defended consistently, differentiation + distinctiveness, Binet & Field budget allocation. ([Reference](references/pillar-ritson.md))

**Strategic Thinking** (Rumelt, Clausewitz, Dixit & Nalebuff) — Is what you are doing actually a strategy? How to operate under uncertainty, when to stop pushing, and what the other side will do. ([Reference](references/pillar-strategy.md))

Plus [estimation](references/estimation.md) — why your gut is wrong, critical chain buffers, and calibration exercises.

JTBD sits underneath the other five. You can't find the constraint if you don't know what job the customer hired you to do.

## Things you can ask

| You say | It does |
|---|---|
| "What should we work on this week?" | Runs the triage. Finds the bottleneck. Helps you pick three priorities. |
| "We have no customers yet" | Problem validation before code. Napkin math, five tests, Mafia Offer. |
| "Should we build X or focus on sales?" | Asks where the constraint is and whether X serves it. |
| "We're spread too thin" | Figures out what to stop. WIP audit, team state check. |
| "Why do deals ghost?" | Walks through the four forces. Where is the deal dying? |
| "Nobody knows we exist" | Maps Category Entry Points. Audits physical availability. Builds a reach cadence. |
| "How long will this take?" | Helps you build an honest buffer instead of giving you a number. |
| "Help me prep for our weekly review" | Runs the review format for your stage: constraint, numbers, pile, focus. |

## The weekly review

Same structure, scaled to your stage:

- **Pre-revenue** (10 min) — How many conversations? What did we learn? Has the hypothesis survived?
- **Growth** (10 min) — Name the constraint, check throughput, find where work piles up, set 3 priorities.
- **Scaling** (25 min) — Funnel diagram, buffer/flow check, traffic lights on initiatives, policy constraint scan.

## Credits

- **Clayton Christensen** — *The Innovator's Dilemma*, *Competing Against Luck*. Jobs To Be Done.
- **Bob Moesta** — *Demand-Side Sales 101*. Forces of progress, switch interviews.
- **Tony Ulwick** — *Jobs to be Done: Theory to Practice*. Outcome-Driven Innovation.
- **Eli Goldratt** — *The Goal*, *Critical Chain*. Theory of Constraints.
- **Ash Maurya** — *Running Lean*, *Scaling Lean*. Customer Factory, Lean Canvas, Mafia Offer.
- **Byron Sharp** — *How Brands Grow*. Mental and physical availability.
- **Mark Ritson** — Mini MBA in Marketing. Marketing strategy discipline, STP, positioning.
- **Richard Rumelt** — *Good Strategy Bad Strategy*, *The Crux*. The kernel of strategy, bad strategy signs, proximate objectives.
- **Carl von Clausewitz** — *On War*. Fog, friction, center of gravity, culminating point, moral forces.
- **Avinash Dixit & Barry Nalebuff** — *The Art of Strategy*. Game theory for business: commitment, cooperation, information asymmetry.
- **Les Binet & Peter Field** — *The Long and the Short of It*. Brand building vs. activation budget allocation.
- **April Dunford** — *Obviously Awesome*. Positioning from JTBD.
- **Douglas Hubbard** — *How to Measure Anything*. Estimation calibration.

---

Made by [Swiftner](https://swiftner.com).
