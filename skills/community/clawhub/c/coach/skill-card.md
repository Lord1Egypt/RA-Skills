## Description:

Coach helps an agent run coaching conversations, shape goals and commitments, support professional coaching workflows, and route clinical or crisis situations out of scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and coaching practitioners use this skill to run coaching sessions, create accountability structures, set and review goals, prepare intake and agreements, and distinguish coaching from therapy, consulting, mentoring, or managing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically read and write broad local records about coaching, contacts, projects, health, and finances.

Mitigation: Install it only when long-term local coaching records are desired; restrict access to coaching-only files where possible and ask the agent to confirm writes before applying them.

Risk: Client records may include sensitive coaching history, goals, commitments, rates, referrals, or sponsor context.

Mitigation: Review stored records periodically, delete client records when requested or no longer needed, and avoid storing health or finance information unless it is explicitly required for the coaching goal.

Risk: The skill covers boundaries near clinical, crisis, financial, legal, and employment topics.

Mitigation: Use the skill's referral and red-flag guidance to stop coaching when clinical care, emergency help, licensed advice, or specialist support is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/coach)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Clawic Coach skill page](https://clawic.com/skills/coach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown and plain text coaching guidance with optional local note updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or update local coaching notes, commitments, client records, due dates, and configuration files under declared local data paths.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
