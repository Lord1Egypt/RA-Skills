## Description:

Provides Chinese-first email draft generation, reply suggestions, template-based writing, tone adjustment, subject suggestions, and simple email record statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to draft common work, business, personal, job-search, and finance-related emails in Chinese or English and adjust tone before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated email drafts may include placeholders, incorrect assumptions, or wording that is unsuitable for the recipient.

Mitigation: Review each draft, replace placeholders, and verify facts, recipients, tone, and attachments before sending.

Risk: Saved email records may contain confidential email content in local JSON files.

Mitigation: Avoid saving sensitive email bodies unless local storage has been reviewed, and delete saved records when they are no longer needed.

Risk: Broad email prompts may cause the skill to draft or classify messages from incomplete context.

Mitigation: Provide only the minimum necessary context and check the generated category or draft before acting on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cp3d1455926-svg/skills/email-helper)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted email drafts, suggestions, templates, and brief statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts may include placeholders that the user should replace before sending.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
