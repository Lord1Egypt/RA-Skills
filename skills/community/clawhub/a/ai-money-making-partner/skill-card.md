## Description:

Sidekick Os Pro V2.0 helps agents generate personalized Chinese side-income plans based on a user's skills, available time, budget, income goal, and market assumptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect a user's side-income constraints, compare suitable opportunities, create a phased execution plan, and track progress with follow-up suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for personal work, time, budget, and income-goal details.

Mitigation: Collect only the details needed for planning, avoid sensitive financial identifiers, and make clear how the information will be used.

Risk: Market and income recommendations may be stale, incomplete, or overconfident if the agent does not perform current research.

Mitigation: Verify market conditions with current sources before presenting recommendations and label income estimates as non-guaranteed examples.

Risk: The progress tracker can save local progress notes.

Mitigation: Tell the user before saving progress locally, avoid sensitive notes, and delete stored tracker files when no longer needed.

Risk: The skill is written for Chinese output by default.

Mitigation: Ask for the user's preferred language when Chinese output is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/e2e5g/skills/ai-money-making-partner)
- [SKILL.md](artifact/SKILL.md)
- [Market analyzer script](artifact/scripts/market_analyzer.py)
- [Proposal generator script](artifact/scripts/proposal_generator.py)
- [Execution tracker script](artifact/scripts/tracker.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, JSON]

**Output Format:** [Markdown guidance with structured plan sections; helper scripts can emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese by default; outputs may include income estimates, market assumptions, phased action plans, and progress summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
