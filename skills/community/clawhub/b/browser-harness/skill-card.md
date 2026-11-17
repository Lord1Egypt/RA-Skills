## Description:

Browser Harness lets an agent control a local Edge or Chrome browser over CDP to open pages, capture screenshots, extract rendered content, and automate browser actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[19770117](https://clawhub.ai/user/19770117)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect dynamic webpages, capture browser screenshots, extract JavaScript-rendered content, and run browser automation through a local Edge or Chrome debugging session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable third-party browser automation code at install time.

Mitigation: Install from a pinned release or reviewed commit before use.

Risk: Browser automation over a local debugging session can expose sensitive pages, screenshots, or extracted page text.

Mitigation: Use a separate browser profile with no unrelated logged-in sessions and avoid capturing sensitive pages.

Risk: Remote browser mode can expose browsing activity to an external provider.

Mitigation: Avoid remote cloud mode unless the provider and data handling are understood and trusted.

## Reference(s):

- [Browser Harness repository](https://github.com/browser-use/browser-harness)
- [ClawHub skill page](https://clawhub.ai/19770117/skills/browser-harness)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and browser automation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots or extracted page text through browser-harness commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
