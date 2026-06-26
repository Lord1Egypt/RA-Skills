## Description: <br>
Guides an agent to design database structures from provided data, insert that data, and build dynamic HTML dashboards that poll a specified API every 60 seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realRoc](https://clawhub.ai/user/realRoc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to turn supplied data into database-backed HTML dashboards with chart-level API calls and periodic refresh behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to create database structures and store provided data without clear approval boundaries. <br>
Mitigation: Require explicit confirmation of the target database, collection names, schema, and write operations before execution. <br>
Risk: The skill directs recurring calls to an external API endpoint every 60 seconds. <br>
Mitigation: Verify the endpoint is trusted, avoid sensitive data unless retention and access controls are understood, and review polling frequency against operational limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realRoc/coding-2) <br>
- [Configured dashboard data API endpoint](https://teamo-dev.floatai.cn/api/engine/generalDataApi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration, Shell commands] <br>
**Output Format:** [Markdown with code, API request details, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database schema design, data insertion steps, dashboard code, and polling behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
