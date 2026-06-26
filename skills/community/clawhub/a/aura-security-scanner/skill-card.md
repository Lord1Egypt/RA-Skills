## Description: <br>
Scan AI agent skills for malware, credential theft, prompt injection, and dangerous permissions before installing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aurasecurity-creator](https://clawhub.ai/user/aurasecurity-creator) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to submit an AI agent skill URL to AURA Security and receive a safety verdict before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the submitted skill URL to AURA or the configured AURA_API_URL endpoint. <br>
Mitigation: Avoid submitting private repositories, presigned links, token-bearing URLs, or internal service URLs unless the configured endpoint is trusted. <br>
Risk: A scanner verdict may not be final proof that a skill is safe. <br>
Mitigation: Use the returned verdict alongside human review and other security checks before installing or deploying the scanned skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aurasecurity-creator/aura-security-scanner) <br>
- [AURA Security website](https://aurasecurity.io) <br>
- [AURA Security GitHub repository](https://github.com/aurasecurityio/aura-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns verdicts, risk scores, findings, recommendations, and badge status from the configured AURA Security API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
