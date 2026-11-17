## Description:

Formats a manuscript into a 5.5" x 8.5" printed paperback and a Kindle ebook, generating a cover page, table of contents, headers, and an About the Author section.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vega6dev](https://clawhub.ai/user/vega6dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and publishing-focused agents use this skill to turn a raw text or Markdown manuscript into print-ready paperback and Kindle ebook deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates files and may run local manuscript conversion commands.

Mitigation: Run it in the intended workspace, review generated commands before execution, and confirm output paths before sharing or publishing files.

Risk: Paperback and ebook formatting can be wrong if required local tools are missing or misconfigured.

Mitigation: Confirm python3 and pandoc are installed and inspect the generated PDF, DOCX, and EPUB before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vega6dev/skills/format-book)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with local code and shell commands that produce PDF, DOCX, and EPUB files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces named paperback and Kindle ebook files in the user's working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
