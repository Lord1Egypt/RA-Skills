## Description:

Browse Bring! recipe inspirations, recipe metadata, images, links, and tags from the CLI, with JSON output for scripting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkdevelopers](https://clawhub.ai/user/darkdevelopers)

### License/Terms of Use:


## Use Case:

External Bring! users and developers use this skill to discover recipe inspirations, inspect recipe metadata, filter all or personal recipes, and obtain JSON output for scripting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Bring account credentials, including a password, for recipe browsing.

Mitigation: Set BRING_EMAIL and BRING_PASSWORD only for the current terminal session, avoid committing them to files, and do not store the password in shared shell profiles or logs.

Risk: Users may expect ingredient lists or shopping-list changes that the Bring! Inspirations API does not provide.

Mitigation: Use the skill only for browsing recipe metadata and manually add needed items to a shopping list.

## Reference(s):

- [Bring Recipes on ClawHub](https://clawhub.ai/darkdevelopers/skills/bring-recipes)
- [darkdevelopers ClawHub profile](https://clawhub.ai/user/darkdevelopers)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browse-only; recipe ingredient lists are not provided by the Bring! Inspirations API.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
