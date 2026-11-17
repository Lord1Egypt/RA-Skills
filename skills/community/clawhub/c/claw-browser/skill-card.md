## Description:

A visual, human-like browser helper for OpenClaw agents that can read JavaScript-rendered pages, take screenshots, and run in visible mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canbirlik](https://clawhub.ai/user/canbirlik)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when a task needs a real Chromium browser to render dynamic websites, read visible page text, or capture screenshots for visual verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open and read arbitrary URLs from the local runtime without destination safeguards.

Mitigation: Use it only in an isolated environment and confirm destinations before opening untrusted, internal, or authenticated pages.

Risk: Printed page text and evidence.png may contain sensitive information.

Mitigation: Treat console output and screenshots as sensitive artifacts and avoid sharing them outside the intended review context.

Risk: The Playwright dependency is unpinned, which can reduce repeatability.

Mitigation: Pin or lock Playwright before relying on repeatable installs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration]

**Output Format:** [Console text and PNG screenshot file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The read action prints page title and up to 5000 characters of page text; the screenshot action writes evidence.png.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
