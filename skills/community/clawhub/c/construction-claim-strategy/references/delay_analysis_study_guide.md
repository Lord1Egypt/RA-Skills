# Delay Analysis Study Guide for Contract Managers

Practical study notes for delay analysis in construction and infrastructure projects.

**Sources:** SCL Delay and Disruption Protocol 2nd Edition (February 2017) + Rider 1 (February 2022), AACEi Recommended Practice 29R-03, published case law.

> **Caution:** Always confirm which contract edition applies before relying on any clause references. This guide does not constitute legal advice.

---

## Part 1: What Is Delay Analysis?

Delay analysis is the process of identifying what caused a project delay, who is responsible, and what the time/cost consequences are.

It answers two distinct questions:
1. **Is the contractor entitled to an Extension of Time (EOT)?** — a time question
2. **Is the contractor entitled to compensation?** — a money question

These are linked but separate inquiries (see SCL Principle 12).

---

## Part 2: Key Concepts

### 2.1 Delay vs Disruption vs Prolongation

| Concept | What It Is | Result | Claim Type |
|---------|-----------|--------|------------|
| **Delay** | Activity takes longer than planned or starts late | Critical path pushed → later completion | EOT (time) |
| **Disruption** | Reduced productivity / efficiency — more resources needed per unit of work | Additional cost, may or may not affect completion date | Money (cost) |
| **Prolongation** | Extended presence on site due to delay | Additional preliminaries, site overheads | Money (cost) |

**Key distinction:** You can have disruption WITHOUT delay (if the affected activity is not on the critical path). You can also have delay WITHOUT disruption (if the activity simply stops).

### 2.2 Types of Delay

| Type | Who Bears Risk | EOT? | Compensation? |
|------|---------------|------|---------------|
| **Employer Risk Event** (late instructions, design changes, site access) | Employer | ✓ Yes | ✓ Yes (usually) |
| **Neutral/Excusable Event** (exceptionally adverse weather, force majeure) | Shared | ✓ Yes | ✗ Usually not |
| **Contractor Risk Event** (poor planning, resource shortages) | Contractor | ✗ No | ✗ No |
| **Concurrent Delay** (employer + contractor delays at same time) | Complex | ✓ Yes (SCL view) | Debatable — see 2.4 |

**Excusable vs Compensable:** An excusable delay relieves the contractor from LD (i.e. EOT). A compensable delay additionally entitles the contractor to money. All compensable delays are excusable, but not all excusable delays are compensable.

### 2.3 Critical Path & Float

The **critical path** is the longest sequence of activities that determines the project completion date. Only delays to activities on the critical path will actually delay the project.

**Float** = the time an activity can slip without affecting the critical path.

**Who owns the float?** The SCL Protocol says float should generally be available to the project (not owned by either party) unless the contract says otherwise.

#### Understanding Float Types

| Float Type | What It Means | EOT Implication |
|-----------|---------------|-----------------|
| **Positive Float** | Activity has buffer — can slip without delaying completion | Employer delay may consume float before affecting critical path |
| **Zero Float** | Activity is on the critical path — any delay directly delays completion | Every day of employer delay = one day of EOT entitlement |
| **Negative Float** | Projected completion already exceeds contract completion date | EOT can still be claimed for employer risk events — see below |

#### Negative Float & EOT Entitlement

Negative float does **NOT** bar an EOT claim. Negative float occurs when the programme's projected completion date already exceeds the contract completion date, even before a new delay event arises. This is common on complex infrastructure projects.

The SCL Protocol (Principles 6, 7 and 10) requires that each delay event be assessed for its own **incremental impact** on the critical path. If an employer risk event extends the completion date by a further 2 weeks — even where the programme already shows negative float — that 2-week impact remains an employer-caused delay.

**Three practical scenarios:**

