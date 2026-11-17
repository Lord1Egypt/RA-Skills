## Description:

Resolves arXiv paper links by downloading PDFs, extracting metadata and section text from arXiv HTML, and guiding an agent to assemble a Chinese Markdown document following the paper's own structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jin-liquor](https://clawhub.ai/user/jin-liquor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to process arXiv papers into local paper folders and Chinese Markdown study documents. It is intended for paper reading workflows where an agent should preserve formulas, skip references or appendices, and organize extracted sections before translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads arXiv PDFs and HTML and writes extracted paper artifacts to local storage.

Mitigation: Run it as a normal user account, choose the output directory intentionally, and review downloaded and generated files before sharing or reusing them.

Risk: Network and file handling have hardening gaps for sensitive or internal-network environments.

Mitigation: Pin dependencies and add PDF host and size validation before using the skill in sensitive environments.

Risk: arXiv HTML is experimental and format changes can cause incomplete or incorrect section extraction.

Mitigation: Review the generated section structure and raw section files before relying on the translated Markdown output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jin-liquor/skills/arxiv-paper-resolver)
- [Publisher profile](https://clawhub.ai/user/jin-liquor)
- [arXiv](https://arxiv.org/)
- [Python](https://www.python.org/)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus local PDF, JSON metadata, section text files, and a final Chinese Markdown document.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to a user-selected output directory; generated Markdown is expected to preserve LaTeX formulas and avoid HTML anchor tags.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
