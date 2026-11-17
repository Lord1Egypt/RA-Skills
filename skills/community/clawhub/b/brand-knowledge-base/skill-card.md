## Description:

Build a reusable brand knowledge package from uploaded brand documents and/or a filled intake form.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, marketing, support, and knowledge operations teams use this skill to convert company materials or a structured intake form into a reusable brand single source of truth for downstream content, sales, FAQ, RAG, and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded brand materials and intake data are sent in full to the configured OpenAI-compatible API provider.

Mitigation: Use only organization-approved API providers and avoid uploading secrets, confidential customer records, regulated data, or unredacted transcripts.

Risk: A raw source_bundle.md may be kept in the output directory.

Mitigation: Review and remove or protect source_bundle.md before sharing outputs or loading them into production workflows.

Risk: Pinned document-processing dependencies may need security updates before PDF processing.

Mitigation: Review and update vulnerable pinned dependencies before processing PDFs.

Risk: Generated brand claims may be incomplete or require verification when source materials are sparse.

Mitigation: Keep human review in the publication workflow and resolve fields marked as pending confirmation before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljseeking/skills/brand-knowledge-base)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Manifest](artifact/manifest.json)
- [Brand knowledge schema](artifact/templates/brand_knowledge_base.json)
- [Intake guidance](artifact/prompts/intake.md)
- [Extraction guidance](artifact/prompts/extraction.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, YAML, guidance]

**Output Format:** [Generated files including brand_knowledge_base.json, brand_knowledge_base.yaml, brand_knowledge_base.md, faq.md, glossary.md, standard_messaging.md, llms.txt, analysis_report.md, and optional intake templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retain source_bundle.md containing the raw supplied materials when building from source inputs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
