## Description:

专业级合同风险审查工具，自动识别 20+ 类常见风险条款，给出修改建议和法律依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[amaxclaw](https://clawhub.ai/user/amaxclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as founders, legal staff, and freelancers use this skill to review Chinese-language contract text for common clause risks, prioritized findings, revision suggestions, and cited legal-reference text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contract text can contain confidential business or personal information.

Mitigation: Redact unnecessary sensitive details before use and avoid submitting information that is not needed for the review.

Risk: The review output may be incomplete or unsuitable as formal legal advice.

Mitigation: Use the output as risk-reference guidance only and consult a qualified lawyer for major contracts or binding decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amaxclaw/skills/contract-risk-reviewer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured report with a risk score, prioritized risk list, revision suggestions, legal-reference text, and revised clause examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes contract text with optional contract type, party role, and review depth; includes a disclaimer that the output is not formal legal advice.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
