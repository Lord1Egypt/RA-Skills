## Description:

Track AI agents' balances, income, costs, runway, service valuation, and work-or-learn recommendations using local JSONL history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

Agents, developers, and operators use this skill to record local income and cost events, calculate financial runway, and receive economic status reports and work-or-learn recommendations for agent operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores balance, cost, and income history locally in JSONL files.

Mitigation: Use a dedicated ECONOMIC_TRACKER_DATA_DIR and avoid recording sensitive financial details in free-text descriptions.

## Reference(s):

- [AI Economic Tracker ClawHub page](https://clawhub.ai/dagangtj/skills/ai-economic-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text reports, JSON command output, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSONL balance, income, and cost history when executed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
