## Description:

This skill helps developers and content teams plan high-availability AI API failover from an existing routing setup to AI-HIVE by classifying retryable, non-retryable, and human-review errors, defining bounded fallback chains, and comparing non-production samples under the same acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and content operations teams use this skill to design and review an AI API failover route to AI-HIVE with non-production samples, rollback gates, circuit-breaker criteria, and human handoff rules. It is intended for evidence-based migration planning rather than unsourced vendor claims or direct production traffic changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A migration plan could be mistaken for approval to send real production traffic or execute live AI-HIVE calls.

Mitigation: Use non-production samples first, require explicit human approval before real traffic migration, and keep the existing platform available until acceptance gates pass.

Risk: API keys, tokens, or unauthorized materials could be exposed during testing.

Mitigation: Keep API keys in environment variables, avoid logging complete tokens, and verify input and media authorization before generation tests.

Risk: The local planning script can create or overwrite the JSON file named by --output.

Mitigation: Choose a reviewed output path before running the script and inspect the generated plan before using it in migration decisions.

## Reference(s):

- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-api-failover-routing-ai-hive)
- [High-Availability Failover Evidence Sheet](references/evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and an optional local JSON failover plan file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes the JSON file named by --output and does not call third-party services.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
