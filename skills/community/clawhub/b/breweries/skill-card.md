## Description: <br>
CLI for AI agents to find breweries for their humans. Uses Open Brewery DB. No auth required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to search Open Brewery DB for breweries by name, city, state, type, or random discovery and return concise brewery details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends brewery search prompts to the public Open Brewery DB API. <br>
Mitigation: Avoid submitting sensitive personal or confidential location-search context, and use the skill only when public brewery lookup is acceptable. <br>
Risk: The reviewed package does not include the executable scripts referenced by the README. <br>
Mitigation: Inspect any cloned executable files before granting execute permissions or running the commands. <br>


## Reference(s): <br>
- [Open Brewery DB](https://www.openbrewerydb.org) <br>
- [Open Brewery DB API v1](https://api.openbrewerydb.org/v1/breweries) <br>
- [Breweries ClawHub Release](https://clawhub.ai/jeffaf/breweries) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text brewery results with command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns concise brewery name, location, type, and URL when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
