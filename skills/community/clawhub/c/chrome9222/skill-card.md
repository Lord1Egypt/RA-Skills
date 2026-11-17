## Description:

Launches Chrome with remote debugging enabled on port 9222 for local debugging and development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aizzaua](https://clawhub.ai/user/aizzaua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to start a local Chrome browser with DevTools remote debugging available on port 9222. It is intended for browser debugging and automation setup where a dedicated Chrome profile is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently force-close existing Chrome windows before launching the debug browser.

Mitigation: Review before installation, save browser work first, and modify the skill to prompt before closing Chrome if used in regular workflows.

Risk: The skill starts a Chrome instance with remote debugging enabled and persistent local state.

Mitigation: Use it only on trusted machines, avoid sensitive accounts in the debug browser, and prefer a private or disposable profile directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aizzaua/skills/chrome9222)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Text status message after executing local browser launch commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill launches a local Chrome process, may close existing Chrome sessions, and uses a dedicated local user data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
