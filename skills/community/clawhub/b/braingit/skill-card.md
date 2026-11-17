## Description:

Automate committing Markdown-only changes in a git repo with safe staging, ideal for note snapshots without affecting code or binaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gleb-urvanov](https://clawhub.ai/user/gleb-urvanov)

### License/Terms of Use:


## Use Case:

Developers, writers, and teams use Braingit to snapshot Markdown notes, specs, plans, and research in a Git repository without intentionally staging code or binaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The commit script can accidentally include files that were already staged before it runs, including non-Markdown files.

Mitigation: Run it only in repositories with a clean index or use dry-run first; avoid scheduled automation until the script aborts on pre-existing staged files or uses an isolated Git index.

Risk: Scheduled snapshots can commit sensitive Markdown content if secrets are stored in notes.

Mitigation: Keep ignore rules and path exclusions current, and avoid storing secrets in Markdown repositories that are committed automatically.

## Reference(s):

- [Braingit protocol](references/protocol.md)
- [Braingit article](https://github.com/gleb-urvanov/braingit/blob/master/braingit-article.md)
- [ClawHub skill page](https://clawhub.ai/gleb-urvanov/skills/braingit)
- [Publisher profile](https://clawhub.ai/user/gleb-urvanov)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides command examples and environment-variable options; it does not produce binary artifacts.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
