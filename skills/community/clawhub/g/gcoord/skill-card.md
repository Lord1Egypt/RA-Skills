## Description:

Use when converting coordinates between WGS84, GCJ02, BD09, BD09MC, or WebMercator coordinate systems for Chinese map services (Baidu, Amap, Google China, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhyt1985](https://clawhub.ai/user/zhyt1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mapping-data operators use this skill to convert points, coordinate arrays, GeoJSON, or batch coordinate text between common Chinese web-map coordinate systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinate conversion output may be used in workflows subject to Chinese mapping and surveying rules.

Mitigation: Review generated coordinate data against applicable legal and operational requirements before publication or production use.

Risk: Dependency changes could alter conversion behavior if installation ignores the included lockfile.

Mitigation: Install with the included package-lock.json honored and review dependency updates before deployment.

Risk: Chinese-first prompts and command output may be hard to operate in English-only workflows.

Mitigation: Confirm the target users can work with Chinese prompts and output, or localize the interaction text before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhyt1985/skills/gcoord)
- [gcoord 1.0.7 package artifact](https://registry.npmmirror.com/gcoord/-/gcoord-1.0.7.tgz)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON coordinate conversion output, with shell command examples and interactive parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the input shape for supported point, array, GeoJSON, and batch coordinate text inputs where possible.]

## Skill Version(s):

1.1.0 (source: evidence release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
