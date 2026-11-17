## Description:

Audits local skill packages or archives with auto, native, or external scanner engines and can optionally enable LLM semantic review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyzlmh](https://clawhub.ai/user/cyzlmh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a local security review before installing a skill package, archive, or release bundle. It helps summarize scanner engine status, findings, risk level, and installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the packaged binary and checksum are missing, so the claimed bundled binary should not be trusted without verification.

Mitigation: Confirm the package contains the expected binary and checksum before running it; verify the SHA-256 value or build from source.

Risk: Default auto mode may run a locally resolved external scanner with the current user's permissions.

Mitigation: Use --engine native unless the resolved external scanner and its configuration are trusted.

Risk: Optional LLM review or report upload can send scan data to configured endpoints.

Mitigation: Enable --use-llm or --upload-url only with endpoints you control and whose data-handling behavior is understood.

## Reference(s):

- [CMIC Skill Scanner ClawHub Page](https://clawhub.ai/cyzlmh/skills/cmic-skill-scanner-linux-amd64)
- [CMIC Skill Scanner source repository referenced by package documentation](https://gitee.com/random_player/cmic-skill-scanner.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and optional JSON or Markdown scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write scan reports to a user-specified output directory.]

## Skill Version(s):

0.11.1 (source: server release metadata and assets/build/build-info.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
