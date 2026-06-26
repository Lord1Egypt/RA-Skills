## Description: <br>
Clipcat is a TikTok e-commerce video creation skill for video search, product insights, viral replication, product-to-video generation, breakdown analysis, and video download through the Clipcat CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a2888409](https://clawhub.ai/user/a2888409) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate the Clipcat CLI for TikTok Shop market research, viral video replication, product video generation, image generation, video analysis, downloads, and asynchronous task tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs a third-party Clipcat CLI binary. <br>
Mitigation: Install only when the user trusts Clipcat as the provider and the versioned download source shown in the metadata is acceptable. <br>
Risk: The CLI requires a Clipcat API key and uses it for authenticated requests. <br>
Mitigation: Configure only the intended API key, keep it out of prompts and logs, and rotate it if exposure is suspected. <br>
Risk: Some video generation and social-video replication commands can consume paid credits. <br>
Mitigation: Review parameters and obtain confirmation before running commands that consume credits, especially social URL replication that may add a download credit. <br>
Risk: Async task IDs are stored locally for resume behavior. <br>
Mitigation: Treat local task history as user data and avoid sharing task IDs or generated signed URLs outside the intended workflow. <br>


## Reference(s): <br>
- [Clipcat homepage](https://clipcat.ai) <br>
- [Clipcat API key settings](https://clipcat.ai/workspace?modal=settings&tab=apikeys) <br>
- [ClawHub skill page](https://clawhub.ai/a2888409/clipcat) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit asynchronous video or image tasks and return task IDs, signed URLs, or JSON results through the Clipcat CLI.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata and OpenClaw install URLs) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
