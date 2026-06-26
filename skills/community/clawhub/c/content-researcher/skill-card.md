## Description: <br>
Content Researcher searches, collects, and summarizes articles, videos, and news into a structured material library with keyword and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, researchers, and developers use this skill to run multi-keyword web research, deduplicate search results, and produce structured Markdown or JSON reports with optional AI summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and snippets may be sent to the configured search and summarization services. <br>
Mitigation: Avoid confidential keywords or sensitive snippets unless those services are approved for that data. <br>
Risk: The report is written to the requested output path and can overwrite an existing file. <br>
Mitigation: Choose a dedicated output path and review it before running the skill. <br>
Risk: The skill depends on local claw and summarize commands. <br>
Mitigation: Install and run the skill only in environments where those local tools are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/content-researcher) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json] <br>
**Output Format:** [Markdown report or JSON document written to a user-selected output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally include AI-generated summaries for each search result when the summarize dependency is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
