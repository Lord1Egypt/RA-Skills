## Description:

Creates Google Docs from Markdown by converting content to DOCX and uploading it through gog and Google Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techlaai](https://clawhub.ai/user/techlaai)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill when they need an agent to create an editable Google Doc from Markdown content through an authenticated gog workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can run an unverified Pandoc converter from a predictable /tmp path.

Mitigation: Install Pandoc through a trusted package manager, or require checksum verification and a user-owned cache path before running the script.

Risk: Selected Markdown content is uploaded to Google Drive through the user's authenticated gog account.

Mitigation: Use the skill only for content intended to be uploaded to that Google account, and review files before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/techlaai/skills/gdocs-markdown)
- [Pandoc 3.1.11 Linux AMD64 release archive](https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-linux-amd64.tar.gz)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown instructions with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a DOCX conversion and Google Drive upload workflow that returns a Google Docs link.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
