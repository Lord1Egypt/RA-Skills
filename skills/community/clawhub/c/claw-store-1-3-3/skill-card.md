## Description: <br>
Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Regan-Milne](https://clawhub.ai/user/Regan-Milne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to save, load, list, and recover encrypted agent memory across sessions and machines using Jackal decentralized storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use can require npm dependency installation while the skill handles long-lived wallet and encryption secrets. <br>
Mitigation: Install dependencies in a clean environment, avoid unrelated secrets in process environment or nearby .env files, and keep wallet, mnemonic, and encryption key output private. <br>
Risk: Memory content persists across sessions and may contain personal or operationally sensitive data even though payloads are encrypted. <br>
Mitigation: Review what the agent saves, avoid proactively storing raw secrets, and store API keys, encryption keys, and wallet mnemonics only in local environment variables. <br>
Risk: Use depends on trust in the publisher, the Railway API host, Jackal providers, and the npm dependency chain. <br>
Mitigation: Install only after reviewing the publisher and service endpoints, and run npm install yourself in a clean environment before use. <br>


## Reference(s): <br>
- [Claw Store ClawHub Listing](https://clawhub.ai/Regan-Milne/claw-store-1-3-3) <br>
- [Obsideo Homepage](https://obsideo.io) <br>
- [Project Repository](https://github.com/Regan-Milne/jackal-memory) <br>
- [Claw Store API Host](https://web-production-5cce7.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for memory save/load workflows and local environment configuration; runtime commands may read or write encrypted memory state.] <br>

## Skill Version(s): <br>
1.3.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
