## Description:

Helps agents use the a7w.cn AI plugin market to discover and call image, video, audio, digital-human, editing, voice, music, and document QA creation APIs through one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and content operations teams use this skill to inspect available a7w.cn AI creation plugins, configure an API key, and run image, video, audio, digital-human, editing, and document workflows from an agent or command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, optional uploaded files, document URLs, and API credentials are sent to the third-party a7w.cn service.

Mitigation: Install and use the skill only when that data sharing is acceptable for the intended workload.

Risk: API key exposure can reveal account access and paid balance.

Mitigation: Use environment variables or the chmod-protected login file, avoid committing keys or pasting them into shared shell history, and rotate the key if exposure is suspected.

Risk: Voice samples, likenesses, documents, and other media can raise consent, rights, or privacy issues.

Mitigation: Submit only content the user has rights and consent to process, and review generated content before publication.

Risk: Repeated asynchronous task submissions may create duplicate charges.

Mitigation: Record task IDs, query task status before resubmitting, and monitor account charges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2253128/skills/aigc-market)
- [AI plugin market](https://aigc.a7w.cn/)
- [a7w API and compute marketplace](https://api.a7w.cn/)
- [Complete plugin and API catalog](references/catalog.md)
- [Getting started: registration, billing, and API key setup](references/getting-started.md)
- [Plugin selection guide](references/选型指南.md)
- [General usage, async task, permission, and billing notes](references/通用说明.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and curl command examples; bundled scripts can return JSON results from the a7w.cn API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided A7W_API_KEY or local a7w configuration; some workflows save JSON or generated media only when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
