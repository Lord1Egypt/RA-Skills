## Description: <br>
Runs Cue deep research for global macro scenarios, cross-checking public data and returning conclusions with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to run Cue-powered research on global macro topics such as inflation, central bank policy, GDP, trade, and cross-country comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can clone or update a local Cue runner before executing research. <br>
Mitigation: Review the clone or update command and confirm the Cue runner source is trusted before running it. <br>
Risk: The research run consumes Cue credits and uses the local Cue API key. <br>
Mitigation: Ask for explicit user approval before starting any credit-consuming research run. <br>
Risk: Macro research may be incomplete or unsuitable as a substitute for due diligence, legal review, or underwriting. <br>
Mitigation: Preserve source links, report empty results honestly, and treat findings as research support rather than a final professional determination. <br>


## Reference(s): <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue skills runner source](https://github.com/sensedeal/cue-skills) <br>
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills) <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-global-macro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown report with source links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user approval before spending Cue credits; reports should preserve source links and avoid fabricated content when the runner returns empty results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
