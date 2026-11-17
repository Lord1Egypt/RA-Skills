## Description:

Capture fleeting ideas in local daily Markdown files, with divider-separated entries and quick add and search commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bosichong](https://clawhub.ai/user/bosichong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to quickly record, search, and review personal idea fragments or lightweight notes without leaving an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local flash thoughts are stored as plaintext Markdown and may contain sensitive personal notes.

Mitigation: Use a private notes directory and avoid recording secrets or regulated data.

Risk: Security evidence reports that a crafted date argument can read Markdown files outside the note folder.

Mitigation: Validate date inputs and avoid using the show command with untrusted instructions until the issue is fixed.

Risk: Search uses user-provided patterns across local note files.

Mitigation: Treat search terms from untrusted sources cautiously and review matches before sharing note contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bosichong/skills/flash-thoughts)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, command-line confirmations, and text search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads local plaintext note files in the configured flash-thoughts directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
