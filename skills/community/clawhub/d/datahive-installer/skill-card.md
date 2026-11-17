## Description:

Automates DataHive sign-in using a magic link workflow: requests the link, retrieves it from Gmail via gog, and opens it in a Chrome DevTools tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuleyko](https://clawhub.ai/user/tuleyko)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use this skill to automate DataHive dashboard authentication by installing browser prerequisites, requesting a magic link, retrieving it through an authenticated gog Gmail account, and opening it in Chrome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs packages and applies managed Chrome policy using administrative privileges.

Mitigation: Review the scripts before execution and run only on hosts where sudo package installation and browser-policy changes are acceptable.

Risk: The skill launches persistent Chrome with DevTools remote debugging enabled on localhost.

Mitigation: Keep the debugging endpoint local, use a trusted machine, and stop the browser supervisor after the login flow is complete.

Risk: Magic links are login secrets retrieved from Gmail and passed to a browser tab.

Mitigation: Treat magic links as secrets, avoid logging or sharing them, and rerun the request flow when links expire.

## Reference(s):

- [ClawHub Skill: DataHive Installer](https://clawhub.ai/tuleyko/skills/datahive-installer)
- [Publisher Profile: tuleyko](https://clawhub.ai/user/tuleyko)
- [DataHive Dashboard](https://dashboard.datahive.ai/auth)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gog, curl, websocat, Chrome, and Ubuntu or macOS; handles short-lived magic login links.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
