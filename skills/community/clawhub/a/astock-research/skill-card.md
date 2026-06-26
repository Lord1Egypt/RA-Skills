## Description: <br>
An A-share equity research framework for analyzing listed companies across fundamentals, capital flows, technical signals, sentiment, and news to prepare trading scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zif10765-maker](https://clawhub.ai/user/zif10765-maker) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Analysts, traders, and agents use this skill to structure A-share company research and draft trading plans from market, company, capital-flow, technical, sentiment, and news signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact ships an embedded QVeris API key. <br>
Mitigation: Remove and rotate the key before release, and require users to provide QVERIS_API_KEY from their own environment. <br>
Risk: The stock lookup script calls an under-documented external market-data helper. <br>
Mitigation: Document the external request path and verify the QVeris helper from a trusted source before running it. <br>
Risk: The skill can generate ratings, position guidance, and trading scenarios. <br>
Mitigation: Present generated outputs as informational research only and require human review before any investment decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zif10765-maker/astock-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research guidance with structured tables and optional bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stock research outputs should be treated as informational analysis, not investment advice.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, target metadata, artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
