## Description:

caibao is a Chinese-language financial statement analysis skill that interprets reported financial data, asset-heavy cycle signals, fraud warnings, and investment decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houyucheg](https://clawhub.ai/user/houyucheg)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and financial analysts use this skill to receive concise Chinese-language interpretation of stock financial reports, industrial-cycle signals, and fraud-risk alerts. Its conclusions should support human review rather than automatic trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide investment-style conclusions such as adding a stock to a core pool or blacklisting it.

Mitigation: Verify the underlying financial data and treat outputs as analysis for human review rather than automatic trading instructions.

Risk: The evidence reports no executable code, persistence, network behavior, or data-access mechanism, so the skill depends on data supplied by the user or surrounding agent workflow.

Mitigation: Provide current, source-checked financial statements and alert data before relying on the analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houyucheg/skills/caibaojiedu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown or plain-text financial analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; analysis quality depends on verified financial data and alerts supplied to the agent.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
