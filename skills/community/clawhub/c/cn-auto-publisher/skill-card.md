## Description:

Automates publishing prepared content to Zhihu answers and articles and Xiaohongshu image-text notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to publish prepared text and optional images to Zhihu and Xiaohongshu through browser automation. It is intended for accounts where automated public posting is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public content without a final confirmation step.

Mitigation: Inspect and approve content before invocation, and use only accounts where automated posting is acceptable.

Risk: Saved login cookies under ~/.qclaw may contain reusable account sessions.

Mitigation: Protect or delete the cookie files after use and avoid running the skill on shared machines.

Risk: Automated posting may violate platform rules or account expectations if used too frequently or with unsuitable content.

Mitigation: Follow the target platform's rules and keep posting frequency conservative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-auto-publisher)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text status and JSON command results from browser automation scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce public posts or result URLs on supported platforms when invoked with valid account sessions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
