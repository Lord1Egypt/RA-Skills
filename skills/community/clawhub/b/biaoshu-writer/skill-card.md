## Description:

Biaoshu Writer helps an agent parse Chinese tender files, draft technical bid content against scoring criteria, check chapter word counts, humanize Chinese text, merge chapters, and produce formatted Word documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliwenjing](https://clawhub.ai/user/wuliwenjing)

### License/Terms of Use:

MIT-0

## Use Case:

External bid writers and procurement teams use this skill to turn tender files and scoring criteria into Chinese technical bid drafts, supporting Markdown chapter generation, quality checks, and DOCX conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender documents may contain sensitive procurement, pricing, or project information.

Mitigation: Use the skill only in a controlled workspace and avoid sending documents to public OCR or conversion services unless approved by the organization.

Risk: Generated bid content may be incomplete, inaccurate, or misaligned with tender scoring requirements.

Mitigation: Require human review of outlines, chapter drafts, word-count checks, and final DOCX output before submission.

Risk: Dependency and font installation can introduce supply-chain exposure.

Mitigation: Install pinned Python dependencies from trusted sources and obtain SimSun.ttf only from verified systems or approved internal software sources.

Risk: DOCX metadata rewriting and AI-trace removal can affect document provenance.

Mitigation: Review document metadata and keep an internal audit copy before submitting or distributing generated Word files.

## Reference(s):

- [Biaoshu Writer ClawHub listing](https://clawhub.ai/wuliwenjing/skills/biaoshu-writer)
- [humanizer-zh reference](references/humanizer-zh.md)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, local command guidance, and generated DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts for tender-file parsing, chapter word-count checks, Markdown merging, and DOCX conversion with configurable document formatting.]

## Skill Version(s):

5.4.0 (source: server release metadata and SKILL.md changelog, released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
