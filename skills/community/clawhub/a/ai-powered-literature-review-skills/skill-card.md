## Description: <br>
Literature Reviewer Skill helps agents perform systematic Chinese and English academic literature reviews by generating search strategies, using browser automation across academic databases, deduplicating and checking paper metadata, formatting GB/T 7714-2015 citations, and drafting structured Markdown review documents. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[stephenlzc](https://clawhub.ai/user/stephenlzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, students, and academic-writing agents use this skill to collect, organize, analyze, and synthesize literature for a defined research topic. It is intended for academic research workflows that need bilingual search coverage, citation formatting, and Markdown review outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can use the current browser login state for academic sites. <br>
Mitigation: Run the skill in Docker, a dedicated browser profile, or incognito mode, and avoid sensitive logged-in accounts. <br>
Risk: Automated searches and downloads can trigger academic database rate limits, CAPTCHA checks, account restrictions, or terms-of-service issues. <br>
Mitigation: Review each database's terms, keep request volumes reasonable, and be prepared to handle manual verification or stop the run. <br>
Risk: Research outputs and downloaded metadata are retained in local sessions and output directories. <br>
Mitigation: Limit write access to the sessions and output directories and clear them when the research data should not be retained. <br>


## Reference(s): <br>
- [CNKI Literature Search Guide](references/cnki-guide.md) <br>
- [Academic Database Access Guide](references/database-access.md) <br>
- [GB/T 7714-2015 Reference Format Guide](references/gb-t-7714-2015.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown reports with JSON session files and plain-text citation lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates session-scoped files such as references.md, papers_analysis.md, literature_review.md, gb7714_citations.txt, and intermediate paper metadata JSON.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence, mcp.json, install.yaml, README.md, SECURITY.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
