## Description: <br>
Create and configure custom agents in Microsoft Copilot Studio via a guided web app process, including triggers, knowledge, tools, topics, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SaikiranParamkusham09](https://clawhub.ai/user/SaikiranParamkusham09) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and makers use this skill to plan, create, configure, test, and publish Microsoft Copilot Studio agents. It is most useful when setting up agent basics, topics, knowledge sources, triggers, Power Automate tools, authentication, and publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copilot Studio agents and connected flows can expose sensitive knowledge sources or run with maker credentials. <br>
Mitigation: Review knowledge sources, connections, and author-versus-user credential behavior for least privilege before publishing. <br>
Risk: Event triggers can cause unintended autonomous actions or recurring billing impact. <br>
Mitigation: Validate trigger payloads, action scope, trigger frequency, and billing expectations, then monitor activity after publishing. <br>
Risk: Power Automate tools can perform actions across Microsoft services when connected to an agent. <br>
Mitigation: Test tools in a controlled environment, confirm inputs and outputs, and review run-only permissions before enabling production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SaikiranParamkusham09/copilot-studio-agent) <br>
- [Microsoft Learn: Create an agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-first-bot) <br>
- [Microsoft Learn: Build initial agent training](https://learn.microsoft.com/en-us/training/modules/create-copilots-copilot-studio/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with step-by-step instructions, tables, links, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no files, scripts, or executable code are generated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
