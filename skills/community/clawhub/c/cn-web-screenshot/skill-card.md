## Description:

Cn Web Screenshot captures PNG screenshots of web pages from a URL, including full-page, viewport, mobile, tablet, and delayed captures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and agents use this skill to capture rendered web pages as PNG files for visual review, regression checks, archival snapshots, or page previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to user-supplied URLs, including sensitive internal, localhost, metadata, authenticated, or confidential endpoints.

Mitigation: Run the skill in an isolated environment and avoid using it against internal, localhost, metadata, authenticated, or confidential URLs.

Risk: The skill can save screenshots to caller-selected paths.

Mitigation: Use a restricted output directory and review requested output paths before execution.

Risk: The skill depends on Playwright and Chromium at runtime.

Mitigation: Install and pin dependencies in the execution environment before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-web-screenshot)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [AISoBrand website](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON status with a PNG screenshot file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes PNG screenshot files to the requested output path or to /tmp by default.]

## Skill Version(s):

1.0.2 (source: server evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
