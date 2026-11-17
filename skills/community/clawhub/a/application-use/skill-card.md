## Description:

Automate macOS tasks by opening apps, clicking elements, filling forms, typing, scrolling, and controlling the desktop through CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qdore](https://clawhub.ai/user/qdore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to automate macOS desktop workflows such as app launching, form filling, browser navigation, screenshots, and Finder interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over macOS applications, visible screen contents, focused text fields, browser sessions, and Finder actions.

Mitigation: Install only after review, run it in a controlled desktop session, and require explicit confirmation before submissions, file changes, screenshots, or interactions with sensitive apps.

Risk: Desktop automation can expose or enter sensitive data such as passwords, account details, or private screen contents.

Mitigation: Avoid using the skill for passwords, financial actions, account approvals, or workflows involving sensitive applications unless additional human review is in place.

Risk: The documented install command uses an unpinned global npm package installation.

Mitigation: Prefer a pinned and reviewed package version before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qdore/skills/application-use)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce screen snapshots or screenshots as visual feedback after desktop actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
