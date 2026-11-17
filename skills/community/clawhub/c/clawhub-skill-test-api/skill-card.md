## Description:

Weaver E10 Api helps agents call Weaver E10 workflow APIs to create workflows, list pending tasks, approve or reject requests, query workflow details, and manage OAuth 2.0 tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xfnet](https://clawhub.ai/user/xfnet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to automate Weaver E10 workflow actions from an agent, including workflow creation, pending-task lookup, approval, rejection, and workflow status queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles OAuth secrets and token cache files.

Mitigation: Use only a trusted Weaver E10 server over HTTPS, secure the .env file and token cache, and avoid shared hosts.

Risk: Approve and reject commands can immediately change business workflows.

Mitigation: Restrict the app permissions and review workflow-changing commands before execution.

Risk: ClawHub security evidence marks the release as suspicious because safeguards are weak.

Mitigation: Review before installing and deploy only where the connected Weaver E10 permissions are appropriately limited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xfnet/skills/clawhub-skill-test-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create, approve, or reject workflow requests in the connected Weaver E10 system.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact _meta.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
