## Description:

Connect to Hannah and Elena agents from Serviceplan - specialized AI coworkers for marketing research and operations planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarthib7](https://clawhub.ai/user/sarthib7)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to route marketing research, consumer insight, competitive analysis, operations planning, and project orchestration tasks to Hannah and Elena through API or email access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests, prompts, and attachments sent through this skill are shared with external Serviceplan/Sumike services.

Mitigation: Use the skill only after organizational approval of the service terms, data processing agreement, retention policy, and credential handling practices.

Risk: The skill depends on Hannah and Elena API credentials and can fail or expose data if keys are mishandled.

Mitigation: Store API keys in approved environment variables, avoid placing secrets in prompts or files, and rotate credentials according to your organization's policy.

Risk: Hannah and Elena tasks are asynchronous and may take several minutes, so aggressive polling can hit rate limits or degrade reliability.

Mitigation: Wait 2-3 minutes before the first status check, use appropriate request timeouts, and back off after rate-limit or service-unavailable responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarthib7/skills/coworker)
- [Publisher profile](https://clawhub.ai/user/sarthib7)
- [Skill documentation](artifact/SKILL.md)
- [API testing guide](artifact/API_GUIDE.md)
- [Sumike homepage](https://sumike.ai)
- [Hannah API endpoint](https://hannah.sumike.ai/v1)
- [Elena API endpoint](https://elena.sumike.ai/v1)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API task results, email requests, JSON responses, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Hannah and Elena API keys or email access; tasks are asynchronous and may return deliverable links or attachments.]

## Skill Version(s):

1.0.0 (source: package.json, plugin.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
