## Description:

Use when running the OpenClaw/ClawHub Bring! skill to search recipes on the web, parse recipe URLs for ingredients, and add ingredients to a Bring shopping list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dolverin](https://clawhub.ai/user/dolverin)

### License/Terms of Use:


## Use Case:

External users use this agent skill to find German recipe ideas, inspect recipe ingredients, manage Bring shopping lists, and add selected recipe ingredients after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bring account credentials or account tokens could be exposed through weaker credential handling.

Mitigation: Provide Bring credentials through protected environment variables or a secret manager and avoid passing passwords as command-line arguments.

Risk: The content URL workflow can fetch arbitrary URLs supplied to --content-url.

Mitigation: Only use official Bring template-content URLs and review or restrict the --content-url behavior before installation.

Risk: Shopping-list modification commands can add items to a user's Bring account.

Mitigation: Require explicit user confirmation before adding recipe ingredients or other items to a list.

Risk: Runtime dependency changes could affect security or behavior.

Mitigation: Install with the committed package-lock.json lockfile.

## Reference(s):

- [Bring Inspirations API Reference](references/bring-inspirations.md)
- [ClawHub Skill Page](https://clawhub.ai/dolverin/skills/bring-rezepte)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with concise text, JSON summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [German user-facing recipe and shopping-list guidance by default; list changes require explicit user confirmation.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
