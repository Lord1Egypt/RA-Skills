## Description: <br>
Scans GitHub, Algora, and Opire bounty issues, ranks opportunities by payout and competition, and reports actionable targets for developer review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanxevo3](https://clawhub.ai/user/lanxevo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers can use this skill to discover and prioritize paid open-source issues before deciding which bounty work to pursue. It produces scan results and summaries that should be reviewed before any code changes or pull requests are attempted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises autonomous pull request and fix-session behavior without clear approval safeguards. <br>
Mitigation: Require explicit human review before code changes, pushes, or pull request creation. <br>
Risk: The scanner uses the authenticated GitHub CLI and stores bounty activity in a local state file. <br>
Mitigation: Use a least-privilege GitHub login and keep the state directory out of shared or synced locations when activity history is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanxevo3/bounty-hunter-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Console summary and JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes ranked bounty results to a local JSON state file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
