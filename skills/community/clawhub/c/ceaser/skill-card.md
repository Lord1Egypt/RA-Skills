## Description: <br>
Interact with the Ceaser privacy protocol on Base L2 using ceaser-mcp CLI commands and public Ceaser API endpoints for shield, unshield, note management, and protocol queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zyra-V21](https://clawhub.ai/user/Zyra-V21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Ceaser protocol status, prepare shield transactions, manage local notes, and unshield ETH through the Ceaser facilitator on Base L2. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle spend-capable Ceaser note backups and local note files. <br>
Mitigation: Treat backup strings and ~/.ceaser-mcp/notes.json like wallet secrets; keep them out of logs, shared chats, and screenshots. <br>
Risk: Shield and unshield workflows may move funds on Base L2 through CLI-generated proofs, unsigned transactions, or facilitator settlement. <br>
Mitigation: Review commands and transaction details before signing or submitting, and use a separate low-privilege environment for meaningful funds. <br>
Risk: The workflow depends on the ceaser-mcp npm package at runtime. <br>
Mitigation: Pin or inspect the ceaser-mcp package before use and avoid granting admin or unrelated credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Zyra-V21/ceaser) <br>
- [Publisher Profile](https://clawhub.ai/user/Zyra-V21) <br>
- [Ceaser Homepage](https://ceaser.org) <br>
- [OpenAPI Specification](references/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, node, and npx; Ceaser CLI commands emit JSON on success and failure.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
