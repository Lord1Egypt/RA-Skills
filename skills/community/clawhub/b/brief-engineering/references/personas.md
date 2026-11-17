# Persona presentation policy

Same evidence, different framing. Persona changes ranking weight and presentation,
never permissions or scope.

## Engineer / on-call

Leads with things that page you or will page you.

Rank order: production incident, failed or stuck prod deploy, SLO burn rate, latency
regression against a 7/28/90-day baseline, error-rate spike, DLQ age and backlog
growth, overdue critical workflow, red CI on the release branch, migration deadline
affecting a confirmed dependency.

Always include the evidence link, the exact metric or query, and the runbook when
`get_suggested_resources_by_key` returns one.

Exclude roadmap discussion, adoption metrics, and anything without an operational
consequence today.

## Engineering manager

Leads with patterns, not events.

Rank order: recurring failures across the team's services, ownership gaps such as a
service with no Compass owner or no linked on-call schedule, cross-team blockers,
delivery risk, customer-impact themes, 30 and 90-day reliability trend.

Aggregate only. No private messages. No individual activity scoring. No per-person
attribution of failures. If a signal cannot be expressed without naming one person's
work pattern, drop it.

## PM

Leads with customer and commitment consequences.

Rank order: customer escalations backed by an explicit support artifact, adoption or
consumption change, roadmap risk, deadline slippage, migration commitments, unresolved
cross-team dependencies.

Include technical health only where it changes a customer or delivery outcome. A
latency regression is a PM item when it breaches a customer commitment, not because it
is technically interesting.
