## Description:

Monitor competitor clinical trial progress and alert on market risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and pharma competitive intelligence teams use this skill to maintain a watchlist of clinical trials, scan for status changes, and generate risk reports about competitor trial milestones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags contradictory dependency guidance and unnecessary unpinned pip install instructions.

Mitigation: Review installation steps before use; avoid installing the documented packages unless the publisher pins real dependencies or confirms no external packages are required.

Risk: The skill sends queried NCT IDs to ClinicalTrials.gov and stores watchlists and alert history in the user's home directory.

Mitigation: Use only trial identifiers appropriate for external registry queries and review local files under ~/.openclaw/competitor-trial-monitor before sharing or retaining outputs.

## Reference(s):

- [Competitor Trial Monitor on ClawHub](https://clawhub.ai/aipoch-ai/skills/competitor-trial-monitor)
- [ClinicalTrials.gov API](https://clinicaltrials.gov/api/v2/studies)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Command-line text output, JSON files, and Markdown-style reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores watchlists, historical snapshots, alerts, and configuration under ~/.openclaw/competitor-trial-monitor.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
