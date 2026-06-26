## Description: <br>
93pct autocompletes agency next steps by ranking concrete, viable actions by ROI/effort ratio and returning one job ID for approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironiclawdoctor-design](https://clawhub.ai/user/ironiclawdoctor-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agency operators use this skill to inspect local workflow state, rank concrete next steps by expected value and effort, and select one job ID for approval or completion tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads finance, wallet, draft, and secret-adjacent local state and writes task state to an agency database. <br>
Mitigation: Review before installing and run only in an environment where that local inspection and database writing are acceptable. <br>
Risk: The suggested GCP, Gmail, Cash App, BTC, and publishing actions are specific to the publisher's workflow. <br>
Mitigation: Treat suggestions as workflow-specific proposals and manually review any command, URL, or approval ID before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ironiclawdoctor-design/93pct) <br>
- [Publisher profile](https://clawhub.ai/user/ironiclawdoctor-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with ranked suggestions, job IDs, blockers, URLs, and commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Suggestions include Shannon score, estimated effort, blocker, expected output, and optional command or URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
