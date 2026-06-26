## Description: <br>
Inspect and edit the workspace's git-backed context repository (the GTM knowledge base of markdown/MDX files) and its runtime sandbox using the Cargo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, RevOps teams, and GTM operators use this skill to inspect, author, edit, and troubleshoot markdown/MDX knowledge-base files in a Cargo workspace context repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use Cargo credentials against a workspace context repository. <br>
Mitigation: Install and enable it only for agents that should inspect or update that Cargo workspace, and protect OAuth sessions or API tokens. <br>
Risk: Cargo context write and edit operations push commits immediately to the default branch. <br>
Mitigation: Verify the Cargo workspace name before writes or edits, review proposed content, and apply edits one at a time when derived from sales-call analysis. <br>
Risk: The declared install path uses @cargo-ai/cli@latest, so CLI behavior can change as the package updates. <br>
Mitigation: Use extra care with the latest CLI dependency and pin or test the CLI version where reproducibility is required. <br>


## Reference(s): <br>
- [Cargo Context ClawHub Page](https://clawhub.ai/cargo-ai/cargo-context) <br>
- [Cargo Skills Homepage](https://github.com/getcargohq/cargo-skills) <br>
- [Cargo Workspaces Example Repository](https://github.com/getcargohq/cargo-workspaces) <br>
- [Context repo conventions](references/conventions.md) <br>
- [Response shapes](references/response-shapes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Authoring examples](references/examples/authoring.md) <br>
- [Lifecycle examples](references/examples/lifecycle.md) <br>
- [Graph query examples](references/examples/graph-queries.md) <br>
- [Bootstrap from domain example](references/examples/bootstrap-from-domain.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and Cargo CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to run Cargo CLI commands that return JSON and to write or edit markdown/MDX context files.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
