## Description: <br>
Dual-mode defensive firewall and lightweight security review skill for Codex/OpenClaw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alethean-kaw](https://clawhub.ai/user/alethean-kaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to contain prompt-injection risks, review risky commands or artifacts before execution, and produce structured security review outcomes for Codex/OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill adds security-review instructions to an agent, so users may over-trust its recommendations without checking the exact installed behavior. <br>
Mitigation: Review the skill page and SKILL.md before installation, as recommended by the server security guidance. <br>
Risk: A single VirusTotal engine hit was reported, although the available evidence did not show artifact-backed malicious or suspicious behavior. <br>
Mitigation: Treat the hit as a caution signal, confirm the artifact hash and source before deployment, and do not block solely on that isolated signal. <br>
Risk: The skill may propose command or artifact review steps that users could mistake for permission to execute untrusted content. <br>
Mitigation: Keep the skill's read-before-execute boundary: inspect untrusted commands, scripts, installers, archives, patches, and diffs before any execution or state change. <br>


## Reference(s): <br>
- [Detection Checklist](references/detection-checklist.md) <br>
- [Examples And Test Samples](references/examples.md) <br>
- [Review Output](references/review-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown conversation responses with structured review labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to conversation output; scan artifacts or persistent reports are produced only when explicitly requested.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
