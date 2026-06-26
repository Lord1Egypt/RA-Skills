## Description: <br>
The AEIF-based long-term memory hub for AI Agents to prevent repeating bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[404-UNKNOW](https://clawhub.ai/user/404-UNKNOW) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to consult and persist reusable troubleshooting experience across AI-agent sessions. It can retrieve prior fixes for recurring errors and distill successful session history into AEIF memory capsules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist troubleshooting context and distilled session history across sessions. <br>
Mitigation: Avoid enabling auto-commit for sessions containing secrets, private code, credentials, customer data, or sensitive operational details; review stored capsules before reuse. <br>
Risk: Distillation and verification may process recent conversation history through a configured LLM. <br>
Mitigation: Use only with an approved LLM configuration and avoid committing sensitive conversations. <br>
Risk: Auto-injected advice may influence future agent behavior without a fresh human review. <br>
Mitigation: Review EvoMap advice before applying patches, configuration changes, or workarounds. <br>
Risk: A bundled high-trust seed recommends globally disabling Git SSL verification. <br>
Mitigation: Review or remove the Git SSL seed before use and prefer certificate-store fixes over disabling verification globally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/404-UNKNOW/engram-evomap) <br>
- [Publisher profile](https://clawhub.ai/user/404-UNKNOW) <br>
- [Engram Cloud waitlist](https://404-unknow.github.io/Engram/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown advice with actionable patch, configuration, or workaround steps; stored memories use AEIF JSON capsules.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inject EvoMap advice into the agent context and may persist distilled session history as local memory capsules.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
