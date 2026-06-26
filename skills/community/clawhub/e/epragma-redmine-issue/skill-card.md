## Description: <br>
Read Redmine issues from any Redmine server via REST API with configurable URL and credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agelospanagiotakis](https://clawhub.ai/user/agelospanagiotakis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect, filter, create, update, and comment on Redmine issues and time entries through a configured Redmine REST API connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Redmine changes even though it is described mainly as a reader. <br>
Mitigation: Grant only a least-privilege Redmine API key and require confirmation before create, update, comment, or time-entry commands. <br>
Risk: Misconfigured REDMINE_URL or REDMINE_API_KEY can send requests to the wrong Redmine server or with the wrong credential. <br>
Mitigation: Verify REDMINE_URL and REDMINE_API_KEY before use and store credentials through the skill configuration mechanism rather than in prompts or shared logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agelospanagiotakis/epragma-redmine-issue) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/agelospanagiotakis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or JSON returned from Redmine command-line API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDMINE_URL and REDMINE_API_KEY to access the target Redmine server.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
