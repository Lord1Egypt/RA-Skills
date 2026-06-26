## Description: <br>
Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adhamelswesy](https://clawhub.ai/user/adhamelswesy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to create and manage Billions/Iden3 decentralized identities, link agent and human identities, sign challenges, and verify DID ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys are stored unencrypted under $HOME/.openclaw/billions. <br>
Mitigation: Install only on trusted single-user machines, restrict local filesystem and backup access, and rotate or abandon identities if kms.json is exposed. <br>
Risk: Signed identity material can be sent to caller-provided recipients. <br>
Mitigation: Verify every --to recipient before linking or signing and stop if the recipient or challenge is unexpected. <br>


## Reference(s): <br>
- [Billions Network](https://billions.network/) <br>
- [DryptoBillions on ClawHub](https://clawhub.ai/adhamelswesy/dryptobillions) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return plain text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or reads local identity files under $HOME/.openclaw/billions and may send direct messages through openclaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
