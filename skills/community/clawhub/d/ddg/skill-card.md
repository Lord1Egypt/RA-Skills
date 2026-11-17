## Description:

Use ddgr (DuckDuckGo from the terminal) to perform privacy-focused web searches from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[instant-picture](https://clawhub.ai/user/instant-picture)

### License/Terms of Use:


## Use Case:

Developers, engineers, and command-line users use this skill to run DuckDuckGo searches through ddgr, including non-interactive searches, site-specific queries, time filters, JSON output, and DuckDuckGo bangs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some installation paths ask users to trust unpinned third-party code with administrator privileges.

Mitigation: Prefer a trusted packaged source such as the recommended snap or an official OS package; use PPA or source installation only after verifying the publisher and release.

Risk: Browser-opening and unsafe-search modes can expose users to unexpected web content.

Mitigation: Treat --ducky, interactive result opening, and --unsafe as explicit opt-in modes and review commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/instant-picture/skills/ddg)
- [ddgr usage patterns](references/usage-patterns.md)
- [ddgr GitHub repository](https://github.com/jarun/ddgr)
- [DuckDuckGo](https://duckduckgo.com)
- [DuckDuckGo bangs](https://duckduckgo.com/bang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on network access, DuckDuckGo availability, ddgr installation, selected region and time filters, and whether interactive or browser-opening modes are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
