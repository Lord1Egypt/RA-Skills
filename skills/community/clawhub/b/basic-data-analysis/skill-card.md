## Description: <br>
保险Excel自动数据分析工具 analyzes insurance-oriented CSV, Excel, and JSON datasets, generates exploratory statistics and charts, supports Kimi or DeepSeek insight generation, and exports a Word analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbwin](https://clawhub.ai/user/wwbwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance analysts, operations teams, and agents use this skill to turn insurance datasets into EDA summaries, cleaned data notes, charts, AI-generated business insights, and Word reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dataset-derived summaries can be sent to third-party AI services during the insight generation step. <br>
Mitigation: Use the AI insight step only when organizational policy permits sending the derived summaries to Kimi or DeepSeek; otherwise run the local analysis and reporting steps with local or redacted insight text. <br>
Risk: The skill is designed for insurance data that may include customer, policy, claims, underwriting, financial, or other regulated information. <br>
Mitigation: Review and redact sensitive fields before use with real data, and validate the generated report before sharing it externally. <br>
Risk: API keys are required for external insight generation. <br>
Mitigation: Keep API keys scoped and avoid persistent shell-profile storage on shared machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwbwin/basic-data-analysis) <br>
- [Workflow guide](references/workflow.md) <br>
- [Insight generation guide](references/insight_generation.md) <br>
- [Kimi chat completions endpoint](https://api.moonshot.cn/v1/chat/completions) <br>
- [DeepSeek chat completions endpoint](https://api.deepseek.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated JSON summaries, PNG charts, and Word report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied datasets and may require KIMI_API_KEY or DEEPSEEK_API_KEY for AI insight generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: skill metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
