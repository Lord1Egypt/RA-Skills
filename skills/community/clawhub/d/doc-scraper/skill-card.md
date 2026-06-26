## Description: <br>
Documentation extraction and indexing. Extracts information from markdown files and syncs to workspace-db. Works alongside workspace-db which handles synchronization and organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to extract structured information from Markdown documentation, index it into docs.db, and keep documentation data searchable alongside workspace-db workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad local Markdown watching and persistent indexing without clear limits or cleanup controls. <br>
Mitigation: Use narrow trusted folders, avoid watching an entire mixed workspace, review files before recursive indexing, and confirm how indexed data can be cleared or excluded. <br>


## Reference(s): <br>
- [Doc Scraper on ClawHub](https://clawhub.ai/kikikari/doc-scraper) <br>
- [workspace-db Skill](https://clawhub.com/skills/workspace-db) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, YAML, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe indexing, watch, search, and workspace-db integration workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
