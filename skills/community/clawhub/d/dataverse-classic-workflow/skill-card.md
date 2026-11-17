## Description:

Helps agents read, analyze, compare, edit, copy, scaffold, and publish Microsoft Dataverse Classic Workflow XAML while preserving WF4 round-trip details and avoiding unsupported flow types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rwilson504](https://clawhub.ai/user/rwilson504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, modify, compare, copy, and publish Microsoft Dataverse Classic Workflows stored as WF4/XAML in solution repositories. It also guides custom workflow activity scaffolding and PAC CLI-based publishing while requiring review before environment-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow edits or publish commands can affect live Dataverse behavior, especially in production environments.

Mitigation: Review every proposed diff and PAC command, verify the auth profile and target environment, and require explicit confirmation before import, activation, or deactivation.

Risk: RunAs Owner and SYSTEM-context custom activity code can execute with broader privileges than the initiating user expects.

Mitigation: Inspect RunAs settings and generated C# service creation paths before approval, and use initiating-user context unless elevated execution is intentional.

Risk: Incorrect XAML edits can break classic designer round-tripping or activation.

Mitigation: Preserve namespaces, UserData, x:Key, and VisualBasicValue blocks, then re-read the edited file and validate workflow category before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rwilson504/skills/dataverse-classic-workflow)
- [Project homepage from metadata](https://github.com/rwilson504/agent-skills/tree/main/dataverse-classic-workflow)
- [Dataverse classic workflow processes](https://learn.microsoft.com/power-automate/workflow-processes)
- [Power Platform CLI introduction](https://learn.microsoft.com/power-platform/developer/cli/introduction)
- [Workflow extensions](https://learn.microsoft.com/power-apps/developer/data-platform/workflow/workflow-extensions)
- [Replace classic workflows with flows](https://learn.microsoft.com/power-automate/replace-workflows-with-flows)
- [XAML anatomy reference](reference/xaml-anatomy.md)
- [Activity type catalog](reference/activity-types.md)
- [Trigger type reference](reference/trigger-types.md)
- [VB expression reference](reference/vb-expressions.md)
- [Web research index](reference/web-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, command snippets, configuration notes, and proposed file edits where applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write workflow XAML and C# custom activity snippets after user confirmation; publish flows require PAC CLI authentication and explicit target-environment confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
