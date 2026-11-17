## Description:

PDEBench competition workflow orchestration with expflow, covering full, fast, and skip pipeline modes, distributed HPO, pruner integration, and ClearML HyperParameterOptimizer native mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to orchestrate PDEBench competition training, evaluation, submission, and hyperparameter optimization workflows with expflow, ClearML, and Optuna.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HPO, distributed jobs, and pipeline submissions can spend GPU time, queue capacity, and artifact storage.

Mitigation: Require an explicit go-ahead before launching these workflows and use recorded run data rather than estimates when discussing cost.

Risk: ClearML and Langfuse credentials or dataset paths may be needed for the workflow.

Mitigation: Keep credentials and local paths in untracked local configuration such as .env or config.yaml files.

Risk: Unpinned or stale expflow-pde launches can run an unexpected package version.

Mitigation: Verify the expflow-pde package and version before use, and pin uvx or tool-run invocations when launching the CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diamond2nv/skills/expflow-pipeline-hpo)
- [expflow repository](https://github.com/diamond2nv/expflow)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples for expflow, uv, pip, pipx, ClearML, Optuna, and Hermes MCP configuration.]

## Skill Version(s):

0.7.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
