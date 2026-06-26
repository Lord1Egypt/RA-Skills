## Description: <br>
Direct dating and matchmaking workflow via curl against the dating HTTP API for creating profiles, setting match preferences, checking candidates, revealing contact details, and submitting reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1asdwz](https://clawhub.ai/user/1asdwz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run dating and matchmaking workflows against an external backend, including profile updates, photo uploads, match task creation, candidate review, contact reveal, and post-chat reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dating profile details, photos, location, contact handles, and match preferences may be sent to the configured external backend. <br>
Mitigation: Confirm the exact base URL before use, obtain explicit approval for each write, upload, or contact-reveal action, and send only fields needed for the current workflow. <br>
Risk: Temporary request files or tokens may contain sensitive dating workflow data. <br>
Mitigation: Delete temporary request files and tokens after the workflow and avoid storing unnecessary sensitive fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1asdwz/ai-dating) <br>
- [README](artifact/README.md) <br>
- [Curl Dating API Operations](artifact/references/curl-api-operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for external API calls; does not execute requests without user approval.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; artifact metadata reports 1.3.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
