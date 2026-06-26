## Description: <br>
Aegis Shield screens untrusted text for prompt-injection and data-exfiltration risks before summarization, replies, or memory writes, and provides a safe memory append workflow that scans, lints, and accepts or quarantines content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Deegerwalker](https://clawhub.ai/user/Deegerwalker) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to screen untrusted web, email, social, or similar text for prompt-injection, data-exfiltration, and tool-abuse patterns before using it in summaries, replies, or memory. The bundled workflow can append sanitized, sourced memory entries or quarantine flagged text for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes that raw flagged text can be persisted in quarantine memory files. <br>
Mitigation: Do not feed secrets or sensitive content through the workflow unless quarantine storage and cleanup processes are acceptable. <br>
Risk: The bundled script depends on an unbundled local scanner module at a hard-coded path. <br>
Mitigation: Install and review the expected local scanner before relying on the safe memory append workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Deegerwalker/aegis-shield) <br>
- [Publisher profile](https://clawhub.ai/user/Deegerwalker) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, json, markdown] <br>
**Output Format:** [Markdown instructions with shell command examples; the bundled script emits JSON status and can append Markdown memory or quarantine entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepted content is written as sourced memory entries; flagged content may be quarantined with scan and lint details for review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
