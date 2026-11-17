## Description:

CCPA/CPRA Compliance Check for businesses subject to California privacy law, covering 12 core compliance checks with optional CQDev cloud scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to preview CCPA/CPRA check items and run a yes/no self-assessment for California consumer privacy compliance. Scored runs send the answers to the CQDev cloud service and return a local compliance report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored runs send CCPA/CPRA assessment answers, quota metadata, and either an anonymous trial ID or API key to compliancehub.cn.

Mitigation: Use the offline preview before any scored run, confirm the destination service is acceptable, and avoid submitting sensitive compliance details unless cloud processing is approved.

Risk: The server security summary reports a verified HTML-report injection risk from cloud-returned content.

Mitigation: Avoid opening HTML reports from untrusted or unexpected cloud results until report fields are escaped or equivalent CSP protections are added; prefer text or JSON output when reviewing uncertain results.

## Reference(s):

- [API Key Setup](references/api_key.md)
- [CCPA Check Skill Page](https://clawhub.ai/wwumit/skills/ccpa-check)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON preview or report, HTML report file, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored assessments use a cloud API; offline preview mode lists bundled check items without network access.]

## Skill Version(s):

2.2.4 (source: evidence.json release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
