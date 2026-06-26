## Description: <br>
Crypto market data from AiCoin Open API v3 across 200+ exchanges, including prices, K-lines, derivatives metrics, news, airdrops, treasuries, indices, market signals, and AI coin recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[procaross](https://clawhub.ai/user/procaross) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve live AiCoin market data and related crypto research signals through a Node.js command-line interface. It is intended for market lookup and analysis, not trading execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local environment files and can store an AiCoin API key in plaintext. <br>
Mitigation: Use a low-privilege AiCoin market-data key, keep unrelated credentials out of readable environment files, and protect the local .env file. <br>
Risk: The bundled public key and paid endpoints can create confusing access differences, including 403 responses for unavailable API tiers. <br>
Mitigation: Check the returned JSON envelope before using results, treat 403 responses as plan or key limitations, and avoid retry loops. <br>
Risk: The skill exposes broader analytics than ordinary price lookup, including liquidation, whale order, treasury, and market signal data. <br>
Mitigation: Present analytics as market data rather than financial advice and avoid making trading recommendations from a single response. <br>


## Reference(s): <br>
- [AiCoin Open Data](https://www.aicoin.com/opendata) <br>
- [ClawHub skill page](https://clawhub.ai/procaross/aicoin-market) <br>
- [Source metadata](https://github.com/aicoincom/coinos-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API calls return a JSON envelope with ok, data, error, and meta fields.] <br>

## Skill Version(s): <br>
4.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
