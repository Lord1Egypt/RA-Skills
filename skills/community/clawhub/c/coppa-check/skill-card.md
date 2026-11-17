## Description:

COPPA Check helps agents run a COPPA compliance questionnaire covering 12 core items and generate text, JSON, or HTML reports with scoring from the CQDev cloud compliance engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and compliance reviewers use this skill to preview COPPA checks and generate a compliance report for products or services that may collect information from children under 13.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored checks send questionnaire answers, an API key or anonymous trial ID, and normal network metadata to compliancehub.cn.

Mitigation: Use the skill only when that data transfer is acceptable, confirm the destination before scoring, and avoid providing sensitive details that are not needed for the questionnaire.

Risk: The security review says the advertised offline preview still contacts the cloud.

Mitigation: Review before installing if a truly offline preview is required, and run in a network-controlled environment when offline behavior must be enforced.

Risk: HTML reports may trust cloud-provided text before output escaping is fixed.

Mitigation: Prefer text or JSON reports for untrusted responses, or sanitize and review generated HTML before opening or sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/coppa-check)
- [ComplianceHub cloud endpoint](https://compliancehub.cn)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, shell commands, configuration, guidance]

**Output Format:** [Text, JSON, or HTML reports, with Markdown usage guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include cloud-scored results, local fallback scores, quota status, and registration guidance.]

## Skill Version(s):

1.1.2 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
