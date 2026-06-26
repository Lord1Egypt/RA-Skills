## Description: <br>
Clawked helps agents interact with the Ceaser privacy protocol on Base L2 by querying protocol status and preparing shield or unshield workflows through API and CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Se7enHvn](https://clawhub.ai/user/Se7enHvn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use this skill to inspect Ceaser protocol state, calculate fees, monitor Merkle and nullifier status, and prepare shield or unshield workflows on Base L2. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate ETH shield, unshield, import, and settlement workflows through an external npm command. <br>
Mitigation: Install only when the publisher and ceaser-mcp package are trusted, and require explicit confirmation of Base network, amount, recipient address, fees, and note ID before transaction-related actions. <br>
Risk: Ceaser note backups and ~/.ceaser-mcp/notes.json contain secrets needed to recover or spend notes. <br>
Mitigation: Treat note backups and notes.json like private keys: keep them protected, do not paste them into shared chats or logs, and avoid exposing them in command output. <br>
Risk: The artifact documents client-side ZK proof generation and requires confirmed notes before unshielding. <br>
Mitigation: Use the Ceaser frontend or ceaser-mcp for proof generation, verify that the shield transaction has confirmed and the note has a valid leaf index, and check nullifier status before unshielding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Se7enHvn/agent-privacy-skill) <br>
- [Ceaser homepage](https://ceaser.org) <br>
- [ceaser-mcp npm package](https://www.npmjs.com/package/ceaser-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON API examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command outputs from Ceaser APIs and ceaser-mcp are described as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
