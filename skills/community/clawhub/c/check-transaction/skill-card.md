## Description: <br>
Allows users to check the status of a blockchain transaction by submitting a TxId and querying the AOX transaction API for human-readable results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpd](https://clawhub.ai/user/charles-lpd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users can use this skill to look up AOX blockchain transaction status from a TxId and receive a readable summary of status, parties, amount, confirmations, and timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction IDs submitted for lookup are sent to AOX's public API. <br>
Mitigation: Only submit transaction IDs that are acceptable to disclose to AOX, and avoid including wallet secrets, API keys, or account credentials. <br>
Risk: Public API responses may be unavailable, delayed, or return an error for invalid or missing transaction IDs. <br>
Mitigation: Check the returned status or error message before relying on the result, and retry or verify through another source when transaction state is important. <br>


## Reference(s): <br>
- [AOX Transaction API](https://api.aox.xyz/docs) <br>
- [AOX Website](https://aox.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional curl commands and human-readable transaction fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-provided TxId and returns public transaction status data from AOX; no credentials are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
