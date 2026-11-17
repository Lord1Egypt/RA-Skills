## Description:

Ganidhuz-FoxX lets an agent browse X/Twitter through a logged-in Firefox session by exporting Firefox cookies and running Playwright browser plans for profiles, tweets, searches, screenshots, and page text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganidhuz](https://clawhub.ai/user/ganidhuz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect X/Twitter pages with an existing logged-in Firefox session when API access is unavailable or unsuitable. It supports profile viewing, tweet retrieval, live search, scrolling feeds, screenshots, and extracting selected page text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable X/Twitter session cookies can expose account access if cookie or storage-state files are leaked.

Mitigation: Treat `secrets/x-cookies.json` and any storage-state file as sensitive account data, store them only in protected locations, and prefer a disposable X/Twitter account.

Risk: Plan files can drive browser actions while authenticated to X/Twitter.

Mitigation: Run only trusted plans, review target URLs and actions before execution, and prefer a version that limits navigation to X/Twitter and disables write actions by default.

Risk: Screenshots and extracted page text may contain private account, feed, or session-adjacent information.

Mitigation: Confine outputs to a protected directory and avoid sharing screenshots, extracted text, or validation artifacts unless they have been reviewed for sensitive content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ganidhuz/skills/ganidhuz-foxx)
- [Publisher Profile](https://clawhub.ai/user/ganidhuz)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown instructions with shell commands and JSON plan examples; runtime output is JSON with optional screenshots, storage state, and extracted page text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, Playwright, Firefox, an active X/Twitter login, and careful handling of exported cookie and storage-state files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
