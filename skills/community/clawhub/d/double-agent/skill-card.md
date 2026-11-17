## Description:

DoubleAgent helps developers design Generator-Evaluator agent loops where a separate evaluator validates generated outputs against a spec through real interaction and structured scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design multi-agent quality-assurance workflows that separate generation from evaluation. It is especially suited to AI-generated UIs, multi-step workflows, API implementations, and content generation that benefit from independent rubric-based review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluator workflows may require browser, file, network, or credential access when adapted to a real artifact.

Mitigation: Grant Playwright, file, network, and credential access only for the specific artifact, specification, and test environment being evaluated.

Risk: Evaluator prompts or logs could expose sensitive production credentials if used against production systems.

Mitigation: Use non-production credentials and avoid placing secrets in evaluator prompts or generated logs.

Risk: The included loop and calibration scripts are templates and are not a complete sandbox for untrusted generated artifacts.

Mitigation: Treat the skill as a design template and run adapted generators and evaluators inside an appropriately isolated test environment.

## Reference(s):

- [DoubleAgent Architecture Reference](references/architecture.md)
- [Evaluator Prompt Templates](references/evaluator-prompts.md)
- [ClawHub Skill Page](https://clawhub.ai/zmy1006-sudo/skills/double-agent)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python templates, JSON schemas, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces adaptable templates for evaluator prompts, score rubrics, calibration fixtures, and iteration-loop control.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
