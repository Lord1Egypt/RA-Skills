## Description:

Evaluates whether a company may be suitable for 10-year holding using a Duan Yongping-inspired long-term investment checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment researchers use this skill to structure a long-term company holding review across industry durability, moat, management, financial health, valuation, and shareholder returns. Outputs should be treated as an analysis checklist rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce directive buy, hold, reduce, sell, or avoid recommendations from simplified scoring.

Mitigation: Treat outputs as research prompts and checklist results, not as instructions to buy, hold, or sell; verify conclusions with independent research or professional advice.

Risk: Long-horizon investment forecasts can be overconfident or miss disruption, policy, market, or black-swan risks.

Mitigation: Use conservative assumptions, scenario analysis, and periodic review before relying on any long-term holding conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lj22503/skills/duan-longterm)
- [Publisher profile](https://clawhub.ai/user/lj22503)
- [Long-term test template](artifact/templates/longterm-template.md)
- [Local checklist script](artifact/scripts/check-longterm.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown checklist and optional terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external data access; the local helper script can print a scored checklist for a company name.]

## Skill Version(s):

2.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
