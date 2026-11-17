## Description:

Generate ARRIVE 2.0 compliant animal research protocols with structured experimental design, sample size calculations, and reporting checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theresayao0614-sudo](https://clawhub.ai/user/theresayao0614-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, institutional reviewers, and developers use this skill to draft or validate ARRIVE 2.0 animal-study protocols, checklists, sample-size rationales, randomization plans, and ethics review materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated animal-study protocols may omit study-specific, institution-specific, or species-specific requirements.

Mitigation: Review generated protocols with qualified ethics, veterinary, and statistical reviewers before using them for approvals, experiments, or publication.

Risk: The skill writes generated protocol or checklist files locally, which can overwrite or mix outputs if reused in a shared directory.

Mitigation: Run the skill in a dedicated output directory and set explicit output paths for generated files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theresayao0614-sudo/skills/arrive-guideline-architect-2)
- [ARRIVE 2.0 Essential 10 Checklist](artifact/arrive_checklist.md)
- [Example ARRIVE Protocol](artifact/example_protocol.md)
- [Example Study Brief](artifact/example_study_brief.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown protocols and checklists, plain-text validation reports, and JSON study-brief inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read local study briefs or protocol files and write generated protocol or checklist files to a user-selected output path.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
