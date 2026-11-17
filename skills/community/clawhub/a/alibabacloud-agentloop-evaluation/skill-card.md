## Description: <br>
Orchestrates AgentLoop evaluation workflows through the Aliyun CLI plugin, including evaluator management, one-shot and batch runs, polling, result inspection, and low-score analysis from SLS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to preview, run, monitor, and analyze Alibaba Cloud AgentLoop evaluation tasks from compact JSON specifications, including saved evaluator management and SLS-based result analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can update Aliyun CLI plugins or enable automatic plugin installation, changing the local toolchain beyond the evaluation workflow. <br>
Mitigation: Review setup commands first; prefer a test environment and manually install or update only the needed AgentLoop and SLS plugins where change control matters. <br>
Risk: Execution can create or change AgentLoop evaluation resources and may launch costly continuous or unbounded evaluation work. <br>
Mitigation: Use dry-run previews, require explicit approval before execution or allow flags, and keep batch runs bounded unless the user accepts the scope and cost. <br>
Risk: Evaluation outputs and SLS result queries may contain operational or customer data. <br>
Mitigation: Store output JSON files in a private path and include raw content only when exact content is necessary and explicitly authorized. <br>


## Reference(s): <br>
- [Workflow specification](references/spec-format.md) <br>
- [AgentLoop evaluation API map](references/api-map.md) <br>
- [Evaluation result analysis](references/result-analysis.md) <br>
- [RAM Policies - AgentLoop Evaluation](references/ram-policies.md) <br>
- [Alibaba Cloud CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Verification Method - AgentLoop Evaluation](references/verification-method.md) <br>
- [Acceptance Criteria - alibabacloud-agentloop-evaluation](references/acceptance-criteria.md) <br>
- [Related CLI Commands - AgentLoop Evaluation](references/related-commands.md) <br>
- [One-shot evaluation example](references/examples/oneshot-example.json) <br>
- [Batch trace evaluation example](references/examples/batch-trace-example.json) <br>
- [Batch dataset evaluation example](references/examples/batch-dataset-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run previews, evaluation/result-analysis commands, and private JSON output paths; cloud mutations require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
