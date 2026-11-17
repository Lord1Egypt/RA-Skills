## Description:

Analyze the structure and content of .docx (Word) files using MinerU, returning structured Markdown that preserves headings, tables, lists, and layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Content reviewers, editors, developers, and agents use this skill to inspect Word document structure and extract Markdown views of headings, tables, lists, and layout. It supports quick MinerU analysis without a token and full token-backed analysis for more complex documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party mineru-open-api CLI installation.

Mitigation: Install the CLI in an isolated environment and pin or review the package before use where possible.

Risk: Full analysis requires MINERU_TOKEN and may process document contents through MinerU tooling.

Mitigation: Protect MINERU_TOKEN and avoid sensitive documents until the CLI's data handling and token storage behavior are understood.

## Reference(s):

- [Docx Analysis on ClawHub](https://clawhub.ai/mzlzyca/skills/docx-analysis)
- [MinerU](https://mineru.net)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce stdout Markdown from MinerU or file and directory outputs when the CLI is invoked with -o.]

## Skill Version(s):

0.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
