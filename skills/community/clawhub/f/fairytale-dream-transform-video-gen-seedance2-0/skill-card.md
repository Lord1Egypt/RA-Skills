## Description: <br>
Transforms text briefs or public HTTPS images into creamy pastel fairytale videos using WeryAI Seedance 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative operators use this skill to expand a short idea or a single public image URL into a detailed, on-style prompt, submit it to WeryAI Seedance 2.0, and receive playable video links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and public image URLs are sent to WeryAI for processing. <br>
Mitigation: Avoid submitting secrets, private media URLs, unreleased campaign assets, or regulated data unless third-party processing is approved. <br>
Risk: The skill requires WERYAI_API_KEY and each wait run may consume paid credits. <br>
Mitigation: Keep the API key out of files and logs, run in a short-lived environment when appropriate, and confirm parameters before submitting or rerunning jobs. <br>
Risk: The documentation locks the skill to SEEDANCE_2_0, but the script requires the caller to pass the model value. <br>
Mitigation: Review the confirmation table or dry-run JSON and ensure the request uses model SEEDANCE_2_0 before submission. <br>


## Reference(s): <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [ClawHub release page](https://clawhub.ai/zoucdr/fairytale-dream-transform-video-gen-seedance2-0) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with confirmation tables, JSON command payloads, and inline video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; generation submits prompts and optional public image URLs to WeryAI and may consume paid credits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
