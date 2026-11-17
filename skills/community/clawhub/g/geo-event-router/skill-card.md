## Description:

Analyzes, classifies, scores, and routes geostrategic news events using multi-factor scoring and optional LLM semantic analysis for push decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to integrate geostrategic news event detection, scoring, fingerprinting, and push-routing decisions into market monitoring or operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a Chinese-language utility, which may not fit teams that require English-language operational review.

Mitigation: Confirm Chinese-only output is acceptable before installation and add translation or bilingual review steps where required.

Risk: The optional LLM analyzer may receive truncated news content if that dependency is installed.

Mitigation: Enable optional LLM analysis only under approved data-handling and model-use policies, and review what news content is sent before use.

Risk: The security review notes a limited cooldown bug, so alert suppression may not be reliable for strict anti-spam or alert-fatigue controls.

Mitigation: Fix and test cooldown behavior before relying on the skill for strict notification throttling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liweijie0709-cmyk/skills/geo-event-router)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python API examples; Python functions return event classifications, scores, fingerprints, push decisions, and dataclass objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language documentation; optional LLM semantic analysis can be used for selected high-value news candidates.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
