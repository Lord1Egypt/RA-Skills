## Description:

Log bKash, Nagad, Rocket, and cash transactions conversationally in Bengali or English, with weekly spending digests for Bangladesh-focused expense tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabbiramin113008](https://clawhub.ai/user/sabbiramin113008)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to log Bangladesh-oriented mobile wallet and cash expenses from conversational Bengali, English, or mixed-language messages, then view recent transactions or weekly spending digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles financial transaction data and the security summary flags inaccurate local-only privacy claims around Anthropic API sharing.

Mitigation: Disclose when transaction text is sent to Anthropic, require explicit opt-in for parsing and digest generation, and provide a documented local-only mode.

Risk: The security guidance flags unsafe shell-string command templates for transaction parsing and logging.

Mitigation: Replace shell-string templates with argument-array execution and preserve quoting for user-supplied transaction notes.

Risk: Automatic weekly digests may run without a fresh user prompt and process stored financial data.

Mitigation: Require explicit opt-in for heartbeat digests and document how users can disable the schedule.

Risk: Stored transaction data may persist locally without clear retention expectations.

Mitigation: Document storage location, deletion behavior, retention policy, and any manual cleanup steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sabbiramin113008/skills/bkash-nagad-tracker)
- [ClawHub Publisher Profile](https://clawhub.ai/user/sabbiramin113008)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown with JSON snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transaction confirmations, weekly digest summaries, recent transaction lists, deletion confirmations, setup guidance, and parser JSON for agent use.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
