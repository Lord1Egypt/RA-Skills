## Description:

Baize Task Bot helps outbound-call operations teams query task, line, script, and template data and perform Baize platform actions for AI outbound campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard-collab](https://clawhub.ai/user/richard-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Operations staff and administrators use this skill to inspect AI outbound-call tasks, lines, scripts, templates, and concurrency, parse natural-language operation requests into structured instructions, and carry out approved campaign or account changes in Baize.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write actions can start, stop, resume, or modify outbound-call campaigns and create accounts using a shared Baize API token.

Mitigation: Install only in a controlled Baize operations environment with an HTTPS-only BAIZE_BASE_URL, a least-privileged BAIZE_TOKEN, and external approval controls for every write action.

Risk: Campaign starts, concurrency changes, line changes, regional blocking changes, and account creation are high-impact operations with weak in-skill safeguards.

Mitigation: Require confirmation enforcement in the agent workflow or Baize server before executing these operations, and avoid broad admin tokens until role checks are in place.

Risk: Local task and line data used for lookup or natural-language instruction parsing may be stale relative to the live Baize platform.

Mitigation: Refresh the bundled JSON data and verify resolved task IDs, line IDs, and account scope before executing any write operation.

## Reference(s):

- [Skill documentation](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/richard-collab/skills/baize-task-bot)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text summaries and JSON instruction arrays]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single response per tool call; action tools return Baize success or error messages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
