## Description: <br>
Resolve A-share stocks, ETFs, funds, and other mainland China securities from Chinese names into tradable codes using Eastmoney search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-11even](https://clawhub.ai/user/mr-11even) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to resolve Chinese security names into tradable mainland China stock, ETF, fund, or related instrument codes and to enrich watchlists or portfolio files with exchange-aware identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each lookup term is sent to Eastmoney's public search API, which may disclose Chinese security names, watchlist entries, or portfolio constituents. <br>
Mitigation: Avoid using confidential portfolio data unless disclosure to Eastmoney is acceptable; ask for confirmation when results are ambiguous. <br>
Risk: Ambiguous names can return multiple instruments across stocks, funds, ETFs, or related markets. <br>
Mitigation: Prefer exact Chinese-name matches and expected instrument categories; show the top candidates and ask for confirmation when confidence is low. <br>


## Reference(s): <br>
- [Eastmoney Suggest API Reference](references/eastmoney-api.md) <br>
- [Eastmoney suggest API](https://searchapi.eastmoney.com/api/suggest/get) <br>
- [ClawHub skill page](https://clawhub.ai/mr-11even/cn-security-code-resolver-openclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON resolver output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Resolver responses may include raw code, exchange suffix, standard code, quote ID, security type, candidate list, source, and timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
