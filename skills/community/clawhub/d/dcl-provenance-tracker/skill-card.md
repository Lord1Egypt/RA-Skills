## Description: <br>
Verifies ClawHub skill updates by comparing a trusted baseline with a candidate version to detect supply-chain drift and produce a deterministic provenance proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daririnch](https://clawhub.ai/user/daririnch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and compliance teams use this skill to review ClawHub skill updates for behavioral drift, permission creep, and supply-chain attack patterns before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate skill text may be untrusted evidence and could contain malicious or misleading instructions. <br>
Mitigation: Paste only the versions intended for comparison and treat the resulting PASS, WARN, or BLOCK verdict as advisory until reviewed. <br>
Risk: Optional audit-chain publication can expose hashes and verdict metadata externally. <br>
Mitigation: Do not enable any separate audit-chain commit unless publishing those hashes and verdict metadata is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daririnch/dcl-provenance-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/daririnch) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [Structured JSON with a verdict, risk score, hashes, findings, recommendation, and DCL fingerprint] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory PASS, WARN, or BLOCK results from local comparison of user-provided skill versions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
