## Description:

Smart health management solution with food and exercise recognition, nutrition and calorie analysis, secure data storage, and comprehensive data management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guangxiankeji](https://clawhub.ai/user/guangxiankeji)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to log meals, exercise, and weight, estimate nutrition and calorie burn, and query or manage health-tracking records after confirmation.

### Deployment Geography for Use:

Global, with documented United States and China service endpoints.

## Known Risks and Mitigations:

Risk: The skill handles health-tracking data, email-based authentication, Bearer tokens, screenshots, image URLs, food records, exercise records, weight values, and BMI data through provider services.

Mitigation: Install only when users are comfortable with the provider processing and retaining this information; avoid uploading screenshots or images that expose unrelated personal details.

Risk: Evidence security review reports conflicting privacy claims because the artifact describes local processing while also documenting mandatory cloud storage, cloud analysis APIs, token reuse, and 24-month data retention.

Mitigation: Treat cloud processing and storage as expected behavior, confirm consent before saving records, and review provider privacy and retention terms before deployment.

## Reference(s):

- [ClawHub Calorie Tracker Listing](https://clawhub.ai/guangxiankeji/skills/calorie-tracker)
- [Calorie Tracker Homepage](https://us.guangxiankeji.com/calorie/)
- [United States API Specification](https://us.guangxiankeji.com/calorie/service/user/api-spec)
- [China API Specification](https://cn.guangxiankeji.com/calorie/service/user/api-spec)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Concise natural-language summaries with structured JSON-like nutrition, exercise, weight, and record-management data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include food names, weights, calories, macronutrients, exercise duration and intensity, BMI, trend summaries, and confirmation prompts before storing records.]

## Skill Version(s):

1.0.24 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
