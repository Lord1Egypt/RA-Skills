## Description: <br>
B站评论分析 retrieves first-level Bilibili comments from a video link or BV ID, supports page-by-page review and four-dimension sentiment analysis, and can generate a local interactive HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brand operators, content planners, product managers, and researchers use this skill to retrieve Bilibili video comments, inspect audience feedback, and summarize sentiment, demand, and competitor signals. It supports lightweight public-comment monitoring with optional local HTML reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill sends a Bilibili BV ID and the RedFox API key to redfox.hk. <br>
Mitigation: Use only a RedFox-issued key, confirm its scope and revocability, and avoid exposing the key in code, prompts, logs, or output files. <br>
Risk: Generated HTML reports can include commenter names, profile links, timestamps, IP regions, and AI-generated summary HTML saved locally. <br>
Mitigation: Review reports before sharing, store them appropriately, and remove sensitive or unnecessary comment data before distribution. <br>


## Reference(s): <br>
- [Core Workflow](references/core_workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/bilibili-comment) <br>
- [RedFox Hub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with work details, comment tables, and analysis; scripts return JSON and can write an optional local HTML report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY. Comment retrieval sends the BV ID and API key to redfox.hk and fetches one page of 20 first-level comments per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
