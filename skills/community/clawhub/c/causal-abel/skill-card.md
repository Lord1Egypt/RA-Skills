## Description:

Causal Abel helps agents use Abel causal graph probes and web grounding to analyze market, macro, asset, career, housing, lifestyle, education, and investment decisions with meaningful tradeoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[exenvitor](https://clawhub.ai/user/exenvitor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route meaningful financial, market, career, education, housing, lifestyle, and investment decisions through Abel causal graph analysis, web grounding, contradiction checks, and a concise decision report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to an Abel account and may store an Abel API key locally.

Mitigation: Review before installing, prefer session-only secrets or a real secret store, and avoid broad .env files near the skill.

Risk: Custom Abel service endpoints could receive Abel credentials.

Mitigation: Do not pass custom --base-url values with Abel credentials unless the endpoint is trusted and intended for that account.

Risk: Graph probes may inform financial and life-decision advice while reusing stored profile details such as income or risk tolerance.

Mitigation: Treat outputs as decision support, minimize stored personal profile details, and review advice before acting on meaningful money, career, housing, education, or downside-risk decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/exenvitor/skills/causal-abel)
- [Source homepage](https://github.com/Abel-ai-causality/Abel-skills)
- [Setup Guide](references/setup-guide.md)
- [Probe Usage](references/probe-usage.md)
- [Direct Graph Route](references/routes/direct-graph.md)
- [Proxy-Routed Route](references/routes/proxy-routed.md)
- [Web Grounding](references/web-grounding.md)
- [Rendering Rules](references/rendering.md)
- [Causal Abel Report Guide](assets/report-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown decision reports with optional shell command snippets, configuration guidance, and setup instructions when requested or required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is the main answer only; traces, appendices, probe transcripts, and raw graph details are omitted unless explicitly requested.]

## Skill Version(s):

1.1.6 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
