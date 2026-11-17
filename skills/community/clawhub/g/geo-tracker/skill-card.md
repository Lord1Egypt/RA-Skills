## Description:

Track and optimize brand visibility across AI search engines including ChatGPT, Perplexity, Gemini, Google AI Overview, and Claude.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and marketing teams use this skill to query AI engines for brand and competitor visibility, score mentions, and produce optimization reports for generative engine optimization work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and brand information may be sent to third-party AI providers.

Mitigation: Only audit prompts and brand data that are appropriate to share with OpenAI, Perplexity, Google, and Anthropic.

Risk: Dependency or environment drift could affect script behavior.

Mitigation: Install the skill in a virtual environment and pin dependencies where possible.

Risk: Google AI Overview and scheduling capabilities may be limited in practice.

Mitigation: Treat Google AI Overview support and scheduled monitoring as limited unless the runtime environment provides the required support.

## Reference(s):

- [GEO Optimization Guide](references/geo-optimization.md)
- [GEO Prompts Library](references/prompts.txt)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [GEO Tracker on ClawHub](https://clawhub.ai/x-rayluan/skills/geo-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Console text, optional JSON, and optional Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include per-engine mention counts, visibility scores, competitor comparisons, source prompts, and optimization recommendations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
