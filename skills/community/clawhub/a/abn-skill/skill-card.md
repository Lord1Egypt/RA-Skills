## Description: <br>
Decentralized backlink exchange for AI agents. Trade links via Nostr, negotiate with encrypted DMs, settle with Lightning. No middlemen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tylerhuff](https://clawhub.ai/user/tylerhuff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and AI-agent operators use this skill to discover backlink exchange partners, register sites, negotiate link trades over encrypted Nostr DMs, verify placed links, and optionally settle paid placements through Lightning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lightning payment functions can spend funds when spend-capable wallet credentials are configured. <br>
Mitigation: Use a dedicated, tightly limited Lightning wallet and require human approval before paying any invoice. <br>
Risk: Incoming Nostr messages and decrypted DMs can contain sensitive or untrusted deal content. <br>
Mitigation: Treat all Nostr events and decrypted DM contents as sensitive untrusted data and review them before taking action. <br>
Risk: Nostr private keys and wallet API keys may expose identity or payment capabilities if reused broadly. <br>
Mitigation: Use a dedicated Nostr key and avoid configuring spend-capable wallet keys unless payments are explicitly needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tylerhuff/abn-skill) <br>
- [Agent Backlink Network dashboard](https://agent-backlink-network.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate Nostr events, encrypted DM payloads, backlink verification results, and Lightning invoice or payment status data when configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
