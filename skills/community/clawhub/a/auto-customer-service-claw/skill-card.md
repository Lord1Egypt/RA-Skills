## Description: <br>
自动客服应答虾 helps an agent configure and operate an automated customer-service reply system with intent classification, FAQ matching, human handoff rules, and conversation management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and customer-support operators use this skill to configure FAQ content, intent rules, response templates, and service commands for automated replies across support channels. It is intended for customer inquiry triage, routine answer generation, and escalation to human support for sensitive or unresolved cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive customer conversations and conversation logs. <br>
Mitigation: Define privacy rules before deployment, including what customer data is logged, retention limits, access controls, and deletion procedures. <br>
Risk: The bundled service script can expose a local web service without built-in authentication. <br>
Mitigation: Bind the service to localhost or place it behind authentication and network controls before use in a live support environment. <br>
Risk: Knowledge-base import and service-control commands can modify live support behavior. <br>
Mitigation: Require operator review or confirmation before importing FAQ data, reloading knowledge, or changing a running support service. <br>


## Reference(s): <br>
- [FAQ 知识库](references/faq-database.md) <br>
- [意图识别规则](references/intent-rules.md) <br>
- [回复话术库](references/response-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and customer-service response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service management commands, FAQ import/export guidance, and generated customer reply text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
