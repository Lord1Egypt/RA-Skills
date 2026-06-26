## Description: <br>
Native security prompts and best practices to instantly make your OpenClaw instance safer without relying on 3rd party APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sooyoon-eth](https://clawhub.ai/user/sooyoon-eth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add prompt-based runtime guardrails that help agents evaluate supply-chain risk, indirect prompt injection, exfiltration attempts, tool use, and jailbreak-style requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-based guardrails can influence refusal behavior and may be over- or under-inclusive for a local agent's policy needs. <br>
Mitigation: Review SKILL.md before relying on the skill and tune local agent configuration to match the deployment's security policy. <br>
Risk: Some documentation references files that are not present in this release. <br>
Mitigation: Treat SKILL.md and the packaged files as the installable source of truth, and verify any referenced auxiliary guidance exists before depending on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sooyoon-eth/failsafe-secureclaw) <br>
- [Failsafe homepage](https://getfailsafe.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown guidance and prompt instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only skill with no executable code or network behavior.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter, package.json, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
