## Description: <br>
Converts natural-language questions into SQL queries, executes them through a local AI chat orchestrator, and returns SQL, tabular results, concise summaries, and processing-region traces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LoveNerverMore](https://clawhub.ai/user/LoveNerverMore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business analysts use this skill to ask business-data questions in natural language and receive generated SQL, executed results, and a short answer summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates execution to an unbundled local Winner-Ai project, so behavior depends on code and configuration outside the artifact. <br>
Mitigation: Inspect and trust the local Winner-Ai project before installation or deployment. <br>
Risk: Generated SQL may access or alter sensitive data if connected with broad database privileges. <br>
Mitigation: Use a read-only, least-privilege database account and require review of generated SQL before execution. <br>
Risk: Business data may be exposed through prompts, outputs, logs, or retained raw messages. <br>
Mitigation: Avoid sensitive data unless data retention, logging, and output handling are approved for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LoveNerverMore/chat-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [JSON containing status, SQL, result rows, summary, regions, and raw messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns an error object with the exception class name when execution fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
