## Description: <br>
Manage Asana via the Asana REST API. Use when you need to list workspaces, projects, tasks, search tasks, comment, update, complete, or create tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k0nkupa](https://clawhub.ai/user/k0nkupa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Asana authentication and let an agent inspect or manage Asana workspaces, projects, and tasks through the Asana REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable Asana credentials are stored locally under ~/.openclaw/asana. <br>
Mitigation: Use least-privilege credentials, protect the ~/.openclaw/asana directory, and avoid syncing or committing config and token files. <br>
Risk: The skill can modify live Asana workspace data, including task updates, comments, completions, and task creation. <br>
Mitigation: Review agent requests carefully before allowing write actions, and use read-only or narrower credentials when write access is not required. <br>


## Reference(s): <br>
- [Asana Developer Documentation](https://developers.asana.com/docs) <br>
- [Asana endpoints quick reference](references/asana-endpoints.md) <br>
- [ClawHub Asana skill page](https://clawhub.ai/k0nkupa/asana) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from Node.js helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an Asana PAT or OAuth token; local configuration and token state are stored under ~/.openclaw/asana.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