- **Scenario 1 — Negative float from contractor delays:** The contractor still claims EOT for any employer risk event's incremental impact. Time Impact Analysis (TIA) handles this best.
- **Scenario 2 — Negative float from employer delays:** This strengthens the EOT position. The employer delay events that drove the programme into negative float are themselves grounds for EOT.
- **Scenario 3 — Concurrent delay with negative float:** The most complex scenario. Under the *Malmaison* approach, the contractor still gets EOT to protect against LDs but may not recover prolongation costs for the concurrent period.

**Bottom line:** Float status (positive, zero, or negative) does not determine EOT entitlement. It is the **cause and incremental impact** of each delay event that matters.

#### Terminal Float

Terminal float is the gap between the contractor's planned completion date and the contract completion date.

Per SCL Protocol Principle 13 (Early Completion): if the contractor planned to finish early and an employer delay consumes that terminal float, the contractor may still have a **compensation claim** for disruption to its planned programme — even if the contract date has not been breached.

### 2.4 Concurrent Delay

**SCL Protocol position:** Where employer delay is concurrent with contractor delay → contractor gets EOT (to protect from LD). But contractor may **NOT** recover prolongation costs for the concurrent period. This is the *Malmaison* approach (*Henry Boot v Malmaison* [1999]).

#### Three Critical Nuances

**Nuance 1 — True Concurrent vs Sequential Concurrent**

True concurrent delay means two delay events start and end at the same time, both independently affecting the critical path. Sequential concurrent delay means the events overlap but do not start together. Tribunals apply the *Malmaison* approach more readily to true concurrent delay; sequential concurrent delay is often analysed by isolating each event's impact via TIA.

**Nuance 2 — Contractual Allocation**

The *Malmaison* default can be contracted out. In *North Midland Building Ltd v Cyden Homes Ltd* [2018] EWCA Civ 1744, the English Court of Appeal upheld a contract clause that expressly excluded EOT where contractor delay was concurrent with employer delay. Parties are free to allocate the risk of concurrent delay as they choose.

**Practical action:** Read the EOT clause carefully. Some bespoke amendments may include a "contractor caused concurrent delay" carve-out that strips the contractor of EOT entitlement. If found, raise this with management early — it is a major risk allocation issue.

**Nuance 3 — Apportionment Approach**

In *City Inn Ltd v Shepherd Construction Ltd* [2010] CSIH 68, the Scottish courts took a different view: where it is impossible to say which delay was "dominant", the tribunal can apportion the EOT between employer and contractor causes (e.g. 60/40). This approach has not been adopted in English courts but remains influential and may be argued in arbitration.

**Practical tip:** Always try to separate and identify each delay cause individually. Strong contemporaneous records are the best defence against concurrent delay arguments.

### 2.5 Pacing Delays

**What is pacing?** Pacing occurs when one party (usually the contractor) deliberately slows non-critical work to match the pace of the other party who is causing the critical path delay. It is a rational business decision.

**Why it matters:** Pacing is **not** a contractor culpable delay. But it is frequently mischaracterised as one — especially in retrospective analysis.

**How to prove pacing:**
- Issue contemporaneous notice that you are pacing in response to the specific employer delay event
- Identify the employer delay event you are pacing (cite notice/event reference)
- Show the activity being paced was not on the critical path but for the employer delay
- Demonstrate you had the resources and capability to proceed at planned pace
- Confirm pacing did not extend the project completion date beyond the employer delay impact

**Quick test:** "Could I have proceeded at planned pace if the employer delay event had not occurred?" If YES → pacing. If NO → genuine contractor delay.

---

## Part 3: The SCL Protocol — 22 Core Principles

> References are to the SCL Delay and Disruption Protocol, 2nd Edition (February 2017), as supplemented by Rider 1 (February 2022). Rider 1 added guidance on COVID-19, BIM, concurrent delay analysis, and the relationship between EOT and compensation.

