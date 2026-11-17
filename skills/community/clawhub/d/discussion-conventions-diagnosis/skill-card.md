## Description:

Diagnoses academic-writing conventions in the Discussion section of an English psychology research paper, checking achievement and contribution claims, limitations, future work, citation density and function, and hedging without generating or rewriting prose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laninga](https://clawhub.ai/user/laninga)

### License/Terms of Use:

MIT-0

## Use Case:

External academic writers, students, instructors, and researchers use this skill to audit psychology research-paper Discussion sections for contribution claims, limitations, future-work specificity, citation function, and appropriate hedging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers could cause the skill to be invoked outside its intended academic-writing context.

Mitigation: Use it specifically for English psychology research-paper Discussion sections and confirm the provided diagnosis against the paper's actual study design.

Risk: Some reference guidance is partly Chinese, which may be harder for reviewers who do not read Chinese to audit.

Mitigation: Have bilingual or domain-aware reviewers check the rubric and examples before relying on the diagnostic conventions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laninga/skills/discussion-conventions-diagnosis)
- [Conventions rubric](references/rubric.md)
- [Conventions checklist](references/checklist.md)
- [Example: Results-Type Contribution](references/examples/good_costello_2021_results_contribution.md)
- [Example: Limitations + Future Work](references/examples/good_ebert_2020_limitations_future.md)
- [Example: Method-Type Contribution](references/examples/good_epskamp_2018_method_contribution.md)
- [Example: Multiple Contribution Types](references/examples/good_midgley_2020_three_contributions.md)
- [Example: Synthetic - Missing Limitations](references/examples/bad_synthetic_no_limitations.md)
- [Example: Synthetic - Vague Achievement](references/examples/bad_synthetic_vague_achievement.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diagnostic report with checklist-style findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not generate or rewrite prose; provides structured diagnostic feedback only.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
