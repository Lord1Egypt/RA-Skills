## Description:

Analyzes Android project source code to generate static prior-knowledge profiles that help AI automated testing agents understand business flows, assertions, state dependencies, edge cases, test traps, and executable test cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-lancer](https://clawhub.ai/user/x-lancer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and AI testing agents use this skill to analyze Android application source code and produce a static-profile JSON package before automated tests run. The profile gives downstream agents concise guidance on what to test, how to navigate core flows, what to assert, and which dead ends or risky actions to avoid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Android source code and may include sensitive implementation details, credentials, or proprietary information in generated profile text.

Mitigation: Run it only on projects approved for LLM processing, add redaction where needed, and review static-profile.json before committing or uploading it.

Risk: Generated static-profile content can be inaccurate or misleading because it depends on source interpretation and LLM-generated summaries.

Mitigation: Treat generated profile text as untrusted input to downstream agents and have a developer or QA reviewer confirm flows, assertions, and test data before use.

Risk: Using the wrong project path can expose unrelated source files or produce an incorrect test profile.

Mitigation: Confirm the exact Android project path before running analysis.

## Reference(s):

- [Android Static Profile output schema](references/output_schema.json)
- [ClawHub skill page](https://clawhub.ai/x-lancer/skills/android-static-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON static-profile file plus Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated profile is intended for review before upload or commit because it may summarize source code, credentials, or proprietary details.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
