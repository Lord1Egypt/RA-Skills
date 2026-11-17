## Description:

Designs paid-ad creative, landing-page, and incrementality tests, then reads user-owned exported results for effect size, uncertainty, guardrails, and owner-governed decision status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, growth teams, and analytics practitioners use this skill to design A/B/n or incrementality tests for paid advertising and to interpret completed tests from their own exported performance data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process ad test briefs or exported performance CSVs that contain sensitive business data.

Mitigation: Use only data the user is comfortable sharing with the agent and keep exported inputs within the user's normal data-handling workflow.

Risk: Statistical read-outs can be mistaken for authorization to change live campaigns.

Mitigation: Treat output as design and interpretation support; require the named decision owner and precommitted action rule before making campaign changes.

## Reference(s):

- [Ad Test Design Guide](references/test-design-guide.md)
- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/ad-test-designer)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown with structured test design or read-out sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a handoff summary, documented assumptions, calculated statistical fields, guardrail status, and decision UNDECIDED when owner approval or precommitted action rules are missing.]

## Skill Version(s):

19.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
