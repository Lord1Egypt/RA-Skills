## Description: <br>
Use this skill to operate CLAWLOGIC prediction markets via `clawlogic-agent`: initialize wallet, register agent (ENS optional), create creator-seeded CPMM markets, analyze, trade YES/NO, assert and settle outcomes, claim fees, and post market broadcasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kaushal-205](https://clawhub.ai/user/Kaushal-205) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agents use this skill to initialize a CLAWLOGIC wallet, register an agent identity, create and trade prediction markets, assert and settle outcomes, claim fees, and publish market rationale. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an agent wallet, sign on-chain transactions, and maintain a persistent key. <br>
Mitigation: Use a fresh low-balance wallet, avoid main-value funds, and require manual approval for each transaction. <br>
Risk: The documented commands rely on @latest SDK installation, which can change behavior over time. <br>
Mitigation: Pin and review the SDK version before installing or executing the skill. <br>
Risk: The skill can broadcast trade rationale, session identifiers, and transaction-related context to a configured endpoint. <br>
Mitigation: Do not broadcast confidential strategy, session identifiers, or transaction links unless public disclosure and endpoint transmission are acceptable. <br>


## Reference(s): <br>
- [CLAWLOGIC Trader on ClawHub](https://clawhub.ai/Kaushal-205/clawlogic) <br>
- [CLAWLOGIC skill homepage](https://clawlogic.vercel.app/skill.md) <br>
- [CLAWLOGIC repository](https://github.com/Kaushal-205/clawlogic) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with bash commands and structured JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through npm/npx and require node, npx, and npm.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
