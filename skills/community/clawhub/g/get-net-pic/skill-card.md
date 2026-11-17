## Description:

Fetches image resources from a public website homepage and organizes the downloaded images into a DOCX document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavindu223](https://clawhub.ai/user/gavindu223)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect publicly accessible homepage images, preview the downloaded files, and assemble them into a Word document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch arbitrary website content and download page-referenced images.

Mitigation: Use it only on public sites you trust, avoid internal or authenticated URLs, and confirm the target URL before fetching or downloading content.

Risk: The workflow writes downloaded images and generated DOCX files to the Desktop.

Mitigation: Confirm the destination folder and expected file count before running download or document-generation commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with PowerShell and JavaScript code blocks that produce downloaded image files and a DOCX document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local Desktop image folders and DOCX files; intended for public, unauthenticated websites.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
