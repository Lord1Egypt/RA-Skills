## Description: <br>
Instruction-only compliance checker for AI outputs that detects jailbreaks, prompt injection, regulatory issues, unsafe financial or medical advice, and privacy issues entirely within the agent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daririnch](https://clawhub.ai/user/daririnch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agent builders, LLM pipeline teams, and compliance reviewers use this skill to locally check generated text against policy checklists before delivery. It is suited for reviewing AI outputs against safety, privacy, and regulated-domain guardrails without sending text outside the agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the skill's compliance verdict as legal, medical, financial, or regulatory certification. <br>
Mitigation: Use it as a local checklist and have qualified reviewers compare the policy criteria and verdicts against the applicable requirements before relying on them. <br>
Risk: Instruction-only checklist analysis can miss context-specific issues or produce false positives. <br>
Mitigation: Apply human review for regulated or high-impact outputs, especially when the verdict affects delivery, user rights, financial decisions, or health-related content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daririnch/dcl-policy-enforcer) <br>
- [Fronesis Labs privacy policy](https://fronesislabs.com/#privacy) <br>
- [DCL Security Suite](https://hub.fronesislabs.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with a JSON verdict schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only local checklist; no network, credential, privileged access, persistence, or code execution behavior indicated by security evidence.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact text states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
