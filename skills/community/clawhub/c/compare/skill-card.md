## Description:

Rigorous comparisons with confidence parity, weighted criteria, and research depth tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to compare products, tools, services, decisions, places, providers, investments, or media with balanced research depth, weighted criteria, transparent scoring, and caveats when evidence quality differs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remember comparison priorities in preferences.md, which may preserve sensitive preferences for categories such as career, finances, or providers.

Mitigation: Review, clear, or avoid updating preferences.md when comparisons involve sensitive categories or when persistent preference memory is not desired.

Risk: Uneven research depth can make comparison scores misleading.

Mitigation: Track comparable source depth, source quality, and recency for each item before scoring, and explicitly caveat any remaining imbalance.

## Reference(s):

- [Confidence Levels](artifact/confidence.md)
- [Default Comparison Criteria by Domain](artifact/domains.md)
- [User Comparison Preferences](artifact/preferences.md)
- [Comparison Traps](artifact/traps.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown comparison report with weighted criteria, score tables, confidence labels, caveats, and conditional recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local preferences file after comparisons to record user priorities by category.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
