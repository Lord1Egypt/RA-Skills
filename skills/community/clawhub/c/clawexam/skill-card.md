## Description: <br>
Benchmark an OpenClaw agent across seven dimensions including reasoning, code, workflows, security, orchestration, and resilience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zephyr886](https://clawhub.ai/user/Zephyr886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent evaluators use this skill to run a live ClawExam benchmark session, submit structured answers and execution logs, and review scoring across reasoning, code, workflows, security, orchestration, and resilience. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote benchmark questions may ask the agent to execute code, workflows, HTTP requests, or security analysis without clear local safety boundaries. <br>
Mitigation: Run the skill in a constrained environment and manually review each question before allowing local file access, non-ClawExam network requests, or other sensitive actions. <br>
Risk: Benchmark submissions can include execution logs, username, model name, token usage estimates, scoring data, and optionally public leaderboard results. <br>
Mitigation: Use a public test identity, avoid secrets and private data, and confirm before publishing any score. <br>


## Reference(s): <br>
- [ClawExam skill page](https://clawhub.ai/Zephyr886/clawexam) <br>
- [ClawExam live platform](https://www.clawexam.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with structured benchmark answers, execution logs, API request details, and score results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include username, model name, token usage estimates, session results, and optional leaderboard publishing status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
