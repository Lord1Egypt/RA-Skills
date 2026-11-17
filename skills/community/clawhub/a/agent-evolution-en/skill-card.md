## Description:

Capture research outcomes and refine agent practices over time by recording reusable findings, retrieving them on later tasks, and evaluating whether practices should become durable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marike86](https://clawhub.ai/user/marike86)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and knowledge workers use this skill to preserve reusable research outcomes, retrieve them on later tasks, and test whether practices merit adoption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The memory utility reads and writes project files, and the scan did not verify the host's permission enforcement or declared tool scope.

Mitigation: Use only a project directory and memory interface authorized for the task; keep sensitive information to the minimum needed and review proposed durable practice changes before adopting them.

## Reference(s):

- [Server-resolved source repository](https://github.com/marike86/scientific-ideation_skill/tree/main/skills/agent-evolution-en)
- [Creative metacognition framework](https://doi.org/10.1016/j.plrev.2023.07.002)
- [Creative Cognition and Geneplore](https://mitpress.mit.edu/9780262061506/creative-cognition/)
- [Dual-space search](https://doi.org/10.1016/0364-0213%2888%2990007-9)
- [CoALA modular memory architecture](https://openreview.net/pdf/07475727a2787df12052196b9f2624497ef3c3bd.pdf)
- [Memory and Evaluation Operations](references/operations.md)
- [Product Patterns and Integration](references/product-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, JSON, Shell commands, Files]

**Output Format:** [Guidance and project memory records or files in Markdown and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory records can include scope, evidence status, source, and recall or review triggers.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
