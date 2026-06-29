## Description: <br>
Manage Flux kanban boards, cards, columns, and labels through the Flux REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uminai-dev](https://clawhub.ai/user/uminai-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents that automate Flux kanban work: creating and moving cards, managing boards and columns, assigning members, toggling labels, searching content, and using undo workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to create, update, move, or soft-delete Flux board data. <br>
Mitigation: Install it with a Flux API key scoped only to the actions the agent should perform, and review proposed write operations before execution. <br>
Risk: Attachment workflows can initiate uploads to the configured Flux or S3-backed service. <br>
Mitigation: Limit API key and storage permissions, and review attachment file names, MIME types, and target cards before upload. <br>


## Reference(s): <br>
- [Flux](https://flux.umin.ai) <br>
- [Flux API Reference](https://flux.umin.ai/llms.txt) <br>
- [Flux Interactive API Docs](https://flux.umin.ai/api-docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/uminai-dev/flux-kanban-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with endpoint references, request examples, and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLUX_API_KEY and optionally FLUX_BASE_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
