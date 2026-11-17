## Description:

HunterAI helps freelancers qualify Upwork opportunities, draft tailored proposals, maintain a local application ledger, and promote successful hooks into a reusable proposal vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dttnpole-commits](https://clawhub.ai/user/dttnpole-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers and small agencies use this skill to screen Upwork-style job opportunities against budget, client quality, competition, skills, and blacklist criteria, then generate proposal drafts and local run reports. It is also used to track application outcomes and reuse hooks from proposals that led to interviews or hires.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files may contain freelancer profile details, generated proposals, job history, and reusable winning hooks.

Mitigation: Keep the workspace private, avoid committing sensitive local data, and review or redact profile, ledger, and vault files before sharing the skill workspace.

Risk: Generated proposal drafts could include inaccurate claims, overstate capabilities, or fail to match the freelancer's real experience.

Mitigation: Review each proposal before submission and keep FREELANCER_PROFILE.md limited to accurate skills, rates, and credibility anchors.

Risk: The skill uses auto-apply language, but server security guidance treats it as local drafting and logging unless connected to a real Upwork workflow.

Mitigation: Require explicit human review and confirmation before any real Upwork submission or external automation is connected.

Risk: Qualification and blacklist rules may reject or prioritize jobs incorrectly if the local criteria files are stale or incomplete.

Mitigation: Regularly update FREELANCER_PROFILE.md and IDEAL_JOB_CRITERIA.md, and inspect qualification reports before relying on a run's recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dttnpole-commits/skills/ai-upwork-job-auto-apply-system)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Freelancer profile template](artifact/FREELANCER_PROFILE.md)
- [Ideal job criteria and scoring rubric](artifact/IDEAL_JOB_CRITERIA.md)
- [Proposal vault](artifact/PROPOSAL_VAULT.md)
- [Pre-apply qualification filter](artifact/pre-apply-check.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, proposal drafts, application log entries, proposal-vault updates, and human-readable shell output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates local workspace files for freelancer profile data, job criteria, proposal hooks, and application history.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
