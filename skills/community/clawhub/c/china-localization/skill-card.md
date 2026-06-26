## Description: <br>
China Localization provides Chinese-language prompts, Baidu-first search, weather summaries, and optional Feishu, WeChat, DingTalk, AMap, and Alipay integrations for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to localize OpenClaw workflows for Chinese users, including Chinese UI strings, Baidu-oriented search, weather lookups, and optional China-market workplace, messaging, maps, and payment integrations. <br>

### Deployment Geography for Use: <br>
Global, with China-focused localization and service integrations. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests credentials for workspace, messaging, maps, and payment services without enough documented scoping or data-flow boundaries. <br>
Mitigation: Configure only the integrations needed for the deployment, start with localization and search, and add Feishu, WeChat, DingTalk, AMap, or Alipay credentials only after validating permissions, data sharing, and user approval boundaries. <br>
Risk: Payment-related credentials such as Alipay private keys could expose high-impact capabilities if configured too broadly. <br>
Mitigation: Use sandbox mode and least-privilege credentials first, keep private keys in managed environment secrets, and require a separate review before enabling payment flows. <br>
Risk: Search and weather behavior may return mock or derived results rather than authoritative live service data in some code paths. <br>
Mitigation: Verify external service wiring and result provenance before using outputs for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/china-localization) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, TypeScript examples, shell commands, and structured text returned by helper methods] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are primarily Chinese-language strings, search result summaries, weather summaries, and integration setup guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
