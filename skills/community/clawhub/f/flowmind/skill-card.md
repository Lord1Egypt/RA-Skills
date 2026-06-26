## Description: <br>
Manage productivity with FlowMind - goals, tasks with subtasks, notes, people, and tags via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fancygobot](https://clawhub.ai/user/fancygobot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
FlowMind users and their agents use this skill to manage a FlowMind productivity workspace through REST API calls, including goals, tasks, notes, people, and tags. It is suited for organizing focus work, tracking progress, preparing for meetings, and maintaining related productivity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key that gives an agent access to the user's FlowMind workspace. <br>
Mitigation: Use a revocable or scoped API key when available, store it securely, and install the skill only when workspace access is intended. <br>
Risk: Documented endpoints can update or delete goals, tasks, notes, people, and tags. <br>
Mitigation: Require explicit user confirmation before deletions or large updates to FlowMind records. <br>


## Reference(s): <br>
- [FlowMind API Reference](references/api.md) <br>
- [FlowMind](https://flowmind.life/) <br>
- [FlowMind API Base URL](https://flowmind.life/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown with REST endpoint references and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FlowMind API key and can read, create, update, or delete FlowMind workspace records.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
