## Description: <br>
Use the cochesnet CLI to search coches.net listings and fetch listing details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjtf93](https://clawhub.ai/user/pjtf93) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, automation users, and marketplace researchers use this skill to get the exact cochesnet CLI commands for searching coches.net listings, fetching listing details, and requesting JSON output for scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local `cochesnet` command, so a user could run an unintended executable if their PATH is misconfigured. <br>
Mitigation: Confirm the installed `cochesnet` CLI is the intended package before running generated commands. <br>
Risk: Search queries and listing IDs may be sent to the configured coches.net endpoint. <br>
Mitigation: Avoid submitting sensitive search terms or identifiers unless sharing them with the configured endpoint is acceptable. <br>


## Reference(s): <br>
- [Cochesnet Cli on ClawHub](https://clawhub.ai/pjtf93/cochesnet-cli) <br>
- [coches.net API endpoint](https://apps.gw.coches.net) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced CLI can return table output or JSON for search results and listing details.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
