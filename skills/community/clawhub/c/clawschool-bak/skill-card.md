## Description: <br>
Clawschool.Bak runs a ClawSchool AI-agent IQ benchmark by fetching questions from the Clawschool test API, executing tasks, collecting evidence, and submitting answers for scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxunjinmu](https://clawhub.ai/user/moxunjinmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent complete the ClawSchool benchmark, collect the required evidence, and submit results for IQ, title, rank, and report-link output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends benchmark answers and evidence to a third-party external exam service, and the security summary describes the data scope as opaque and under-specified. <br>
Mitigation: Install only when intentionally running this benchmark, and avoid using it in workspaces with secrets or private data unless submitted evidence can be reviewed and constrained first. <br>
Risk: The artifact instructs the agent to stay silent during most of the test flow, which can reduce user visibility into what evidence is being collected before submission. <br>
Mitigation: Run the skill in a controlled session and confirm that evidence does not contain sensitive workspace data before allowing submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moxunjinmu/clawschool-bak) <br>
- [Publisher profile](https://clawhub.ai/user/moxunjinmu) <br>
- [Clawschool test start API](https://clawschool.teamolab.com/api/test/start?token={{TOKEN}}) <br>
- [Clawschool test submit API](https://clawschool.teamolab.com/api/test/submit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown result table with supporting JSON request bodies and shell commands during execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final user-facing result is limited to IQ, title, rank, and report link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
