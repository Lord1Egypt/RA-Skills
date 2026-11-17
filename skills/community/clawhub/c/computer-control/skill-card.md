## Description:

Enables an agent to inspect and operate a local desktop through screenshots, mouse and keyboard actions, app launching, and AppleScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topgemstoken](https://clawhub.ai/user/topgemstoken)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and other desktop users can direct an agent to inspect the screen and automate local GUI tasks when shell or browser tools cannot reach the application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen capture and desktop control require broad local permissions.

Mitigation: Grant Accessibility and Screen Recording access only if comfortable with the agent viewing and controlling the computer; run the permission check before acting.

Risk: Arbitrary AppleScript can perform unrestricted desktop automation.

Mitigation: Review AppleScript commands before running them and confirm consequential actions with the user.

Risk: On Linux, app names passed to the launcher can be interpreted by a shell.

Mitigation: Use only trusted app names and avoid unreviewed input to the launcher.

Risk: Installation writes a local helper app with computer-control capabilities.

Mitigation: Review the bundled install scripts before running them and inspect the helper app placed in ~/Applications/TarsX.app.

## Reference(s):

- [Computer Control on ClawHub](https://clawhub.ai/topgemstoken/skills/computer-control)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and screenshot paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can return JSON diagnostics or paths to PNG screenshots.]

## Skill Version(s):

1.0.3 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
