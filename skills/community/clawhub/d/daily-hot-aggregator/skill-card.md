## Description: <br>
Aggregates trending topics from multiple Chinese content platforms, analyzes hot-list data, recommends content ideas, detects alerts, and can push reports to WeCom groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq853632587](https://clawhub.ai/user/qq853632587) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content operators use this skill to collect platform hot lists, summarize trends, generate reports, recommend content topics, and configure alert or WeCom push workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships credential-like values, including an enabled WeCom webhook configuration. <br>
Mitigation: Remove bundled webhook values before use, replace them with private user-managed secrets, and keep webhook keys out of shared artifacts. <br>
Risk: Automated collection and push workflows can write local report files and send hot-list content outside the user's environment. <br>
Mitigation: Review the enabled configuration, output paths, and scheduled push settings before installing or running recurring jobs. <br>
Risk: The security verdict is suspicious due to bundled credential-like values. <br>
Mitigation: Review the skill before installing and follow the server security guidance before enabling collection or push behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qq853632587/daily-hot-aggregator) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with shell commands, plus generated JSON and HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write hot_reports files and send configured WeCom webhook messages.] <br>

## Skill Version(s): <br>
7.1.0 (source: server release metadata; artifact package.json reports 7.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
