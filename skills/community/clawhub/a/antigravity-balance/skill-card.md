## Description:

Check Google Antigravity AI model quota/token balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finderstrategy-cyber](https://clawhub.ai/user/finderstrategy-cyber)

### License/Terms of Use:


## Use Case:

Developers and Antigravity users use this skill to check remaining AI model quota, token balance, rate-limit status, and reset timing from a running local Antigravity instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects local Antigravity process arguments and handles a CSRF token while querying the local language-server API.

Mitigation: Run it only in trusted local environments, avoid verbose mode, and prefer a future version that uses an official or better-scoped API and validates the local endpoint before sending credentials.

Risk: Verbose output may expose sensitive command-line data.

Mitigation: Use normal or JSON output for routine checks and reserve verbose mode for controlled debugging sessions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text or JSON from a local Node.js script, with Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a running Antigravity or Windsurf language-server process.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
