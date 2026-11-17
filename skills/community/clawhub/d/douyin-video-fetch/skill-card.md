## Description:

Downloads Douyin videos to local MP4 files, prioritizing watermark-free video, for downstream video analysis or recreation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kamiender](https://clawhub.ai/user/kamiender)

### License/Terms of Use:


## Use Case:

Developers and content-analysis practitioners use this skill to fetch individual or batch Douyin videos from URLs or video IDs into a controlled local output directory for later analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can open and download from arbitrary web URLs, which may create avoidable network and disk-use risk.

Mitigation: Use only trusted Douyin inputs, run with restricted outbound network access where possible, choose a controlled output directory, and avoid untrusted batch files until host validation and download size limits are enforced.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Guidance]

**Output Format:** [Markdown usage guidance with shell commands; runtime output is MP4 files plus plain-text or JSON status results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output directory is ./downloads; file names are based on video IDs when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