| # | Principle | Key Point |
|---|-----------|-----------|
| 1 | **Programme & Records** | Maintain a proper baseline programme and comprehensive contemporaneous records. No records = no claim. |
| 2 | **Purpose of EOT** | EOT relieves the contractor from LD liability and preserves the employer's right to levy LD. |
| 3 | **Contractual Requirements** | Comply with notice requirements strictly. Late notice can be a time-bar. |
| 4 | **Do NOT "Wait and See"** | Analyse delay impact contemporaneously. Prospective analysis is preferred over retrospective. |
| 5 | **Procedure for Granting EOT** | Contract Administrator should assess and grant EOT promptly. |
| 6 | **Effect of Delay** | Distinguish between employer risk events and contractor risk events. |
| 7 | **Incremental Review** | Review EOT entitlement incrementally as delay events occur. |
| 8–9 | **Float** | Float belongs to the project, not one party. See Section 2.3 for negative float. |
| 10 | **Concurrent Delay & EOT** | Contractor entitled to EOT for employer delay even if concurrent with contractor delay. |
| 11 | **Time-Distant Analysis** | Use recognised methods for retrospective analysis (see Part 4). |
| 12 | **EOT ≠ Compensation** | EOT entitlement does not automatically mean compensation. |
| 13 | **Early Completion** | Employer delay consuming terminal float may still entitle contractor to compensation. |
| 14 | **Concurrent Delay & Compensation** | Contractor may not recover prolongation costs during concurrent delay periods. |
| 15 | **Mitigation** | Both parties have mitigation obligations. |
| 16 | **Acceleration** | Directed → compensation. Voluntary → own cost. Constructive → may claim costs (notify first!). |
| 17 | **Global Claims** | Permissible only when impracticable to separate causes/effects. Courts are sceptical. |
| 18 | **Disruption** | Distinct from delay. Prove using measured mile, project-specific study, earned value, or industry studies. |
| 19 | **Variations** | Variations can cause both time and cost impact. Consider disruptive effect. |
| 20 | **Prolongation Costs** | Based on actual additional cost incurred due to extended time on site. |
| 21 | **Tender Allowances** | Actual cost, not tender rates, should be the basis for prolongation compensation. |
| 22 | **Period of Evaluation** | Assess compensation for the period the delay actually affected. |

---

## Part 4: Delay Analysis Methods

### Method Frameworks

Two recognised frameworks:
- **SCL Protocol** (UK) — identifies six delay analysis methodologies
- **AACEi Recommended Practice 29R-03** (US) — classifies methods using a 9-method matrix

Both are accepted in international arbitration.

### Overview — Seven Methods

| Method | When Used | Prospective/Retrospective | Complexity |
|--------|-----------|--------------------------|------------|
| **As-Planned vs As-Built** | Simple comparison | Retrospective | Low |
| **Impacted As-Planned** | Add delay events to baseline | Prospective | Medium |
| **Collapsed As-Built (But-For)** | Remove delay events from as-built | Retrospective | Medium-High |
| **Time Impact Analysis (TIA)** | Insert delay events at time they occurred | Both | High |
| **Windows Analysis** | Divide project into time windows | Both | High |
| **Retrospective Longest Path** | Trace longest path on as-built | Retrospective | Medium |

### As-Planned vs As-Built
- Compare the original programme to what actually happened
- **Pros:** Simple, easy to understand
- **Cons:** Doesn't show causation; doesn't account for logic changes
- **Best for:** Initial overview or simple disputes

### Impacted As-Planned
- Start with the baseline programme; add delay events as constraints
- **Pros:** Forward-looking; easy to model
- **Cons:** Assumes baseline was realistic; doesn't consider actual progress
- **Best for:** Early-stage EOT applications

### Collapsed As-Built (But-For)
- Start with the as-built programme; remove delay events
- **Pros:** Based on what actually happened
- **Cons:** Difficult to reconstruct; subjective removal of events
- **Best for:** Post-completion claims

### Time Impact Analysis (TIA) — Preferred Method
- Insert each delay event into the programme at the time it occurred
- Analyse the critical path impact of each event progressively
- **Pros:** Most rigorous; shows causation; accepted by tribunals; handles negative float correctly
- **Cons:** Resource-intensive; requires good records and updated programmes
- **Best for:** Complex projects, especially where negative float is present

