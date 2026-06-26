## Description: <br>
Distills any commercial entity into a personalized brand agent with authentic voice, declared service capabilities, a standard service contract, and support for creating brand identity from existing content or from scratch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neiljo-gy](https://clawhub.ai/user/neiljo-gy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, brand operators, and agencies use this skill to generate commercial brand-agent persona packs with declared services, customer-facing behavior guidance, A2A discoverability, and service contracts for external agent interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated brand agents may receive broad shell, file, and network authority by default. <br>
Mitigation: Before running generated agents, confirm the output directory, review overwrite behavior, and remove unnecessary shell, curl, Python, broad file access, and web access permissions unless the specific brand service requires them. <br>
Risk: ACN/A2A registration or action services such as payments, orders, and bookings can create real-world effects. <br>
Mitigation: Treat registration and state-changing commercial services as opt-in and require explicit user confirmation before execution. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/neiljo-gy/brand-persona-skill) <br>
- [Brand Persona Template](artifact/assets/brand.persona.template.json) <br>
- [Behavior Guide Template](artifact/assets/behavior-guide.template.md) <br>
- [Service Contract Template](artifact/references/SERVICE-CONTRACT.template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration, shell commands, and generated persona-pack files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a self-contained brand-agent skill directory with persona.json, SKILL.md, behavior guide, agent-card metadata, ACN configuration, and a service contract.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
