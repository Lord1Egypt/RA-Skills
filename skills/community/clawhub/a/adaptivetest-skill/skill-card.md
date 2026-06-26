## Description: <br>
Adaptive testing engine with IRT/CAT, AI question generation, and personalized learning recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woodstocksoftware](https://clawhub.ai/user/woodstocksoftware) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Educators, assessment developers, and education-platform teams use this skill to create and administer adaptive tests, generate assessment questions, calibrate items, manage student and class records, and retrieve learning recommendations and analytics from the AdaptiveTest API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send student, class, assessment, response, and analytics data to the remote AdaptiveTest API. <br>
Mitigation: Use it only when authorized to share that data with AdaptiveTest, minimize student PII where possible, and follow the applicable education data policies for the deployment. <br>
Risk: ADAPTIVETEST_API_KEY is an account credential for authenticated API access. <br>
Mitigation: Store the key in the environment or a secret manager, avoid pasting it into prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Some workflows create, update, delete, enroll, submit, or calibrate records in the AdaptiveTest service. <br>
Mitigation: Review request payloads and confirm before delete, bulk enrollment, calibration, or other record-changing actions. <br>
Risk: AI-generated questions and personalized recommendations may be unsuitable without domain review. <br>
Mitigation: Have qualified educators or content owners review generated items, rationales, standards alignment, and recommendations before using them for instruction or assessment. <br>


## Reference(s): <br>
- [AdaptiveTest API endpoint reference](references/api-endpoints.md) <br>
- [Adaptive testing concepts](references/adaptive-testing.md) <br>
- [Item calibration guide](references/calibration.md) <br>
- [AdaptiveTest API base URL](https://adaptivetest-platform-production.up.railway.app/api) <br>
- [AdaptiveTest developer homepage](https://adaptivetest.io/developers) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with HTTP endpoint examples, shell commands, and JSON request and response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and an ADAPTIVETEST_API_KEY environment variable for authenticated API requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, SKILL.md frontmatter, clawhub.json, and CHANGELOG.md released 2026-02-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
