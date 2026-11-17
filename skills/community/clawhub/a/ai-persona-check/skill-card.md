## Description:

AI Persona Check helps agents evaluate AI persona-based interactive services against 10 compliance items from China's Interim Measures and produce local reports with optional cloud scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill when they explicitly request an AI persona-based interactive service compliance check. It previews or scores self-reported answers, then returns compliance guidance and a report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored checks send self-reported compliance answers and an API key or anonymous trial ID to compliancehub.cn.

Mitigation: Use --non-interactive for offline preview, and run scored mode only after reviewing the data sharing behavior and key handling.

Risk: Generated HTML reports may render cloud-supplied text without escaping.

Mitigation: Prefer text or JSON output, or treat generated HTML as untrusted until dynamic report fields are escaped.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wwumit/skills/ai-persona-check)
- [complianceHub Account and API Key Page](https://compliancehub.cn/account.html?skill=ai-persona-check)
- [complianceHub Service](https://compliancehub.cn)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text, JSON, or HTML reports with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored mode sends answers and an API key or anonymous trial ID to compliancehub.cn; non-interactive preview stays offline.]

## Skill Version(s):

1.0.0 (source: package.json, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
