## Description:

Helps agents add instrumentation, build golden datasets, write and run eval-based tests, root-cause failures, and iterate on Python LLM applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiouli](https://clawhub.ai/user/yiouli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and iterate on evaluation pipelines for Python applications that call LLMs. It guides agents through instrumentation, trace capture, dataset creation, eval test writing, test execution, and root-cause analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to upgrade pixie-qa and reinstall the skill from remote sources before starting work.

Mitigation: Approve the exact package and skill versions before upgrades, prefer pinned dependencies, and run the workflow in a virtual environment or container.

Risk: Evaluation traces and datasets may contain prompts, user inputs, model outputs, and metadata.

Mitigation: Treat the pixie_qa directory as sensitive, review it before committing or sharing, and redact secrets or private data.

## Reference(s):

- [Pixie API Reference](references/pixie-api.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code changes, generated eval files, JSON datasets, and test results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update pixie_qa working files, including notes, traces, datasets, tests, and helper scripts.]

## Skill Version(s):

0.1.11 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
