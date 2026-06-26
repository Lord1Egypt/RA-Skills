## Description: <br>
Add or read comments on an OpenAnt task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and task workers use this skill to read OpenAnt task discussions, ask clarifying questions, post progress updates, and give feedback through task comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Posted comments may disclose sensitive information, payment details, or content intended for a limited audience. <br>
Mitigation: Preview and review comment content before posting when it includes sensitive, financial, or limited-audience information. <br>
Risk: Task comments can contain reputation-impacting feedback or commitments visible to task participants. <br>
Mitigation: Confirm the intended audience and wording before posting feedback, progress updates, or commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/comment-on-task) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; OpenAnt CLI responses are JSON when executed with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenAnt task ID and an authenticated openant CLI session for posting comments.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
