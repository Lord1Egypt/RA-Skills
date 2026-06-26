## Description: <br>
26-tool autonomous research agent - academic papers, arXiv, PubMed, PubChem, Census, web search, and more via x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plagtech](https://clawhub.ai/user/plagtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-focused agents use this skill to gather, cross-reference, and synthesize sourced information from web, academic, biomedical, chemistry, demographics, and government data endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends research queries, URLs, and extracted page content to an external paid gateway and upstream providers. <br>
Mitigation: Avoid submitting secrets, private business material, regulated personal data, or sensitive medical, legal, or financial details unless provider handling and cost controls have been reviewed. <br>
Risk: Endpoint calls can incur real x402 micropayment costs. <br>
Mitigation: Use the documented quick, deep, fact-check, and compare modes to limit redundant calls and confirm the configured gateway and API key before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/plagtech/deep-research-x402) <br>
- [Default research gateway](https://gateway.spraay.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown research answers with citations and inline shell command examples; gateway responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESEARCH_API_KEY for authenticated gateway access; uses curl and python3; endpoint calls may incur x402 micropayments.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
