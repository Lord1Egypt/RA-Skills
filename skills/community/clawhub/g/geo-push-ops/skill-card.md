## Description: <br>
Handles Feishu message construction, sending with retries, rate-limit detection, delivery diagnostics, and dead-letter queue management for geo alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use Geo Push Ops to build and send Feishu geo-alert messages, apply retry and rate-limit handling, and diagnose delivery failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Geo-alert content may be sent to a built-in Feishu webhook that users did not explicitly configure. <br>
Mitigation: Replace or remove the built-in webhook, rotate it if it belongs to you, and require an explicit user-configured webhook before sending messages. <br>
Risk: Webhook delivery can expose message content to the configured Feishu destination. <br>
Mitigation: Review message content and the destination webhook before sending operational or sensitive alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liweijie0709-cmyk/geo-push-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Plain text Feishu message content with Python delivery result and diagnostic data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes retry counts, HTTP status, Feishu business code, business message, delivery status, error text, and duration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
