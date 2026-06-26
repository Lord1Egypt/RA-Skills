## Description: <br>
Use AICADE Galaxy on https://www.aicadegalaxy.com/ to discover and invoke platform tools for AI monetization, paid APIs, subscriptions, memberships, blockchain-based payments with AicadePoint, and reward-earning workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shifenghu](https://clawhub.ai/user/shifenghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover AICADE Galaxy gateway tools, configure access, export the current tool artifact, and invoke paid or token-related platform services through Node.js or Python commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and sensitive payment-related request data can be exposed in logs, especially when debug output is enabled. <br>
Mitigation: Keep AICADE_GALAXY_DEBUG disabled when using real credentials or sensitive requests, and avoid sharing command logs that include request data. <br>
Risk: Bootstrap or setup can rewrite a local .env file. <br>
Mitigation: Review any existing .env before running bootstrap and keep credential files out of source control. <br>
Risk: Invoking an unintended exported artifact could call the wrong AICADE Galaxy endpoint or service. <br>
Mitigation: Invoke only artifacts exported from the intended AICADE Galaxy endpoint and review the listed tools before use. <br>


## Reference(s): <br>
- [AICADE Galaxy](https://www.aicadegalaxy.com/) <br>
- [ClawHub skill page](https://clawhub.ai/shifenghu/aicade-galaxy-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and normalized JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use a generated AICADE Galaxy artifact and args files to list or invoke platform tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
