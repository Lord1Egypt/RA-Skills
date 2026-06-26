## Description: <br>
Agentshield Audit runs local security checks for AI agents, creates Ed25519-based certificates, and supports peer verification and trust handshakes across OpenClaw, Hermes Agent, n8n, LangChain, and custom platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bartelmost](https://clawhub.ai/user/bartelmost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit AI agents, obtain local security test results, request certificates, and verify or handshake with peer agents before agent-to-agent communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote AgentShield registry may receive agent identity metadata, public keys, challenge signatures, and summarized test results. <br>
Mitigation: Use the skill only when that remote submission is acceptable; prefer manual mode and inspect the payload and code path before submitting. <br>
Risk: Automation flags such as --auto or --yes can reduce user review before file reads or submissions. <br>
Mitigation: Run manual mode for sensitive agents and reserve --yes for pre-reviewed, sandboxed, or CI environments where the submitted data is understood. <br>
Risk: Peer-verification results should not be treated as cryptographic proof until signature verification is implemented. <br>
Mitigation: Use peer verification as a registry signal, and require independent cryptographic validation before relying on it for high-trust decisions. <br>
Risk: Handshake session keys may be exposed through shared terminals or logs. <br>
Mitigation: Run handshakes in controlled terminals, avoid logging sensitive output, and restrict access to generated local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bartelmost/agentshield-audit) <br>
- [AgentShield documentation](https://agentshield.live/docs) <br>
- [AgentShield website](https://agentshield.live) <br>
- [Agent skills open standard](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style certificate, verification, and handshake output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local key and certificate files and submit summarized audit results to a remote API.] <br>

## Skill Version(s): <br>
1.0.36 (source: server release metadata, SKILL.md frontmatter, and CHANGELOG.md, released 2026-06-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
