## Description: <br>
Appflowy Skill helps agents authenticate with AppFlowy Cloud/GoTrue and automate workspace, document, database, search, and collaboration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BaloneGit](https://clawhub.ai/user/BaloneGit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to call AppFlowy APIs, obtain authentication tokens, inspect workspaces, and create or update AppFlowy documents and grids. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly modify or delete live AppFlowy workspace content using user credentials. <br>
Mitigation: Run it first in a test workspace, back up important documents, and verify workspace, view, and database IDs before executing data-changing commands. <br>
Risk: Credentials may be exposed if passwords are passed directly on the command line. <br>
Mitigation: Avoid command-line passwords where possible and prefer short-lived tokens or least-privilege accounts. <br>
Risk: Template, grid, and collaboration operations can change existing documents in place. <br>
Mitigation: Treat update-user-management-doc, apply-grid, and collab commands as live data-changing operations and review planned changes before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/BaloneGit/appflowy-skill) <br>
- [AppFlowy API Reference](references/appflowy_api_reference.md) <br>
- [Configuration Example](references/config.example.json) <br>
- [Usage Examples](examples/README.md) <br>
- [Grid Plan Template](references/templates/grid_plan.example.json) <br>
- [Fitness Plan Template](references/templates/fitness_plan.example.json) <br>
- [User Management Document Template](references/templates/user_management_doc.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, and generated AppFlowy API requests or scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live AppFlowy API operations that create, update, or delete workspace content when executed with user credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
