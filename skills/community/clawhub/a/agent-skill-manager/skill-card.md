## Description:

Agent Skill Manager is a cross-platform `askill` CLI for managing, installing, syncing, and removing agent skills across supported Chinese AI agent products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxdwind](https://clawhub.ai/user/yxdwind)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent-skill authors use this skill to keep a central local skill repository and distribute skills across multiple AI coding products. It helps inspect status, install or adopt skills, run local audits, sync skill files, and package skills for products that require upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact filesystem and repository-changing behavior with weak scoping can affect local skill repositories and product skill directories.

Mitigation: Review before installing and use only in a disposable or backed-up environment until remove and install path validation is fixed.

Risk: Using --sync with remote URLs can quickly distribute remote skill content across agent products.

Mitigation: Avoid --sync for remote URLs and run audits before distributing skills to agent products.

Risk: Unrelated add-contributor scripts are present in the package.

Mitigation: Remove those scripts from the release package if they are not intentionally needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yxdwind/skills/agent-skill-manager)
- [Server-Resolved Source Repository](https://github.com/yxdwind/agent-skill-manager)
- [README.en.md](README.en.md)
- [Product Skill Paths Reference](docs/product-paths.md)
- [SECURITY.md](SECURITY.md)
- [PRIVACY.md](PRIVACY.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create or remove local skill files, filesystem links or junctions, audit reports, and DuMate zip packages when executed by the user.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json; pyproject.toml lists 0.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
