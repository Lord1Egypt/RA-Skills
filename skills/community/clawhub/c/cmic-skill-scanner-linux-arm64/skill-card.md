## Description:

Audits local skill packages or archives with auto, native, or external scanning engines, with optional LLM semantic review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyzlmh](https://clawhub.ai/user/cyzlmh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill before installing local skill packages, archives, or release bundles to generate scan findings, risk levels, and a short installation conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default auto mode may run a locally resolved external scanner with the current user's permissions.

Mitigation: Use --engine native for routine scans, review any external scanner and its configuration before use, and avoid running the tool as an elevated user.

Risk: The install path depends on bundled or downloaded executable artifacts that require separate trust.

Mitigation: Verify the binary checksum against an independent trusted source before execution, or build from reviewed source when stronger assurance is needed.

Risk: Explicitly enabled upload or LLM review can send findings or bounded target text to configured endpoints.

Mitigation: Enable --upload-url or --use-llm only with approved endpoints and confirm endpoint data-handling policy before scanning sensitive targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyzlmh/skills/cmic-skill-scanner-linux-arm64)
- [Installation guide](INSTALL.md)
- [Build metadata](assets/build/build-info.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports and terminal command guidance, with optional local report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional upload and LLM review features require explicit endpoint configuration.]

## Skill Version(s):

0.11.1 (source: server release metadata; artifact build-info.json reports v0.11.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
