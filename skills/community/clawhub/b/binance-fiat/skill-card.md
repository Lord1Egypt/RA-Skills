## Description: <br>
Binance Fiat request using the Binance API. Authentication requires API key and secret key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexploarer](https://clawhub.ai/user/dexploarer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Binance users use this skill to call authenticated Binance Fiat deposit, withdrawal, order, and payment-history endpoints through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Binance API credentials for authenticated financial API requests, including fiat withdrawal endpoints. <br>
Mitigation: Use a dedicated least-privilege Binance API key, disable withdrawal permission unless it is required, restrict API access by IP where possible, and require explicit approval for every authenticated request. <br>
Risk: Credentials may be read from plaintext local files such as secrets.env, .env, or TOOLS.md. <br>
Mitigation: Do not store real keys in generic .env files or committed TOOLS.md files; keep secrets in dedicated local files with restricted permissions and avoid logging or echoing raw credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dexploarer/binance-fiat) <br>
- [dexploarer publisher profile](https://clawhub.ai/user/dexploarer) <br>
- [Project homepage](https://github.com/binance/binance-skills-hub/tree/main/skills/binance/fiat/SKILL.md) <br>
- [Binance Authentication](references/authentication.md) <br>
- [Binance API mainnet base URL](https://api.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl, openssl, and date to prepare signed Binance Fiat API requests and return endpoint responses in JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
