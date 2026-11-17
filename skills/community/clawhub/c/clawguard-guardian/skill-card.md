## Description:

ClawGuard Guardian v3 provides agent-facing workflows for monitoring AI agent operations, showing audit and status information, replaying sessions, and issuing freeze or unfreeze responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stardreaming](https://clawhub.ai/user/stardreaming)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators can use this skill to ask an agent for guardian-style status, logs, session replay, freeze and unfreeze flows, and security-oriented operational guidance while managing AI agent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged CLI cannot start as shipped because guardian.js imports a shared rule module that is not included in the artifact.

Mitigation: Include or replace the missing rule module and run a CLI smoke test before installation or operational use.

Risk: The skill advertises blocking, freezing, and interception, but evidence.security says those controls are not technically enforced.

Mitigation: Treat the skill as advisory until enforcement is implemented and independently tested; do not rely on it as a runtime security boundary.

Risk: Audit logs may contain sensitive operation targets and are written locally under the user's home directory.

Mitigation: Review log contents, retention, and permissions before enabling the CLI in environments that handle secrets or regulated data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stardreaming/skills/clawguard-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style agent responses and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSONL audit logs under ~/.clawguard/logs/ when the CLI runs.]

## Skill Version(s):

3.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
