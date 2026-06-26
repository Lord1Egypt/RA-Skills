## Description: <br>
Queries and searches medical records from the CareMax Health API using structured filters and AI-powered semantic search with RAG answers and citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kittenyang](https://clawhub.ai/user/kittenyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to retrieve, search, and ask questions about CareMax medical records, including check-up history, hospital visits, lab results, imaging, pathology, and genetic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive health records and medical questions through AI and vector-search backends. <br>
Mitigation: Use only with trusted CareMax services and explicit user consent before authentication, record retrieval, semantic search, or chat requests. <br>
Risk: Medical chat history is saved automatically and may retain sensitive excerpts or citations. <br>
Mitigation: Tell users when chat history is being used and delete saved chat history when it is no longer needed. <br>
Risk: The skill depends on a separate caremax-auth helper for credentialed API calls. <br>
Mitigation: Install and review the companion authentication helper before use, and confirm authentication actions with the user. <br>


## Reference(s): <br>
- [CareMax Records on ClawHub](https://clawhub.ai/kittenyang/caremax-records) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include natural-language answers with citations, matched record data, semantic search hits, and chat history operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
