## Description: <br>
Retrieves AOX bridge status and supported AO, Ethereum, BSC, and Arweave token mapping information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpd](https://clawhub.ai/user/charles-lpd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check current AOX bridge availability, supported token mappings, minimum withdrawal amounts, and withdrawal fees before answering AO cross-chain status questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AOX bridge availability, withdrawal fees, and token support can affect financial decisions and may change after the lookup. <br>
Mitigation: Verify bridge availability and fees independently before initiating financial transactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charles-lpd/check-aox-info) <br>
- [AOX info API](https://api.aox.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON response containing success status, closeServer bridge-status fields, token mappings, and error text when the lookup fails.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contacts the public AOX info API at runtime and returns current bridge/token status without requesting credentials or modifying accounts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
