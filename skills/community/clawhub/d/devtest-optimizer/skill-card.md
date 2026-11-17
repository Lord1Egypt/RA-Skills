## Description:

Optimize Azure dev/test environment costs with auto-shutdown schedules and Dev/Test pricing enrollment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud engineers, and FinOps teams use this skill to review Azure dev/test VM and cost exports, identify non-production resources that appear to run outside business hours, estimate savings, and draft shutdown automation or tagging policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Azure inventory, cost, and subscription exports can contain sensitive operational details.

Mitigation: Share only the minimum required exports, remove credentials or secret values before analysis, and prefer read-only Azure data sources.

Risk: Generated runbooks or Azure Policy templates could affect availability or cost if applied without review.

Mitigation: Review all generated automation and policy changes, test them in a non-production subscription, and apply them through normal Azure change controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recommendations and templates from user-provided Azure exports; it does not directly access Azure or apply cloud changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
