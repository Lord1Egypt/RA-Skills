## Description: <br>
Searches recent discussions from Xiaohongshu, Douyin, and WeChat Official Accounts, then synthesizes cross-platform sentiment and trend reports for Chinese social media topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, market researchers, and other external users use this skill to research Chinese social media topics, monitor sentiment, compare brands or products, and generate structured Markdown plus optional JSON/HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and derived search terms may be sent to WebSearch and RedFox. <br>
Mitigation: Avoid sensitive topics unless disclosure to those services is acceptable, and confirm the intended query before running broad research. <br>
Risk: The bundled public API key uses shared public quota and may not provide user-level control. <br>
Mitigation: Use a personal REDFOX_API_KEY or the --api-key option when quota, traceability, revocation, or access control matters. <br>
Risk: JSON and HTML reports are saved as persistent local files. <br>
Mitigation: Choose and review the output directory before use, and delete or protect reports that contain sensitive research topics or links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/cn-last30days-redfox) <br>
- [Output rules and templates](references/output-rules.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration] <br>
**Output Format:** [Markdown research report with cited links, plus optional JSON data files and interactive HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script writes persistent report files to the selected output directory and can regenerate HTML from prior JSON without making API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
