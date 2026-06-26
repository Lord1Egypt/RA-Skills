## Description: <br>
Submits Dataify Builder tasks that collect Reddit post comments from one or more Reddit URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who collect Reddit discussion data use this skill to confirm collection parameters, submit Dataify Reddit comment jobs, and receive the resulting task ID and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reddit collection tasks and parameters are sent to Dataify, and broad requests may invoke the skill implicitly. <br>
Mitigation: Use explicit prompts, review the target Reddit URL and collection parameters before submission, and install only if sending this task data to Dataify is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-reddit-comment-by-url) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown parameter tables, shell commands, and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Dataify task ID, status, submitted parameters, file name, dashboard URL, and token setup guidance when needed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
