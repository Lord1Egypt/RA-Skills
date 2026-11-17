## Description:

Analyzes web trend signals for keywords and classifies each as Rising, Peaking, Declining, or Insufficient_Data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinu4you](https://clawhub.ai/user/jinu4you)

### License/Terms of Use:

ISC

## Use Case:

Developers and analysts use this agent to search recent web results for up to five keywords, classify trend lifecycle signals, and receive a short brief with evidence URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword queries and retrieved article snippets are sent to Tavily and the configured LLM provider.

Mitigation: Disclose provider data transfer, configure API keys only in trusted environments, and avoid sensitive keywords or source content.

Risk: Untrusted web content can influence trend classifications and generated briefs.

Mitigation: Treat results as advisory, review evidence URLs, and add input size limits plus strict schema validation before production use.

Risk: Outdated dependencies or provider API changes can affect reliability.

Mitigation: Keep dependencies current and test configured Tavily and LLM provider integrations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinu4you/skills/agent-trend-radar)

## Skill Output:

**Output Type(s):** [json, text, markdown]

**Output Format:** [JSON result object with trend classifications, scores, evidence URLs, and a concise markdown-style Korean brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are sorted by score and include the requested timeframe and region.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
