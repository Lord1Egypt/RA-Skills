## Description:

Provides fast manual CI for Docker Compose apps by mapping DCC requests to a remote controller that pulls, builds, deploys, restarts, and verifies a named app on a known Docker server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drodecker](https://clawhub.ai/user/drodecker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy, restart, recreate, inspect, or dry-run Docker Compose applications on a known Docker host when a traditional CI pipeline is unavailable or too slow. The skill is intended for exact app names and requires clarification when the target server or deployment is ambiguous.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent root-level control over a remote Docker server.

Mitigation: Install only for an intended Docker host, confirm the server and app names before use, and prefer a restricted sudoers rule or service account.

Risk: The skill can install a persistent controller on the remote server.

Mitigation: Review the bundled controller before installation and do not replace an existing controller without explicit approval.

Risk: Deployment actions can change running containers and application code on the target host.

Mitigation: Use exact deployment names, run dry-run or status checks when uncertain, and report success only after the command exits successfully and containers reach running or healthy state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drodecker/skills/dcc-docker-container-control)
- [Project Homepage](https://github.com/localsplash/dcc-docker-container-control-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports important command output and final Compose status; asks for the Docker server or deployment name when ambiguous.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
