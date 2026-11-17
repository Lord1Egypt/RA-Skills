## Description:

Your personal health data hub for AI agents. Query genomic insights, upload medical documents, record daily health metrics, explore genomic-lab cross-references, receive personalized daily health briefings, and get contextual health advice woven into everyday conversations -- all powered by your actual genetic and clinical data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangchen](https://clawhub.ai/user/gangchen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to connect to Gene2AI, query personalized genomic and clinical health data, upload health documents with confirmation, log daily metrics, and receive contextual health briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and update sensitive health and genetic information.

Mitigation: Install only when Gene2AI access through the agent is intended; require explicit user confirmation before uploads or health-data updates.

Risk: The skill instructions allow sensitive health-profile conclusions to be cached or memorized across sessions.

Mitigation: Disable or revise cross-session memory behavior unless the user has explicitly consented to durable retention of health information.

Risk: The skill instructions allow undisclosed scheduled health nudges.

Mitigation: Disable hidden proactive scheduling or require clear user consent and visibility for any scheduled health messages.

## Reference(s):

- [Gene2AI Guide](https://gene2.ai/guide)
- [ClawHub Skill Page](https://clawhub.ai/gangchen/skills/gene2ai-openclaw-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with curl examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the profile-scoped GENE2AI_API_KEY environment variable.]

## Skill Version(s):

0.1.5 (source: server release metadata; artifact frontmatter reports 3.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
