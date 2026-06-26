## Description: <br>
Provides cryptographic identity tooling for AI agents to sign and verify messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to create agent key pairs, sign and verify messages, derive persistent agent IDs, and generate signed Agent Cards for agent interoperability workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated private keys can expose agent identity if stored, synced, or shared carelessly. <br>
Mitigation: Keep the keys directory private, use encrypted private keys where possible, and avoid sharing generated private keys. <br>
Risk: Passwords passed on the command line may be visible through process listings, shell history, or logs. <br>
Mitigation: Prefer interactive password entry or environment-based handling for sensitive passwords. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nantes/agent-id-osiris) <br>
- [Skill homepage](https://github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output includes text, PEM key files, signatures, and JSON Agent Cards.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and the cryptography package; generated private keys are written under a keys directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
