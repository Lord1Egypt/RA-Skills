## Description: <br>
Runs an adversarial second-model review of draft agent responses before delivery, noting that draft text may be sent to the configured model API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keaneyan](https://clawhub.ai/user/keaneyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to add a mandatory quality gate that critiques draft responses for factual, logical, tone, and completeness issues before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft responses may be sent to an additional model provider API, which can expose confidential, regulated, credential-containing, or proprietary content. <br>
Mitigation: Configure a local reviewer model for sensitive work, or skip or uninstall the skill when draft text should not be shared with another provider. <br>
Risk: The reviewer can add cost and latency to normal responses. <br>
Mitigation: Use a lower-cost reviewer model when cloud review is acceptable, and account for the extra review step in latency-sensitive workflows. <br>
Risk: Adversarial critique may be wrong or overly cautious. <br>
Mitigation: Apply reviewer feedback only when it is valid, and keep final judgment with the primary agent or human operator. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keaneyan/adversary-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text critique with a PASS result or a concise issue list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adds latency and token usage because each reviewed draft may be sent to a second model.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
