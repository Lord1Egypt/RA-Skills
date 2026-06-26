## Description: <br>
Designs DP Data Processing Platform pipelines from natural-language requirements, generating StreamJob XML and guiding submission, execution, monitoring, and troubleshooting through the DP REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hxp365](https://clawhub.ai/user/hxp365) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to translate data source, transformation, and output requirements into DP platform pipeline designs, StreamJob XML, and operational guidance for Flink-based data-processing jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an API key to submit and start live DP data-processing jobs. <br>
Mitigation: Require explicit user approval before any submit or start action, and show the target server, StreamJob XML, inputs, outputs, quota impact, and stop plan first. <br>
Risk: A misconfigured or untrusted DP server could expose sensitive pipeline metadata or execute unintended workloads. <br>
Mitigation: Use only a trusted HTTPS DP server and a scoped API key with the minimum permissions needed for the intended job. <br>
Risk: Generated pipeline XML or troubleshooting guidance may be incorrect for the user's available resources and operators. <br>
Mitigation: Review the pipeline design, resource references, and operator choices before execution, and limit generated pipelines to documented DP operators. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hxp365/dp-pipeline-designer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with XML configuration, REST API curl commands, status summaries, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include StreamJob XML, DP REST API requests, quota-impact notes, and job stop or monitoring plans.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
