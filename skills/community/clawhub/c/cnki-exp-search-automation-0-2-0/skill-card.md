## Description: <br>
CNKI（中国知网）高级搜索自动化技能。使用浏览器自动化技术搜索文献并获取结果列表及摘要信息。建议在有头浏览器环境下使用以便于处理反机器人验证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and agents use this skill to run CNKI advanced searches, collect literature result metadata, and extract article abstracts for academic literature review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to control a browser on CNKI and save extracted literature data. <br>
Mitigation: Use a dedicated browser profile when possible, review output file paths, avoid excessive scraping, and follow CNKI access rules and terms. <br>
Risk: CNKI may present anti-robot verification during automated browsing. <br>
Mitigation: Use a headful browser and require the user to complete verification manually before continuing. <br>


## Reference(s): <br>
- [CNKI professional search fields](references/cnki-fields.md) <br>
- [CNKI professional search query examples](references/query-examples.md) <br>
- [CNKI advanced search](https://kns.cnki.net/kns8s/AdvSearch?type=expert) <br>
- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/cnki-exp-search-automation-0-2-0) <br>
- [Publisher profile](https://clawhub.ai/user/zhangyingzhuangk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with browser-action instructions, JavaScript snippets, and JSON or CSV data examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce saved literature metadata files when the agent follows the export guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
