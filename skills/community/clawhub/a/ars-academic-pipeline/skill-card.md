## Description:

10-stage end-to-end research-to-publication pipeline orchestrator on Hermes Agent, covering planning, research, drafting, review, revision, polish, ethics, disclosure, formatting, and delivery with resume support.

This skill is for research and development only.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

CC BY-NC 4.0

## Use Case:

Researchers, academic writers, and agent operators use this skill to coordinate a staged research-to-publication workflow that produces plans, research syntheses, manuscript drafts, reviews, revisions, ethics checks, disclosures, formatted outputs, and delivery packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential manuscripts, unpublished research, reviewer correspondence, or private chat history may be processed through the AI workflow.

Mitigation: Use the skill only with material appropriate for the configured AI provider, and remove confidential or private content before running pipeline stages.

Risk: Pipeline state and stage outputs may be retained long term in session storage or Hindsight memory.

Mitigation: Disable or avoid Hindsight retention unless long-term storage is intended, and periodically review or clear retained session artifacts.

Risk: Generated revisions, process records, and manuscript diffs may contain inaccurate or unintended changes.

Mitigation: Inspect generated records, manuscript diffs, citations, and final publication files before sharing or submitting them.

Risk: Credential handling instructions are under-scoped for durable shell configuration.

Mitigation: Prefer session-scoped secrets and avoid placing API keys or private credentials in shell startup files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andyrenxu7255/skills/ars-academic-pipeline)
- [Original Academic Research Skills Repository](https://github.com/Imbad0202/academic-research-skills)
- [Wang and Zhang 2026 Collaboration Depth Paper](https://doi.org/10.1186/s41239-026-00585-x)
- [Scientific Reports 2023 Reference](https://doi.org/10.1038/s41598-023-41032-5)
- [GPTZero NeurIPS Citation Hallucination Reference](https://gptzero.me/news/neurips/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown and structured text, with optional LaTeX and publication-package file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stage-gated outputs may include project plans, research briefs, bibliographies, syntheses, manuscript drafts, review reports, revision plans, disclosure statements, formatted deliverables, and process records.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
