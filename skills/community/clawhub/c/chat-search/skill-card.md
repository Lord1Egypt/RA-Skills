## Description: <br>
Searches Feishu and Telegram chat history with semantic matching, similarity scores, and message source labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fhqoopp](https://clawhub.ai/user/fhqoopp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to find relevant prior messages in Feishu or Telegram chat history through semantic search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may search or persist private Feishu or Telegram chat history without enough scope, permission, or cleanup guidance. <br>
Mitigation: Before use, confirm which chat data is indexed, how access is authorized, where Qdrant stores data, and how indexed records can be deleted. <br>
Risk: Vague search requests could expose broader private chat results than intended. <br>
Mitigation: Require explicit confirmation for vague searches and limit queries to the minimum necessary sources. <br>


## Reference(s): <br>
- [Chat Search on ClawHub](https://clawhub.ai/fhqoopp/chat-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with search results, similarity scores, source labels, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include private chat content from Feishu or Telegram indexes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
