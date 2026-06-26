## Description: <br>
Git archaeology engine that reconstructs the why behind code: what pressures, failures, and pivots shaped the codebase into its current form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze Git history, reconstruct design decisions, identify volatile or aging code areas, and understand how incidents, refactors, ownership patterns, and architectural shifts shaped a repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository history can contain old secrets, sensitive internal context, or private decision history that is no longer visible in the current working tree. <br>
Mitigation: Use the skill only on repositories whose historical commits are appropriate for the agent to inspect, and avoid sharing generated summaries outside the intended audience. <br>
Risk: A broad trigger phrase may cause the agent to inspect Git history when the user intended a narrower code-history question. <br>
Mitigation: Use explicit prompts that name the repository area, time range, or excavation mode needed before asking the agent to analyze history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jcools1977/fossil-record) <br>
- [Publisher Profile](https://clawhub.ai/user/jcools1977) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with timelines, maps, decision trees, risk notes, and repository history summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Git history analysis; no API access or external service is described in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
