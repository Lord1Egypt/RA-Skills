## Description:

Scan web files for broken hyperlinks and weak SEO anchor text, then interactively replace, strip, or skip each dead URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content maintainers use this skill to audit project files for dead absolute URLs, weak SEO anchor text, and interactive repair options across common web formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically checks URLs found in project files.

Mitigation: Use it only on trusted files and avoid running it where local or cloud metadata services are reachable.

Risk: Broken URLs may be sent to GitHub Copilot for replacement suggestions.

Mitigation: Avoid Copilot suggestions for URLs that may contain secrets, signed query strings, customer identifiers, or internal hostnames.

## Reference(s):

- [Fix Broken Links ClawHub Page](https://clawhub.ai/jhauga/skills/fix-broken-links)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text link-check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt interactively when run against explicit file paths; can update matching source files when the user accepts a replacement, removal, or custom URL.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
