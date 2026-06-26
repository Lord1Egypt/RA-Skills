## Description: <br>
Get new study items for any subject, using a local study list and progress tracking to avoid repeating learned items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buiphuc](https://clawhub.ai/user/buiphuc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to retrieve daily learning items from a configurable local JSON study list, track completed items, and optionally prepare practice quizzes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Study data and progress are stored locally in the skill folder and may include user-provided learning material. <br>
Mitigation: Avoid placing private or sensitive content in data/data.json unless local storage and copying into learned_items.json are acceptable. <br>
Risk: Optional Quizbuild use may send quiz material to an external service. <br>
Mitigation: Enable Quizbuild only after reviewing the service configuration and confirming that sharing the selected study content is acceptable. <br>


## Reference(s): <br>
- [Daily Tutor on ClawHub](https://clawhub.ai/buiphuc/daily-tutor) <br>
- [Publisher profile](https://clawhub.ai/user/buiphuc) <br>
- [Data format examples](references/EXAMPLES.md) <br>
- [Quizbuild MCP endpoint](https://api.quizbuild.com/mcp/quizbuild) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text study items with Markdown instructions and optional JSON quiz tool arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; reads local JSON study data and writes local progress state.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
