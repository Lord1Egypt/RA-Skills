## Description:

Bioinfo Daily generates Chinese daily reports of recent bioinformatics and oncology papers by querying PubMed, filtering high-impact journals, and summarizing selected research highlights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangwang](https://clawhub.ai/user/shixiangwang)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, bioinformatics teams, and oncology teams use this skill to create a daily digest of high-impact PubMed literature across bioinformatics, tumor immunology, single-cell sequencing, spatial transcriptomics, and clinical cancer research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shell wrapper sources a project-local .env file as shell code.

Mitigation: Set NCBI_EMAIL and NCBI_API_KEY through OpenClaw config or the process environment, and avoid the project-local .env wrapper path unless the file is created and reviewed locally.

Risk: Documentation claims .env is git-ignored, but the security evidence says that claim is unsupported.

Mitigation: Add and verify a .gitignore before creating any credential file, and keep unrelated secrets out of the skill directory.

Risk: Feishu publishing appears manual or incomplete unless separate upload logic is added.

Mitigation: Treat generated files as manual publishing artifacts or review any added Feishu upload implementation before automation.

## Reference(s):

- [Bioinfo Daily ClawHub listing](https://clawhub.ai/shixiangwang/skills/bioinfo-daily-skill)
- [PubMed E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [NCBI E-utilities API keys](https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese daily report text and optional Markdown files with command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes report artifacts under /tmp/bioinfo_daily_YYYYMMDD.txt and, through the wrapper, /tmp/bioinfo_daily_YYYYMMDD.md.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
