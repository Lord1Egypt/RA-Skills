## Description:

Set up and verify a first Dataify workflow, then route the user to MCP, local skills, or REST without losing their original task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure Dataify credentials, verify account readiness, and choose the smallest working access path for a first Dataify task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Dataify token may be used for API calls and one task-waiting path places the token in request URLs.

Mitigation: Use a limited-scope or easily rotated token, avoid sharing logs or URLs from task-waiting runs, and rotate the token if it may have been exposed.

Risk: Queries, URLs, and task parameters can be sent to Dataify during verification or workflow execution.

Mitigation: Review inputs before execution and avoid sending confidential, regulated, or unnecessary data.

Risk: The package includes broader task-running and local report-writing helpers beyond basic onboarding.

Mitigation: Run only the onboarding or verification commands needed for setup unless the broader Dataify reports and local output files are intended.

## Reference(s):

- [Dataify Documentation](https://doc.dataify.com)
- [Dataify Support](https://www.dataify.com/)
- [Access paths](references/access-paths.md)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-agent-onboarding)
- [Publisher profile](https://clawhub.ai/user/dataify-server)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Markdown, Files]

**Output Format:** [Markdown guidance with inline shell commands, optional JSON status output, and local JSON or Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Dataify APIs and may write local workflow state, raw result, report.json, and report.md files when broader task workflows are run.]

## Skill Version(s):

1.1.1 (source: server release evidence and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
