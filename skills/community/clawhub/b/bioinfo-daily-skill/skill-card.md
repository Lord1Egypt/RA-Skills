## Description: <br>
Bioinfo Daily searches PubMed for recent high-impact bioinformatics and oncology papers and generates a Chinese daily report with summaries, highlights, journal metadata, and source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShixiangWang](https://clawhub.ai/user/ShixiangWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, lab teams, and developers use this skill to generate daily literature briefings for bioinformatics, cancer immunology, single-cell sequencing, spatial transcriptomics, and oncology clinical progress. It can be run manually or through scheduled OpenClaw workflows when PubMed API credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PubMed API credentials may be exposed if stored in broadly readable local files. <br>
Mitigation: Prefer OpenClaw configuration or environment variables; if a .env file is used, limit it to NCBI_EMAIL and NCBI_API_KEY and keep it writable only by trusted users. <br>
Risk: The optional web_search helper can send research topics to the configured external search provider. <br>
Mitigation: Avoid confidential or sensitive research topics when using the optional search helper, or run only the PubMed-based workflow in a controlled environment. <br>
Risk: Scheduled runs can repeatedly call external services and publish or stage generated reports. <br>
Mitigation: Review the scheduled command, configured channel, and generated report content before enabling automated delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ShixiangWang/bioinfo-daily-skill) <br>
- [PubMed E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [NCBI E-utilities API Key Guidance](https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Plain text and Markdown daily report files with inline article metadata and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated report files under /tmp and may print shell commands for retrieving generated Markdown.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
