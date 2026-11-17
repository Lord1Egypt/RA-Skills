## Description:

Content QA Guard audits publication text with sensitive-word, semantic, platform-rule, and pipeline compliance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to review platform content before publication, detect compliance risks, and return pass, warning, or blocked decisions with suggested remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed content may be sent to configured OpenClaw or MCP agents and possibly to a QA test chat.

Mitigation: Use only approved endpoints, disable or control verification messaging for sensitive content, and avoid confidential, regulated, or unpublished business text unless outbound handling is explicitly approved.

Risk: Safety claims may exceed what the implementation can reliably prove.

Mitigation: Treat the skill output as advisory and require human review before publication decisions in sensitive or regulated workflows.

Risk: Compliance checking can fall back to a reduced local pattern check when dependent detectors are unavailable.

Mitigation: Monitor downgraded results, keep the sensitive-word and risk-detector dependencies available, and avoid treating fallback results as full compliance clearance.

## Reference(s):

- [Business rules](references/business_rules.md)
- [Error codes](references/error_codes.md)
- [Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/content-qa-guard)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON results and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pass, warning, or blocked decisions with risk levels, details, and suggested changes.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
