## Description: <br>
Fetches OKX public spot prices for specified cryptocurrency symbols, displays them in USD, and preserves the user's input order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chgy123](https://clawhub.ai/user/chgy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and end users use this skill to answer cryptocurrency price lookup requests with current OKX spot prices for user-provided symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Price queries are sent to OKX, which exposes requested symbols to a third-party market data service and depends on that service's availability. <br>
Mitigation: Use the skill for public market lookups only, avoid sending sensitive trading intent, and verify critical prices against another trusted source. <br>
Risk: The skill depends on a local Python environment with the requests package installed. <br>
Mitigation: Install dependencies from trusted package sources and run the command in a controlled environment before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chgy123/btc-price) <br>
- [OKX public market API](https://www.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text price list or JSON array from a Python CLI command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and the requests package; contacts OKX public market endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
