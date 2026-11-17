## Description:

Open a browser tab so a human can highlight-and-comment on a Markdown file, then return structured comments that an agent can read and address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxl-lxz](https://clawhub.ai/user/zxl-lxz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Commentmd to collect targeted human feedback on generated Markdown documents, then revise the document using the returned structured comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill expects a local serve.py script that is not present in the reviewed artifact.

Mitigation: Install only from a package that includes the expected server script, or inspect and trust the local server implementation before running the workflow.

Risk: Opening a local review browser can expose the Markdown document to local tooling and user interaction.

Mitigation: Use the workflow only for documents appropriate for local review, and get explicit user approval before opening the review browser or static review page.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zxl-lxz/skills/commentmd)
- [Server-Resolved GitHub Provenance](https://github.com/zxl-lxz/commentmd/tree/main/skills/commentmd)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown instructions with shell commands and structured JSON comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The review output records highlighted quotes, anchor context, human comments, timestamps, comment count, and whether the Markdown file changed during review.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
