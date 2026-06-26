## Description: <br>
Analyze AWS CloudTrail logs for suspicious patterns, unauthorized changes, and MITRE ATT&CK indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security analysts, incident responders, and cloud engineers use this skill to review user-provided AWS CloudTrail exports for suspicious activity, assemble an incident timeline, map events to MITRE ATT&CK cloud techniques, and identify containment steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CloudTrail exports can contain sensitive operational details or accidental secrets. <br>
Mitigation: Export only the relevant account, region, and time window, and review logs before sharing them with the agent. <br>
Risk: Users might paste AWS access keys, session tokens, or other credentials while providing incident data. <br>
Mitigation: Provide exported logs or console output only, and remove any AWS keys, secret keys, or session tokens before analysis. <br>
Risk: AWS CLI export commands require account access even though the skill itself does not access AWS. <br>
Mitigation: Run any export commands yourself with a least-privilege read-only role limited to CloudTrail and CloudWatch log retrieval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/cloudtrail-threat-detector) <br>
- [Publisher profile](https://clawhub.ai/user/anmolnagpal) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown threat summary with timeline, findings table, attack narrative, containment actions, detection gaps, and optional inline shell commands for user-run exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-supplied CloudTrail, S3, CloudWatch Logs, or incident-description data only; the skill does not access AWS accounts directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
