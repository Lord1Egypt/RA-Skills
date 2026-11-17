## Description:

Argus Edge helps agents analyze prediction-market betting opportunities by estimating expected value from TA-implied probability versus market odds, applying freshness and consensus guards, and proposing Kelly-style sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamierossouw](https://clawhub.ai/user/jamierossouw)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for prediction-market edge analysis, EV calculations, Polymarket strategy checks, market scans, and Kelly-style stake-sizing recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides prediction-market betting analysis and includes win-rate and edge claims that server security guidance treats as unverified.

Mitigation: Require human review of assumptions and calculations before acting, and do not treat outputs as guaranteed performance or financial advice.

Risk: The skill can prompt live market scans and stake-sizing recommendations that may influence financial decisions.

Mitigation: Require explicit user confirmation before live market analysis or sizing, prohibit automated bet placement, and do not provide account credentials to an agent based solely on this skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown or plain text betting analysis with formulas, market checks, and sizing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include expected-value estimates, freshness or consensus checks, asset calibration notes, and Kelly-style stake-sizing guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
