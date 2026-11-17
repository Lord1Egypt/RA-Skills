## Description:

Defines an advertising planning optimization pipeline that turns improvement goals into optimization strategies for existing delivery objects, draft plans, strategy variables, or goal-only requests, with diagnosis used only as optional supporting evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizejia668-code](https://clawhub.ai/user/lizejia668-code)

### License/Terms of Use:

MIT-0

## Use Case:

Advertising operations agents use this skill to structure optimization conversations, collect appropriate planning evidence, decide when diagnosis is useful, and produce concise optimization plans. It is intended for improving delivery strategy, budget, bids, audience, geography, cadence, and creative direction without directly executing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimization recommendations may rely on advertiser performance, audience, and creative evidence, so stale or incomplete evidence could lead to poor budget, bid, targeting, or creative decisions.

Mitigation: Use current evidence summaries when available, surface data gaps as warnings, and require review before acting on optimization recommendations.

Risk: The skill may propose budget, bid, targeting, draft-plan, or campaign-adjacent actions that could affect advertising delivery if executed without oversight.

Mitigation: Keep the skill limited to recommendations and route any execution action through a separate confirmation flow before changing campaigns, budgets, bids, or targeting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizejia668-code/skills/ads-brain-planning-optimize-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or structured JSON guidance for advertising optimization plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optimization actions, tradeoffs, expected impact, risk notes, warnings, draft patches, and next-action guidance; does not directly execute campaign changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
