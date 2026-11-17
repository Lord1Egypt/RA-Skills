## Description:

Guides an agent through clarifying a FaMou evolution task, writing problem.md, and generating and validating init.py, evaluator.py, and prompt.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaom0](https://clawhub.ai/user/zhaom0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn a vague optimization, machine learning, or search problem into a structured FaMou task definition and validated starter materials for an evolution experiment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may inspect local project files while defining a task.

Mitigation: Run it in a workspace that contains only the files needed for the FaMou task and no secrets or unrelated private data.

Risk: The workflow validates generated Python files and may run evaluator.py against init.py.

Mitigation: Review problem.md, evaluator.py, and init.py before validation, and execute validation only in a sandboxed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaom0/skills/famou-artifact-generator)
- [Publisher profile](https://clawhub.ai/user/zhaom0)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown documents, Python scripts, and validation command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces problem.md, prompt.md, init.py, and evaluator.py; prompt.md is constrained to 100 lines or fewer.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
