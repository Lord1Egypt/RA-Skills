## Description:

Architecture personal assistant for daily news digests, project tracking, research scouting, design concept exploration, client message drafting, and passive project context capture for independent architects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hao-tian-xu](https://clawhub.ai/user/hao-tian-xu)

### License/Terms of Use:

MIT-0

## Use Case:

Independent architects use this skill to track active projects, maintain project notes, compile architecture news digests, scout research and competitions, explore design concepts, and draft professional client or collaborator messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can passively capture project context during future conversations and update workspace notes without asking each time.

Mitigation: Install only when passive capture is desired, review the generated workspace rules, and remove the project-capture directive from workspace/AGENTS.md to disable it.

Risk: Project files may store sensitive client, payment, team, budget, deadline, and decision details in Markdown.

Mitigation: Keep the workspace access-controlled, avoid entering unnecessary sensitive data, and periodically review or delete stored project notes.

Risk: The first-run flow recommends scheduled background digest, check-in, and research runs.

Mitigation: Review cron entries before enabling them, make scheduled behavior explicit to users, and remove unwanted jobs from the user's crontab.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hao-tian-xu/skills/architect-assistant)
- [Publisher profile](https://clawhub.ai/user/hao-tian-xu)
- [Architecture Information Sources](references/config/sources.md)
- [Project Template](references/project-template.md)
- [Materials Knowledge Reference](references/knowledge/materials.md)
- [Construction Methods Knowledge Reference](references/knowledge/construction.md)
- [Cost & Schedule Knowledge Reference](references/knowledge/cost-schedule.md)
- [Retail & Commercial Design Knowledge Reference](references/knowledge/retail-commercial.md)
- [Sustainability Knowledge Reference](references/knowledge/sustainability.md)
- [Digest Procedure](references/procedures/digest.md)
- [Research Procedure](references/procedures/research.md)
- [Check-in Procedure](references/procedures/checkin.md)
- [Concept Exploration Procedure](references/procedures/concept-explore.md)
- [Draft Message Procedure](references/procedures/draft-message.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with generated workspace files and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project files, digest files, source configuration, workspace agent rules, and cron setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
