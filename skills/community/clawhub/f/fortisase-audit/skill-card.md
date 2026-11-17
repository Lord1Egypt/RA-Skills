## Description:

Fortinet FortiSASE audit for Secure Web Gateway policy review, ZTNA application gateway assessment, thin edge FortiGate integration validation, SD-WAN security overlay analysis, FortiClient endpoint compliance verification, and cloud security posture evaluation across FortiSASE tenants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Security operators and network engineers use this skill to audit Fortinet FortiSASE tenant posture across SWG, ZTNA, thin edge integration, endpoint compliance, FortiGuard services, and logging controls. It helps structure read-only reviews, evidence collection, and findings for enterprise SASE environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable FortiCloud or FortiGate administrator credentials can be exposed through prompts, logs, command history, or reports.

Mitigation: Use dedicated read-only service accounts or scoped API tokens, keep secrets out of prompts and generated reports, and avoid direct administrator authentication unless it is strictly necessary.

Risk: The security evidence requires review because credential-handling safeguards are not adequate for normal installation without operator controls.

Mitigation: Review the skill before deployment and enforce least-privilege access, token scoping, and trusted-host controls in operating procedures.

## Reference(s):

- [FortiSASE REST API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/skills/fortisase-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline API request examples and audit findings guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only FortiSASE audit guidance requiring a scoped FortiSASE API token.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
