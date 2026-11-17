## Description:

Download a file from a URL and save it locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to download HTTP/HTTPS resources such as images, documents, audio, video, or reports to a specified local path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download from arbitrary URLs, which may retrieve untrusted or malicious files.

Mitigation: Verify the URL source before use and scan or inspect downloaded files before opening or executing them.

Risk: The skill can write files wherever the agent process has permission, including unsafe destinations or existing files.

Mitigation: Use a dedicated downloads directory, avoid sensitive paths, and review the requested save path before execution.

Risk: Running the downloader with elevated privileges increases the impact of unsafe file writes.

Mitigation: Run the agent without elevated privileges and restrict filesystem permissions to the intended workspace.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Downloaded file saved to disk with JSON status on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the requests package and accepts a required url plus an optional save_path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
