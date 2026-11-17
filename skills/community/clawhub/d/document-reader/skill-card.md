## Description:

Document Reader extracts text from PDF, DOCX, XLSX, PPTX, RTF, ODT, HTML, plain text, and selected files inside common archives for agent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaliu00](https://clawhub.ai/user/xiaoyaliu00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use this skill to read common office documents, text files, and files stored inside archives so the extracted content can be analyzed or processed by an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archive handling and document extraction can expose the agent environment to untrusted or oversized files.

Mitigation: Use the skill only on files the user intends the agent to read, avoid untrusted oversized archives, and review extracted content before relying on it.

Risk: The documented dependency installation command can install packages system-wide.

Mitigation: Install dependencies in an isolated virtual environment or container before running the document reader.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text or JSON emitted by a command-line document reader, with Markdown documentation and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can list archive contents or read a specified file from an archive; long text output may be truncated in human-readable mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
