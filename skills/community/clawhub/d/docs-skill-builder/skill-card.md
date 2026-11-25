## Description:

Use when creating or refreshing a local documentation skill for another tool, SDK, API, or docs repository, with install instructions for Codex or OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold or refresh local documentation skills for another tool, SDK, API, or documentation repository. It guides source mapping and creates a bundle with generation scripts, installable skill instructions, and mirrored references for Codex or OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis was partial, with undeclared tool scope and some references unresolved.

Mitigation: Review the generated bundle's selected paths and any tools it invokes before execution, and confirm the referenced documentation is present.

## Reference(s):

- [Documentation Skill Model](references/docs-skill-model.md)
- [OpenClaw skills CLI](https://docs.openclaw.ai/cli/skills)
- [ClawHub release page](https://clawhub.ai/theangrypit/skills/docs-skill-builder)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Local documentation skill bundle with Markdown references and Bash generation scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selected source documentation is mirrored verbatim and can be refreshed from its source.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
