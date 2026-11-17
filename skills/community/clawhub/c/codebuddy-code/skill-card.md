## Description:

CodeBuddy Code for OpenClaw guides agents through installing, configuring, and using Tencent's CodeBuddy Code CLI for natural-language-driven development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmwalkercao](https://clawhub.ai/user/pmwalkercao)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install CodeBuddy Code, choose login and permission modes, run interactive or single-task CLI sessions, use slash commands, create custom commands, update the tool, and understand the security posture of permission-bypass flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation can execute package installation behavior and place the CodeBuddy CLI on the user's PATH.

Mitigation: Install only after trusting the CodeBuddy npm package and publisher, prefer a pinned reviewed version, and avoid administrator privileges.

Risk: Permission-bypass modes such as -y or bypassPermissions can allow unintended file changes, deletion, scope creep, or data loss.

Mitigation: Use default or plan permissions for normal projects and reserve permission bypass for disposable sandboxes with recoverable files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmwalkercao/skills/codebuddy-code)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI installation and update commands, login options, slash commands, custom command locations, and security notes.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
