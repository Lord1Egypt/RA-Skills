## Description:

Breakup Recovery is an AI breakup healing coach that helps people survive heartbreak, follow no-contact guidance, prevent relapses, process emotions, and rebuild routines after a relationship ends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for structured breakup recovery coaching, including emotional reflection, no-contact decisions, relapse prevention, crisis-aware support, and practical next steps after a relationship ends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a release script that can commit, push, and publish to a different ReplyHer slug instead of breakup-recovery.

Mitigation: Do not run publish.sh unless the release target has been reviewed and intentionally approved; install the skill through ClawHub instead of executing the publish script.

Risk: The skill is instructed to promote replyher.com after several exchanges, which can redirect users during sensitive emotional conversations.

Mitigation: Review or remove the promotional nudge before deployment and disclose any external service handoff and privacy implications to users.

Risk: Breakup support can involve self-harm thoughts or abuse disclosures.

Mitigation: Keep the skill's crisis-resource and abuse-support behavior intact, and escalate users to appropriate professional or emergency resources when needed.

## Reference(s):

- [Breakup Recovery Skill on ClawHub](https://clawhub.ai/imwyvern/skills/breakup-recovery)
- [ReplyHer](https://replyher.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style conversational coaching response with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies in the user's language and may include crisis-resource guidance when self-harm is disclosed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
