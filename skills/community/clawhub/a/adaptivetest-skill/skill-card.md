## Description:

Adaptive testing engine with IRT/CAT, AI question generation, and personalized learning recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodstocksoftware](https://clawhub.ai/user/woodstocksoftware)

### License/Terms of Use:

proprietary

## Use Case:

Developers and education teams use this skill to call the AdaptiveTest API for adaptive assessments, AI question generation, learning recommendations, item calibration, student and class management, and results analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an AdaptiveTest API key and may access sensitive education records.

Mitigation: Keep ADAPTIVETEST_API_KEY in the environment, do not expose it in prompts or logs, and use real student identifiers only when privacy requirements are satisfied.

Risk: The API supports record creation, updates, enrollment, calibration, and deletion workflows.

Mitigation: Require explicit user confirmation before creating, changing, enrolling, calibrating from, or deleting records.

Risk: Adaptive testing and calibration quality depends on adequate item data and representative response samples.

Mitigation: Confirm item calibration prerequisites, response counts, and sample diversity before using calibration results or relying on CAT behavior.

## Reference(s):

- [AdaptiveTest API Endpoint Reference](references/api-endpoints.md)
- [Adaptive Testing Concepts](references/adaptive-testing.md)
- [Item Calibration Guide](references/calibration.md)
- [AdaptiveTest Developer Site](https://adaptivetest.io/developers)
- [AdaptiveTest API Base URL](https://adaptivetest-platform-production.up.railway.app/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples and curl-style API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ADAPTIVETEST_API_KEY and curl; API rate limits depend on the account tier.]

## Skill Version(s):

1.0.1 (source: frontmatter, clawhub.json, CHANGELOG released 2026-02-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
