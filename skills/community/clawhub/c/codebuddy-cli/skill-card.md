## Description:

CodeBuddy CLI for OpenClaw helps agents guide installation, configuration, usage, and troubleshooting for Tencent's CodeBuddy Code CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmwalkercao](https://clawhub.ai/user/pmwalkercao)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to install, configure, operate, and troubleshoot Tencent's CodeBuddy Code CLI from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permission-skipping options such as --dangerously-skip-permissions and bypassPermissions can allow file changes or deletion without confirmation.

Mitigation: Use default or plan permission modes for normal projects, and reserve permission-skipping options for disposable sandboxes.

Risk: Global npm installation can introduce supply-chain and privilege risks if the package or publisher is not verified.

Mitigation: Verify the npm package and publisher before installation, and avoid running npm or CodeBuddy with elevated privileges.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
