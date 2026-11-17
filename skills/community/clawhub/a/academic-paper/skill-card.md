## Description:

Academic Paper is a multi-agent academic writing workflow for planning, drafting, revising, citation checking, bilingual abstracts, AI-use disclosure, and manuscript formatting.

This skill is for research and development only.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

CC BY-NC 4.0

## Use Case:

Researchers, students, and academic writers use this skill to structure and produce scholarly manuscripts, literature reviews, reviewer responses, citation audits, bilingual abstracts, and journal-ready formatting outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manuscript or reference content may be processed by delegated agents or sent to third-party AI providers when optional cross-model verification is enabled.

Mitigation: Use the skill only with content appropriate for AI-provider processing, and leave ARS_CROSS_MODEL disabled unless the user explicitly accepts third-party API processing and costs.

Risk: Provider API keys may be exposed or retained if stored in shell profile files for optional cross-model checks.

Mitigation: Avoid storing provider API keys in shell profiles; prefer temporary session-scoped environment variables and remove them after use.

Risk: Generated drafts may contain hidden citation comments, automatic citation edits, or unsupported academic claims.

Mitigation: Review drafts, citation changes, DOI checks, and disclosure statements before sharing or submitting manuscripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyrenxu7255/skills/academic-paper)
- [Original repository metadata](https://github.com/Imbad0202/academic-research-skills)
- [Attribution notice](ATTRIBUTION.md)
- [Mode selection guide](references/mode_selection_guide.md)
- [Paper structure patterns](references/paper_structure_patterns.md)
- [Citation format switcher](references/citation_format_switcher.md)
- [Journal submission guide](references/journal_submission_guide.md)
- [Disclosure mode protocol](references/disclosure_mode_protocol.md)
- [Cross-model verification](shared/cross_model_verification.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown manuscript sections, academic tables, citation reports, disclosure statements, LaTeX snippets, reviewer-response plans, and formatting guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bilingual English and Traditional Chinese abstracts, journal-format templates, and citation-integrity checklists.]

## Skill Version(s):

3.1.4 (source: server release metadata; artifact frontmatter reports 3.1.1-hermes-1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
