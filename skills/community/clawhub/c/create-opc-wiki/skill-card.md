## Description:

Scaffolds a personal LLM wiki using the Karpathy pattern, with multi-agent files, an MCP server, and an optional SEO/GEO publish target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mackding](https://clawhub.ai/user/mackding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scaffold a local personal-knowledge-base vault with reusable wiki ingest, query, and lint workflows. It helps maintain compiled Markdown knowledge for use across agents and optional public publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses create-opc-wiki@latest from npm, so the executed package can change after this skill review.

Mitigation: Pin a specific reviewed package version, install only from a trusted npm publisher, and run scaffolding in a constrained directory or sandbox.

Risk: The generated vault includes agent rules, MCP server files, and site publishing files that can affect agent behavior or expose public-tagged content.

Mitigation: Inspect generated files before opening the vault in an agent or running npm install/npm start, and confirm privacy tags before publishing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mackding/skills/create-opc-wiki)
- [npm package](https://www.npmjs.com/package/create-opc-wiki)
- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Project GitHub repository](https://github.com/MackDing/create-opc-wiki)
- [Quick examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Running the recommended npx command can scaffold files in the target vault; the --json flag emits a machine-readable result.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