### Windows Analysis
- Divide the project into time "windows" (e.g. monthly or by milestone)
- Analyse the critical path and delays within each window
- **Pros:** Systematic; handles concurrent delays well
- **Cons:** Window boundary selection is subjective; very resource-intensive
- **Best for:** Large projects with many delay events

### Retrospective Longest Path Analysis
- Identify the longest path on the as-built programme (the actual critical path)
- Walk back through the activities and identify what delayed each one
- **Pros:** Grounded in what actually happened; intuitive; useful when baseline is disputed
- **Cons:** May ignore parallel critical paths; can miss delays absorbed by float
- **Best for:** Disputes where the baseline programme is challenged

### Choosing a Method

**For prospective/ongoing analysis:**
- Time Impact Analysis — insert delay events as they occur
- Impacted As-Planned — for quick early-stage EOT applications

**For retrospective/post-completion analysis:**
- Windows Analysis — if many delay events across the project
- Collapsed As-Built — if isolating specific employer delay events
- Retrospective Longest Path — if as-built records are strong but baseline is disputed

---

## Part 5: Disruption Claims — How to Prove It

### The Walter Lilly Test (UK, 2012)

Four elements:
1. **Compensable event** — identify the contract clause
2. **Event caused disruption** — causal link (but-for test)
3. **Disruption caused loss** — quantify the financial impact
4. **Notice given** — comply with contractual notice requirements

### Causation Standard

Per *Costain Ltd v Charles Haswell & Partners Ltd* [2009] EWHC B25 (TCC): the contractor must prove not just that disruption occurred but that the **specific event caused identifiable productivity loss**. General assertions of "inefficiency" without linking specific events to specific losses will fail.

**Practical implication:** For each disruption claim, build a causation chain:
1. What was the event?
2. Which activities were affected?
3. What was the productivity benchmark?
4. What was the actual productivity?
5. What is the difference in cost?

### How to Quantify Disruption

| Method | Description | Persuasiveness |
|--------|-------------|----------------|
| **Measured Mile** | Compare productivity in disrupted vs undisrupted period on the same project | Highest |
| **Project-Specific Study** | Detailed analysis of the project's productivity data | High |
| **Earned Value Analysis** | Compare planned vs actual resource usage per unit of work | Medium-High |
| **Industry Studies** | Published productivity loss factors (Leonard, MCAA) | Lower |
| **System Dynamics** | Computer modelling of productivity impacts | Variable |

Measured Mile is the most accepted method. Industry studies are weakest because tribunals view them as too generic.

### Common Causes of Disruption

- Variations / change orders
- Late information or approvals
- Change in work sequencing
- Restricted site access
- Trade stacking (too many trades in same area)
- Acceleration instructions

---

## Part 6: Force Majeure & Frustration

### Force Majeure (Contract-Based)

- Defined in the contract — check the specific FM clause
- Consequences depend on contract terms (EOT? Termination? Cost sharing?)
- Common FM events: war, pandemic, natural disaster, government action

#### Hardship vs Force Majeure

**Hardship is NOT Force Majeure.** An event becoming more expensive or difficult does not qualify as FM. FM requires the event to make performance **impossible or legally impermissible**, not merely uneconomical.

#### COVID-19 Lessons

- Generic FM clauses without specific pandemic reference often failed to trigger
- Government-mandated shutdowns generally qualified as FM (or "change in law")
- Modern FM clauses now expressly list "pandemic", "epidemic", and "public health emergency"
- Notice and mitigation obligations were strictly enforced

### Frustration (Common Law — Last Resort)

- Contract is discharged — both parties walk away
- Only applies when performance is impossible, illegal, or radically different
- Very rarely successful — courts set a very high bar
- **NOT frustration:** cost increases, labour shortages, bad weather, design changes

---

## Part 7: Key Case Law Quick Reference

