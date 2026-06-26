## Description: <br>
Accurately and efficiently extracts and analyzes pharmaceutical company intelligence to provide professional company profiles and investment or collaboration recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and life science teams use this skill to research pharmaceutical companies, including company overviews, financing history, R&D pipelines, patent activity, and drug deals or collaborations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PatSnap API key and uses MCP URLs that can embed credentials. <br>
Mitigation: Use a dedicated API key where possible, keep MCP connection URLs private, and rotate the key if it may have been exposed. <br>
Risk: Company names, research prompts, and tool parameters may be sent to PatSnap LifeScience services during use. <br>
Mitigation: Use the skill only for work appropriate for PatSnap processing and avoid submitting confidential information unless the user has approved that disclosure. <br>
Risk: The skill depends on the configured PatSnap MCP endpoint being authentic and reachable. <br>
Mitigation: Verify the PatSnap endpoint before adding it and stop processing if the MCP connectivity check fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patsnaplifescience/company-profiling) <br>
- [PatSnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Dev Portal](https://open.patsnap.com/devportal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown report text with setup guidance and inline shell commands when MCP connectivity is not configured.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected to include an abstract, Roman-numeral sections, a conclusion, dates, disclaimer text, data source notes, and evidence-backed summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter metadata says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
