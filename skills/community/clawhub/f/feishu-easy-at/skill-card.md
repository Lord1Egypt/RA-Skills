## Description: <br>
Guides agents to create real @ mentions in Feishu by using post rich text messages with at nodes and user_id or open_id values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lens-lzy](https://clawhub.ai/user/Lens-lzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to answer Feishu mention-formatting questions, explain why plain @ text does not notify users, and provide a reusable post-message JSON pattern for correct mentions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu user_id, open_id, member lists, and mention metadata can identify workplace users. <br>
Mitigation: Treat those values as workplace identity data and avoid exposing them beyond the intended Feishu workflow. <br>
Risk: Generated mention payloads could notify the wrong person if the identifier is stale, guessed, or mapped from an ambiguous nickname. <br>
Mitigation: Confirm the user_id or open_id from reliable Feishu member data or prior message mentions before sending. <br>
Risk: A generated Feishu message may have unintended notification impact. <br>
Mitigation: Review the final message content and target identifiers before sending it. <br>


## Reference(s): <br>
- [Complete mention skill for Feishu on ClawHub](https://clawhub.ai/Lens-lzy/feishu-easy-at) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu post message content examples that require user_id or open_id values supplied by the user or workspace tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
