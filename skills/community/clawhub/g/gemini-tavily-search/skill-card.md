## Description:

Use this skill when the user asks about current events, real-time information, recent news, live scores, financial data, price updates, recent changes, or any question that may require up-to-date web information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josearroyave](https://clawhub.ai/user/josearroyave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer time-sensitive questions by routing web lookup requests through Gemini with Google Search grounding and falling back to Tavily when Gemini cannot provide a usable response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries may be sent to Gemini, Google Search grounding, and Tavily, including automatic fallback cases.

Mitigation: Do not send secrets, personal data, internal project names, or regulated information unless sharing it with those providers is acceptable.

Risk: Installation from a mutable source can differ from the reviewed release.

Mitigation: Install only from a pinned, reviewed version or commit, preferably as an unprivileged user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josearroyave/skills/gemini-tavily-search)
- [Tavily skills repository](https://github.com/tavily-ai/skills)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON with provider, answer, source results, fallback status, and searched-with attribution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns normalized provider output and marks web snippets as untrusted when web search is used.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
