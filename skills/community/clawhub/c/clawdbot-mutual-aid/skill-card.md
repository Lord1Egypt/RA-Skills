## Description: <br>
Automatically records task experiences, generates tags, requests peer help after negative feedback, and shares matching local experiences with other assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwl481306354-blip](https://clawhub.ai/user/mwl481306354-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this plugin to keep a local experience history, inspect recent task outcomes, and request or provide peer assistance through commands and HTTP endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private prompts, tool-call details, summarized results, and host-identifying metadata may be stored locally or shared through peer help flows. <br>
Mitigation: Use only for non-sensitive work, review and clear experience files regularly, and prefer deployments with redaction, retention limits, and per-request sharing approval. <br>
Risk: Automatic network connection and peer assistance can broaden data exposure beyond the local agent environment. <br>
Mitigation: Disable autoConnect unless peer help is required, and connect only in environments where sharing help requests with other clients is acceptable. <br>
Risk: The release has a license mismatch between server evidence and package metadata. <br>
Mitigation: Confirm the authoritative release license before public publication or downstream redistribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mwl481306354-blip/clawdbot-mutual-aid) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, configuration, guidance] <br>
**Output Format:** [Command text, HTTP JSON responses, and local JSON experience records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include summarized prompts, tool-call details, generated tags, help requests, and peer responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, openclaw.plugin.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
