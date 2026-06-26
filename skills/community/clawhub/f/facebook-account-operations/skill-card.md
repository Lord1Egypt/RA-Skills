## Description: <br>
Operating doctrine for Facebook Page automation through Meta Business Suite, with role separation, Page-vs-profile-vs-group surface awareness, comment and Messenger workflows, moderation discipline, and recovery patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, agencies, and developers use this skill to guide agents that assist with owned Facebook Page inbox, comment, posting, and moderation workflows while preserving Page Quality and account safety. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent could act outside the intended owned Facebook Page workflow or attempt outbound engagement on other Pages. <br>
Mitigation: Limit use to Meta Business Suite Page inbox, comments, and moderation for owned Pages, and require human approval for outbound comments on other Pages. <br>
Risk: Logged-in browser profiles, alert webhooks, and local memory logs may expose account access or user conversation data. <br>
Mitigation: Protect browser profiles and webhook URLs, and define local retention, redaction, and restricted-access rules for logs before deployment. <br>
Risk: Unsafe automation behavior can affect Page Quality or trigger Facebook restrictions. <br>
Mitigation: Apply the skill's phase gates, quotas, Page Quality checks, and recovery playbook, and stop automation when warnings, restrictions, or session problems appear. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/alexbloch-ia/facebook-account-operations) <br>
- [Meta Business Suite Inbox](https://business.facebook.com/latest/inbox) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides doctrine, quotas, checklists, memory-file conventions, and recovery guidance for agent-assisted Facebook Page operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
