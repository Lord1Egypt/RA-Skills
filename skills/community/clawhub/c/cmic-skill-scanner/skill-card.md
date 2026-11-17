## Description:

Audits local skill packages or archives with auto, native, or external scanner engines and can optionally enable LLM-assisted semantic review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyzlmh](https://clawhub.ai/user/cyzlmh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before installing local skills, archives, or release bundles to review scanner findings and risk level. It helps inspect target files locally by default, with optional configured report upload or LLM review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded binaries require trust in the release host and may not match the reviewed source.

Mitigation: Build from source when possible, or verify the published SHA-256 checksum before running a binary.

Risk: The default auto engine may execute a locally resolved external scanner with the current user's permissions.

Mitigation: Use `--engine native` when you want to prevent external scanner execution.

Risk: Optional LLM review or report upload can send scan data to a configured endpoint.

Mitigation: Use `--use-llm` and `--upload-url` only with trusted endpoints and scan only directories intended for inspection.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyzlmh/skills/cmic-skill-scanner)
- [Gitee Releases](https://gitee.com/random_player/cmic-skill-scanner/releases)
- [Release SHA256SUMS](https://gitee.com/random_player/cmic-skill-scanner/raw/main/releases/v0.11.1/SHA256SUMS)
- [Gitee Source Repository](https://gitee.com/random_player/cmic-skill-scanner.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with inline shell commands and risk findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local report files to an output directory; optional upload and LLM review require explicit endpoint configuration.]

## Skill Version(s):

0.11.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
