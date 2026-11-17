## Description:

Benchmark and rank AI providers/models against a user-specific prompt suite derived from the user's purpose, domain, and usage frequency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankisstank](https://clawhub.ai/user/tankisstank)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and technical teams use this skill to build user-specific benchmark suites, compare models on the same prompts, score results across quality, depth, cost, and speed, and generate auditable model-selection reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark runs can send prompts and a configured bearer token to the HTTPS endpoint selected in the benchmark spec.

Mitigation: Run only trusted benchmark specs, use approved endpoints, and keep auth_env set to a dedicated low-privilege benchmark key such as BENCHMARK_API_KEY.

Risk: Sensitive prompts, model outputs, or internal reports could be exposed if benchmark or publishing steps are run without review.

Mitigation: Review benchmark specs and generated reports before execution or publication, and avoid sensitive prompts unless the endpoint and delivery target are approved.

Risk: Unpinned dependencies or unfamiliar endpoints can make benchmark execution harder to control.

Mitigation: Pin dependencies and run the skill in a controlled environment before using it for important model-selection decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tankisstank/skills/benchmark-model-provider)
- [Benchmark Schema](references/benchmark-schema.md)
- [Execution Modes](references/execution-modes.md)
- [Scoring Rubric](references/scoring-rubric.md)
- [Pricing Sources Policy](references/pricing-sources.md)
- [Output Modes](references/output-modes.md)
- [Runtime Safety](references/runtime-safety.md)
- [Environment Variables and Dependencies](references/environment-vars.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, PDF, YAML/JSON benchmark artifacts, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves raw model outputs and metrics for audit and reranking; estimated cost metrics should be visibly marked.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
