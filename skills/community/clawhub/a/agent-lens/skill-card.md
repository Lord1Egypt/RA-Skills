## Description: <br>
Track AI agent API calls, analyze token usage, and optimize costs for OpenAI, Anthropic, Google, DeepSeek, and similar LLM APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Agent Lens to monitor LLM API spending, inspect token usage, review latency and error patterns, and generate cost reports for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records local LLM API telemetry that may include sensitive prompts or usage metadata. <br>
Mitigation: Review what the integration records before use and avoid storing sensitive data unless the local environment and retention policy are appropriate. <br>
Risk: Local SQLite history can accumulate long-term API usage records. <br>
Mitigation: Use the documented cleanup workflow periodically when long-term history retention is not desired. <br>


## Reference(s): <br>
- [Agent Lens ClawHub listing](https://clawhub.ai/lrg913427-dot/agent-lens) <br>
- [lrg913427-dot ClawHub publisher profile](https://clawhub.ai/user/lrg913427-dot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance can include local CLI commands, integration snippets, cost-analysis steps, and data-retention advice.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
