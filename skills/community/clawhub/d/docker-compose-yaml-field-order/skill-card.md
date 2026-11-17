## Description:

Provides a default ordering convention for fields in customized Docker Compose YAML files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xfl12345](https://clawhub.ai/user/xfl12345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when writing, editing, or reviewing customized Docker Compose files to keep service fields in a consistent order. It does not apply to upstream Compose files copied without changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because two local Markdown references could not be resolved.

Mitigation: Check those references before installing if they matter to your use.

## Reference(s):

- [Server-resolved source repository](https://github.com/xfl12345/skills/tree/main/skills/docker-compose-yaml-field-order)
- [Compose field-ordering reference](https://github.com/foxydock/foxydock/blob/c875b600ce8ccac60a896103e158e55e80e0e9bd/compose/tool/find_unordered.py)
- [ArchiveBox Compose example](https://github.com/ArchiveBox/ArchiveBox/blob/c8d0e2e8e70b27c6d3db059f8fe765cb17aab418/docker-compose.yml)

## Skill Output:

**Output Type(s):** [Configuration guidance, Text]

**Output Format:** [Markdown guidance with an ordered list and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines relative ordering for listed service fields; fields that are absent can be skipped.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
