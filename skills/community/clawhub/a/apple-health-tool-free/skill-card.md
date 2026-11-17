## Description: <br>
Helps personal users query and discuss Apple Health-derived workout, heart-rate, activity-ring, and performance data through natural-language prompts backed by the Transition API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External personal users and agent developers use this skill to configure an agent for Apple Health-related queries, workout lookups, activity-ring checks, heart-rate trend review, and training suggestions through Transition API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Apple Health-derived questions and results may be sent to Transition's API. <br>
Mitigation: Use the skill only for explicit Apple Health tasks and avoid routing unrelated data-analysis requests through it. <br>
Risk: The skill requires a Transition API key and includes examples that configure it in shell environments. <br>
Mitigation: Store the API key in a secret manager or locked-down environment variable and do not commit it to repositories or shared configuration files. <br>
Risk: Artifact examples suggest local caching of health results, which can expose personal health data if the cache file is not protected. <br>
Mitigation: Avoid local caching unless the storage path, access controls, retention period, and deletion process are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/apple-health-tool-free) <br>
- [Transition API base URL](https://api.transition.fun) <br>
- [Transition coach chat endpoint](https://api.transition.fun/api/v1/coach/chat) <br>
- [Transition workout-of-the-day endpoint](https://api.transition.fun/api/v1/wod?sport=run&duration=45) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, YAML, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured JSON-style health query results, execution logs, configuration snippets, and curl commands that call Transition API endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
