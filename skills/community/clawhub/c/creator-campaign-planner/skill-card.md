## Description: <br>
Plans KOL/KOC creator collaboration schedules, content reuse, follow-up cadence, and goal mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, growth, and creator operations teams use this skill to draft reviewable creator campaign plans from audience, budget, channel, and timing inputs. It helps structure collaboration goals, creator tiers, content cadence, asset reuse, risk controls, review items, and recap metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper reads user-selected files or directories, which may include sensitive campaign, creator, or personal data. <br>
Mitigation: Use scoped input files, avoid broad directories, and redact sensitive material before processing. <br>
Risk: Generated campaign plans may be incomplete, inaccurate, or unsuitable for a specific platform, jurisdiction, or brand policy. <br>
Mitigation: Treat outputs as review drafts and verify claims, compliance requirements, creator fit, and publication decisions before external use. <br>
Risk: The skill can optionally write a report file when an output path is supplied. <br>
Mitigation: Choose an explicit output location and review generated files before sharing, publishing, or using them operationally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/creator-campaign-planner) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Campaign Planning Spec](resources/spec.json) <br>
- [Output Template](resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON campaign-planning brief, with optional shell command guidance for local execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local input files or directories; may write a report file when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
