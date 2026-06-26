## Description: <br>
Runs a Feynman Technique study session for OpenAlgernon by asking the user to teach concepts back, probing gaps with Socratic questions, and revealing reference answers only after repeated attempts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AntonioVFranco](https://clawhub.ai/user/AntonioVFranco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenAlgernon users use this skill to consolidate study material by explaining selected concepts in their own words. The agent selects study cards, evaluates accuracy, depth, and transfer, asks targeted follow-up questions, and summarizes the session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local OpenAlgernon study data and persist study-session summaries. <br>
Mitigation: Use it only with study data you are comfortable exposing to the agent, and review saved summaries for sensitive content. <br>
Risk: Optional Notion integration can send session summaries to a configured Notion page. <br>
Mitigation: Enable Notion only with a trusted CLI, account, and page ID, and avoid routing sensitive study material to Notion unless that storage is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Conversational text and Markdown summaries with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read an OpenAlgernon SQLite study database and optionally append session summaries to Notion or local memory when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
