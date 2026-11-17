## Description:

Runs Codex CLI coding tasks in the background for long-running development work, with commands for starting, monitoring, logging, and stopping jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyn1990](https://clawhub.ai/user/tianyn1990)

### License/Terms of Use:


## Use Case:

Developers use this skill to delegate long-running coding, build, and test tasks to Codex CLI while monitoring progress through logs and process commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background Codex tasks can run with sandbox and approval protections disabled.

Mitigation: Use the skill only in isolated throwaway workspaces or containers, and avoid running it against sensitive repositories or normal home directories.

Risk: Shell wrappers accept task names, paths, and task text without robust validation or safe encoding.

Mitigation: Rewrite the wrappers to validate inputs, safely encode JSON, quote shell arguments, and track only their own process IDs before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianyn1990/skills/codex-runner)
- [Publisher profile](https://clawhub.ai/user/tianyn1990)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces background-task launch instructions, process status, and log excerpts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
