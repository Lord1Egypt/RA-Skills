## Description:

Audits local skill packages or archives with auto, native, or external scanner engines, with optional LLM semantic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyzlmh](https://clawhub.ai/user/cyzlmh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to run pre-install checks on local skill packages, archives, or release bundles and review findings before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package integrity is inconsistent because the advertised executable and checksum are missing and the fallback source build is unpinned.

Mitigation: Obtain and verify the missing binary and checksum from a trusted release, or build from a pinned and reviewed source revision before installation.

Risk: The auto engine may invoke a locally resolved external scanner with the current user's permissions.

Mitigation: Use --engine native unless the external scanner and its configuration are trusted.

Risk: Optional upload or LLM review can send reports or sampled target text to configured endpoints.

Mitigation: Enable --upload-url or --use-llm only with trusted endpoints after reviewing their data-handling expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyzlmh/skills/cmic-skill-scanner-darwin-arm64)
- [Install guide](artifact/INSTALL.md)
- [Build metadata](artifact/assets/build/build-info.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and scan-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local report files when --output-dir is used.]

## Skill Version(s):

0.11.1 (source: server release metadata; binary build-info reports v0.11.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
