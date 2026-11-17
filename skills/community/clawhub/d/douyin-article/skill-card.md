## Description:

Douyin Article helps an agent batch-transcribe audio and video links from Douyin, Bilibili, Xiaoyuzhou, YouTube, Vimeo, TikTok, Twitter/X, and other yt-dlp-supported platforms into semantically segmented Markdown transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and external users can use this skill to turn batches of public audio or video URLs into structured transcript files for review, reuse, translation, or content production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes untrusted remote media and transcript text in a tool-capable agent workflow.

Mitigation: Run it in a dedicated environment with limited tool access and restrict input URLs to known hostnames before execution.

Risk: The pipeline downloads remote media, invokes external tools, and writes intermediate artifacts under outputs/.

Mitigation: Review inputs before running, monitor disk usage, and delete the outputs directory when intermediate audio, subtitle, and transcript files are no longer needed.

Risk: Dependency and tool installation can broaden the local execution surface, especially global npm installation of agent-browser.

Mitigation: Pin Python dependencies where practical and avoid global npm installs when an isolated tool environment is available.

Risk: Setting SKIP_CERT_CHECK disables TLS certificate validation for selected download paths.

Mitigation: Leave certificate validation enabled by default and set SKIP_CERT_CHECK only when the user explicitly accepts the TLS risk.

Risk: Proxy environment variables may contain sensitive routing or credential information.

Mitigation: Redact proxy values from logs and shared outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/douyin-article)
- [Project homepage](https://github.com/EdwardWason/douyin-article)
- [README](README.md)
- [Pipeline details](references/pipeline-details.md)
- [Route rules](references/route-rules.md)
- [Examples](references/examples.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown transcript files with supporting JSON manifests and boundary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One Markdown transcript is produced per input video; non-Chinese content can include bilingual Chinese translation plus source-language blockquotes.]

## Skill Version(s):

4.1.2 (source: release evidence, SKILL.md frontmatter, README, and changelog, released 2026-07-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
