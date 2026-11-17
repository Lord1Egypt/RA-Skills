## Description:

解析用户的自然语言临床科研问题，输出结构化研究参数（研究类型、终点、变量、推荐workflow）。当用户提出一个科研问题并需要将其转为结构化任务时触发。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[emergenceronearth](https://clawhub.ai/user/emergenceronearth)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, and agent users use this skill to turn a natural-language clinical research question into structured study parameters, a task preview, recommended workflow steps, and recommended skills. The current artifact demonstrates that workflow from fixed mock data and asks the agent to disclose demo data when the user's question does not match the mock scenario.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a real clinical research-question parser even though the security summary says it reads a fixed mock-data file rather than parsing the user's actual question.

Mitigation: Install only for the intended demo workflow, disclose mock-data behavior to users, and update the artifact to parse actual user input before relying on it for real research-question parsing.

Risk: The artifact expects `/home/ubuntu/workspace/demo/mock_data/task_create.json` and a local reporting service on port 5001, which may be absent or inappropriate in another environment.

Mitigation: Confirm the expected demo file and local reporting service exist before use, or adapt the skill to configurable paths and reporting endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergenceronearth/skills/agentic-research-question-parser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown or text with tables or sectioned lists; includes local status-reporting shell commands in the artifact instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should not expose raw JSON; the artifact reads a fixed mock-data file and reports status to a local service on port 5001.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
