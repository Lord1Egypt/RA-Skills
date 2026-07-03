## Description: <br>
Diagnoses Yunxiao Flow pipeline execution failures and provides fix recommendations across build, deployment, testing, and runtime stages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to inspect Yunxiao Flow pipeline runs, retrieve failed step logs, identify root causes, and receive practical remediation guidance for build, deployment, testing, and runtime failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yunxiao personal access tokens grant pipeline read access and may expose sensitive pipeline data if mishandled. <br>
Mitigation: Use a least-privilege read-only token, prefer the YUNXIAO_ACCESS_TOKEN environment variable, and do not paste, echo, log, or hardcode the full token. <br>
Risk: Live terminal access can expose source code, secrets, environment variables, or build machine state. <br>
Mitigation: Use log and API retrieval first; provide a terminalUrl only for explicit live inspection, review every command and output, and exit the terminal when troubleshooting is complete. <br>
Risk: Troubleshooting recommendations or shell commands may affect pipeline configuration or runtime behavior if applied without review. <br>
Mitigation: Confirm all customizable parameters with the user and review proposed commands or configuration changes before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-yunxiao-flow-analysis) <br>
- [Yunxiao Flow troubleshooting guide](references/troubleshooting-guide.md) <br>
- [Yunxiao fundamentals](references/yunxiao_base.md) <br>
- [Pipeline runs API field documentation](references/yunxiao_flow_get_pipeline_runs.md) <br>
- [Related script commands](references/related-commands.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis report with inline shell commands and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-derived pipeline status, failed job and step summaries, error log excerpts, root cause analysis, and remediation steps.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
