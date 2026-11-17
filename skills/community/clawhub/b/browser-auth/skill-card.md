## Description:

Browser Auth starts a remote browser tunnel for manual user authentication, including Captcha, 2FA, and login flows, and captures reusable session data for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lksrz](https://clawhub.ai/user/lksrz)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill when an agent needs a human to complete login, Captcha, 2FA, or bot-detection steps without sharing account passwords. The skill captures cookies and localStorage into a reusable session file for later automated browser work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a sensitive remote browser session that can be misused if the token URL or listening host is exposed.

Mitigation: Set AUTH_HOST=127.0.0.1 explicitly, use only a trusted encrypted tunnel for remote access, and avoid sharing the printed token URL through logs or insecure channels.

Risk: The generated session file contains reusable login cookies and localStorage values.

Mitigation: Protect the session file as a secret and delete it immediately after the agent no longer needs it.

Risk: Browser activity and optional proxy settings can expose authenticated traffic to untrusted infrastructure.

Mitigation: Run the skill in an isolated VM or container and avoid untrusted proxies.

## Reference(s):

- [Browser Auth ClawHub listing](https://clawhub.ai/lksrz/skills/browser-auth)
- [AI Commander homepage](https://aicommander.dev)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown-style guidance with inline shell commands, plus a JSON session file containing cookies and localStorage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, chromium-browser, express, socket.io, playwright-core, and careful handling of the generated session file.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
