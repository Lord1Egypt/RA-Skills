## Description: <br>
Daily Game News crawls multiple game-news sources, categorizes articles, and generates daily reports for Feishu delivery and local Word/text archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CzwFelix](https://clawhub.ai/user/CzwFelix) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Gaming analysts, news curators, and operations teams use this skill to collect daily game-industry articles, group them into practical categories, and publish or archive a dated report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled crawling and report delivery can expose collected report content through outbound requests or a configured messaging workflow. <br>
Mitigation: Use approved public news sources, add URL allowlisting, and review messaging destinations before scheduling. <br>
Risk: The RSS helper disables normal TLS certificate verification. <br>
Mitigation: Restore TLS verification or disable the RSS helper before using the skill with sensitive sources. <br>
Risk: Generated reports are stored locally in the workspace reports directory. <br>
Mitigation: Apply local access controls and retention policies, and avoid using the crawler for internal or sensitive URLs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CzwFelix/daily-game-news) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report plus Word (.docx) and text archive files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include categorized article titles, sources, publication times, links, and optional summaries.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence; artifact CHANGELOG lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
