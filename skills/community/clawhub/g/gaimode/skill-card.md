## Description:

Perform unofficial Google AI Mode searches from an agent using a local Chrome DevTools Protocol session or exported Google cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisdhana](https://clawhub.ai/user/whoisdhana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to query Google AI Mode for current web information such as sports scores, stock prices, news, weather, and AI summaries. It is suited to workflows that can tolerate unofficial browser automation and the risks of using a dedicated Google session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes sensitive Google session access through exported cookies or a browser debugging endpoint.

Mitigation: Use a dedicated low-privilege Google account, avoid primary-account cookies, and restrict cookie file permissions.

Risk: Chrome DevTools Protocol on localhost can let local processes inspect or control the dedicated browser session.

Mitigation: Run CDP only when needed, close the dedicated browser after use, and avoid keeping the debugging port open continuously.

Risk: The launcher can terminate existing Chrome sessions before starting a CDP-enabled browser.

Mitigation: Review the launcher behavior before use and run it only when closing existing Chrome sessions is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whoisdhana/skills/gaimode)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output is truncated by the CLI and depends on the active Google session, browser state, and Google response behavior.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
