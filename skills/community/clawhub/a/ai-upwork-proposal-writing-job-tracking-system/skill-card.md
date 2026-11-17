## Description:

AI-assisted local assistant that filters Upwork jobs, drafts personalized proposals, tracks applications, and learns from interview or hire outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dttnpole-commits](https://clawhub.ai/user/dttnpole-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers use this skill to review pasted Upwork job listings, reject poor-fit opportunities, draft human-reviewed proposals, and maintain a local history of applications and outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted job fields passed to pre-apply-check.sh could trigger unsafe local command behavior.

Mitigation: Do not run the script on untrusted pasted job data; rely on manual review until numeric validation, job-type allowlisting, duplicate matching, and path handling are fixed.

Risk: Local profile, proposal vault, and application log files can contain personal, client, and proposal details.

Mitigation: Keep these files local, review entries before updates, and avoid sharing them publicly or committing them to version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dttnpole-commits/skills/ai-upwork-proposal-writing-job-tracking-system)
- [Publisher profile](https://clawhub.ai/user/dttnpole-commits)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with proposal drafts, scored job summaries, dashboard metrics, local log or vault entries, and shell preflight results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file updates may append to APPLICATION_LOG.md and PROPOSAL_VAULT.md after user review.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
