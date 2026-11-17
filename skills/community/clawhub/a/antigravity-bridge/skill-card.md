## Description:

One-directional knowledge bridge from Google Antigravity IDE to OpenClaw that syncs only .md documentation files from Antigravity projects into the OpenClaw workspace for native vector indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heintonny](https://clawhub.ai/user/heintonny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to pull Markdown context from Antigravity or Gemini project folders into an OpenClaw workspace so the content can be indexed for memory search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom path handling and scheduled syncing can write outside the intended workspace or index unintended content if the YAML config is unsafe.

Mitigation: Install only with a trusted YAML config, keep the destination as a simple workspace subfolder, avoid parent-directory or unusual path names, and run with --dry-run before enabling real sync or cron.

Risk: Synced Markdown may include private docs, prompts, or proprietary project context that becomes searchable through OpenClaw memory indexing.

Mitigation: Review every configured Markdown source before adding the destination to memorySearch.extraPaths or scheduled sync.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heintonny/skills/antigravity-bridge)
- [Setup guide](artifact/setup.md)
- [Configuration template](artifact/config-template.yaml)
- [Mike Farah yq](https://github.com/mikefarah/yq)
- [Mike Farah yq releases](https://github.com/mikefarah/yq/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup and sync guidance; runtime behavior depends on user-controlled YAML paths and local rsync/yq availability.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
