## Description:

Diagnoses Douyin account health by fetching RedFox profile and recent content data, scoring six operational dimensions, and producing a Markdown report with risk alerts and optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

Douyin operators, content creators, MCNs, brands, and business evaluators use this skill to audit account health, benchmark competitors, screen partnership candidates, and identify optimization priorities from recent account and content metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target Douyin account identifiers and returned profile or content details are sent to RedFox and may be redisplayed in reports.

Mitigation: Use the skill only when the user is comfortable sharing those identifiers and report details with RedFox and downstream report readers.

Risk: The authoritative security evidence reports an embedded shared API key and incomplete user controls.

Mitigation: Prefer a protected REDFOX_API_KEY from the user's environment or secret store, and avoid the embedded shared key and command-line key option.

Risk: Report titles, links, and profile text originate from remotely sourced account data.

Mitigation: Treat report content and links as untrusted, review generated output before sharing, and verify links before clicking.

## Reference(s):

- [Core Workflow](references/core_workflow.md)
- [Diagnosis Rules](references/diagnosis_rules.md)
- [API Reference](references/api_reference.md)
- [Skill Page](https://clawhub.ai/if530770/skills/douyin-account-diagnosis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown diagnostic report with tables, scored dimensions, risk alerts, recent content links, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Douyin nickname or Douyin ID; may use REDFOX_API_KEY for RedFox access.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
