## Description: <br>
City Life Copilot turns city-life requests into local HTML cards for mood-based outings, social-media route replication, housing-area scans, and accessibility-aware travel planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzhyjr2021-beep](https://clawhub.ai/user/hzhyjr2021-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to plan local city trips, convert social-media recommendations into routes, assess housing-area amenities, and generate accessibility-aware route reports with embedded map views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer and workflows have broad local, network, browser, and persistent file capabilities. <br>
Mitigation: Review the installer before running it, preferably in a sandbox and without elevated privileges. <br>
Risk: Exact home, work, social-media, and accessibility details may be sent to or embedded in external map, browser, and fetch providers and persisted in local reports. <br>
Mitigation: Minimize sensitive location details where practical, review generated reports, and remove local files when they are no longer needed. <br>
Risk: Housing and accessibility route recommendations may be incomplete or inaccurate. <br>
Mitigation: Verify housing assessments, routes, access points, and accessibility conditions independently before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hzhyjr2021-beep/city-life-copilot) <br>
- [Workflow rules](references/workflows.md) <br>
- [AMap LBS Skill dependency](https://www.modelscope.cn/skills/@AMap-Web/amap-lbs-skill) <br>
- [web-fetch dependency](https://clawhub.ai/dlutwuwei/web-anti-crawl-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance plus local HTML report files with embedded map links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed outputs are written as rendered HTML files in the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
