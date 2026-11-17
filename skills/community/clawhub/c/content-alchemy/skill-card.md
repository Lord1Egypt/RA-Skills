## Description:

Turn articles, web pages, PDFs, and excerpts into structured notes, key insights, practical actions, and reusable takeaways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inf-lucas](https://clawhub.ai/user/inf-lucas)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and developers use this skill to turn plain text, web pages, and PDFs into saved notes, insights, action items, and reusable takeaways. It is especially useful for long-document reading workflows that need segmentation, checkpoints, and resumable progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The web extraction workflow can fetch URLs from the agent environment, including local or internal resources if the user provides them.

Mitigation: Avoid file://, localhost, private-network, cloud-metadata, and other sensitive internal URLs; review requested URLs before running extraction.

Risk: The --insecure option disables normal TLS verification for web extraction troubleshooting.

Mitigation: Use --insecure only with an explicitly trusted source and prefer normal HTTPS extraction otherwise.

Risk: Long-PDF reading workflows save progress and derived notes locally under ~/.content-alchemy/sessions.

Mitigation: Clear ~/.content-alchemy/sessions after working with confidential documents or avoid persistent long-PDF workflows for sensitive material.

## Reference(s):

- [Content Alchemy ClawHub Skill Page](https://clawhub.ai/inf-lucas/skills/content-alchemy)
- [Content Alchemy Feature Guide](docs/FEATURE_GUIDE.md)
- [Content Alchemy README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown notes and command guidance; helper scripts may emit JSON plans, extracted text, and saved Markdown segment or checkpoint files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long-PDF workflows may persist reading plans, state files, segment results, and checkpoint summaries under ~/.content-alchemy/sessions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
