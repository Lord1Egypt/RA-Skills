## Description:

Guides an agent through the Docsiphon CLI-first workflow to export a small documentation subtree and inspect the resulting audit artifacts without presenting Docsiphon as a hosted or MCP-first product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to invoke Docsiphon from the CLI, run a small documentation corpus export, and inspect generated manifest, report, table-of-contents, and HTML audit artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and demo flow invokes mutable GitHub code via uvx without a pinned commit or reviewed release.

Mitigation: Use a pinned commit or verified release, review the Docsiphon source and dependencies before execution, and run it in a low-privilege or disposable environment with only the intended output directory writable.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/xiaojiou176/skills/docsiphon-doc-corpus-operator)
- [Install](references/INSTALL.md)
- [Demo](references/DEMO.md)
- [Capabilities](references/CAPABILITIES.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [Docsiphon GitHub Repository](https://github.com/xiaojiou176-open/docsiphon.git)
- [uv Installation](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and artifact checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing instructions for CLI invocation and local audit artifact inspection.]

## Skill Version(s):

1.0.0 (source: manifest.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
