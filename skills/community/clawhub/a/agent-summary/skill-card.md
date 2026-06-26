## Description: <br>
Agent Summary monitors subagent activity and produces brief progress status summaries every 30 seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent coordinators use this skill to check active subagents, summarize recent status messages, and report concise progress updates only when work changes, completes, or fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads recent subagent messages, which may contain secrets, regulated data, or private content. <br>
Mitigation: Use it only in tasks where recent subagent conversation content may be safely summarized and surfaced in progress updates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangxiaofei860208-source/agent-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with concise status text and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are intended to be 3-5 words and emitted only on status changes, completion, or failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
