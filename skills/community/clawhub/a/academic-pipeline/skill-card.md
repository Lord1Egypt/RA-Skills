## Description:

Academic Pipeline v1 orchestrates a full academic paper workflow from literature search through finalization, coordinating dependent research, writing, review, revision, integrity-checking, humanization, and process-documentation skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric-promax](https://clawhub.ai/user/eric-promax)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and academic-writing teams use this skill to coordinate an end-to-end paper production workflow with staged handoffs, checkpoints, integrity verification, review, revision, final formatting, and process records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate persistent process records from conversation history, including user text and behavioral scoring.

Mitigation: Treat generated process records and PDFs as sensitive, review them before sharing, and avoid using the pipeline with confidential drafts or reviewer comments unless the environment is approved for that data.

Risk: Optional cross-model verification can share reference data with another model.

Mitigation: Disable or avoid cross-model verification unless the user and deployment owner accept that data-sharing posture.

Risk: The server security summary flags inconsistent integrity-gate rules and warns that the integrity gate is not a guarantee after failed verification.

Mitigation: Require human review before relying on integrity results, and do not proceed after failed verification unless the user explicitly records the rationale and accepted limitations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eric-promax/skills/academic-pipeline)
- [Pipeline State Machine](references/pipeline_state_machine.md)
- [Mode Advisor](references/mode_advisor.md)
- [Integrity Review Protocol](references/integrity_review_protocol.md)
- [AI Research Failure Mode Checklist](references/ai_research_failure_modes.md)
- [Claim Verification Protocol](references/claim_verification_protocol.md)
- [Plagiarism Detection Protocol](references/plagiarism_detection_protocol.md)
- [External Review Protocol](references/external_review_protocol.md)
- [Two-Stage Review Protocol](references/two_stage_review_protocol.md)
- [Process Summary Protocol](references/process_summary_protocol.md)
- [Reproducibility](references/reproducibility_audit.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, status dashboards, verification and review reports, handoff schemas, and optional downstream document-generation commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate downstream production of BibTeX, JSON metadata, drafts, DOCX, LaTeX, PDF, and bilingual process-record files when the dependent skills and tools are available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 3.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
