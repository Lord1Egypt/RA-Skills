## Description: <br>
Generates a Markdown AI news digest from configured RSS feeds, with keyword ranking, short summaries, language grouping, and media previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swordman20](https://clawhub.ai/user/swordman20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to collect AI industry updates from configured RSS feeds and generate a structured daily Markdown report for review or publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches external RSS feeds and includes third-party article text, links, and image URLs in the generated report. <br>
Mitigation: Review the RSS feed list before use and treat generated article content, links, and images as untrusted third-party material. <br>
Risk: The cron example can schedule recurring external feed fetching and local report generation. <br>
Mitigation: Enable scheduled execution only when daily automated fetching is intended and the runtime environment is appropriate. <br>
Risk: Runtime dependencies must be available for the script to parse YAML configuration. <br>
Mitigation: Install dependencies such as PyYAML from trusted package sources before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swordman20/ai-news-feishu-doc) <br>
- [RSS feed configuration](assets/ai-news-rss.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands] <br>
**Output Format:** [Markdown file generated from configured RSS feed content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated local AI news report and prints fetch and article-count status to the console.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
