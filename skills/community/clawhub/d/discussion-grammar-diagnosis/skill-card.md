## Description:

Diagnoses grammar in Discussion sections of English psychology research papers, covering tense choice, subject-verb agreement, article usage, voice, and punctuation without generating or rewriting prose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laninga](https://clawhub.ai/user/laninga)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, and academic-writing reviewers use this skill to diagnose grammar issues in English psychology research-paper Discussion sections. It supports move-by-move tense auditing, grammar issue lists, and severity-ranked feedback without rewriting the submitted prose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad grammar-check trigger may route ordinary grammar requests to this specialized Discussion-section skill.

Mitigation: Confirm that the user is asking about grammar in an academic Discussion section before applying the skill's rubric.

Risk: Diagnostic advice may be incomplete or misaligned with a journal, instructor, or field-specific style requirement.

Mitigation: Present findings as review guidance and ask the user to confirm final wording against the applicable publication or course requirements.

Risk: Reference materials include Chinese explanatory labels alongside English academic-writing examples.

Mitigation: Keep user-facing feedback in the user's language and avoid relying on untranslated labels when clarity matters.

## Reference(s):

- [Grammar Rubric](references/rubric.md)
- [Grammar Checklist](references/checklist.md)
- [Example: Within-Paragraph Tense Switch](references/examples/good_costello_2021_present_past_switch.md)
- [Example: Modal + Present Simple](references/examples/good_epskamp_2018_modal_present.md)
- [Example: Tense Alignment](references/examples/good_midgley_2020_tense_alignment.md)
- [Example: Active/Passive Balance](references/examples/good_schmidt_2016_active_passive_balance.md)
- [Example: Synthetic Tense Confusion](references/examples/bad_synthetic_tense_confusion.md)
- [Example: Synthetic Tense Consistency Violation](references/examples/bad_synthetic_tense_consistency.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diagnostic report with tables, issue lists, and severity-ranked findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnostic feedback only; does not generate or rewrite user prose.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
