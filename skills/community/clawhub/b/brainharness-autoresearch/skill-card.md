## Description:

Runs iterative prompt experiments to evaluate and improve AI agent skills against user-defined criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zning1994](https://clawhub.ai/user/zning1994)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use it to benchmark prompt variants against defined evaluations and improve an existing skill's instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Experiments can automatically rewrite the target skill prompt.

Mitigation: Run on a copy or version-controlled skill and review the diff before retaining changes.

Risk: Prompt and evaluation content is sent to third-party LLM APIs.

Mitigation: Do not use confidential prompts or evaluation data without approval for the chosen provider.

Risk: Installation commands may fetch a changing release.

Mitigation: Pin the installed version where possible.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zning1994/skills/brainharness-autoresearch)
- [Project homepage (listed in skill metadata)](https://github.com/zning1994/brainharness-autoresearch)
- [Evaluation guide](eval-guide.md)
- [Autoresearch methodology](https://github.com/karpathy/autoresearch)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance and JSON evaluation definitions; experiment results in TSV and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write revised prompt files, experiment logs, and an original-prompt backup.]

## Skill Version(s):

0.3.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
