## Description: <br>
Queries Google Trends keyword interest through the Clawec API, with support for multi-keyword comparison and country or region filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, market researchers, and agents use this skill to compare keyword search interest by region and turn Google Trends responses into concise trend summaries, related-query findings, and product-research observations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trend research keywords, region codes, and the Clawec API token are sent to Clawec as part of the lookup. <br>
Mitigation: Avoid highly confidential query terms, keep CLAWEC_API_KEY out of logs and shared terminals, and use a revocable or scoped API key when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-google-trend) <br>
- [Response schema](references/response-schema.md) <br>
- [Clawec API base URL](https://www.clawec.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and parsed JSON response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is Chinese and should note that trend interest is not sales volume.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
