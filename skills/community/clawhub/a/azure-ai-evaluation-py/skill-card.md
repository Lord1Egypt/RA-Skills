## Description:

Azure AI Evaluation SDK for Python for evaluating generative AI applications with quality, safety, and custom evaluators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegovind](https://clawhub.ai/user/thegovind)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure Azure AI Evaluation SDK workflows, select built-in or custom evaluators, and run single-row or batch assessments of generative AI applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-backed evaluators may send evaluation data to Azure services.

Mitigation: Use sanitized or approved datasets and review Azure data-handling requirements before enabling model-backed evaluators or Foundry logging.

Risk: Examples may encourage use of production secrets in local demos or shared evaluation scripts.

Mitigation: Use non-production credentials for demos, keep secrets out of datasets and prompts, and rely on approved secret-management practices.

Risk: Custom prompt-evaluator examples can be vulnerable to prompt injection or malformed evaluator output when used as deployment gates.

Mitigation: Harden custom evaluator prompts, validate returned schemas, and review results before using them for compliance or release decisions.

Risk: Unpinned dependencies can reduce reproducibility across evaluation runs.

Mitigation: Pin dependencies and record Azure model deployment versions for reproducible evaluation environments.

## Reference(s):

- [Built-in Evaluators Reference](references/built-in-evaluators.md)
- [Custom Evaluators Reference](references/custom-evaluators.md)
- [Batch Evaluation CLI Tool](scripts/run_batch_evaluation.py)
- [ClawHub skill page](https://clawhub.ai/thegovind/skills/azure-ai-evaluation-py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Azure environment variable names, evaluator configuration examples, and batch-evaluation command examples.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
