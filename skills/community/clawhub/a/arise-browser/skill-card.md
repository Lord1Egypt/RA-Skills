## Description:

Browser automation for AI agents that controls Chrome through CLI commands with persistent element refs, YAML accessibility snapshots, and WebRTC live view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yourens](https://clawhub.ai/user/yourens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Arise Browser to operate a local Chromium browser, inspect page state through snapshots, and interact with web pages through stable element references and CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local browser-control service can drive a Chromium session and interact with arbitrary pages.

Mitigation: Install only in environments where local browser automation is acceptable, bind it to localhost, and avoid exposing the control or viewing ports through containers, tunnels, or public interfaces.

Risk: Authentication may be optional or weak for local control and viewing interfaces.

Mitigation: Set ARISE_BROWSER_TOKEN before use and avoid running the service where untrusted local processes can access it.

Risk: Using a daily browser profile can expose saved logins, cookies, history, or other personal data.

Mitigation: Use a fresh or dedicated browser profile and do not run profile mode against a personal daily browser profile.

Risk: The evaluate endpoint can execute arbitrary JavaScript in the page context.

Mitigation: Review any use of evaluate before execution and prefer snapshot, click, type, select, press, and scroll commands when they are sufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yourens/skills/arise-browser)
- [AriseBrowser API Reference](references/api.md)
- [AriseBrowser Trust & Security Model](TRUST.md)
- [Project Homepage](https://github.com/AriseOS/arise-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and browser snapshot examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser-control commands, page snapshots, screenshots, and API request guidance during use.]

## Skill Version(s):

0.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
