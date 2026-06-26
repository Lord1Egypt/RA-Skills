## Description: <br>
Manage Claude Managed Agents end to end through a Python helper CLI, with ant CLI equivalents documented as a secondary path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronfaby](https://clawhub.ai/user/aaronfaby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, update, inspect, archive, and steer Claude Managed Agents resources through a Python helper CLI, with documented ant CLI equivalents for manual operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Claude Managed Agents resources using an Anthropic API key. <br>
Mitigation: Use a least-privilege key where possible, run preflight checks, and review agent, environment, session, file, and resource IDs before mutations. <br>
Risk: Misconfigured API base URLs or networking settings could send credentials or session traffic to an unintended endpoint. <br>
Mitigation: Keep ANTHROPIC_API_BASE_URL pointed at a trusted Anthropic endpoint and prefer limited networking with explicit allowed hosts. <br>
Risk: File uploads and mounted resources may expose local data to the managed-agent service. <br>
Mitigation: Upload only files intended for the session and review mounted file paths before starting or modifying sessions. <br>
Risk: Permanent delete operations can remove agents, environments, sessions, files, or mounted resources. <br>
Mitigation: Archive before deleting unless the user clearly requests permanent cleanup for disposable resources. <br>


## Reference(s): <br>
- [Claude Managed Agents on ClawHub](https://clawhub.ai/aaronfaby/claude-managed-agents) <br>
- [Quickstart](references/quickstart.md) <br>
- [Lifecycle Recipes](references/lifecycle-recipes.md) <br>
- [Files API Workflows](references/files-api.md) <br>
- [Event Model and Steering](references/event-model.md) <br>
- [ant CLI Recipes](references/ant-cli-recipes.md) <br>
- [Known Gaps and Assumptions](references/known-gaps.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include resource IDs, lifecycle status, exact follow-up commands, or raw JSON when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
