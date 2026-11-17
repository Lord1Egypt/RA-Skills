## Description:

Guides Android developers through integrating the AMap LLM Agent SDK for natural-language map and navigation interactions, including quick setup, AI queries, result handling, AMap app linking, transport modes, logging, lifecycle management, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs-amap](https://clawhub.ai/user/lbs-amap)

### License/Terms of Use:

MIT-0

## Use Case:

External Android developers use this skill to integrate AMap's LLM Agent SDK into Android applications and generate code or guidance for SDK initialization, natural-language navigation queries, result handling, AMap app linking, lifecycle cleanup, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated integrations can collect or share location and navigation context.

Mitigation: Require explicit user consent and Android runtime permissions before location updates or data sharing, and call the required privacy policy APIs before SDK use.

Risk: Voice or text commands can trigger navigation-changing actions or remote AMap app control.

Mitigation: Keep command destinations scoped, avoid passive or global voice activation, and add user confirmations before starting or stopping navigation, switching routes, or invoking cross-app actions.

Risk: Dynamic SDK dependencies and verbose logging can introduce supply-chain or sensitive-data exposure risks.

Mitigation: Pin SDK versions for production builds, review generated Android code, and remove or redact production logs that may contain locations, session identifiers, route details, or error payloads.

## Reference(s):

- [Quick Start](artifact/api/quick-start.md)
- [Agent Query API](artifact/api/agent-query.md)
- [Query Result Handling](artifact/api/query-result.md)
- [LinkClient AMap App Communication](artifact/api/link-client.md)
- [Lifecycle Management](artifact/api/lifecycle.md)
- [Core Classes](artifact/references/core-classes.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Voice Commands](artifact/references/voice-commands.md)
- [AMap Open Platform Console](https://console.amap.com/)
- [Cursor Official Documentation](https://docs.cursor.com/)
- [ClawHub Skill Page](https://clawhub.ai/lbs-amap/skills/android-llm-agent-sdk)
- [Publisher Profile](https://clawhub.ai/user/lbs-amap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Java, Gradle, XML, shell, and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Android SDK integration snippets, dependency declarations, lifecycle guidance, troubleshooting steps, and navigation command examples.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
