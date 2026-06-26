## Description: <br>
Identifies likely courier carriers from tracking numbers, guides package-status lookup through official or trusted courier sources, parses logistics timelines, and flags common delivery exceptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhili007](https://clawhub.ai/user/zhili007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to identify China-focused courier carriers, choose a query path, summarize logistics timelines, and provide practical next steps when delivery status appears abnormal. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers may be entered into third-party aggregator or courier websites during lookup. <br>
Mitigation: Prefer official courier sources where possible, use trusted aggregators deliberately, and avoid entering extra personal information unless the courier site requires it. <br>
Risk: Some courier lookups may request phone verification, login, or captcha completion. <br>
Mitigation: Handle verification steps deliberately on the courier's official site and ask the user before providing or using sensitive verification details. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhili007/express-query) <br>
- [Carrier Recognition Rules](artifact/references/carriers.md) <br>
- [Official Source Mapping](artifact/config/official_sources.json) <br>
- [Test Cases](artifact/data/test_cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include carrier confidence, tiered query options, logistics timeline summaries, abnormal-status assessment, and suggested user actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
