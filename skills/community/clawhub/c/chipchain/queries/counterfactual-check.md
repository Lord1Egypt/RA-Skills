# Counterfactual Consistency Check
> When to Trigger | The Check (3 questions + falsifier construction) | Circular Sourcing Trap | Output Format

Run this on any claim graded STRONG INFERENCE or higher. The goal: catch
cases where evidence looks like it confirms a claim but has a plausible
alternative explanation.

Inspired by Wang et al., "Fact-Checking with Large Language Models via
Probabilistic Certainty and Consistency" (arXiv:2601.02574).

## When to Trigger

- **Always** before upgrading a triangulated claim to STRONG INFERENCE
- **Always** when two sources give conflicting numbers or relationships
- **Recommended** for any CONFIRMED claim that rests on a single source

## The Check

### 1. "If this were FALSE, how would I explain my evidence?"

For each piece of evidence supporting the claim, construct a plausible
alternative explanation that doesn't require the claim to be true.

Evidence that looks like proof of a relationship (award, patent, co-authorship,
trade flow, revenue geography) almost always has a mundane alternative: the
award is old, the patent is research not commercial, the co-authorship is
academic, the trade flow covers non-target uses, the revenue geography doesn't
name the specific customer. Walk through each piece and ask: "Does this
evidence REQUIRE my claim to be true, or is it merely consistent with it?"

If the alternative explanations are equally plausible, downgrade from
STRONG INFERENCE to MODERATE INFERENCE.

**Causal check:** Evidence that entity A makes product X and entity B buys
product X does not prove A supplies B. Making and supplying require different
evidence. A product catalog proves manufacturing. A regulatory filing naming
a specific trading partner proves a commercial relationship. These are
different grades of evidence. Don't collapse them.

### 2. "What would I search to disprove this?"

Every falsifier must be **executable**. If you can't turn it into a search
query you could run right now, you haven't thought hard enough.

**Format:**
```
CHECK: [exactly what to search or look up]
CHANGES MIND IF: [what result would weaken or kill the claim]
```

A vague falsifier ("find contradicting evidence") is worthless. A good
falsifier names a specific source, a specific data point, and a threshold
that would change your conclusion.

**Self-test:** If the CHECK could return any result and you'd still believe
the claim, you don't have a falsifier. You have a confirmation search.

#### Four angles to attack a claim

Most falsifiers only attack the obvious angle (is the entity really that
big/important?). A complete check considers multiple angles. Not all four
apply to every claim. Pick the 1-2 most relevant.

**A. Numerator — "Is the entity's position different than claimed?"**

Attacks: spotlight effect. You're researching entity X, so you overestimate
its importance because it's the focus of your attention.

Check the entity's actual revenue or volume in the *specific segment* (not
total revenue, not an adjacent segment). Compare against the claim. A large
conglomerate can be a small player in the niche you care about. Also check
whether competitors have data that changes the picture.

**B. Denominator and scope — "Is the market defined the way I think it is?"**

Attacks: denominator neglect and category reification. Share = numerator /
denominator, but people challenge the numerator while accepting whatever
denominator they found first. And market categories are analytical constructs,
not natural kinds. Different analysts draw boundaries differently.

Find a second independent estimate of the total market. If two estimates
diverge by >30%, the share figure is unreliable regardless of the numerator.
Check what the market definition includes and excludes. If moving the boundary
(including/excluding a sub-segment, a technology generation, an adjacent
product) changes the entity's share by >10 points, the scope is load-bearing
and must be stated explicitly.

**C. Visibility — "Are there players or capacity my data can't see?"**

Attacks: survivorship bias in data sources. You can only see what gets
reported. Systematically invisible: private companies, captive/internal
production, state-owned enterprises, vertically integrated suppliers,
intermediaries (trading companies, distributors), and producers publishing
in languages or databases you didn't search.

For any concentration claim, ask: "Who in this supply chain would NOT appear
in my data source?" Then construct a search that targets the gap. If a
customer produces or recycles part of a material internally, the merchant
market is smaller than reported and the leading supplier's real share of
total consumption is lower than it appears.

Language and geography are the most common blind spots. A producer that
publishes only in one language won't appear in market reports written in
another. New entrants in geographies you didn't search won't appear at all.
Market reports have a 1-2 year lag. For any "top N hold >X%" claim, search
for recent entrants (IPOs, new listings, new capacity announcements) in the
product category.

**D. Temporal — "When was this measured, and what has changed since?"**

Attacks: stale data treated as current fact. A market position from 2022 can
be meaningless in segments with rapid capacity additions, trade restrictions,
or localization drives.

Check the date of the underlying data (not the publication date, the
measurement date, which is often 1-2 years earlier). Name at least one event
since the measurement date that could have changed the picture: new entrant,
capacity expansion, export control, trade dispute, demand shift. If such an
event exists, the claim needs fresh verification even if the original source
was authoritative.

#### Good falsifier vs bad falsifier

| Property | Good | Bad |
|---|---|---|
| Specificity | Names a source and a data point | "Find contradicting evidence" |
| Threshold | States a number: "if X exceeds Y" | "If it turns out differently" |
| Angle | Attacks denominator, visibility, or time (non-obvious) | Only attacks the numerator (obvious) |
| Executability | Can be turned into a search right now | Requires access you don't have |
| Independence | Checks a source your evidence didn't use | Re-checks the same source |

At least one falsifier must appear in the report's "Recommended Next Steps"
as an executable action, not just a thought exercise.

### 3. "Do my sources actually agree?"

Check for contradictions you might be glossing over:

- Source A says [claim/number]. Source B says [claim/number].
- Do they agree? If not: which is more authoritative for this specific
  question, and why?
- **Are they measuring the same thing?** Different scope definitions produce
  different numbers that aren't actually contradictory, just incomparable.
- **Are they from the same time period?** A 2022 figure and a 2025 figure
  may both be correct for their respective dates.

Surface contradictions as findings, not problems to hide. A well-documented
disagreement is more valuable than a false consensus. Don't average divergent
numbers. State both and explain what would resolve the gap.

## Circular Sourcing Trap

Multiple sources citing the same original estimate create the illusion of
independent confirmation. This is invisible and common.

Pattern: an analyst report says "Company X has ~70% share." A journalist
cites the report. A broker report cites the journalist. A forum post cites
the broker. You now have "four sources" that are one source with three echoes.

**How to catch it:**
- Check whether sources cite each other or share a common ancestor
- Look at dates: if all sources cluster within 6 months, they're probably
  echoing one original estimate
- Suspiciously round numbers (~70%, ~50%, ~90%) are estimates. Real
  measurements produce numbers like 64.3%. Round numbers get copied
- If every source gives the exact same number, that's suspicious. Independent
  measurements should scatter around the true value

When you suspect circular sourcing, say so explicitly in the report.

## Output: Append to Report

```markdown
## Counterfactual Check

### [Claim tested]
- **Original grade:** [grade]
- **Alternative explanation:** [what would explain the evidence if the claim is false]
- **Plausibility:** [LOW / MEDIUM / HIGH]
- **Revised grade:** [unchanged / downgraded]
- **Falsifier:**
  CHECK: [what to search]
  CHANGES MIND IF: [what result would weaken the claim]
- **Circular sourcing:** [do sources trace to a common ancestor? same round number?]
- **Contradictions:** [any source disagreements, with explanation of likely cause]
```
