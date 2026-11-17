## Description:

Helps agents use ddgr to run privacy-focused DuckDuckGo web searches from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shelehovnick1-spec](https://clawhub.ai/user/shelehovnick1-spec)

### License/Terms of Use:


## Use Case:

Developers and terminal-oriented users use this skill to install and run ddgr searches, including non-interactive, site-specific, time-filtered, JSON, and DuckDuckGo bang queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions include root-level installation from unpinned third-party sources without verification guidance.

Mitigation: Review the install path before use, prefer trusted OS packages or verified releases, and avoid running sudo make install from an unpinned clone.

Risk: Interactive result selection or --ducky can open third-party pages in the browser.

Mitigation: Review destination URLs before opening results and apply normal browser and endpoint safeguards for untrusted web pages.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [ddgr GitHub Repository](https://github.com/jarun/ddgr)
- [DuckDuckGo](https://duckduckgo.com)
- [DuckDuckGo Bangs](https://duckduckgo.com/bang)
- [ClawHub Skill Page](https://clawhub.ai/shelehovnick1-spec/skills/ddg-1-0-0)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, json]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ddgr commands that produce plain text or JSON search results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
