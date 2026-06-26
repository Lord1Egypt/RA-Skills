## Description: <br>
DCL Prompt Firewall is an instruction-only prompt-screening skill that checks untrusted inputs for prompt injection, jailbreaks, role-switch attacks, instruction overrides, token smuggling, indirect injection, social engineering, and context overflow before an agent or LLM acts on them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daririnch](https://clawhub.ai/user/daririnch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of AI agents and LLM pipelines use this skill to screen user-supplied or external prompt content before it reaches a model, producing a local checklist-based verdict and findings for risky instruction patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the instruction-only checklist as a technical enforcement boundary. <br>
Mitigation: Use it as a prompt-screening aid and review any real logging, blocking, or pipeline integration separately before deployment. <br>
Risk: Screening quality depends on the agent applying the checklist consistently to the supplied input. <br>
Mitigation: Review findings for high-impact workflows and keep downstream policy, redaction, secret scanning, and output-sanitization controls in place where required. <br>


## Reference(s): <br>
- [DCL Prompt Firewall on ClawHub](https://clawhub.ai/daririnch/dcl-prompt-firewall) <br>
- [Fronesis Labs Privacy Policy](https://fronesislabs.com/#privacy) <br>
- [DCL Security Suite Hub](https://hub.fronesislabs.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON-style screening report with verdict, risk score, findings, checked categories, and clear categories] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as an instruction-only local checklist; no code execution, install steps, credentials, persistence, or data transmission are requested by the artifact.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
