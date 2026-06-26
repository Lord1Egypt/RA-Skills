## Description: <br>
Use when user asks about Agent architecture, design, or how an Agent works. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyxin-del](https://clawhub.ai/user/joeyxin-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent users, and learners use this skill to get plain-language explanations of agent concepts and source-backed architecture explanations for a specific agent implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture questions may cause the agent to inspect and summarize local source code, including sensitive implementation details in private projects. <br>
Mitigation: Install only where local source inspection is acceptable, and avoid asking it to inspect config, secrets, memories, profiles, or databases unless those details may be discussed. <br>


## Reference(s): <br>
- [Agent Native Speaker release page](https://clawhub.ai/joeyxin-del/agent-native-speaker) <br>
- [README](README.md) <br>
- [Harness Engineering Glossary](references/harness-engineering-glossary.md) <br>
- [Hermes Agent Architecture Map](references/hermes-agent-architecture-map.md) <br>
- [Trigger Domain Reference](references/trigger-domain-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown explanations with source file references and occasional code snippets or search commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Layer 2 architecture answers are expected to be grounded in local source-code inspection.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
