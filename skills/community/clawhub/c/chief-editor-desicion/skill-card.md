## Description: <br>
AI agent for chief editor decision reporting tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamolab](https://clawhub.ai/user/teamolab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and editors use this skill to collect information from supplied attachments and source URLs, then produce a long-form decision narrative with a conclusion, MECE logic, a Mermaid tree diagram, charts, and cited references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to read supplied attachments and visit selected links found inside them, which can expose confidential or sensitive material. <br>
Mitigation: Use it only with material the user is authorized to process, avoid confidential documents unless a review gate is available, and inspect the generated report before submission. <br>
Risk: The citation instructions can make attachment-derived research appear directly sourced from original URLs. <br>
Mitigation: Verify cited URLs against the provided source material and require reviewer approval before relying on or publishing the report. <br>
Risk: The skill creates and submits a long decision report with limited user control during the workflow. <br>
Mitigation: Require human review before final submission and check the conclusion, supporting logic, charts, and references for accuracy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teamolab/chief-editor-desicion) <br>
- [Publisher profile](https://clawhub.ai/user/teamolab) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report with Mermaid diagram, charts, and inline URL citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a detailed decision narrative report and submits it as an attachment file; source material should be reviewed before submission.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
