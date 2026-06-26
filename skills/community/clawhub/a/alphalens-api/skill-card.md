## Description: <br>
AlphaLens API turns the AlphaLens API into agent workflows for company discovery, product research, competitive landscape maps, investor networks, peer benchmarks, white space analysis, and pipeline enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walidmustapha](https://clawhub.ai/user/walidmustapha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business development, investment, and market research users use this skill through an agent to query AlphaLens, find and compare companies or products, map competitive landscapes, analyze investor networks, benchmark peers, identify white space, and enrich AlphaLens pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive company names, domains, product descriptions, organization IDs, and submitted pipeline documents may be sent to AlphaLens. <br>
Mitigation: Use the skill only with an approved AlphaLens account and avoid confidential deal materials unless internal policy allows that use. <br>
Risk: Public company domains may be sent to Google's favicon service when workflows fetch logos. <br>
Mitigation: Use only public domains returned by AlphaLens and avoid internal or confidential hostnames. <br>
Risk: The skill requires a sensitive AlphaLens API key. <br>
Mitigation: Store ALPHALENS_API_KEY as a secret, alias it to KEY before API calls, and never paste literal credentials into generated commands or documents. <br>
Risk: Pipeline enrichment can mutate AlphaLens pipeline state and credit-gated workflows may consume account credits. <br>
Mitigation: Inspect existing pipeline items first and confirm budget or user approval before large enrichment runs or bottom-up suite workflows. <br>


## Reference(s): <br>
- [AlphaLens](https://alphalens.ai) <br>
- [AlphaLens API Reference](references/REFERENCE.md) <br>
- [AlphaLens API Examples](references/EXAMPLES.md) <br>
- [AlphaLens ClawHub Listing](https://clawhub.ai/walidmustapha/alphalens-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash curl commands and generated self-contained HTML report code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALPHALENS_API_KEY and an active AlphaLens subscription with API access.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
