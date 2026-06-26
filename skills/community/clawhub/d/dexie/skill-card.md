## Description: <br>
Dexie tracks Chia DEX offers, tokens, trading pairs, prices, liquidity, and platform statistics through the public Dexie.space API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agents use this skill to answer Chia DEX market questions, check token prices, inspect offers, search CAT assets, and format Dexie.space market data for CLI or chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency hygiene risk around axios. <br>
Mitigation: Review the dependency lockfile before installing and use a patched, pinned axios version. <br>
Risk: Market and trading data comes from an external API and may be incomplete, delayed, or unsuitable for financial decisions. <br>
Mitigation: Treat responses as informational Dexie.space API data and verify important trading decisions against authoritative sources. <br>


## Reference(s): <br>
- [Dexie Skill Page](https://clawhub.ai/Koba42Corp/dexie) <br>
- [Dexie.space](https://dexie.space) <br>
- [Dexie.space API](https://api.dexie.space/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code] <br>
**Output Format:** [Plain text formatted for CLI and chat messages; JavaScript API methods return Dexie.space response data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the public Dexie.space API without an API key; returned market data should be treated as external API data.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
