## Description: <br>
Benchmark and rank AI providers/models against a user-specific prompt suite derived from the user's purpose, domain, and usage frequency. Use when users ask which model is smarter, cheaper, deeper, faster, worth using daily, better as local vs service, or when building repeatable benchmark specs, reranking old runs, generating markdown/HTML/PDF benchmark reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankisstank](https://clawhub.ai/user/tankisstank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and power users use this skill to build repeatable text-model benchmarks from their own workflow needs, run comparable model evaluations, rerank existing results, and generate reviewable benchmark reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark runs can send prompts and credentials to the configured provider endpoint. <br>
Mitigation: Use a scoped API key, verify base_url before running, and send only prompts that are acceptable for the selected provider. <br>
Risk: Benchmark reports and raw artifacts can store prompts, model outputs, metrics, and other local run details. <br>
Mitigation: Review generated artifacts before sharing or publishing, and avoid sensitive benchmark prompts unless local storage is acceptable. <br>
Risk: Dependency hygiene issues in PyYAML and reportlab can affect runtime safety. <br>
Mitigation: Install the skill in an isolated environment with pinned, current PyYAML and reportlab versions. <br>


## Reference(s): <br>
- [Initial Project Specification](artifact/references/initial-project-spec.md) <br>
- [Benchmark Schema](artifact/references/benchmark-schema.md) <br>
- [Scoring Rubric](artifact/references/scoring-rubric.md) <br>
- [Pricing Sources Policy](artifact/references/pricing-sources.md) <br>
- [Execution Modes](artifact/references/execution-modes.md) <br>
- [Output Modes](artifact/references/output-modes.md) <br>
- [Runtime Safety](artifact/references/runtime-safety.md) <br>
- [Environment Variables and Dependencies](artifact/references/environment-vars.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tankisstank/benchmark-model-provider) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown, HTML, PDF, YAML, JSON, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces versioned benchmark specs, raw per-model answer files, raw metrics JSON, score breakdown JSON, markdown summaries, HTML landing pages, PDFs when requested, and publish metadata when delivery occurs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
