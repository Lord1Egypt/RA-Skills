## Description: <br>
Read-only factual data about historical Ethereum mainnet contracts, including contract addresses, deployment era, deployer, runtime bytecode, decompiled code, and documented history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cartoonitunes](https://clawhub.ai/user/cartoonitunes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to look up factual Ethereum mainnet contract history by address, era, timestamp range, or documentation status. It is suited for read-only contract discovery and historical contract analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract addresses, date ranges, and related lookup queries may be sent to ethereumhistory.com. <br>
Mitigation: Avoid sending sensitive investigative queries unless sharing them with the external service is acceptable. <br>
Risk: Historical contract facts may be incomplete or require high confidence for downstream decisions. <br>
Mitigation: Verify important technical or historical claims against primary blockchain records or trusted explorer sources when accuracy matters. <br>


## Reference(s): <br>
- [Ethereum History](https://ethereumhistory.com) <br>
- [Ethereum History agent manifest](https://ethereumhistory.com/api/agent/manifest) <br>
- [Ethereum History skill page](https://clawhub.ai/cartoonitunes/ethereum-history) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, JSON, guidance] <br>
**Output Format:** [Markdown or text summaries grounded in JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GET-only unauthenticated endpoints and returns factual contract data with snake_case JSON fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
