## Description: <br>
Analyzes Android project source code and helps generate source-derived testing knowledge so AI test agents know what to test, how to assert outcomes, and which traps to avoid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-lancer](https://clawhub.ai/user/x-lancer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to inspect Android application source, derive business flows and assertions, and package a static profile for AI-driven automated testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Android source code and extracted test data may contain sensitive implementation details, credentials, or production identifiers. <br>
Mitigation: Run the skill only on intended project directories, redact secrets and production credentials before use, and review generated files before committing or uploading them. <br>
Risk: Generated testing guidance can be incomplete or misleading if the analyzed source is partial or stale. <br>
Mitigation: Validate generated flows, assertions, and static-profile content against the target app before using them in automated test runs. <br>


## Reference(s): <br>
- [Output schema](artifact/references/output_schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON static-profile artifacts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces source-derived testing knowledge, LLM prompts, navigation graph JSON, and static-profile JSON for manual review and import.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
