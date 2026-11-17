## Description:

Generates clinical case reports from patient records and formats them as GB/T 7713.2-2022-compliant Word documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanqing203](https://clawhub.ai/user/fanqing203)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, medical writers, and health-care documentation teams use this skill to draft clinical case reports from authorized patient records, check reference requirements, and produce formatted Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive patient records and examples include identifiable-looking patient details.

Mitigation: Use only authorized or de-identified patient material, avoid patient names in prompts and output filenames, and confirm document storage and retention controls before use.

Risk: Referenced knowledge files may be missing from the packaged artifact.

Mitigation: Verify required writing, citation, and Word-formatting references are bundled or otherwise available before relying on generated outputs.

Risk: Clinical statements and literature references may be incomplete, outdated, or unsuitable for the intended case.

Mitigation: Require qualified human review of clinical content, citation authenticity, source quality, and formatting before publication or care-related use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanqing203/skills/clinical-case-writer)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact examples](artifact/examples.md)
- [Word generation script](artifact/scripts/clinical_case_writer.py)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Clinical case report text, Markdown drafts, DOCX files, and validation notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain sensitive clinical content and should be generated only from authorized or de-identified patient material.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
