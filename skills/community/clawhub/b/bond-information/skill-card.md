## Description: <br>
BondInformation queries FEEDAX bond market news and filters by bond type, sentiment, and time range to support bond credit risk monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longgggggg](https://clawhub.ai/user/longgggggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to search bond-market news, monitor default risk, track rating changes, and analyze issuer sentiment from FEEDAX data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed through chat, full .env reads, plaintext config files, or command-line arguments. <br>
Mitigation: Provide credentials through a protected environment variable or secret manager, avoid pasting keys into chat, and do not ask the agent to read full credential files. <br>
Risk: Bond-news queries can be retained in generated CSV and Markdown output files by default. <br>
Mitigation: Use --no-output for sensitive searches or write outputs only to a protected directory with appropriate retention controls. <br>
Risk: The documented FEEDAX endpoint uses HTTP, which may not protect real credentials or sensitive query data in transit. <br>
Mitigation: Confirm a trusted HTTPS endpoint with FEEDAX before using production credentials or sensitive search terms. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/longgggggg/bond-information) <br>
- [Publisher profile](https://clawhub.ai/user/longgggggg) <br>
- [FEEDAX](https://www.feedax.cn) <br>
- [FEEDAX bond news API endpoint](http://221.6.15.90:18011/data-service/v1/news/bond/external/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Terminal summaries plus CSV and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FEEDAX API key; generated result files can be disabled with --no-output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
