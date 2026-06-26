## Description: <br>
Connects agents to the AlphaPai/PaiPai financial research API for investment Q&A, RAG data retrieval, stock research agents, announcement lookup, and chart search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boteeenchan-ship-it](https://clawhub.ai/user/boteeenchan-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External financial research users and developers use this skill to call AlphaPai/PaiPai APIs for market research questions, source-data retrieval, stock and industry research workflows, announcement lookup, and chart discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The submitted artifact includes a plaintext API key in config.json. <br>
Mitigation: Remove the bundled key before installation and configure a user-owned credential securely with the provided config command. <br>
Risk: The skill includes a remote self-upgrade flow that can replace local files. <br>
Mitigation: Avoid the self-upgrade flow unless the update source and resulting file changes have been independently verified. <br>
Risk: Queries and contextual data are sent to AlphaPai/Rabyte. <br>
Mitigation: Use the skill only with data the user is comfortable sending to that third-party service. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/boteeenchan-ship-it/alphapai-research) <br>
- [AlphaPai Open API reference](references/api_reference.md) <br>
- [AlphaPai API service endpoint](https://open-api.rabyte.cn) <br>
- [AlphaPai install and update document](https://open-api.rabyte.cn/alpha/open-api/v1/file/api-docs/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON returned from AlphaPai API calls, with shell commands for CLI usage and configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to preserve AlphaPai response formatting and references, and supports optional raw JSON output for API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
