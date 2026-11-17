## Description:

Review an existing YouTube thumbnail, social media cover, article cover, or podcast cover design, then turn the findings into a practical thumbnail-optimization and cover-improvement plan. This AI thumbnail analyzer identifies the visual hook, focal hierarchy, title-to-image fit, text-safe contrast, mobile readability, and crop resilience, then produces targeted edit directions and two or three video cover improvement candidates ready to compare. It can optionally read the field your cover is entering: the titles and public counts of what already ranks for the same topic on YouTube, TikTok, Douyin, and REDnote; on YouTube, a competitor's actual thumbnail image; and your own YouTube channel's recent thumbnails. That turns competitor thumbnail analysis, a thumbnail benchmark, and a cover comparison into evidence sitting beside the review instead of one cover being judged alone. Surfaces with no public data — a WeChat article cover, a podcast cover, and others — simply skip that step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and publishers use the skill to review an existing video, social, article, or podcast cover before publication and get practical revision directions. They can optionally compare it with public same-topic results and request two or three visual candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags broad account permissions and possible shared-state changes.

Mitigation: Review the Beatra authorization request before allowing access, and revoke the device connection in the Beatra Console if it is no longer needed.

Risk: The security assessment flags recurring installation telemetry.

Mitigation: Review the Updates and Security and Installation Registration references to understand the installation information reported before connecting.

Risk: Using a local cover with the remote service can involve uploading that cover.

Mitigation: Upload only cover files appropriate to share with Beatra, and review the upload and paid-call confirmation details before proceeding.

Risk: The security assessment says the scan is partial because some references could not be resolved, so its evidence is incomplete.

Mitigation: Review the bundled security and workflow references and assess the package before installation or use.

## Reference(s):

- [Cover preflight workflow](artifact/references/workflow.md)
- [Same-topic baseline lookup](artifact/references/baseline-lookup.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/cover-performance-preflight)
- [Beatra skill page](https://beatra.ai/skills/cover-performance-preflight)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Image files]

**Output Format:** [Qualitative preflight card and revision directions in Markdown; optionally two or three visual cover candidate files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Qualitative review; no numerical performance score, CTR forecast, or click guarantee. Optional baseline and image generation are separate paid steps requiring confirmation.]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
