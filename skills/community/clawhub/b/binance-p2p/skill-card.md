## Description: <br>
Binance P2P trading assistant for P2P prices, advertisements, payment methods, and authenticated P2P order history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexploarer](https://clawhub.ai/user/dexploarer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Binance P2P market questions, compare ads by payment method, and summarize a user's own P2P order history when read-only API credentials are provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated order-history workflows require Binance API credentials. <br>
Mitigation: Use environment injection, request read-only Binance API permissions, mask secrets in responses, and write credentials to disk only with explicit user agreement. <br>
Risk: Incorrect Binance SAPI signing can cause failed authenticated requests. <br>
Mitigation: Keep SAPI parameters in insertion order, percent-encode according to RFC 3986, include timestamp and signature, and use the required X-MBX-APIKEY and User-Agent headers. <br>
Risk: Users may confuse P2P market lookup with trading operations. <br>
Mitigation: Do not place, cancel, release, appeal, or modify P2P orders; provide official Binance ad or order-page links when the user wants to act. <br>


## Reference(s): <br>
- [Binance P2P Authentication](references/authentication.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dexploarer/binance-p2p) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with structured lists and occasional code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoint guidance, UTC timestamps, masked credentials, and direct Binance P2P ad links when an ad number is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
