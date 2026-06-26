## Description: <br>
PDEBench competition workflow orchestration with expflow: three pipeline modes, distributed HPO, pruner integration, and ClearML HyperParameterOptimizer native mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diamond2nv](https://clawhub.ai/user/diamond2nv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to plan expflow-based PDEBench competition workflows, including full HPO-to-train-to-eval pipelines, faster train-and-eval runs, and selective step skipping. It helps configure ClearML and Optuna execution choices, required script outputs, pruner behavior, metrics, queues, and timeout controls before launching experiments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that can launch costly training or hyperparameter optimization jobs. <br>
Mitigation: Before running commands, review the ClearML queue, trial count, parallelism, timeout, and target scripts to avoid unintended GPU use or wrong experiment submissions. <br>


## Reference(s): <br>
- [expflow project homepage](https://github.com/diamond2nv/expflow) <br>
- [ClawHub skill page](https://clawhub.ai/diamond2nv/expflow-pipeline-hpo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for expflow, ClearML, Optuna, and PDEBench-style experiment pipelines.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
