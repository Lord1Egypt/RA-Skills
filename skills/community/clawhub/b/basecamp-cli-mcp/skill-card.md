## Description: <br>
CLI and MCP server for Basecamp 4 that helps agents interact with projects, todos, messages, schedules, kanban cards, documents, campfires, and related Basecamp workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drkraft](https://clawhub.ai/user/drkraft) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and AI-assisted project teams use this skill to manage Basecamp 4 workspaces through a CLI or MCP host. It supports reading and changing projects, todos, messages, schedules, kanban cards, documents, comments, subscriptions, webhooks, and related records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP client can gain broad access to read, create, modify, delete, archive, trash, and route Basecamp data through webhooks. <br>
Mitigation: Install only for trusted MCP hosts, use a dedicated OAuth app, and prefer a least-privileged or test Basecamp account when possible. <br>
Risk: Basecamp client secrets can be exposed if copied into shared configuration files or repositories. <br>
Mitigation: Keep BASECAMP_CLIENT_SECRET out of shared configs and source control; provide it through local environment variables or a secret manager. <br>
Risk: Agent-initiated destructive or externally visible actions can affect projects, recordings, subscriptions, posts, or webhooks without built-in confirmation safeguards. <br>
Mitigation: Require human confirmation in the MCP host before delete, archive, trash, posting, subscription changes, and webhook create, update, or test actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drkraft/basecamp-cli-mcp) <br>
- [Project Homepage](https://github.com/drkraft/basecamp-cli) <br>
- [npm Package](https://www.npmjs.com/package/@drkraft/basecamp-cli) <br>
- [Basecamp API Reference](https://github.com/basecamp/bc3-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-oriented MCP tool results, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Basecamp OAuth credentials and a configured Basecamp account; CLI commands can emit JSON with --format json.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
