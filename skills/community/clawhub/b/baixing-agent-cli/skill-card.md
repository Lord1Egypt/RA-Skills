## Description: <br>
Installs and uses the baixing-agent-cli npm package to help agents run Baixing CLI workflows for UUID setup, category discovery, category metadata lookup, posting, listing, search, and detail retrieval from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to install and invoke baixing-agent-cli for Baixing classifieds workflows, especially category-aware post preparation, dry-run review, live posting, and reading resulting listings or search details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to submit real Baixing classifieds listings, which may publish incorrect contact details, prices, locations, or category metadata if the agent acts without user review. <br>
Mitigation: Require the agent to show the final listing payload or dry-run output and obtain explicit user confirmation before any live post command. <br>
Risk: The security summary notes missing clear safeguards around live publication, user data, and fabricated required fields. <br>
Mitigation: Do not allow the agent to invent contact numbers, prices, locations, or other required fields for live submissions; ask the user for missing required values. <br>


## Reference(s): <br>
- [Baixing Agent CLI npm package](https://www.npmjs.com/package/baixing-agent-cli) <br>
- [Baixing website](https://www.baixing.com) <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/baixing-agent-cli) <br>
- [Publisher profile](https://clawhub.ai/user/tujinsama) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and CLI output-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to parse stdout JSON, inspect stderr on failure, and rely on process exit codes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
