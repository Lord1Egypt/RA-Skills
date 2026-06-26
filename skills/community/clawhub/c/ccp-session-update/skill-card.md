## Description: <br>
Context Continuity Protocol session update for end-of-session operations: updates STATUS.md, posts to a Notion daily log, syncs an Obsidian vault, and creates Plane issues for new work items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to close out a work session by preserving project status, logging activity, updating knowledge-base notes, and tracking follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent updates to status files, Notion, Obsidian notes, and Plane issues. <br>
Mitigation: Review the intended changes and target workspaces before execution, and keep STATUS.md as the reviewed source of truth for downstream updates. <br>
Risk: The skill requires sensitive credentials and environment-specific resources. <br>
Mitigation: Install only in environments where you control the referenced Notion database, vault, Docker Plane instance, and projects; configure credential access explicitly before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/ccp-session-update) <br>
- [Notion Pages API endpoint](https://api.notion.com/v1/pages) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local project status files, personal knowledge-base notes, Notion pages, and Plane issues when run with the required credentials and environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
