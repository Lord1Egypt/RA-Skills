## Description:

Queries DataEase organizations, switches organization context, lists dashboards or big screens, and exports selected resources as screenshots or PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuwei-fit2cloud](https://clawhub.ai/user/xuwei-fit2cloud)

### License/Terms of Use:

MIT-0

## Use Case:

DataEase administrators and analytics operators use this skill to find organizations and visualization resources, switch to the right organization context, and export dashboards or big-screen views for sharing or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live DataEase tokens may be exposed during browser capture or through terminal logs and generated artifacts.

Mitigation: Use a trusted HTTPS DataEase URL, avoid command-line passwords where possible, keep logs and exported files private, and prefer short-lived least-privilege accounts or tokens.

Risk: The skill accesses organization, dashboard, and big-screen data that may contain sensitive business information.

Mitigation: Install and run it only in controlled environments and limit credentials to the organizations and resources required for the task.

Risk: Browser capture code injects DataEase tokens into local browser storage to render preview pages.

Mitigation: Review or patch the browser capture code before production use and clear local browser/session data after exports when appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuwei-fit2cloud/skills/dataease)
- [DataEase API Reference](references/api.md)
- [Resource Alias Map](references/resource_aliases.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown status text with command output summaries and generated JPEG or PDF file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create dashboard or big-screen export files in the local outputs directory.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
