## Description:

Translate and analyze academic CS papers in English and Chinese, summarize content, answer paper-specific questions, and compare related works.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levinaz69](https://clawhub.ai/user/levinaz69)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and students use this skill to ingest academic papers from arXiv links or PDFs, translate English and Chinese content, summarize methods and findings, and answer follow-up questions with paper-grounded context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download academic papers and use web search for supplementary context.

Mitigation: Review paper URLs and search-derived context before relying on outputs, and use trusted sources for paper ingestion.

Risk: The skill may temporarily store current paper metadata and extracted text under /tmp.

Mitigation: Avoid processing sensitive unpublished PDFs unless the runtime protects /tmp appropriately, and clear temporary files when the session no longer needs them.

Risk: Large PDFs can increase processing time, memory use, and output length.

Mitigation: Use page limits or batch extraction and translation for long papers.

## Reference(s):

- [Academic Translator ClawHub page](https://clawhub.ai/levinaz69/skills/academic-translator)
- [arXiv](https://arxiv.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with extracted paper metadata, translations, summaries, Q&A responses, citations, and occasional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use temporary paper metadata and extracted text under /tmp for multi-turn follow-up.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
