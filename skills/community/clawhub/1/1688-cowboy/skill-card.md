## Description: <br>
A 1688 merchant reception-assistant skill that helps agents hire and manage the preset reception assistant, view daily reports, inspect transferred inquiries, manage knowledge, run simulated replies, and configure required AK credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
1688 merchants and their agents use this skill in the Newton chat entry point to onboard a preset AI reception assistant, review reception performance, inspect human-transfer inquiries, maintain knowledge answers, and route post-hire configuration changes to the reception management page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles AK credentials and 1688 merchant, customer, order, conversation, and knowledge data. <br>
Mitigation: Install only for trusted publishers, verify the configured gateway, protect the OpenClaw configuration file, and review the store-data authorization scope before use. <br>
Risk: The scanner marked the release suspicious because credential handling, cloud knowledge persistence, and local-folder syncing need review. <br>
Mitigation: Review the security summary and disclosure before enabling the skill, and use dedicated folders for knowledge sync rather than broad local directories. <br>
Risk: Configuration and knowledge-write operations can change merchant-facing assistant behavior. <br>
Mitigation: Use the built-in confirmation flow for sensitive commands and route post-hire reception changes through the management page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-cowboy) <br>
- [Publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [OpenClaw runtime requirement](artifact/SKILL.md) <br>
- [Interaction specifications](artifact/references/interaction-specs.md) <br>
- [Configuration command reference](artifact/references/capabilities/configure.md) <br>
- [Reception configuration reference](artifact/references/capabilities/cowboy_config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses, JSON command results, and interaction-card guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and may require AK credentials for authenticated 1688 gateway operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
