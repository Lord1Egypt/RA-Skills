## Description:

This skill generates interactive Gaokao English vocabulary frequency grading webpages that classify words and phrases by exam frequency with mastery tags, warning notes, search, filters, and a responsive dark-themed layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xpscene-ux](https://clawhub.ai/user/xpscene-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and educators use this skill to produce browser-based study tools for Chinese Gaokao English preparation from structured vocabulary data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages may be unsafe to publish if they use untrusted vocabulary data before validation and escaping are confirmed.

Mitigation: Use trusted vocabulary sources, validate counts and required fields, and confirm HTML escaping before hosting generated pages.

Risk: The generator converts JSONL input into JavaScript data, so malformed entries can produce incomplete or misleading study content.

Mitigation: Run the documented data integrity checks for required fields, mastery labels, null values, and non-empty frequency levels before release.

## Reference(s):

- [HTML Template Structure](artifact/references/template_structure.md)
- [ClawHub Skill Page](https://clawhub.ai/xpscene-ux/skills/gaokao-english-vocabulary)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JavaScript, and Python code outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a browser page and external vocabulary data file for local use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
