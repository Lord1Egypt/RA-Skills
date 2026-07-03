## Description: <br>
Provides a paid crypto auto-trading strategy package for OKX, Binance, Bybit, and Bitget with five Node.js strategies, risk controls, Telegram alerts, and deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External crypto traders and developers use this skill to review and deploy a Node.js crypto auto-trading strategy package with exchange templates, configurable risk controls, Telegram alerts, and setup guidance. It is not investment advice and requires careful credential and trading-risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes autonomous crypto trading that uses exchange API keys, which can expose funds or execute unintended trades if credentials are over-permissioned or mishandled. <br>
Mitigation: Use exchange keys without withdrawal permission, restrict keys to the minimum trading permissions needed, keep credentials out of git and shared folders, lock down file permissions, and start with small limits. <br>
Risk: Server evidence marks code provenance as unavailable and the security verdict as suspicious because the package asks users to run a persistent trading process with under-specified credential controls. <br>
Mitigation: Inspect the actual source code before running any persistent trading process and review the package carefully before installing or paying. <br>
Risk: Crypto contract trading can cause significant financial loss and the artifact states that it is not investment advice. <br>
Mitigation: Treat the material as educational, validate behavior in a non-production or low-exposure environment, and use conservative position sizing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/crypto-auto-trader-strategy) <br>
- [Publisher profile](https://clawhub.ai/user/sg345662365-oss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell command snippets, configuration steps, and referenced source/manual materials.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trading strategy descriptions, deployment prerequisites, and credential-dependent setup guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
