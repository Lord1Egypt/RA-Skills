## Description:

Install and operate the agent-browser-shield Chromium extension to mask PII and secrets, neutralize dark patterns, and strip prompt-injection surfaces before the agent sees the page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pixiebrix](https://clawhub.ai/user/pixiebrix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of browser-using agents use this skill to install a Chromium extension and define agent behavior for handling masked content, cart add-on warnings, cleared checkboxes, and rewritten page elements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a high-trust browser extension from mutable external sources without integrity verification.

Mitigation: Install only if the publisher is trusted, prefer a dedicated browser profile with no unrelated logins, and verify the extension source and release artifact before loading it.

Risk: The Browserbase path sends the extension package to Browserbase.

Mitigation: Use the Browserbase installation path only when that upload is acceptable, and protect Browserbase API keys and project credentials.

Risk: The extension mediates pages that the agent reads and acts on.

Mitigation: Keep the extension enabled only in the intended agent browser profile and follow the documented behavior contract for placeholders, masked data, and page markers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pixiebrix/skills/agent-browser-shield)
- [Chrome Web Store listing](https://chromewebstore.google.com/detail/agent-browser-shield/gnejacdioaelglahihpagpfjpddpnamd)
- [Hosted extension ZIP](https://github.com/pixiebrix/agent-browser-shield/releases/latest/download/agent-browser-shield-extension.zip)
- [Browserbase browse CLI documentation](https://docs.browserbase.com/integrations/skills/browse-cli)
- [Issue tracker](https://github.com/pixiebrix/agent-browser-shield/issues)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and browser configuration flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes DOM marker handling guidance and local or Browserbase installation paths.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
