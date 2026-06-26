## Description: <br>
Pre-pump fingerprint scanner. Identifies assets showing accumulation signals before a price move using the 8-signal framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xzahra](https://clawhub.ai/user/0xzahra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to evaluate crypto tokens for early-stage accumulation signals, score active setup indicators, and receive a risk note before considering a trade. The analysis is probabilistic and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that package metadata advertises wallet access, transaction signing, and sensitive-credential capabilities that do not fit the visible market-analysis instructions. <br>
Mitigation: Do not grant wallet access, private keys, seed phrases, exchange credentials, or transaction-signing authority unless the publisher clearly explains why those permissions are necessary. <br>
Risk: The skill analyzes crypto trading setups and may produce incorrect or misleading market conclusions. <br>
Mitigation: Treat outputs as probabilistic analysis only, verify market and on-chain data independently, and preserve the required risk note and NFA disclaimer. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown token analysis with signal score, active-signal list, key level, risk note, and psychology trap] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ends with an NFA probabilistic-use disclaimer and requires unverifiable signals to be marked unconfirmed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
