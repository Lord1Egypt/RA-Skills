## Description: <br>
Helps developers select, integrate, validate, troubleshoot, and audit Tencent DataNexus data collection SDK integrations across mini-program, mini-game, mobile app, and HarmonyOS clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill to choose the correct DataNexus SDK, follow platform-specific onboarding guidance, inspect event instrumentation, run local integration checks, and troubleshoot reporting or reconciliation issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose or add tracking code during SDK integration. <br>
Mitigation: Require explicit user approval before scanning, generating plans, or applying edits; review every generated change before use. <br>
Risk: Secrets such as secret_key may appear in generated snippets, plan files, command arguments, IDE logs, or diffs. <br>
Mitigation: Avoid production secrets during setup, move secrets to environment variables or a configuration service, and inspect generated files and diffs before committing. <br>
Risk: SDK instrumentation may create privacy, consent, permission, URL handling, identifier handling, or auto-tracking issues. <br>
Mitigation: Verify consent gating, privacy disclosures, requested permissions, URL sanitization, identifier handling, and auto-tracking behavior before shipping. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/datanexus-sdk-skills) <br>
- [SDK selection decision tree](references/通用/选型/SDK选型决策树.md) <br>
- [Automation integration protocol](references/通用/自动化/能力7自动化接入协议.md) <br>
- [Integration quality checklist](references/通用/质量/接入质量检查清单.md) <br>
- [Data compliance guide](references/通用/合规/数据合规指引.md) <br>
- [Event type enumeration](references/通用/埋点/行为类型枚举表.md) <br>
- [Reporting parameter guide](references/通用/埋点/上报参数说明.md) <br>
- [Joint debugging guide](references/通用/联调/转化联调指南.md) <br>
- [Data reconciliation guide](references/通用/联调/数据对账.md) <br>
- [Error code reference](references/通用/排障/错误码速查表.md) <br>
- [Script usage guide](scripts/README.md) <br>
- [DataNexus compliance documentation](https://docs.qq.com/doc/DU29kS3Jsd05yWUxO) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration advice, and JSON or human-readable script output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some local scripts emit JSON for framework detection, integration scanning, patch planning, validation, and audit reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
