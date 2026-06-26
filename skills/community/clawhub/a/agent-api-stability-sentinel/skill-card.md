## Description: <br>
API compatibility and breaking-change detection specialist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nntrivi2001](https://clawhub.ai/user/nntrivi2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API maintainers use this skill to test API changes against existing client contracts, identify breaking changes, and produce migration guidance before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live API testing can affect production systems, credentials, rate limits, or state-changing endpoints if the test scope is not constrained. <br>
Mitigation: Define approved endpoints before use, prefer staging or sandbox systems, use least-privilege test credentials and synthetic data, and require separate approval for destructive, load-like, or production requests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON report with compatibility findings and migration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes pass/fail/warning status, endpoint test counts, breaking and non-breaking change lists, version bump recommendation, and migration steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
