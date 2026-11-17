## Description:

Retry browser clicks with automatic obstacle detection and dismissal. Use when browser tool clicks fail due to cookie banners, modals, or fixed headers blocking the target element.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to recover from Playwright or OpenClaw browser click failures when overlays, cookie banners, modals, or fixed headers block the target element.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default browser automation can automatically accept cookie or consent prompts for the user.

Mitigation: Use auto_dismiss=False or manually review consent dialogs before allowing clicks on privacy-sensitive sites or sites with legal terms.

## Reference(s):

- [Browser Smart Click usage guide](references/usage.md)
- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/browser-smart-click)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Playwright click helpers and ClickResult-style status data for success, blocker, retry count, and message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
