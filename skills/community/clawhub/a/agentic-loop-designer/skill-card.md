## Description: <br>
Designs autonomous agent loops for repeatable tasks using triggers, agent actions, approval gates, output routing, memory, and ready-to-use loop templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flynndavid](https://clawhub.ai/user/flynndavid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Founders, developers, and operations teams use this skill to convert repeated manual workflows into agent loops with clear triggers, approval models, destinations, and memory rules. It is suited for planning automations such as standup digests, lead qualification, pull request reminders, revenue snapshots, and content queue capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loops may send external messages, write records, or make irreversible changes without sufficient review. <br>
Mitigation: Require human approval for external messages, confidential data, account or business-record changes, and irreversible actions. <br>
Risk: Loop designs may route sensitive data to Slack, Notion, email, webhooks, or other destinations. <br>
Mitigation: Review each loop's data sensitivity, write access, and output destination before installation or deployment. <br>
Risk: Silent discard rules can hide submissions that contributors expect to be reviewed. <br>
Mitigation: Replace silent discard behavior with a visible review queue or audit trail when submitters expect consideration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flynndavid/agentic-loop-designer) <br>
- [Publisher profile](https://clawhub.ai/user/flynndavid) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with configuration blocks, decision trees, scoring matrices, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces loop designs and deployment guidance; it does not execute automations directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
