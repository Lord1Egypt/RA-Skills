## Description:

Pre-ingestion verification for epistemic quality in RAG systems that qualifies documents before knowledge-base ingestion and produces CGD files while validating SOT files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frmoretto](https://clawhub.ai/user/frmoretto)

### License/Terms of Use:

CC-BY-4.0

## Use Case:

Developers, knowledge-base maintainers, and AI workflow reviewers use this skill before RAG ingestion or AI handoff to identify unqualified claims, enforce uncertainty markers, produce Clarity-Gated Documents, and route claims to human verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill verifies document form and epistemic qualification, not factual truth.

Mitigation: Require human-in-the-loop confirmation before treating CGD or SOT outputs as verified or ready for RAG ingestion.

Risk: The security evidence reports a document_hash.py validation weakness and cautions against treating it as strong authenticity protection.

Mitigation: Use document_hash.py only as a deterministic helper and pair it with independent review or stronger integrity controls until the issue is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/frmoretto/skills/clarity-gate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown review reports and CGD Markdown files, with optional plain-text output from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CGD outputs use .cgd.md structure with HITL status fields and document hash metadata.]

## Skill Version(s):

2.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
