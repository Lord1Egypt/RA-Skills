## Description: <br>
Brickset provides human-friendly Brickset API v3 access for LEGO set lookup, catalog browsing, usage inspection, instructions, images, and automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, builders, and agents use this skill to search LEGO sets, browse Brickset catalog metadata, fetch instructions or image links, inspect API usage, and automate Brickset API workflows with JSON or text output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Brickset API key and can use account-linked Brickset operations. <br>
Mitigation: Install only when the agent is expected to use the Brickset API key, and keep the key scoped through environment or workspace configuration. <br>
Risk: Raw API mode can invoke login, userHash, getCollection, or collection-management methods that may expose or change account-linked collection data. <br>
Mitigation: Prefer the wrapped lookup commands, and review any raw call involving account or collection-management methods before execution. <br>


## Reference(s): <br>
- [Brickset API v3 quick reference](references/api.md) <br>
- [Brickset API v3 endpoint](https://brickset.com/api/v3.asmx) <br>
- [ClawHub Brickset release page](https://clawhub.ai/stanestane/brickset) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON or plain text summaries from Brickset API calls, plus Markdown command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRICKSET_API_KEY or an explicit API key argument; raw API calls may include account-linked parameters.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
