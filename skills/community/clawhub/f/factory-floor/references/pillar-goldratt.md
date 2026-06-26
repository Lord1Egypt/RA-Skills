# Pillar 1: The Theory of Constraints (Goldratt) — Reference

## Contents
- [Origin](#origin)
- [The Five Focusing Steps — Startup Translation](#the-five-focusing-steps)
- [Throughput Accounting for Startups](#throughput-accounting)
- [Little's Law](#littles-law)
- [Drum-Buffer-Rope (DBR)](#drum-buffer-rope)
- [Context-Switching Tax (Weinberg)](#context-switching-tax)

## Origin

Eli Goldratt introduced the Theory of Constraints in *The Goal* (1984). The
core thesis: every system has exactly one constraint at any moment, and the
system's output is limited entirely by that constraint. Improving anything
other than the constraint does not improve the system.

## The Five Focusing Steps — Startup Translation

### 1. Identify the Constraint

In manufacturing, the constraint is the machine with the longest queue. In a
startup, look for these signals:

- **Where does work pile up?** Tickets waiting for engineering? Leads waiting
  for the founder to demo? Signed customers waiting for onboarding?
- **Where do downstream stages starve?** Engineering done but nothing to ship
  because there are no customers? Customers ready but nothing new to show them?
- **What is the team most often waiting on?** The answer reveals the bottleneck.

Common startup constraints by function:

| Function | Signals it's the constraint |
|---|---|
| Sales/Pipeline | Thin pipeline, sparse demos, deals stalling. Engineering and onboarding have spare capacity. |
| Engineering/Product | Feature requests exceed dev capacity. Sales sells what can't be built. Half-built features accumulate. |
| Onboarding/Activation | Deals close but customers can't go live. Churn starts before expansion. Support queue grows. |
| Market/Awareness | Product works well for those who try it, but too few people enter the funnel. Growth is flat despite good retention. |

Important: this is a self-correcting process. If you invest in the wrong area,
the real constraint stays the same and nothing improves. That's your signal to
re-identify.

### 2. Exploit the Constraint

Before spending money, squeeze maximum output from the bottleneck. The
principle: make the constraint more productive with existing resources before
investing new ones. Every minute the constraint spends on non-constraint
work is lost throughput for the entire company.

See the role-by-constraint table in `stages/growth.md` ("What each role does,
based on the current constraint") for the startup-specific translation.

### 3. Subordinate Everything Else

This is the hardest step psychologically. The rules:

- Non-constraints must serve the constraint, even when that means they appear
  underutilized.
- Idle capacity at a non-constraint is not waste — it's buffer. A highway needs
  an emergency lane.
- Non-constraint work that doesn't feed the constraint should stop.

### 4. Elevate the Constraint

Only after Steps 2 and 3. Now you invest: hire at the constraint, buy tools
for the constraint, outsource non-constraint work to free capacity.

Every unit of capacity added at the constraint = throughput of the whole
company. A hire at a non-constraint adds cost without adding throughput.

See `stages/scaling.md` for detailed guidance on hiring as elevation.

### 5. Repeat (Prevent Inertia)

After elevating, the constraint moves. Goldratt's warning: "Do not allow
inertia to become the system's constraint." The processes and policies built
for the old constraint may now be counterproductive.

This is why the weekly constraint review exists. Every week, re-ask: "What is
our constraint now?" If it has shifted, update subordination roles immediately.

## Throughput Accounting for Startups

Goldratt's three metrics, translated:

| Manufacturing term | Startup equivalent |
|---|---|
| **Throughput (T)** | Revenue from happy paying customers. The rate of creating monetizable value. |
| **Inventory (I)** | WIP — half-built features, unworked leads, unsigned proposals, customers in limbo. |
| **Operating Expense (OE)** | Everything spent to run: salaries, cloud infra, tools, rent. Essentially fixed in the short term. |

**The decision hierarchy:**
1. Does this increase T? → Prioritize.
2. Does this reduce I? → Do it next.
3. Does this reduce OE? → Nice, but secondary.

Most founders invert this and start with cost-cutting. TOC says maximize T
first, always. Ash Maurya echoes this: "The idea of throughput accounting is
flipping cost-cutting on its head and saying the bigger potential is thinking
about upside potential."

## Little's Law

WIP = Throughput × Lead Time. This is a mathematical identity, not a theory.

If WIP increases and Throughput holds constant, Lead Time must increase. Every
time you start new work without finishing existing work, you're increasing WIP,
which extends lead time on everything.

The practical implication: **finishing one thing is always better than starting
two things.** A team completing one feature per week delivers more value than a
team with five features "in progress" for three weeks each.

## Drum-Buffer-Rope (DBR)

Drum-Buffer-Rope is Goldratt's scheduling mechanism for managing flow through
a system. Where the Five Focusing Steps tell you *what* to do about the
constraint, DBR tells you *how to pace the whole system* around it.

**Drum:** The constraint sets the pace. It determines the system's maximum
throughput, so everything runs at the constraint's rhythm. In a startup, if
engineering is the constraint and can ship one feature per week, the whole
company operates on a one-feature-per-week drum. Marketing doesn't generate
leads faster than sales can close them. Sales doesn't close deals faster than
onboarding can absorb them. The constraint's capacity IS the tempo.

**Buffer:** A time buffer placed in front of the constraint ensures it never
starves. Work that feeds the constraint should arrive early enough that the
constraint always has something ready to pull. In practice: 2-3 fully
specified, unblocked tasks queued before the bottleneck person or process.
If the buffer runs dry, the constraint sits idle and the entire system loses
throughput.

**Rope:** A signal that ties the start of new work to the constraint's
consumption rate. New work enters the system only when the constraint pulls
it — not when someone upstream is ready to push it. The rope prevents
overproduction at non-constraints, which would pile up as WIP (inventory)
without increasing throughput.

### DBR in a startup

| DBR element | Manufacturing | Startup equivalent |
|---|---|---|
| Drum | Bottleneck machine's cycle time | The constraint's capacity (demos/week, features/sprint, customers onboarded/week) |
| Buffer | Queue of parts in front of the bottleneck | 2-3 ready tasks before the constraint; pre-qualified leads before the sales constraint; signed customers queued before onboarding |
| Rope | Signal to release raw materials | WIP limit — nobody starts new work until the constraint pulls. New leads aren't generated faster than the constraint can process them. |

**The practical rule:** Before starting any new initiative, ask: "Can the
constraint absorb this?" If engineering can ship one thing per sprint,
planning three things is creating inventory, not progress. The rope prevents
this by tying intake to the constraint's actual throughput.

DBR and the Five Focusing Steps work together: the Five Focusing Steps tell
you WHERE to intervene (identify, exploit, subordinate, elevate). DBR tells
you how to PACE the system so non-constraints don't overproduce and the
constraint never starves. The weekly constraint review checks both: is the
constraint identified correctly (Five Focusing Steps)? Is the buffer healthy
and is WIP controlled (DBR)?

---

## Context-Switching Tax (Weinberg)

Gerald Weinberg's research: each additional parallel project costs ~20% in lost
productivity from context-switching.

| Simultaneous projects | % of time available per project | % lost to switching |
|---|---|---|
| 1 | 100% | 0% |
| 2 | 40% | 20% |
| 3 | 20% | 40% |
| 4 | 10% | 60% |
| 5 | 5% | 75% |

For a three-person startup, the practical limit is one active task per person.
WIP limit = team size.
