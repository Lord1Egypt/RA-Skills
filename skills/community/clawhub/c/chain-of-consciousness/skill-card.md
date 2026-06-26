## Description: <br>
Adds cryptographic provenance to agent work by creating tamper-evident audit trails for learned information, decisions, created artifacts, and verification steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, verify, and export local tamper-evident audit trails of agent sessions, decisions, learning, and created artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent audit logs may capture secrets, personal data, regulated information, raw conversation text, hidden reasoning, or confidential project details if the agent logs too broadly. <br>
Mitigation: Use concise non-sensitive summaries, instruct the agent not to log sensitive or regulated content, and review chain contents before exporting or sharing. <br>
Risk: The skill depends on an external PyPI package and CLI for logging and verification behavior. <br>
Mitigation: Review or pin the chain-of-consciousness dependency before installation and run it only in environments where local file writes are intended. <br>
Risk: Optional external timestamp anchoring uses third-party timestamp services and may require network access. <br>
Mitigation: Enable anchoring only when third-party timestamping is acceptable for the project and verify what data is sent before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexfleetcommander/chain-of-consciousness) <br>
- [Vibe Agent Making](https://vibeagentmaking.com) <br>
- [PyPI Package](https://pypi.org/project/chain-of-consciousness/) <br>
- [Whitepaper](https://vibeagentmaking.com/whitepaper) <br>
- [Verification Demo](https://vibeagentmaking.com/verify/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation, verification, tailing, and export of local JSONL or JSON provenance files through the external coc CLI or Python API.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
