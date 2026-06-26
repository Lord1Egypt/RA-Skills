## Description: <br>
AI-powered service for pull request code reviews with optional voice note transcription, Discord alerts, and secure diff URL handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review pull request diffs, optionally transcribe voice notes, and send review status to Discord. The current automated analysis returns pending manual review, so users should treat generated review results as workflow support rather than final approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The healthcheck script can restart host services and send operational status to Discord. <br>
Mitigation: Do not run scripts/healthcheck.sh unless service restart behavior and Discord alerting are intentional for the target host. <br>
Risk: The skill requires sensitive OpenAI and optional Discord credentials. <br>
Mitigation: Use dedicated, least-privilege credentials and rotate them if the execution environment or logs are exposed. <br>
Risk: Reviewing untrusted diff URLs can create network exposure, especially if internal diff URLs are explicitly allowed. <br>
Mitigation: Avoid untrusted diff URLs and leave ALLOW_INTERNAL_DIFF_URLS unset unless internal network access has been reviewed. <br>
Risk: Voice note transcription reads files from the configured voice-note directory. <br>
Mitigation: Keep VOICE_NOTE_BASE_DIR tightly scoped to non-sensitive review audio files. <br>
Risk: The ClawHub publish helper returns success even though publishing is not implemented. <br>
Mitigation: Do not rely on publish_skill for release automation or deployment confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/ai-code-review-service) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Code review service](artifact/references/code_review_service.py) <br>
- [Healthcheck script](artifact/scripts/healthcheck.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON review results from the service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenAI credentials for voice transcription and may use a Discord webhook for notifications.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json; changelog dated 2026-05-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
