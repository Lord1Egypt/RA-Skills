## Description: <br>
Parses recent OpenClaw session logs for LLM API errors and returns a structured health report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toller892](https://clawhub.ai/user/toller892) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect recent OpenClaw session logs for LLM API failures, rate limits, token problems, and service-busy signals. It returns a compact health report with detected error categories and a suggested next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent OpenClaw session logs may contain private prompts, API tokens, account details, or other sensitive operational data. <br>
Mitigation: Review matched log snippets before sharing reports publicly, and install the skill only in environments where local session-log access is acceptable. <br>


## Reference(s): <br>
- [API Health Monitor on ClawHub](https://clawhub.ai/toller892/api-health-monitor) <br>
- [toller892 ClawHub publisher profile](https://clawhub.ai/user/toller892) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object with a health boolean, error summaries, and a recommendation string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw session logs from the recent lookback window; default lookback is one day.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