| Case | Jurisdiction | Key Principle |
|------|-------------|---------------|
| *Henry Boot v Malmaison* [1999] | UK | Concurrent delay — contractor gets EOT even if own delay is concurrent |
| *Walter Lilly v Mackay* [2012] | UK | Disruption: 4 elements + notice; global basis possible |
| *North Midland v Cyden Homes* [2018] EWCA Civ 1744 | UK | Parties can contract out of Malmaison — concurrent delay risk allocation is enforceable |
| *City Inn v Shepherd* [2010] CSIH 68 | Scotland | Apportionment approach — tribunal can split EOT between causes |
| *Costain v Charles Haswell* [2009] EWHC B25 (TCC) | UK | Disruption causation — must link specific events to specific productivity losses |
| *Cleveland Bridge* [2012] | UK | Reasoned assessment on balance of probabilities |
| *Van Oord v Allseas* [2015] | UK | Notice requirements matter |
| *Alliance Concrete v Sato Kogyo* [2014] | Singapore | Frustration — high bar for frustration |
| *Davis Contractors v Fareham* [1956] | UK | Frustration — 8-to-22-month overrun NOT frustration |
| *Evergreat v Presscrete* [2006] | Singapore | Employer must do all things necessary for completion |
| *TT International v Ho Lee* [2017] | Singapore | Employer must not prevent contractor from performing |
| *Zurich Insurance v B-Gold* [2008] | Singapore | Extrinsic evidence admissible for contract interpretation |
| *Lim Chin San v LW Infrastructure* [2011] | Singapore | Proper assessment by SO required; failure opens right to damages |
| *John Doyle v Laing* [2004] | UK | Global claims — permissible if impracticable to separate |
| *Wong Lai Ying v Chinachem* [1979] | Hong Kong | Unforeseeable landslip = frustration |

---

## Part 8: Key Definitions

| Term | Definition |
|------|-----------|
| **EOT** | Extension of Time — additional time to complete without LD |
| **LD** | Liquidated Damages — pre-agreed daily rate for late completion |
| **Critical Path** | Longest chain of dependent activities determining completion date |
| **Positive Float** | Time an activity can be delayed without affecting the critical path |
| **Zero Float** | Activity is on the critical path — any delay directly delays completion |
| **Negative Float** | Projected completion already exceeds contract completion date. Does NOT bar EOT claims. |
| **Terminal Float** | Buffer between contractor's planned completion and contract completion date |
| **Pacing Delay** | Deliberate slowing of non-critical work to match employer-caused critical path delay. Not contractor culpable delay. |
| **Excusable Delay** | A delay that entitles the contractor to EOT. May or may not be compensable. |
| **Compensable Delay** | A delay that entitles the contractor to both EOT and money. |
| **Inexcusable Delay** | A contractor risk delay — no EOT, no compensation. |
| **Logic Links** | Programme dependencies: FS (Finish-to-Start), SS (Start-to-Start), FF (Finish-to-Finish), SF (Start-to-Finish, rare). |
| **Approved Programme** | Programme formally accepted by the Employer/Engineer. Reference point for delay analysis. |
| **Working Programme** | Contractor's internal updated programme reflecting current progress and forecasts. |
| **Baseline Programme** | Original approved programme — reference point for delay analysis |
| **As-Built Programme** | Record of what actually happened |
| **Time-Bar** | Contractual deadline — miss it and you lose the claim |
| **Prolongation** | Extended site presence due to delay |
| **Disruption** | Reduced productivity (more resources per unit of output) |
| **Acceleration** | Measures to recover delay (additional resources, overtime, resequencing) |
| **Concurrent Delay** | Two or more delay events occurring simultaneously, at least one employer risk and one contractor risk |
| **Compensation Event** | NEC term for an event entitling contractor to time and/or money |
| **Measured Mile** | Comparing productivity in disrupted vs undisrupted periods |

---

*This document is based on publicly available sources including the SCL Delay and Disruption Protocol (2nd Ed, Feb 2017 + Rider 1, Feb 2022), AACEi RP 29R-03, and published case law. It is a study and reference aid only. It does not constitute legal advice. Users should verify all information against their specific contract terms and seek qualified legal counsel where required.*
