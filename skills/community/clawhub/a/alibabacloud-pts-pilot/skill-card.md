## Description: <br>
Routes Alibaba Cloud PTS performance testing requests to task, report analysis, or skill discovery sub-skills without executing cloud operations itself. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route Alibaba Cloud PTS requests for scenario operations, report analysis, or Alibaba Cloud skill discovery to the appropriate specialized sub-skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may default Alibaba Cloud PTS requests to cn-shanghai when no RegionId is supplied. <br>
Mitigation: Use only where cn-shanghai is an acceptable default, or explicitly provide RegionId in requests. <br>
Risk: The skill can delegate state-changing PTS operations such as create, start, stop, or delete. <br>
Mitigation: Review the skill before installation and provide explicit resource identifiers so delegated operations target the intended environment. <br>


## Reference(s): <br>
- [Routing Rules](references/routing-rules.md) <br>
- [ClawHub Listing](https://clawhub.ai/sdk-team/skills/alibabacloud-pts-pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries with concise delegation status lines, tables, recommendations, and next-action guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface SceneId, ReportId, JobId, status, PTS performance metrics, bottleneck recommendations, and install commands returned by delegated skills.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
