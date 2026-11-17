## Description:

Summarize clinical case notes into specialty briefs, including structured specialty briefs, differential diagnosis lists, and key findings summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, healthcare staff, and clinical documentation teams can use this skill to turn raw case notes, symptoms, lab results, or handover details into structured drafts for review. It supports clinical briefing workflows but requires qualified professional judgment before any clinical decision or record use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical notes, lab results, and other inputs may contain sensitive medical information that is printed to the terminal.

Mitigation: Use de-identified notes where possible, avoid shared or logged shells for PHI, and confirm local handling practices before use.

Risk: Generated briefs, differential diagnoses, lab interpretations, and next-step suggestions may be incomplete or clinically incorrect.

Mitigation: Treat all output as a draft and rely on qualified clinicians for diagnosis, treatment, and record-entry decisions.

Risk: The generated text includes BytesAgain branding that may be inappropriate in clinical records.

Mitigation: Remove branding before copying generated text into clinical systems or records.

## Reference(s):

- [Bytesagain Clinical Brief on ClawHub](https://clawhub.ai/loutai0307-prog/skills/bytesagain-clinical-brief)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured plain text and Markdown-style clinical briefs with command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include raw user-provided clinical text and should be reviewed before clinical use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
