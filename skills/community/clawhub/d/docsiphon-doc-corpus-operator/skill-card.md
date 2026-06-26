## Description: <br>
This skill helps agents run Docsiphon through its CLI-first path, export a small documentation subtree, and inspect the resulting audit artifacts without claiming hosted or MCP-first product status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a small, scoped Docsiphon CLI export and inspect manifest and report artifacts before attempting larger documentation corpus exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sample uvx command fetches and executes Docsiphon from GitHub. <br>
Mitigation: Verify the repository and preferably pin a trusted commit or release before execution, then run the demo from a low-risk workspace. <br>
Risk: Generated export artifacts may contain unexpected or unreviewed documentation content. <br>
Mitigation: Review ./_outputs, manifest.jsonl, report.json, toc.md, and report.html before reusing the output or expanding the export scope. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/xiaojiou176/docsiphon-doc-corpus-operator) <br>
- [Install](references/INSTALL.md) <br>
- [Demo](references/DEMO.md) <br>
- [Capabilities](references/CAPABILITIES.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [Docsiphon GitHub repository used by install commands](https://github.com/xiaojiou176-open/docsiphon.git) <br>
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces agent-facing operating instructions; export artifacts are produced by the Docsiphon CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
