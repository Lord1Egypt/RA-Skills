## Description:

Agent Kanban provides a Bloomberg Terminal-style web dashboard for monitoring OpenClaw agent status, session history, session file sizes, and related agent files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyh](https://clawhub.ai/user/dyh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and operate a local OpenClaw dashboard for checking agent availability, recent session activity, session file size, and selected agent workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose sensitive agent status, histories, and workspace files too broadly.

Mitigation: Run it only on trusted local hosts, add authentication and per-agent authorization before broader use, and avoid showing raw histories or files by default with sensitive agents.

Risk: The release includes unsafe credential handling for the OpenClaw Gateway token.

Mitigation: Remove and rotate the embedded token, then load credentials from a local private configuration or another secret-management mechanism.

Risk: Network exposure and permissive browser access can increase the blast radius of a local monitoring tool.

Mitigation: Bind the server to localhost, restrict CORS to trusted origins, and do not expose the dashboard on a network as shipped.

Risk: Remote frontend scripts and avatar calls can leak usage metadata or add supply-chain exposure.

Mitigation: Replace remote scripts and avatar calls with local, pinned assets before use with sensitive agents.

## Reference(s):

- [Agent Kanban README](references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Node.js application files, configuration examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local dashboard deployment instructions and supporting application assets for OpenClaw monitoring.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
