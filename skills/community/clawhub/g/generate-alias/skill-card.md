## Description:

Generates concise Chinese enterprise aliases and brand keywords from company names for matching and import workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyqdq888](https://clawhub.ai/user/hyqdq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data operations teams use this skill to normalize Chinese enterprise names into concise aliases or brand keywords for entity matching, imports, and deduplication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional public lookup modes may disclose private or internal company names to third-party web services.

Mitigation: Keep the default offline mode for confidential names, and enable public lookup modules only for queries that are safe to share externally.

Risk: Alias generation based on static mappings and rules may produce incomplete or outdated aliases for some enterprises.

Mitigation: Review generated aliases before using them in high-impact matching, import, or deduplication pipelines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyqdq888/skills/generate-alias)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text alias lists separated with |, with optional Markdown examples and command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline rule-based generation is the default; optional public web and Wikipedia lookups can send queried company names to third-party services when enabled.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
