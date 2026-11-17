## Description:

Compresses natural language memory files such as CLAUDE.md, todos, and preferences into a shorter format while preserving technical substance, code, URLs, and structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyafeichina](https://clawhub.ai/user/liyafeichina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to reduce token usage in natural language memory files while keeping technical details, code blocks, paths, URLs, headings, and list structure intact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected file content is sent to Anthropic or the authenticated Claude CLI.

Mitigation: Use the skill only on files approved for that data boundary, and avoid notes containing secrets, tokens, personal data, or confidential project details.

Risk: Successful compression overwrites the target file.

Mitigation: Confirm the exact target path before running the skill and retain the generated .original.md backup for review or restoration.

Risk: Compression can alter prose in ways that change meaning despite preservation checks.

Mitigation: Review the compressed output against the backup, especially for requirements, instructions, and technical decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyafeichina/skills/file-compress-optimizer)
- [Publisher profile](https://clawhub.ai/user/liyafeichina)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or text file rewrite with CLI status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful compression overwrites the selected file after writing a .original.md backup; validation retries preserve code blocks, inline code, URLs, headings, and paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
