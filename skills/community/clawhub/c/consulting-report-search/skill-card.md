## Description: <br>
Consulting and industry report search and QA skill that prioritizes iResearch free reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiyenwong](https://clawhub.ai/user/hiyenwong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to find public consulting, industry, and market research reports, then retrieve report details or answer questions using visible report evidence. It is most useful for report discovery, source-grouped candidate lists, and conservative summaries grounded in public iResearch and QuestMobile content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to iResearch, QuestMobile, and fallback web-search services. <br>
Mitigation: Avoid using sensitive or confidential terms in report-search queries unless the host environment permits disclosure to those public services. <br>
Risk: A broad report-search trigger could activate for vague market-research requests. <br>
Mitigation: Use normal host-agent intent checks and confirm the user wants public consulting-report search before running networked searches. <br>
Risk: Public summaries, catalogs, and chart lists may not support exact findings from full reports. <br>
Mitigation: Keep answers grounded in visible evidence and state the evidence boundary when page-level data or paid/private content is not available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hiyenwong/consulting-report-search) <br>
- [Report Source Notes](references/iresearch-api.md) <br>
- [iResearch report listing](https://www.iresearch.com.cn/report.shtml) <br>
- [QuestMobile report listing](https://www.questmobile.com.cn/research/reports/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON with report links, source grouping, evidence snippets, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include report metadata, detail summaries, chart/catalog evidence, online reader links, and image links when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
