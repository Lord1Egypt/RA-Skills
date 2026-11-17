## Description:

Removes author names, affiliations, acknowledgments, contact details, and self-citation signals from manuscripts for double-blind peer review while preserving document structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googolme](https://clawhub.ai/user/googolme)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and academic authors use this skill to prepare DOCX, Markdown, or plain text manuscripts for double-blind journal or conference review. It helps redact author identifiers, acknowledgments, contact details, institutional affiliations, and first-person self-citation cues before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removed identifiers can appear in stdout, shared logs, or agent transcripts.

Mitigation: Run the skill in a controlled environment and avoid capturing terminal output in shared logs or transcripts.

Risk: The DOCX dependency is declared as an unpinned wrong package name.

Mitigation: Replace the dependency with a reviewed, pinned python-docx requirement before installation.

Risk: Automated redaction may miss identifiers in document metadata, figures, embedded objects, or hard-to-detect context.

Mitigation: Manually inspect the sanitized manuscript, document properties, figures, and metadata before submission.

Risk: A careless output path can place sanitized or intermediate files in the wrong location.

Mitigation: Choose the output path deliberately and verify the resulting file location before sharing or submitting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googolme/skills/blind-review-sanitizer)
- [ClawHub Publisher Profile](https://clawhub.ai/user/googolme)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Sanitized DOCX, Markdown, or plain text files with terminal status output and usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an input manuscript path and output path; optional author list and acknowledgment/self-citation handling flags affect redaction behavior.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
