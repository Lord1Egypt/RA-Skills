## Description:

AI Trend Hunter Pro helps creators turn global trend and technology news into social media drafts for X, Xiaohongshu, and LinkedIn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[traprapitalianazional-dev](https://clawhub.ai/user/traprapitalianazional-dev)

### License/Terms of Use:

Standard Commercial License

## Use Case:

External creators, agencies, and digital entrepreneurs use this skill to monitor public trend sources, generate persona-driven social media drafts, review them, and optionally stage approved X drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Under-scoped URL scraping may send scraped page text to DeepSeek, save it locally, and use it in X draft automation.

Mitigation: Run the skill only against intended public news URLs, keep the human approval step enabled, and inspect both source content and final drafts before browser automation.

## Reference(s):

- [AI Trend Hunter Pro on ClawHub](https://clawhub.ai/traprapitalianazional-dev/skills/ai-hunter-pro)
- [Publisher profile](https://clawhub.ai/user/traprapitalianazional-dev)
- [DeepSeek chat completions endpoint](https://api.deepseek.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown drafts with intermediate JSON title records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human review is expected before approved drafts are staged through browser automation.]

## Skill Version(s):

1.0.0 (source: manifest.json, workflow.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
