## Description:

Complete Academic Research & Writing Suite for one-click installation of the Academic Pipeline ecosystem, including literature search, deep research, paper writing, peer review, humanization, IMA knowledge-base support, and integrity verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric-promax](https://clawhub.ai/user/eric-promax)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, researchers, and academic writers use this skill to install and run a full academic research and writing workflow. It coordinates literature search, research synthesis, drafting, integrity checks, peer review, revision, humanization, final formatting, and process summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suite can replace multiple local skills during installation.

Mitigation: Review the installed skill list and installation script behavior before deployment, and keep backups of any local skills that may be overwritten.

Risk: Some bundled workflows may use browser automation or Chrome remote debugging.

Mitigation: Avoid enabling Chrome remote debugging for a daily browser profile; use a separate controlled profile when browser automation is needed.

Risk: IMA notes and knowledge-base workflows may rely on user API credentials or custom endpoints.

Mitigation: Use trusted IMA credentials only, avoid setting IMA_BASE_URL or custom baseUrl values unless reviewed, and keep credentials out of shared transcripts and outputs.

Risk: Humanization stages may affect academic disclosure and integrity obligations.

Mitigation: Follow institutional AI-use disclosure, citation, and authorship rules before using outputs in academic submissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eric-promax/skills/academic-pipeline-suite)
- [Complete Usage Guide](https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg)
- [ClawHub Suite Page](https://clawhub.ai/eric-promax/academic-suite)
- [Support and Issues](https://github.com/eric-promax/academic-agents/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, shell commands, configuration prompts, and generated academic documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce research plans, literature matrices, paper drafts, review reports, revision responses, integrity reports, final document instructions, and process summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
