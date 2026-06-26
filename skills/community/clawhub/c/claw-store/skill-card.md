## Description: <br>
Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Regan-Milne](https://clawhub.ai/user/Regan-Milne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Claw Store to save, load, and migrate encrypted AI-agent memory across sessions and machines. Review is recommended before deployment because the skill persists sensitive memory and includes first-run setup flows for wallet, encryption-key, and API-key handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists durable agent memory that may contain sensitive personal or operational data. <br>
Mitigation: Use a dedicated wallet, avoid storing secrets or regulated data, and require explicit user approval before saving new memories. <br>
Risk: First-run setup and backup commands can expose API keys, encryption keys, or wallet mnemonics if handled carelessly. <br>
Mitigation: Set secrets only through local environment variables, run dependency installation in a controlled environment, and treat displayed keys or mnemonics as high-value secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Regan-Milne/claw-store) <br>
- [Obsideo homepage](https://obsideo.io) <br>
- [Repository](https://github.com/Regan-Milne/jackal-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for encrypted memory save, load, list, usage, wallet, key backup, and manifest export workflows; users should avoid storing secrets or regulated data unless explicitly intended.] <br>

## Skill Version(s): <br>
1.3.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
