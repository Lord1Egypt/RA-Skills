## Description:

Diagnoses logical argumentation in English psychology research Discussion sections by checking argument chains, causal claims, epistemic layering, counter-argument handling, generalization scope, and internal consistency without generating or rewriting prose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laninga](https://clawhub.ai/user/laninga)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, editors, and writing-support agents use this skill to review the logic of English psychology research Discussion sections. It maps major claims to evidence and conclusions, audits causal language against study design, checks epistemic hedging, and flags unsupported generalizations or weak counter-argument handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers such as "check logic" may invoke the skill outside English psychology Discussion contexts.

Mitigation: Confirm that the input is an English psychology research Discussion section before applying its rubric and examples.

Risk: Bilingual supporting examples may cause mixed-language diagnostic output when the user has not requested a language.

Mitigation: Ask for or follow the user's preferred response language and keep the diagnosis in that language.

## Reference(s):

- [Logic Rubric](references/rubric.md)
- [Logic Checklist](references/checklist.md)
- [Example: Causal Chain Reasoning](references/examples/good_costello_2021_causal_chain.md)
- [Example: Data-Interpretation-Speculation Structure](references/examples/good_midgley_2020_data_interpretation_speculation.md)
- [Example: Addressing Alternative Explanations](references/examples/good_ebert_2020_alternatives_addressed.md)
- [Example: Honest Limitation without Over-Claim](references/examples/good_schmidt_2016_honest_limitation.md)
- [Example: Synthetic Causal Overreach](references/examples/bad_synthetic_causal_overreach.md)
- [Example: Synthetic Ignoring Alternative Explanations](references/examples/bad_synthetic_ignoring_alternatives.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured sections cover argument-chain mapping, causal-claim audit, epistemic-layer audit, counter-argument handling, and severity-ranked top issues; the skill does not generate or rewrite prose.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
