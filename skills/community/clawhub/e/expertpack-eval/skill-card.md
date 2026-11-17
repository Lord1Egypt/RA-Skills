## Description:

Measure ExpertPack EK (Esoteric Knowledge) ratio and run automated quality evaluations against pack-powered agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhearn](https://clawhub.ai/user/brianhearn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluators use this skill to measure how much ExpertPack content is esoteric to frontier models and to score pack-powered agent answers with LLM-as-judge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pack propositions, eval questions, expected answers, and agent responses may be sent to OpenRouter or to a configured evaluation endpoint.

Mitigation: Use a local or trusted endpoint for sensitive packs and run the skill only when sharing those evaluation inputs with OpenRouter is acceptable.

Risk: Credential discovery can use OPENROUTER_API_KEY and OpenClaw configuration files.

Mitigation: Provide credentials intentionally in an isolated environment and review which API key source will be used before running evaluations.

Risk: External dependencies and network calls are required for full evaluation behavior.

Mitigation: Prefer an isolated virtual environment with pinned dependencies and review generated YAML outputs before using scores for release decisions.

## Reference(s):

- [ExpertPack homepage](https://expertpack.ai)
- [Companion ExpertPack skill](https://clawhub.ai/skills/expertpack)
- [ExpertPack GitHub project](https://github.com/brianhearn/ExpertPack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, YAML]

**Output Format:** [Markdown guidance with shell commands and YAML evaluation result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces EK ratio summaries, per-proposition classifications, quality scores, latency metrics, and LLM-as-judge token usage when evaluations are run.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
