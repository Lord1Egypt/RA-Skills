## Description: <br>
Use when generating, resuming, or checking TikTok videos, ads, or selling videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newt0n](https://clawhub.ai/user/newt0n) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, sellers, and developers use this skill to start, resume, and check TikTok-oriented AI video generation tasks through CreatOK. It helps collect the generation plan, confirm paid execution, poll task status, and return the resulting video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive CreatOK API key and may send prompts and selected reference images to CreatOK. <br>
Mitigation: Install and run it only in trusted environments, configure CREATOK_API_KEY carefully, and rotate the key if it may have been exposed. <br>
Risk: Video generation can spend credits, and some activation phrases are broad. <br>
Mitigation: Confirm the exact model, duration, orientation, reference images, and estimated credits before starting generation; avoid bypass flags unless the user already approved the request. <br>
Risk: The skill depends on network access to CreatOK and may fail if the API key is missing, invalid, or the service is unavailable. <br>
Mitigation: Check CREATOK_API_KEY configuration, handle authorization errors without exposing secrets, and retry later for transient service failures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/newt0n/creatok-generate-video) <br>
- [Common Rules](references/common-rules.md) <br>
- [CreatOK API Keys](https://www.creatok.ai/app/workspace/api-keys) <br>
- [CreatOK Agent Skills](https://www.creatok.ai/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON files plus a final text response with task status and video URL when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists outputs/result.json and outputs/result.md under .artifacts/<run_id>; supports task recovery by task_id.] <br>

## Skill Version(s): <br>
0.1.6 (source: ClawHub release metadata; artifact frontmatter version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
