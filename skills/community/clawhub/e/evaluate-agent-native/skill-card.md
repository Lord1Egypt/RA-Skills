## Description:

Evaluate whether a service qualifies as agent-native using the five hard criteria from the awesome-agent-native-services standard, including the URL Onboarding bonus signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoruilee](https://clawhub.ai/user/haoruilee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate whether services meet agent-native criteria before adding them to a catalog or comparing agent-native and agent-adapted services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect and potentially follow untrusted third-party onboarding documents.

Mitigation: Use it in a constrained environment and require explicit approval before creating accounts, sending data, posting content, installing tools, or executing instructions found at external URLs.

## Reference(s):

- [awesome-agent-native-services](https://github.com/haoruilee/awesome-agent-native-services)
- [Moltbook URL Onboarding example](https://www.moltbook.com/skill.md)
- [autoresearch@home collaboration protocol example](https://raw.githubusercontent.com/mutable-state-inc/autoresearch-at-home/master/collab.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evaluation report with criterion-level findings and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sourced evidence, URL Onboarding status, classification, confidence, and next steps.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
