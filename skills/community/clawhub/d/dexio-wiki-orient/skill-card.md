## Description:

Guides an agent to read a shared wiki's schema, page catalog, recent changes, and relevant pages before answering questions or making edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexio](https://clawhub.ai/user/dexio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents maintaining a shared Markdown wiki use this skill to find the relevant page and current conventions before relying on or changing wiki content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect the wrong wiki or hosted workspace.

Mitigation: Confirm the intended wiki path or hosted wiki tool before reading or editing.

Risk: Wiki notes about mutable systems may be outdated.

Mitigation: Check the original source before acting on prices, configurations, account state, or current roles.

## Reference(s):

- [Wiki Orient (Dexio) on ClawHub](https://clawhub.ai/dexio/skills/dexio-wiki-orient)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies the canonical wiki page and relevant recent changes; does not itself produce a wiki update.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
