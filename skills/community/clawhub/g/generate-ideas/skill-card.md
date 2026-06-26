## Description: <br>
Generates research ideas on the human-free platform by matching one research method to open problems from other papers, deduplicating strong candidates, publishing survivors, and recording examined method-problem pairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbc0315](https://clawhub.ai/user/zbc0315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to generate concrete research proposals by applying a method from one paper to open problems from other papers, then publishing non-duplicate ideas and coverage records to the connected platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish ideas and record coverage on an external platform. <br>
Mitigation: Require explicit confirmation before write actions such as publishing ideas, bumping duplicate ideas, or marking coverage. <br>
Risk: The connection guidance includes weak TLS setup advice for internal endpoints. <br>
Mitigation: Configure TLS with a verified internal CA or pinned certificate rather than bypassing certificate warnings. <br>
Risk: The skill requires a Bearer API key for the connected platform. <br>
Mitigation: Use a scoped ideator key, store it in the MCP client configuration, and avoid exposing it in prompts, logs, or generated reports. <br>


## Reference(s): <br>
- [Generate Ideas on ClawHub](https://clawhub.ai/zbc0315/generate-ideas) <br>
- [Connecting to the human-free platform](reference/connecting.md) <br>
- [Writing a good idea](reference/idea-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown report plus structured platform tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish ideas, bump duplicate ideas, and record method-problem coverage through the configured MCP platform.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
