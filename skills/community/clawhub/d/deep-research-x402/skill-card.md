## Description:

26-tool autonomous research agent for academic papers, arXiv, PubMed, PubChem, Census, web search, and related sources through x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to run cost-aware research workflows across web, academic, biomedical, chemistry, demographics, and government-data sources, then synthesize cited findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make paid external requests through x402 endpoints.

Mitigation: Require explicit approval before paid calls and avoid redundant endpoint calls.

Risk: Research topics, URLs, and the API key may be sent to an external or custom gateway.

Mitigation: Use the default gateway only when acceptable for the data being researched, and keep RESEARCH_GATEWAY_URL unset unless the custom gateway is fully trusted.

## Reference(s):

- [Deep Research Skill Page](https://clawhub.ai/plagtech/skills/deep-research-x402)
- [Research Gateway](https://gateway.spraay.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with citations and optional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve paid external API calls through an x402 research gateway.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
