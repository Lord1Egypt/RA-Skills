## Description: <br>
Helps verify that skill updates publish an auditable record of what changed, including capability, dependency, validation, behavioral-scope, risk-class, chain-of-custody, and update-eligibility changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and registry operators use this skill to assess whether skill updates disclose material changes well enough to support continuous monitoring and update decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server-resolved import provenance is unavailable, so source-repository history should not be assumed from the artifact text. <br>
Mitigation: Verify the publisher profile and release source separately before relying on the skill in workflows that require provenance assurance. <br>
Risk: The skill may lead an agent to query registry endpoints using curl or python3. <br>
Mitigation: Only provide private or internal registry endpoints when the agent is intended to access them for the audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/delta-disclosure-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown audit report with structured verdicts and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include completeness scores, reconstructed material changes, custody status, monitoring tractability, disclosure verdict, and update eligibility.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
