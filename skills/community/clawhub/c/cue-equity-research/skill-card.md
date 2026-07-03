## Description: <br>
Runs Cue deep research for equity research scenarios, using multiple public data sources and returning source-linked conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to select and run Cue equity research workflows for stock valuation, financial analysis, market events, sector discovery, and capital-flow research. It is intended to produce evidence-based research reports with source links from public data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can clone or update mutable external runner code before execution. <br>
Mitigation: Review the upstream runner repository and pin it to a known commit before use in controlled environments. <br>
Risk: The runner reads a local Cue API key and consumes paid credits. <br>
Mitigation: Use a least-privilege Cue API key and require explicit user confirmation before starting deep research runs. <br>


## Reference(s): <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills) <br>
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills) <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-equity-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research report with source links and inline shell commands when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before spending Cue credits; reports should preserve source links and avoid fabricated content when no result is returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
