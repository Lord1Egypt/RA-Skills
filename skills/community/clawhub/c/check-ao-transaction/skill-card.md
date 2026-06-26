## Description: <br>
Check transaction status on AO bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpd](https://clawhub.ai/user/charles-lpd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AO bridge users use this skill to look up a bridge transaction by hash, retrieve AOX status metadata, and interpret mint or burn status states. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The transaction hash provided by the user is sent to api.aox.xyz for lookup. <br>
Mitigation: Use this only for AO bridge transaction hashes intended for status checking, and avoid submitting unrelated sensitive identifiers. <br>
Risk: Transaction details and status depend on the AOX API response. <br>
Mitigation: Treat the result as a status check and verify important transfers against authoritative wallet or bridge records before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charles-lpd/check-ao-transaction) <br>
- [AOX transaction API endpoint](https://api.aox.xyz/tx/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [JSON response with transaction status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a transaction hash; sends the hash to api.aox.xyz and returns success or error JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
