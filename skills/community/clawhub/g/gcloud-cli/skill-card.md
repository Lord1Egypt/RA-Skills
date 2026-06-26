## Description: <br>
Manage Google Cloud Platform resources using the official gcloud CLI, discovering command syntax dynamically with `gcloud <group> --help` before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipe0liveira](https://clawhub.ai/user/felipe0liveira) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud engineers use this skill to prepare, review, and run approved Google Cloud CLI commands for resource management and developer workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help prepare commands that affect Google Cloud resources. <br>
Mitigation: Require explicit user approval before any command execution, including read-only operations. <br>
Risk: Commands may run under the wrong Google Cloud account, project, or environment. <br>
Mitigation: Show the active account and project, confirm the target environment, and prefer a dedicated least-privilege service account. <br>
Risk: Memorized or stale command syntax can produce incorrect Google Cloud CLI commands. <br>
Mitigation: Inspect current `gcloud <group> --help` output before building commands. <br>
Risk: High-impact operations such as IAM, networking, deletion, or service enablement can change access or availability. <br>
Mitigation: Warn clearly for high-impact operations and require explicit approval of the full command before execution. <br>


## Reference(s): <br>
- [Google Cloud CLI reference](https://cloud.google.com/sdk/gcloud) <br>
- [Install Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk) <br>
- [Google Cloud CLI skill page](https://clawhub.ai/felipe0liveira/gcloud-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and command-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request explicit user approval before command execution and may ask the user to confirm account, project, and environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
