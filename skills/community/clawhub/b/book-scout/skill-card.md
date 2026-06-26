## Description: <br>
Expert book recommendation engine via web search. Finds high-quality books (Douban ≥7.5 or Goodreads ≥3.8) based on topic, with deduplication and comprehensive scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kedoupi](https://clawhub.ai/user/kedoupi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find a high-quality book for a topic, avoid previously used titles, and rank candidates by ratings, review volume, and recency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Book topics and per-book lookup queries are sent through web search and public book-page fetches. <br>
Mitigation: Avoid sensitive or confidential topics, and review network-use policy before running the skill in restricted environments. <br>
Risk: The skill reads a narrow reading-history file if present to deduplicate prior recommendations. <br>
Mitigation: Keep sensitive reading history out of memory/reading-history.json or review that file before use. <br>
Risk: The packaged scoring helper executes local Python code. <br>
Mitigation: Review or avoid the helper script if packaged local code execution is unacceptable in the target environment. <br>
Risk: Fallback behavior may use conservative estimated ratings when exact public rating data is unavailable. <br>
Mitigation: Check outputs for estimated-rating notes and verify important recommendations against source pages before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kedoupi/book-scout) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Shell commands] <br>
**Output Format:** [Structured JSON recommendation or JSON error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the highest-scoring book; estimated ratings are marked in the output when used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
