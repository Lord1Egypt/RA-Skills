## Description:

Browser Healthcheck checks browser tool status before use and guides diagnosis or repair for screenshot, automation, timeout, and CDP disconnection issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to check OpenClaw browser readiness, diagnose profile conflicts, CDP connectivity problems, and browser timeouts, and apply guided repair steps before browser-based screenshots or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The repair path may force-kill a local process using a PID found during CDP port diagnosis without proving it is the intended OpenClaw browser process.

Mitigation: Use the isolated openclaw profile where possible, inspect the reported PID before invoking repair actions, and only accept process termination when the process is confirmed to be OpenClaw-managed.

## Reference(s):

- [Browser Healthcheck ClawHub Skill Page](https://clawhub.ai/systiger/skills/browser-healthcheck)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and troubleshooting steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Python healthcheck script that prints local browser, profile, port, and CDP status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
