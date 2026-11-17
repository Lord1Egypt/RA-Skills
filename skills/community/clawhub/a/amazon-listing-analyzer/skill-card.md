## Description:

Amazon Listing Analyzer provides offline listing health scoring, keyword analysis, competitor benchmarking, and structured optimization advice for mid-level Amazon sellers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce operators use this skill to review listing quality, identify keyword opportunities, compare against competitor templates, and receive structured optimization suggestions without real-time marketplace data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste Amazon account credentials, personal information, or confidential business data into listing inputs.

Mitigation: Provide only the listing text needed for analysis and exclude credentials, personal information, and confidential business data.

Risk: Reports are Chinese-localized and may be unsuitable for teams that require English output.

Mitigation: Install only when Chinese-localized reports are acceptable, or route outputs through an approved translation and review process.

Risk: Malformed or overlong inputs may fail instead of returning a clean error.

Mitigation: Keep inputs within the documented 10,000-character limit and validate JSON fields before invoking the skill.

Risk: Optimization advice is generated from built-in rules and templates, not live Amazon marketplace or compliance data.

Mitigation: Treat recommendations as reference guidance and verify final listing changes against current Amazon policies and marketplace research.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/amazon-listing-analyzer)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)
- [Artifact documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON reports with Chinese-localized analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline rule-based analysis; no network calls, persistence, hidden data access, or destructive behavior reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
