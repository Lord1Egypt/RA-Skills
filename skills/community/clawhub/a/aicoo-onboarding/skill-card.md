## Description:

Guides first-time Aicoo users through obtaining an API key, initializing a workspace, syncing selected context, discovering people, creating an agent share link, and posting to Aicoo Square.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to complete first-time Aicoo setup and become discoverable through an agent link and Square post. It helps an agent guide onboarding, propose API calls, create local identity files, and draft sharing or posting actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The onboarding flow can upload selected local project and profile information to Aicoo.

Mitigation: Review the exact files and notes before sync, exclude secrets, customer data, private notes, broad folders, Git history, and memory files unless the user explicitly approves them.

Risk: The sharing flow can create broad read-access agent links and make the user discoverable through public or social actions.

Mitigation: Prefer narrow folder-scoped links, require sign-in when appropriate, avoid all-scope sharing unless intentional, and review the generated Square post before publishing.

Risk: The setup guidance shows API keys in shell commands and mentions shell startup persistence.

Mitigation: Use a secret store or scoped environment injection where possible, avoid committing keys to files, and rotate any exposed key.

## Reference(s):

- [Aicoo Onboarding Skill Page](https://clawhub.ai/xisen-w/skills/aicoo-onboarding)
- [Aicoo API Key Settings](https://www.aicoo.io/settings/api-keys)
- [First-Time Setup Example](examples/first-time-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline bash and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce curl commands, suggested local files, share links, Square post drafts, and onboarding summaries.]

## Skill Version(s):

2.0.0 (source: server release evidence; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
