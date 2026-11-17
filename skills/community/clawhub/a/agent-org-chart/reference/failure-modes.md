# Failure modes

Diagnose a misbehaving multi-agent team by symptom. Most of these are structural, not prompting problems, which is why adding more instructions to the prompt tends not to fix them.

## Work loops between two agents

**Looks like:** A hands to B, B hands back to A, repeat. Token spend climbs with no progress.

**Cause:** Either a cycle in the chart, or two roles with overlapping ownership and no refusal to break the tie.

**Fix:** Enforce the tree invariant, rejecting any edge that would make an agent its own ancestor. Then check whether the two roles are actually one role. If both can legitimately do the work, neither will reliably keep it.

## One agent does everything

**Looks like:** The manager implements, reviews, and reports. Reports sit idle.

**Cause:** The manager has no hard refusal, so delegating is always the slower-looking option in the moment.

**Fix:** Write the refusal as a hard rule. "You do not write code" rather than "prefer to delegate." Verify by giving it a task it could plausibly do alone and checking that it still hands off.

## Reports stall waiting on each other

**Looks like:** Two agents both report "waiting" and nothing moves.

**Cause:** Sideways reachability, meaning agents talking across the chart rather than through their manager, or a shared mutable resource with no serialization.

**Fix:** Restrict reachability to direct reports plus own manager. Serialize any writer on shared state, so the manager runs one report at a time against a shared checkout.

## Output is confidently wrong

**Looks like:** Work arrives looking complete, and is not. Nobody caught it.

**Cause:** No verifier in the chart, or a verifier that is allowed to edit and so quietly rewrites instead of reporting.

**Fix:** Add a reviewer whose refusal is editing. Its output is findings, not a diff. A reviewer that can edit will fix the easy things and stop reporting the hard ones.

## A small request costs a lot

**Looks like:** A one-line ask produces dozens of agent runs.

**Cause:** No fan-out cap, no depth cap, or a vague request that the top of the chart split speculatively.

**Fix:** Cap fan-out per turn (3 is a sane default) and chain depth (10). Then require the top of the chart to clarify ambiguous requests before dispatching, rather than covering every interpretation in parallel.

## A role is missing at runtime

**Looks like:** A manager stalls, or invents a teammate that was never hired.

**Cause:** The manager assumes a full roster.

**Fix:** Make managers degrade gracefully. If the missing work is reasonable to do directly, do it. Otherwise report the gap upward. Never block on a teammate that does not exist, and never hallucinate one.

## Hand-offs lose context

**Looks like:** A report asks for information the manager already had, or produces work against the wrong assumption.

**Cause:** The hand-off carried the request but not the acceptance criteria or the context the report cannot look up.

**Fix:** Fix the hand-off payload, not the prompt. Request, acceptance criteria, and non-lookupable context, every time.

## The human is a bottleneck

**Looks like:** Everything waits on approvals. The team is slower than doing it manually.

**Cause:** Approval policy assigned per agent rather than per tool, so a single risky tool drags an entire agent into ask-mode.

**Fix:** Classify per tool by blast radius. Reads and tests run on allow. Only genuinely irreversible or costly actions ask. If more than about a fifth of actions are stopping for approval, the classification is too conservative.

## Results are unauditable

**Looks like:** Something went wrong and reconstructing why means reading raw logs.

**Cause:** Routing lives in prompts rather than in the chart, so there is no record of which path work took.

**Fix:** Make the chart the routing table, so the path is a property of the structure. Requiring a status line on every reply, separate from the detail, is what makes the trail skimmable afterwards.
