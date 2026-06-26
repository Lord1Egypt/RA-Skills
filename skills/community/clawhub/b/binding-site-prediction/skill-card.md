## Description: <br>
Binding-site and pocket prediction workflows using P2Rank, AF2BIND, and fpocket through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational biologists, and structure-based design teams use this skill to predict and compare likely ligand-binding pockets from protein structures or supported identifiers before docking, screening, or mutational analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on live remote Markdown documentation to shape SciMiner API invocation code while using an API credential and possible file uploads. <br>
Mitigation: Review the selected SciMiner documentation before use, keep the API key scoped and stored only in the documented credentials file, and run only the minimal API request needed for the selected tool. <br>
Risk: Protein structure inputs and API-authenticated requests are sent to SciMiner. <br>
Mitigation: Use the skill only when sharing the relevant structure inputs with SciMiner is acceptable, and avoid submitting sensitive or restricted structures unless permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sciminer/binding-site-prediction) <br>
- [SciMiner tool API files](https://sciminer.tech/tool_api_files/) <br>
- [P2Rank API documentation](https://sciminer.tech/tool_api_files/p2rank_api_doc.md) <br>
- [AF2BIND API documentation](https://sciminer.tech/tool_api_files/af2bind_api_doc.md) <br>
- [fpocket API documentation](https://sciminer.tech/tool_api_files/fpocket_api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API calls, Text] <br>
**Output Format:** [Markdown guidance with inline code or shell commands, SciMiner API request details, result summaries, task IDs, and share URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SciMiner credential file, may upload protein structure inputs, and polls long-running tasks for up to 600 seconds before returning the task ID and share URL.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
