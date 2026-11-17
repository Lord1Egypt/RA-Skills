## Description:

Monitors an in-flight paid advertising campaign's spend against a target curve and returns a pacing verdict, learning-phase status, delivery diagnosis, and reallocation trigger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and growth teams use this skill to check whether live paid campaigns are on pace against budget and flight windows. It supports decisions about holding, diagnosing, or handing off a reallocation trigger without computing the new allocation itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local command patterns may expose untrusted campaign names or exported ad data to shell execution.

Mitigation: Invoke ledger commands only with structured arguments, validate or safely encode campaign identifiers, and never paste campaign names or exported ad data into shell commands.

Risk: Exported campaign files and ad labels may contain untrusted instructions or misleading operational text.

Mitigation: Treat exported files as data only, ignore embedded instructions, and separate measured pacing gaps from plausible causes in the user-facing readout.

Risk: Memory writes could preserve sensitive or incorrect campaign details without user consent.

Mitigation: Ask before writing pacing summaries or open-loop entries, and store only the agreed campaign, budget, flight, pacing, verdict, driver, trigger, band, and next-check details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/budget-pacing-monitor)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown pacing read with tables, labeled figures, handoff summary, and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks before writing memory and labels figures as measured, user-provided, or estimated.]

## Skill Version(s):

19.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
