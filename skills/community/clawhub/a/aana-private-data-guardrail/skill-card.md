## Description: <br>
AANA Private Data Guardrail Skill helps agents minimize, redact, and safely handle private account, billing, payment, health, legal, personal, and sensitive business data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to review drafts, summaries, tickets, exports, and other content before revealing, storing, or forwarding private data. It helps keep sensitive details necessary, authorized, minimized, and redacted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive data could be exposed if an external checker is configured to receive raw secrets, full payment details, health records, legal records, or unrelated private messages. <br>
Mitigation: Use only trusted user- or administrator-approved checkers, and send redacted summaries rather than raw sensitive records. <br>
Risk: Privacy-sensitive responses may still reveal unnecessary private data if the guidance is applied incompletely. <br>
Mitigation: Review high-impact or irreversible disclosures, minimize data before responding, and defer to a verified system or human review when authorization or facts are unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-private-data-guardrail) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, JSON] <br>
**Output Format:** [Markdown guidance with optional redacted JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute code, install dependencies, call services, write files, or persist memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
