## Description: <br>
Fetches public historical cryptocurrency candlestick data from OKX for supported spot trading pairs, with interval selection and timestamp pagination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u91win](https://clawhub.ai/user/u91win) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and trading researchers can use this skill to run a Node.js command that retrieves recent or timestamp-paginated OKX candlestick data for crypto spot pairs such as BTC-USDT, ETH-USDT, and SOL-USDT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested trading pair, interval, and timestamp range are sent to OKX or to any proxy configured in the environment. <br>
Mitigation: Use the skill only when that request metadata can be shared with OKX and review proxy environment variables before running it. <br>
Risk: Server-resolved GitHub import provenance is unavailable for this version. <br>
Mitigation: Review the small JavaScript artifact directly when publisher provenance matters for deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/u91win/crypto-kline-okx) <br>
- [Artifact skill instructions](SKILL.md) <br>
- [OKX K-line script](scripts/okx-kline.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text console output with tabular K-line data and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and network access to OKX; supports optional proxy environment variables and caps API requests at 100 records per call.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
