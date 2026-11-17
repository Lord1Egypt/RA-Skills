## Description:

Install and configure the security-related plugins required by OpenClaw, including the `claw-sentry` plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install the ClawSentry plugin, complete activation, and configure security protections for an OpenClaw environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs a bundled local script, installs a remote plugin package, contacts Volcengine/ClawSentry authorization services, stores login state, enables conversation access for the plugin, and restarts the OpenClaw gateway.

Mitigation: Review the skill before installing and run it only on machines where those installation, authorization, storage, access, and restart actions are acceptable.

Risk: Evidence security guidance flags credential logging, unpinned install, and cleanup-path risks.

Mitigation: Avoid shared or sensitive machines unless those risks are accepted, monitor execution, and rotate any ClawSentry API key if the installer has already produced poll_login.log.

## Reference(s):

- [ClawSentry skill page](https://clawhub.ai/volcengine-skills/skills/clawsentry)
- [ClawSentry README](artifact/README.md)
- [Volcengine](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and activation-link text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a two-phase install and activation flow that can write local login state and update OpenClaw plugin configuration.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
