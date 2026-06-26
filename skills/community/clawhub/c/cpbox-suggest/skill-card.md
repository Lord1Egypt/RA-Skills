## Description: <br>
Provides query autocomplete suggestions, including optional rich entity details, through the cpbox Suggest API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add search-as-you-type suggestions, query refinement for retrieval workflows, entity preview detection, and typo-tolerant query completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic x402 pay-per-use calls can spend funds without clear cost or approval limits. <br>
Mitigation: Review the payment helper, configure spending or approval controls, and enable automatic paid calls only for expected autocomplete traffic. <br>
Risk: Autocomplete queries may contain sensitive or confidential text. <br>
Mitigation: Use the skill only for explicit search-query suggestion workflows and avoid sending private, regulated, or confidential queries. <br>
Risk: The skill depends on external cpbox, cppay, and x402-payment services. <br>
Mitigation: Verify the API provider, facilitator, and payment helper before use and monitor responses before relying on them in production. <br>


## Reference(s): <br>
- [cpbox API provider](https://www.cpbox.io) <br>
- [cpbox Suggest endpoint](https://www.cpbox.io/api/x402/suggest) <br>
- [cppay facilitator](https://www.cppay.finance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents a JSON API response containing query suggestions and optional rich entity fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
