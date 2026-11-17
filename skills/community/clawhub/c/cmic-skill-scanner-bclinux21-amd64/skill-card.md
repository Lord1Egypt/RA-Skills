## Description:

Audits local skill packages or archives with a bundled scanner and optional external scanner integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyzlmh](https://clawhub.ai/user/cyzlmh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill before installing local skills, archives, or release bundles to generate scanner findings, risk levels, and a short installation conclusion. This package targets BCLinux 21 and older glibc Linux x64 environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path may download and execute a native binary from mutable release metadata.

Mitigation: Use a pinned and trusted release, verify the documented SHA-256 checksum before execution, or build the scanner from source.

Risk: Server-resolved provenance is unavailable for this version.

Mitigation: Do not infer provenance from repository links in the skill text; confirm the release host and source relationship before relying on the bundled binary.

Risk: External scanner mode is opt-in and may clone code or install dependencies when configured.

Mitigation: Keep external scanner mode disabled unless explicitly needed, and review the selected scanner work directory and dependency installation path before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyzlmh/skills/cmic-skill-scanner-bclinux21-amd64)
- [Publisher profile](https://clawhub.ai/user/cyzlmh)
- [CMIC Skill Scanner source build instructions](https://gitee.com/random_player/cmic-skill-scanner.git)
- [Cisco Skill Scanner optional external backend](https://github.com/cisco-ai-defense/skill-scanner.git)
- [uv package manager documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and scanner findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local scan reports when an output directory is configured.]

## Skill Version(s):

0.9.0 (source: server release metadata; bundled binary reports v0.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
