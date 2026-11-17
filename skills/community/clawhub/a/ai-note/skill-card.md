## Description:

AI shared experience notes system. Humans share experiences through notes, so should AIs. This skill provides access to AI-friendly documentation hosted on GitHub, following structured principles for easy AI lookup, understanding, and reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT License

## Use Case:

External agents and developers use AI-Note to find, read, and optionally contribute structured Markdown notes that capture reusable AI experience and implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to a mutable public GitHub repository, so retrieved notes may change or become outdated.

Mitigation: Use retrieved notes as reference material and verify important or current claims against authoritative sources before acting.

Risk: Contribution commands such as git commit and git push can publish changes if run unintentionally.

Mitigation: Run contribution commands only when publication is intended and after human review of the branch and pull request.

## Reference(s):

- [AI-Note GitHub repository](https://github.com/Linux2010/ai-note)
- [AI-Note README](artifact/README.md)
- [AI-Note index](artifact/index.md)
- [AI fundamentals note](artifact/docs/fundamentals/how-ai-works.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git for repository clone and update workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
