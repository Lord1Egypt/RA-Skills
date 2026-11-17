## Description:

Doc Export organizes solved conversation issues into Markdown solution documents and publishes them to a web server for user download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binyuli](https://clawhub.ai/user/binyuli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to turn resolved conversation content into a downloadable Markdown guide with background, steps, examples, and common questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived documents may expose secrets or personal data if published to the configured public web domain.

Mitigation: Redact sensitive content and require explicit approval before publishing any generated document.

Risk: Public web copies and retained archive copies may remain accessible longer than intended.

Mitigation: Use private or expiring links where possible and define cleanup for both the public web copy and archived source document.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binyuli/skills/doc-export)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown document and HTTPS download link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents may be copied to a public web directory and retained in a local archive.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
