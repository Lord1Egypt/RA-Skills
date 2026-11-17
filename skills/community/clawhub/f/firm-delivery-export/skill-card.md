## Description:

Post-processing skill for firm-orchestration that converts structured JSON output from a multi-agent workflow run into deliverables such as GitHub pull requests, Jira or Linear tickets, Markdown reports, project briefs, and structured documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to turn final agent workflow output into reviewable team deliverables in GitHub, Jira, Linear, Markdown, or related delivery formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests service credentials and shell or network access for delivery targets, including some workflows that may not need every credential.

Mitigation: Use fine-grained GitHub, Jira, and Linear tokens scoped only to the target repository or project, and expose only the credentials required for the chosen output format.

Risk: Generated pull requests, tickets, or messages could publish incorrect or premature agent output into team tooling.

Mitigation: Keep GitHub pull requests in draft mode, apply human-review labels, and review generated tickets, documents, and digests before relying on or distributing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-delivery-export)
- [Publisher profile](https://clawhub.ai/user/romainsantoli-web)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON schemas and Markdown delivery content for downstream tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create draft GitHub pull requests, Jira tickets, Linear issues, Markdown reports, structured documents, project briefs, or Slack digests depending on configured credentials and requested format.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
