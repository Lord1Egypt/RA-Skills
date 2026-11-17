## Description:

CLI for AI agents to lookup country info for their humans. Uses REST Countries API. No auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffaf](https://clawhub.ai/user/jeffaf)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to answer country lookup questions by name, code, capital city, or region using REST Countries API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or ambiguous prompts may route to the skill when the subject is not actually a country lookup.

Mitigation: Use the skill for explicit country lookup questions and avoid automatic invocation for ambiguous city, company, person, or non-country topics.

Risk: Installation may fail if the package does not include the referenced countries executable or install source.

Mitigation: Confirm the package contents include the countries executable or install source before installing or deploying the skill.

## Reference(s):

- [REST Countries API](https://restcountries.com)
- [Countries Skill on ClawHub](https://clawhub.ai/jeffaf/skills/countries)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text command output with country summaries and detailed country fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, and bc; uses the REST Countries API without authentication.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
