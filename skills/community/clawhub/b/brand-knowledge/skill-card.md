## Description:

Brand Knowledge helps agents create, store, query, switch, and check brand profiles for slogans, visual standards, tone, and messaging templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain brand knowledge for content creation and customer-facing responses. It supports brand profile creation, lookup, active-brand switching, and pre-publication consistency checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand names containing path-like characters could cause profile creation or switching to address files outside the intended brand data folder.

Mitigation: Validate and sanitize brand names before use, reject path separators and traversal patterns, and use only trusted brand names until the path handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/brand-knowledge)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces brand profile records, query results, active-brand state, and consistency-check scores with suggested revisions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
