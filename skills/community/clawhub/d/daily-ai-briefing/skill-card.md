## Description:

Defines a Chinese-language workflow for producing a daily AI briefing with source checks, freshness limits, filtering rules, self-review, and a Markdown output template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tino-chen](https://clawhub.ai/user/tino-chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI analysts use this skill to collect recent AI research, product, industry, and open-source updates, remove weak or stale items, and produce a concise Chinese Markdown briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches public web sources, so briefings may include incorrect or stale information if source pages are unavailable or ambiguous.

Mitigation: Require specific source links, date checks, and final self-review before including each item.

Risk: The skill stores briefing history in ~/Desktop/daily_ai_briefing, which may retain notes the user considers sensitive.

Mitigation: Review or change the storage folder, or instruct the agent not to save files when local retention is not desired.

Risk: The workflow is written for Chinese-language output and may not fit users expecting an English briefing.

Mitigation: Confirm the desired output language before execution and adapt the final template when needed.

## Reference(s):

- [重点关注信息源](references/sources.md)
- [Daily AI Briefing guide](https://tino-chen.github.io/notes/workflows/daily-ai-briefing.html)
- [ClawHub skill page](https://clawhub.ai/tino-chen/skills/daily-ai-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown briefing saved as a local .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current web retrieval for public AI sources and keeps recent briefing history for deduplication.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
