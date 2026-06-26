## Description: <br>
Hire a human gig worker via USD bounty for tasks an AI agent cannot do alone, including physical-presence errands and specialized human work, with photo or text proof before payment approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[getterdone](https://clawhub.ai/user/getterdone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use GetterDone when a task requires physical presence, real-world verification, delivery, photography, mystery shopping, or specialized human work such as writing, design, proofreading, translation, or video. The skill helps an agent create paid tasks, review submitted proof, and approve, dispute, cancel, or monitor work with user confirmation by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create paid tasks and release payment to workers. <br>
Mitigation: Use conservative per-task and daily spending caps, and require explicit user review before task creation, approval, dispute, or cancellation unless autonomous review has been deliberately enabled. <br>
Risk: The skill requires a sensitive GetterDone API key for authenticated workflows. <br>
Mitigation: Keep GETTERDONE_API_KEY private, store it only in the agent host configuration, rotate or revoke it if exposed, and avoid placing credentials in prompts, logs, or task descriptions. <br>
Risk: Task details, attachments, locations, or proof may contain sensitive real-world information. <br>
Mitigation: Review task scope and attachments before posting, share only the information required for the worker to complete the task, and inspect submitted proof before approving payment. <br>
Risk: The companion MCP server is a supply-chain dependency used for paid operations. <br>
Mitigation: Install from the canonical @getterdone/mcp-server package and pin a specific version in production. <br>


## Reference(s): <br>
- [GetterDone ClawHub listing](https://clawhub.ai/getterdone/getterdone) <br>
- [GetterDone platform](https://getterdone.ai) <br>
- [Agent registration](https://getterdone.ai/register-agent) <br>
- [GetterDone MCP server package](https://www.npmjs.com/package/@getterdone/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and tool-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GETTERDONE_API_KEY for paid workflows; paid actions default to explicit user confirmation unless autonomous review is intentionally enabled.] <br>

## Skill Version(s): <br>
1.11.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
