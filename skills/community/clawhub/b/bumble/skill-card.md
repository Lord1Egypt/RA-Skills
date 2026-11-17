## Description:

Automates an operator-owned Bumble web session through a Remote Browser Service to resume sessions, authenticate with SMS, inspect matches and messages, send permitted messages, unmatch, and export visible profile photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vasyaod](https://clawhub.ai/user/vasyaod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to manage their own Bumble web account through a remote browser, including session recovery, match review, message handling, and profile-photo export for content already visible to the account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in Bumble account through the configured Remote Browser Service, including reading messages, sending messages, changing geolocation, exporting photos, and unmatching people.

Mitigation: Install and run it only with a trusted Remote Browser Service endpoint, avoid overriding RBS_BASE_URL unless the endpoint is trusted and uses HTTPS, and confirm sensitive account actions before execution.

Risk: Debug, content, snapshot, message, screenshot, and photo-export commands can expose personal profile data and private messages.

Mitigation: Do not run inspection commands in shared logs, store exported photos only in intended directories, and treat exported files and command output as sensitive personal data.

Risk: Location changes and unmatching are user-visible or potentially irreversible account actions.

Mitigation: Use the skill only for the operator's own account, review the target match and action before execution, and avoid unattended use for destructive actions.

## Reference(s):

- [README](artifact/README.md)
- [Security & Scope](artifact/SECURITY.md)
- [Bumble Web App](https://bumble.com/app)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON command responses, and downloaded photo files when export is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require operator-supplied phone number, SMS code, match name, message text, and output directory.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
