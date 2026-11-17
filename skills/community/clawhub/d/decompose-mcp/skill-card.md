## Description:

Decompose any text into classified semantic units -- authority, risk, attention, entities. No LLM. Deterministic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echology-io](https://clawhub.ai/user/echology-io)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to classify text or fetched URL content into structured semantic units for obligation, risk, attention, entity, date, and financial analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs an unpinned external Python package.

Mitigation: Pin decompose-mcp to a reviewed version before installation.

Risk: URL decomposition can make outbound requests to user-specified URLs.

Mitigation: Run the MCP server with only required network access and use decompose_text when local-only processing is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/echology-io/skills/decompose-mcp)
- [Documentation](https://echology.io/decompose)
- [PyPI Package](https://pypi.org/project/decompose-mcp/)
- [When Regex Beats an LLM](https://echology.io/blog/regex-beats-llm)
- [Why Your Agent Needs a Cognitive Primitive](https://echology.io/blog/cognitive-primitive)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON semantic-unit analysis, with optional agent-facing summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The text path is local-only; URL decomposition performs outbound requests to user-specified URLs when enabled.]

## Skill Version(s):

0.1.2 (source: server release and artifact claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
