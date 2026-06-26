# General Architecture Critic Checklist

For non-web projects, agents, scripts, data pipelines, and operational decisions.
Address each item explicitly. "N/A" is a valid answer — state it.

## Scope Violations
- Does this change touch systems or components outside the stated scope?
- Is the blast radius (number of files, services, data structures) proportional to the value delivered?
- Are there implicit dependencies that expand scope beyond what's written?
- Does this require coordination with other teams, systems, or timelines not mentioned?

## Missing Pieces
- What does the plan assume exists that may not exist?
- What setup, migration, or prerequisite work is not mentioned?
- What error states and edge cases are not handled in the plan?
- What rollback or recovery path is not described?
- What monitoring or observability is missing?

## Integration Risk
- What existing systems, APIs, or data flows does this touch?
- What breaks if this change fails mid-execution?
- Are there ordering or sequencing dependencies between steps?
- Does this change shared state that other processes read or write?

## Security Gaps
- Does this expose credentials, tokens, or sensitive data to new surfaces?
- Are inputs validated before use?
- Does this introduce new privilege escalation paths?
- Are audit/access logs preserved for sensitive operations?

## Operational Risk
- Does this require manual steps in production that could be forgotten?
- Is there a runbook or recovery plan if this goes wrong?
- Are there resource constraints (memory, disk, CPU, rate limits) that could cause failure?
- Does this create new single points of failure?

## Architecture Drift
- Does this duplicate logic or data that already exists elsewhere?
- Does this introduce a pattern inconsistent with how the rest of the system works?
- Does this create technical debt that will compound?
- Does this make the system harder to reason about for future contributors?

## Token / Cost (AI or API-heavy operations)
- Are there unnecessary repeated calls that could be batched or cached?
- Is the model or service tier appropriate for the task?
- Are there cheaper deterministic alternatives for any AI calls?
- Are rate limits and retry budgets defined?
