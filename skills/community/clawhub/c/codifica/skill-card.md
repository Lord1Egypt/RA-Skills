## Description:

Keep context when work moves between agents or between you and a human. Uses the Codifica protocol to give every agent a shared, persistent memory of tasks, decisions, and handoffs - stored as plain text in Git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidedicillo](https://clawhub.ai/user/davidedicillo)

### License/Terms of Use:


## Use Case:

Developers and agents use Codifica to coordinate repository work through shared plain-text task state, execution notes, and Git history across handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to trust repository-controlled Codifica spec and state files.

Mitigation: Install it only in repositories where the Codifica files are trusted, and review the spec and state files before acting.

Risk: The protocol can lead agents to commit or push persistent state, including execution notes.

Mitigation: Confirm the Git remote and branch, prefer manual approval for commits and pushes, and avoid recording secrets, sensitive paths, or unintended project details.

## Reference(s):

- [Codifica Skill Page](https://clawhub.ai/davidedicillo/skills/codifica)
- [Codifica Homepage](https://github.com/davidedicillo/codifica)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, task-state, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Git and repository Codifica files; may produce task state updates, execution notes, artifacts, commits, and pushes when used.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
