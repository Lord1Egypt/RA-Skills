## Description:

Creates conventions for Docker Compose YAML files that keep project resources under the current working directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xfl12345](https://clawhub.ai/user/xfl12345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers adapting Docker Compose projects can use this skill to organize persistent data, environment files, and build resources beneath the project directory. It provides path conventions and examples for updating customized Compose files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing bind-mount paths may leave existing data outside the new locations.

Mitigation: Inspect and back up the current mount directories, then verify the new paths before resuming services.

Risk: The security scan was partial, so it did not inspect every referenced local path.

Mitigation: Review unresolved local path references and related files before applying the guidance.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/xfl12345/skills/tree/main/skills/docker-compose-yaml-all-in-current-directory)
- [Webtop Compose example](https://github.com/xfl12345/webtop/blob/0cd2bb65361e2985fb13c989001bcc94a27fe8a1/docker-compose.example.yaml)
- [New API Compose example](https://github.com/QuantumNous/new-api/blob/3e1e728279884d83358811aec00980dd55f6ad4e/docker-compose.yml)

## Skill Output:

**Output Type(s):** [Configuration, Code, Guidance]

**Output Format:** [Markdown with YAML and environment-file examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker Compose configuration snippets and project path recommendations.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata; SKILL.md frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
