## Description:

This skill lets OpenClaw users search, inspect, install, uninstall, and list 1Panel app-store applications through natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainsunsun](https://clawhub.ai/user/rainsunsun)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and server administrators use this skill to manage 1Panel app-store applications from chat, including search, install, uninstall, and installed-app inventory workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or remove server applications using a saved 1Panel API key.

Mitigation: Use a narrowly scoped API key, review install and uninstall prompts before execution, and avoid unattended batch uninstall workflows.

Risk: HTTP endpoint examples can expose credentials or administrative traffic.

Mitigation: Configure only HTTPS 1Panel endpoints and rotate any API key that may have been used over HTTP.

Risk: Uninstall and batch uninstall flows may remove server applications without a built-in confirmation step.

Mitigation: Confirm the target application and install ID before removal, and add an operator approval step in deployments that manage shared or production servers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rainsunsun/skills/c2a)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with app lists, status messages, configuration examples, and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include application names, versions, install IDs, operation status, and configuration requirements for the configured 1Panel server.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
