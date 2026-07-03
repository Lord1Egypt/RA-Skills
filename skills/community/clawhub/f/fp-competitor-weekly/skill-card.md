## Description: <br>
Generates a Chinese weekly competitor social-media report by combining Socialinsider IG, TikTok, and Facebook CSV exports with Agent-Reach YouTube data, emphasizing insights, charts, and actionable FridayParts recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuxirui677](https://clawhub.ai/user/zhuxirui677) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and operations teams use this skill to turn weekly competitor social-media exports into a structured Chinese operations report. It ranks audience growth and engagement, summarizes top posts and videos, extracts comment and content-strategy insights, recommends charts, and proposes concrete FridayParts actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided social-media exports may contain confidential or sensitive business data. <br>
Mitigation: Only paste exports approved for processing in the active agent environment. <br>
Risk: Incomplete or stale CSV and YouTube inputs can lead to misleading competitor conclusions. <br>
Mitigation: Review the generated report against the provided exports and use the bundled quality checklist before relying on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuxirui677/skills/fp-competitor-weekly) <br>
- [README](artifact/README.md) <br>
- [Import guide](artifact/docs/如何导入GetClawHub.md) <br>
- [Example weekly competitor report](artifact/examples/example_competitor_weekly.md) <br>
- [Output quality checklist](artifact/reference/输出质量checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown report with ranked lists, analysis sections, chart suggestions, and action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only output; expects user-provided Socialinsider CSV and Agent-Reach YouTube JSON inputs; configured max_tokens is 2000.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
