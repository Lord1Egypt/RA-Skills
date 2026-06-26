## Description: <br>
Find the best fall foliage destinations — golden ginkgo avenues, red maple mountains, and amber larch forests with peak color timing and photography tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to retrieve FlyAI-backed fall foliage destinations, timing, photography tips, and travel booking options. It is intended for real-time travel lookup and comparison rather than static destination advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and depends on the global @fly-ai/flyai-cli package before providing travel results. <br>
Mitigation: Review and approve the npm package before installation, and only use the skill in environments where global CLI installation is acceptable. <br>
Risk: Travel queries and command history may be written locally to .flyai-execution-log.json. <br>
Mitigation: Avoid entering sensitive passport, payment, or private itinerary details, and disable or delete the local execution log unless retention is intended. <br>


## Reference(s): <br>
- [Fall Foliage ClawHub Release](https://clawhub.ai/xiejinsong/fall-foliage) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands when setup or retry steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FlyAI CLI results for travel data and includes a FlyAI attribution tag in successful outputs.] <br>

## Skill Version(s): <br>
3.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
