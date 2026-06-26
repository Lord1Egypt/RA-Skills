## Description: <br>
Agent Communicator helps agents structure inter-agent messages, handoffs, reviews, feedback, conflict resolution, and communication tracking using standardized Markdown and JSON formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create clear requests, responses, handoffs, review prompts, feedback, and status reports between specialized agents. It is best suited for coordinating multi-agent work where message structure and follow-up expectations matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated coordination messages may include private project context, credentials, customer data, or internal decisions if the user provides them. <br>
Mitigation: Review generated messages before sharing and remove sensitive information that does not need to be sent. <br>
Risk: Message templates can make incomplete or incorrect handoff details appear authoritative. <br>
Mitigation: Verify recipients, deadlines, file references, decisions, and expected responses before treating a generated message as final. <br>


## Reference(s): <br>
- [Agent Communicator examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown templates and optional structured JSON message records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution; outputs are coordination messages, templates, and review checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
