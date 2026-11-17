## Description:

Spec-driven development assistant that helps agents write precise behavioral specs before coding or reverse-engineer specs from existing code for understanding and alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyan](https://clawhub.ai/user/yuanyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use AutoSpec to align on feature behavior before implementation, generate structured behavioral contracts, or extract factual specs from existing code before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated specs or code may omit security constraints for privacy-sensitive history summarization or network-facing URL validation.

Mitigation: Review generated specs and any implementation before use, with extra attention to privacy, logging, validation, and external request behavior.

Risk: Benchmark examples contain scanner alerts that could be mistaken for runtime behavior.

Mitigation: Treat evaluation outputs as examples and review the actual skill files when assessing installation or runtime risk.

## Reference(s):

- [AutoSpec ClawHub skill page](https://clawhub.ai/yuanyan/skills/auto-spec)
- [README](artifact/README.md)
- [Evaluation summary](artifact/evals/iteration-1/benchmark.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown behavioral specs with optional code when implementation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Specs are presented conversationally by default and written to files only when explicitly requested.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
