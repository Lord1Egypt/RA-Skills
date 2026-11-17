## Description:

Downloads ASMR.one audio works by RJ identifier, compresses audio for QQ-compatible sharing, and generates send lists and collection records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zx0018](https://clawhub.ai/user/zx0018)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search ASMR.one, download ASMR audio by RJ identifier, compress audio for QQ-compatible transfer, import local audio when offline, and maintain collection records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote-download and path handling may write outside the intended folder or consume local and network resources unexpectedly.

Mitigation: Use a dedicated output directory under a restricted user or workspace, monitor disk usage during downloads, and avoid running the tool on sensitive networks.

Risk: Unexpected identifiers or local media inputs can broaden file and network activity.

Mitigation: Only pass RJ identifiers matching RJ plus digits and review untrusted local media files before importing or compressing them.

Risk: The obfuscation option changes filenames and can make review or cleanup harder.

Mitigation: Use obfuscation only when needed and preserve the generated name map with the downloaded files.

## Reference(s):

- [ASMR.one](https://asmr.one)
- [ClawHub skill page](https://clawhub.ai/zx0018/skills/asmrone-downloader)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, file paths, and generated audio or manifest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses RJ identifiers, optional proxy and output-directory configuration, ffmpeg-based compression, and local collection metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
