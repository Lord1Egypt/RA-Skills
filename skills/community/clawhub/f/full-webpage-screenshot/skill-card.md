## Description:

Capture complete webpage screenshots using Puppeteer, including content that loads dynamically on scroll.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifelooploop](https://clawhub.ai/user/lifelooploop)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to capture full-page PNG screenshots of websites for visual documentation, including pages that lazy-load content during scrolling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a Puppeteer-based browser against URLs selected by the user, and evidence.security reports that it launches the browser without sandbox protections.

Mitigation: Use it only for URLs you are comfortable opening in an automated browser, and avoid internal, localhost, cloud metadata, authenticated, or sensitive URLs unless it runs in a disposable container with restricted network egress and no secrets.

Risk: evidence.security reports outdated vulnerable Puppeteer dependencies.

Mitigation: Update Puppeteer and dependencies before broad use, and review the release again after dependency updates.

Risk: evidence.security recommends URL and network safeguards before broad use.

Mitigation: Add allowlists, deny internal network ranges, and remove disabled browser sandbox flags where the runtime environment supports sandboxing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lifelooploop/skills/full-webpage-screenshot)
- [Publisher profile](https://clawhub.ai/user/lifelooploop)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown usage guidance with shell commands; runtime JSON status and PNG screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Viewport size, scroll delay, and post-load wait time can be controlled with environment variables.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
