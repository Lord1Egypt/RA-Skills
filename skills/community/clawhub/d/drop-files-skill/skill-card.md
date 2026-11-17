## Description:

Upload generated HTML/Markdown files to DropFiles and get a shareable public link. Invoke when the user wants to share, publish, or generate a public link for any HTML or Markdown content they produced.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icexun](https://clawhub.ai/user/icexun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish generated HTML or Markdown artifacts through DropFiles and return a shareable URL, with optional expiry and password protection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated links may make uploaded HTML or Markdown publicly accessible to anyone with the URL.

Mitigation: Use the skill only for content intended to be shared publicly, avoid secrets or regulated data, and enable password protection when access should be limited.

Risk: Agents can accidentally upload internal-only documents to a third-party sharing service.

Mitigation: Review the content before upload and confirm that use of the DropFiles service is appropriate for the document.

## Reference(s):

- [Server-resolved source repository](https://github.com/icexun/drop-files-skill)
- [ClawHub skill listing](https://clawhub.ai/icexun/skills/drop-files-skill)
- [DropFiles web interface](https://dropfiles.tokendealhub.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text containing DropFiles URLs, preview URLs, expiry details, passwords when generated, and error guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads support HTML or Markdown content up to 5 MB with expiry options from 1 hour to 30 days.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
