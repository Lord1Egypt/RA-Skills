## Description:

CLI for AI agents to find breweries for their humans. Uses Open Brewery DB. No auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffaf](https://clawhub.ai/user/jeffaf)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to search Open Brewery DB for breweries by name, city, state, type, or random suggestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact contains documentation but not the executable brewery lookup scripts referenced by the installation instructions.

Mitigation: Install only from a pinned, reviewed commit or a release package that includes the executable scripts and verifies their integrity.

Risk: The skill depends on local shell tools and live network calls to Open Brewery DB.

Mitigation: Confirm bash, curl, and jq are available, and review outbound API use before enabling the skill in restricted environments.

## Reference(s):

- [Open Brewery DB](https://www.openbrewerydb.org)
- [Open Brewery DB API v1](https://api.openbrewerydb.org/v1/breweries)
- [ClawHub Skill Page](https://clawhub.ai/jeffaf/skills/breweries)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jeffaf)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Brewery results are described concisely with name, location, brewery type, and URL when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
