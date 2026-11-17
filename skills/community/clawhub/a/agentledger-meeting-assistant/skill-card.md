## Description:

AI meeting partner for solopreneurs and professionals. Generates pre-meeting briefs from your notes and context, captures structured meeting notes during the conversation, and produces action item summaries with owners and deadlines. Integrates with project-tracker, inbox-triage, client-relationship-manager, and solopreneur-assistant skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

Solopreneurs and professionals use this skill to prepare for meetings, capture structured notes, extract action items, maintain local meeting records, and review overdue commitments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting records and action lists can contain privacy-sensitive business information.

Mitigation: Keep the meetings folder scoped to the intended workspace, treat it as sensitive, and review access before sharing or syncing it.

Risk: Follow-up drafts or newsletter ideas generated from meeting notes may expose confidential or inaccurate information if shared without review.

Mitigation: Manually review all outbound drafts and content ideas before sending or publishing them.

Risk: Automatic routing could apply the meeting workflow to unrelated requests.

Mitigation: Use explicit meeting-assistant phrasing when invoking the skill in environments that auto-route skills.

## Reference(s):

- [Meeting Assistant - Advanced Patterns](references/advanced-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local meeting logs, open action lists, meeting archives, agendas, metrics, and follow-up drafts.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
