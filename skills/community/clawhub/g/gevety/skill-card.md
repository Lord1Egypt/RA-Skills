## Description:

Access your Gevety health data, including biomarkers, healthspan scores, biological age, biomarker trajectories, wearable statistics, health protocol items, lab reports, health documents, clinical findings, supplements, medications, activities, and related health content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moclippa](https://clawhub.ai/user/moclippa)

### License/Terms of Use:

MIT-0

## Use Case:

External users connect an agent to their Gevety account so it can retrieve and summarize personal health records, biomarkers, wearable metrics, medications, supplements, activities, lab reports, clinical findings, and protocol actions. The skill is intended for health-data review and organization, not diagnosis or independent medical decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive personal health records through the Gevety API token.

Mitigation: Use it only when the user wants agent access to Gevety health records, protect GEVETY_API_TOKEN, and avoid sharing retrieved values outside the active user interaction.

Risk: The security summary flags an unnecessary remote announcement and update channel that can influence agent responses.

Mitigation: Prefer a version that removes the channel or strictly validates it, and ignore unauthenticated announcements unless they are explicitly trusted.

Risk: Broad health-data retrieval can expose more medical information than needed for a request.

Mitigation: Ask before broad retrieval and request only the endpoints needed to answer the user's current question.

## Reference(s):

- [Gevety](https://gevety.com)
- [Gevety API base URL](https://api.gevety.com)
- [Gevety Developer API settings](https://gevety.com/settings)
- [ClawHub skill page](https://clawhub.ai/moclippa/skills/gevety)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, shell commands, guidance]

**Output Format:** [Markdown with REST API examples, JSON snippets, and concise health-data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEVETY_API_TOKEN for authenticated Gevety API requests.]

## Skill Version(s):

1.12.0 (source: server release metadata; artifact frontmatter is 1.11.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
