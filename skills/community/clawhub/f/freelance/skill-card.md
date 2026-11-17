## Description:

Helps agents advise freelancers and contractors on rates, pipeline health, cash buffers, taxes, contracts, payment disputes, classification, insurance, and growth decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to reason about operating an independent freelance or contractor practice, including pricing, pipeline, cash flow, tax set-asides, contracts, late payment, classification, and scaling. It can also draft reviewable business text such as quotes, chase messages, clauses, outreach notes, and reusable practice documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read, write, move, or delete persistent local business records as part of maintaining freelance-practice memory.

Mitigation: Back up ~/Clawic/data before using it on real records, and require explicit approval for migrations, deletions, shared contact or finance updates, and dispute notes.

Risk: Freelance guidance can affect contracts, tax treatment, worker classification, and payment disputes.

Mitigation: Treat outputs as business guidance and review jurisdiction-specific legal, tax, or contractual decisions with an appropriate professional before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/freelance)
- [Clawic Freelance skill page](https://clawic.com/skills/freelance)
- [Clawic skill library](https://clawic.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured calculations, draft business text, and local configuration or memory updates when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local business memory under configured Clawic data paths when durable freelance-practice facts are produced.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
