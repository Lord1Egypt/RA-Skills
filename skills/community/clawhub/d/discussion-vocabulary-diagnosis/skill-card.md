## Description:

Diagnoses vocabulary in the Discussion section of an English psychology research paper, including academic register, academic expressions, modal verb appropriateness, hedging, colloquialisms, terminology consistency, and psychology-specific lexis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laninga](https://clawhub.ai/user/laninga)

### License/Terms of Use:

MIT-0

## Use Case:

Students, academic writers, editors, and research mentors use this skill to audit Discussion-section vocabulary in English psychology papers for academic register, hedging, modal verb use, terminology consistency, and discipline-specific wording. The skill reports issues and suggestions but does not generate or rewrite prose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers may activate the skill for general vocabulary requests outside psychology-paper Discussion sections.

Mitigation: Confirm that the user is asking for Discussion-section academic vocabulary diagnosis before applying the rubric.

Risk: Some reference guidance is written in Chinese or mixed Chinese-English, which may affect reviewers who expect English-only guidance.

Mitigation: Use the bilingual references as diagnostic evidence and explain final feedback in the user's requested language.

Risk: Vocabulary diagnosis can be mistaken for full prose rewriting.

Mitigation: Keep outputs to categorized findings and localized suggestions, and avoid generating or rewriting complete passages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laninga/skills/discussion-vocabulary-diagnosis)
- [High-Frequency Academic Vocabulary for the Discussion Section](references/academic-vocabulary.md)
- [Modal Verbs in Research Writing](references/modal-verbs.md)
- [Vocabulary Rubric - Discussion](references/rubric.md)
- [Vocabulary Checklist - Discussion](references/checklist.md)
- [Contribution Language Example](references/examples/good_costello_2021_contribution_language.md)
- [Hedging Variety Example](references/examples/good_midgley_2020_hedging_variety.md)
- [Field-Specific Academic Vocabulary Example](references/examples/good_ebert_2020_field_specific_terms.md)
- [Methodological Vocabulary Example](references/examples/good_epskamp_2018_methodology_terms.md)
- [Cognitive Verb Variety Example](references/examples/good_schmidt_2016_cognitive_verbs.md)
- [Synthetic Over-Claim Example](references/examples/bad_synthetic_overclaim.md)
- [Synthetic Vague Future Work Example](references/examples/bad_synthetic_vague_future.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnosis with categorized findings, sentence-level notes, severity labels, and suggested replacements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not rewrite full prose; outputs diagnostic feedback and localized replacement suggestions.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
