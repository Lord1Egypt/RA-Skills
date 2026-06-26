## Description: <br>
Agent Experience Graph recommends tools, skills, and workflow lessons from sanitized prior agent execution traces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yao23](https://clawhub.ai/user/yao23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to query sanitized prior task traces, compare subtasks with solved work, and record reusable lessons for future tool and skill recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trace libraries may expose secrets, private customer data, proprietary snippets, or raw workspace content if users record unsanitized traces. <br>
Mitigation: Use only trusted, sanitized trace libraries and avoid storing sensitive or proprietary content in shared traces. <br>
Risk: Implicit invocation can select the skill automatically for recommendation tasks where users do not want trace-based guidance. <br>
Mitigation: Disable implicit invocation when automatic selection is not desired. <br>
Risk: Recommendations from prior traces can be misleading when prior constraints, environments, or outcomes differ from the current task. <br>
Mitigation: Review matched traces, outcomes, lessons, and current constraints before applying recommendations. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/yao23/agent-experience-graph) <br>
- [ClawHub listing](https://clawhub.ai/yao23/agent-experience-graph) <br>
- [Trace Schema](references/trace_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON examples; the helper script emits JSON recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and sanitized JSON trace libraries; no network access indicated by the security evidence.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
