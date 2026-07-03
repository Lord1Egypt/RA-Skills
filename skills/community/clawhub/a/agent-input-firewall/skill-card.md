## Description: <br>
Helps AI agents scan untrusted inbound text for prompt-injection or jailbreak content before acting on it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorcan84](https://clawhub.ai/user/lorcan84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to screen inbound posts, comments, DMs, tool results, or scraped web text before feeding it into an agent's planning or decision prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text selected for scanning is sent to the publisher's external service. <br>
Mitigation: Do not send secrets, credentials, private content, or regulated data unless the publisher's data-handling terms are acceptable for the use case. <br>
Risk: Future use may involve x402 payment for scans. <br>
Mitigation: Confirm payment behavior and budget controls before enabling the skill in automated agent workflows. <br>
Risk: A prompt-injection detection result could be treated as a complete safety decision. <br>
Mitigation: Use scan results as one control in the input-handling path, and continue treating untrusted content as data rather than instructions. <br>


## Reference(s): <br>
- [Agent Input Firewall homepage](https://x402.cheetahsecurity.de) <br>
- [Agent Input Firewall scan endpoint](https://x402.cheetahsecurity.de/scan) <br>
- [ClawHub skill page](https://clawhub.ai/lorcan84/skills/agent-input-firewall) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scan API response includes safe, verdict, and risk_score fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
