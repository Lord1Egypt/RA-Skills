## Description:

Use the cochesnet CLI to search coches.net listings and fetch listing details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjtf93](https://clawhub.ai/user/pjtf93)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to look up coches.net vehicle marketplace listings from the terminal, fetch listing details by ad ID, and request JSON output for scripting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a separately installed cochesnet-cli package.

Mitigation: Verify the CLI package and its source before using the skill.

Risk: Search queries and listing IDs may be sent to coches.net.

Mitigation: Avoid sensitive search terms and use the skill only where sharing those requests with coches.net is acceptable.

## Reference(s):

- [Cochesnet Cli on ClawHub](https://clawhub.ai/pjtf93/skills/cochesnet-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI can return table output or JSON, with non-zero exit codes on failure.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
