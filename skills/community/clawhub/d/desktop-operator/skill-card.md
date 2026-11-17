## Description:

Operate Electron desktop applications on macOS via Puppeteer CDP. Open an app, find a UI element by text, click it, and take a screenshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondli](https://clawhub.ai/user/bondli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate local Electron desktop applications on macOS by opening an installed app, clicking a visible text target, and capturing a screenshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture the whole desktop and may include sensitive visible information in screenshots.

Mitigation: Use it only with apps and data that are appropriate to automate and capture; close unrelated windows and review stored screenshots before sharing.

Risk: The skill saves screenshot images on disk in the user's home folder.

Mitigation: Review, retain, or delete generated screenshots according to the data sensitivity of the automated session.

Risk: The skill enables local debugging for the target Electron app and can force-close processes with matching app names.

Mitigation: Run it only on trusted local sessions, save work before execution, and verify the app name before starting automation.

## Reference(s):

- [README.md](README.md)
- [ClawHub skill page](https://clawhub.ai/bondli/skills/desktop-operator)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [JSON containing a screenshot path, plus a PNG screenshot file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshot files are saved under the user's home directory in openclaw-skill-data/desktop-oprator.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
