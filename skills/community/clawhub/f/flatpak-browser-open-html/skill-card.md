## Description:

Open local HTML files in a Flatpak browser from the terminal by using Flatpak file forwarding and file URL marker arguments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Linux users use this skill to open local HTML files in Flatpak-packaged browsers and to diagnose browser handler issues when links silently fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example browser IDs or desktop files may not match the user's installed browser.

Mitigation: Confirm the installed Flatpak application ID and desktop file before running the example commands.

Risk: xdg-mime commands can change default browser and link handlers.

Mitigation: Check current MIME defaults before changing them and update only the handlers intended for the target browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/flatpak-browser-open-html)
- [Publisher homepage](https://github.com/mina-atef-00/agent-skills)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux and Flatpak focused troubleshooting guidance]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
