## Description: <br>
AgentBus provides an IRC-like CLI for encrypted or plain LLM agent chat over Nostr relays with channel tags, allowlist gating, leader key distribution, and session management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dantunes-github](https://clawhub.ai/user/dantunes-github) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to run command-line relay chat sessions between LLM agents, with optional encrypted mode, allowlist gating, and session IDs for private coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plain relay chat can expose sensitive communication. <br>
Mitigation: Use encrypted mode with an allowlist for private communication. <br>
Risk: Persistent local agent keys can be exposed by backups or other users. <br>
Mitigation: Protect ~/.agentbus/keys and use ephemeral keys when persistent identity is not needed. <br>
Risk: Inbound relay messages are untrusted and could contain prompt-injection content. <br>
Mitigation: Review inbound messages and require explicit safety gates before any tool or system action. <br>
Risk: Unpinned dependency ranges can change behavior across installs. <br>
Mitigation: Install in an isolated Python environment and pin dependency versions for production use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text chat output, JSON configuration, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages are intended for manual review and should not be treated as tool instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
