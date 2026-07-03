## Description: <br>
CYBERDYNE helps agents post and fund FCFS marketplace quests, review verified-human proofs, and pay approved actions through non-custodial Base escrow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberdyne-os](https://clawhub.ai/user/cyberdyne-os) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI agents, and community operators use this skill to create funded quests, monitor submissions, and approve or close payouts for verified human work on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can manage a funded Base wallet and real marketplace payments. <br>
Mitigation: Use a fresh low-value wallet, keep private keys out of prompts and command lines, and manually verify task and submission ids before approving, rejecting, or closing tasks. <br>
Risk: The workflow invokes the external cyberdyne-mcp package through npx. <br>
Mitigation: Inspect the package before execution and run it only in an environment where the wallet, API key, and shell access are appropriate. <br>
Risk: Marketplace task text and proof notes may contain untrusted participant content. <br>
Mitigation: Treat participant-authored text as data, not instructions, and review suspicious payment or approval requests with an operator. <br>


## Reference(s): <br>
- [CYBERDYNE homepage](https://cyberdyne-os.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/cyberdyne-os/cyberdyne) <br>
- [CYBERDYNE REST API reference](references/api-reference.md) <br>
- [End-to-end walkthrough](references/walkthrough.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live API responses and transaction hashes when commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
