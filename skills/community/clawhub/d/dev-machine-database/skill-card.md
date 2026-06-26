## Description: <br>
Queries the dw MySQL database on the datax development machine over SSH and formats read-only database results for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect tables, schemas, row counts, and limited result sets in a development MySQL data warehouse through natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a development MySQL database over SSH using broad credentials. <br>
Mitigation: Install only where the datax host and dw database are intended to be accessible, and replace root access with a least-privileged read-only account. <br>
Risk: Hard-coded database credentials may expose or preserve unsafe access. <br>
Mitigation: Rotate or remove the hard-coded root password and provide credentials through a secure runtime secret mechanism. <br>
Risk: The claimed read-only posture depends on weak query safeguards. <br>
Mitigation: Enforce SELECT, SHOW, and DESC-only execution with strict table and field allowlists before running generated SQL. <br>
Risk: Database query results may be sent to Feishu. <br>
Mitigation: Require explicit confirmation before posting any database result outside the query session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexmayanjun-collab/dev-machine-database) <br>
- [Publisher profile](https://clawhub.ai/user/alexmayanjun-collab) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown tables and concise text, with SSH/MySQL shell commands or Python helper behavior when execution is required.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query examples and helper behavior default SELECT results to a 50-row limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
