## Description: <br>
Automates Evenrealities order-status checks with Playwright, local status history, and change-only notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thibautrey](https://clawhub.ai/user/thibautrey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with Evenrealities orders use this skill to configure order tracking, run manual checks, and schedule recurring checks that report only status changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order email addresses, order IDs, and status history are stored in local plaintext JSON files. <br>
Mitigation: Keep the memory files out of version control and shared folders, and remove stored order data when tracking is no longer needed. <br>
Risk: Each check submits order email and order ID values to Evenrealities and depends on the tracking site remaining available and compatible with the automation. <br>
Mitigation: Use the skill only for orders you are authorized to track, and review failed or unexpected status results manually on the tracking site. <br>
Risk: A scheduled daily check continues running until the cron job is removed. <br>
Mitigation: Remove the cron job when automated checks are no longer wanted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thibautrey/evenrealities-tracker) <br>
- [Evenrealities tracking](https://track.evenrealities.com) <br>
- [Playwright Python documentation](https://playwright.dev/python/docs/intro) <br>
- [Example orders configuration](references/evenrealities-orders-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local order configuration and status-history JSON files when used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
