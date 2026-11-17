## Description:

Check real-time AI provider status, search model availability, get trending models, LLM benchmark leaderboard, and recent outage incidents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangxm233](https://clawhub.ai/user/fangxm233)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check AI provider availability, model pricing and availability, trending model usage, benchmark rankings, and recent outage incidents before making decisions about AI services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes network requests to aistatus.cc for AI status and model information.

Mitigation: Use it only when sharing provider or model names with that public service is acceptable, and review returned status data before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangxm233/skills/aistatus)
- [aistatus.cc](https://aistatus.cc)
- [All data API](https://aistatus.cc/api/all)
- [Provider status API](https://aistatus.cc/api/status)
- [Model search API](https://aistatus.cc/api/model?q={query})
- [Trending models API](https://aistatus.cc/api/trending)
- [LLM benchmark API](https://aistatus.cc/api/mmlu)
- [Recent incidents API](https://aistatus.cc/api/incidents)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text summarizing public JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider statuses, model availability and pricing, ranked model lists, benchmark scores, and incident timelines.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
