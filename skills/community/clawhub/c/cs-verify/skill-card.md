## Description: <br>
Verify factual claims against live data sources. Returns structured verdicts with confidence scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check factual claims against live data sources and receive structured verdicts with confidence, freshness, and source-count signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claims submitted for verification are sent to a third-party service. <br>
Mitigation: Submit only claims suitable for third-party processing; do not include secrets, private business facts, personal data, health/legal/financial-account details, or regulated information without separate review. <br>
Risk: The optional MCP package and paid x402/USDC use introduce separate installation and payment trust decisions. <br>
Mitigation: Review the MCP package and payment flow independently before installing packages or authorizing paid usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CutTheMustard/cs-verify) <br>
- [Service homepage](https://636865636b73756d.com) <br>
- [Agent card](https://636865636b73756d.com/.well-known/agent.json) <br>
- [Service metadata](https://636865636b73756d.com/.well-known/agent-service.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes API responses with verdict, confidence, current truth, freshness, source count, cache status, request ID, service URL, and referral ID fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
