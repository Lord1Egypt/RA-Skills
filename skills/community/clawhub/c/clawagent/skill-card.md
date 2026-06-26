## Description: <br>
ClawAgent is an enterprise AIGC marketing skill for short video generation, digital human narration, AI product photography, virtual model try-on, product scene imagery, and multi-platform account operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiadouai](https://clawhub.ai/user/jiadouai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, e-commerce, and operations teams use this skill to route AIGC content requests to ClawAgent tools, configure authentication, upload local media for processing, and retrieve generated image or video results. It is intended for external or internal users who need product scenes, model try-on images, reference-image generation, and related marketing assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can configure and use a ClawAgent authorization token. <br>
Mitigation: Use a dedicated revocable ClawAgent token and rotate or revoke it if the skill is no longer trusted. <br>
Risk: The skill can upload local files to cloud storage to produce public URLs for ClawAgent tools. <br>
Mitigation: Confirm every local path and file contents before upload, and avoid uploading confidential or regulated media unless the storage and processing terms are acceptable. <br>
Risk: Unsupported requests may be reported silently with the user's original prompt. <br>
Mitigation: Disable or avoid unsupported-feature reporting unless sharing the original prompt with the provider is acceptable. <br>
Risk: Provider-supplied update instructions can direct changes to the installed skill. <br>
Mitigation: Review update notes and requested actions before approving any update. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jiadouai/clawagent) <br>
- [AI product photography reference](references/ai_design.md) <br>
- [Authentication reference](references/auth.md) <br>
- [Common workflows reference](references/workflows.md) <br>
- [Unsupported feature reporting reference](references/unsupported_feature_reporting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return job IDs, public file URLs, file sizes, status objects, image URLs, or video URLs from ClawAgent MCP tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
