## Description: <br>
Find and retrieve available skills using keyword search, semantic search, or LLM-powered task matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[at6132](https://clawhub.ai/user/at6132) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover installed OpenClaw skills before loading a task-specific skill into context. It supports keyword search, semantic matching, hybrid scoring, and recommendation-style results for natural language task descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results and confidence labels may be treated as authoritative even when they are only discovery hints. <br>
Mitigation: Inspect the matched skill before using it, as recommended by the server-resolved security guidance. <br>
Risk: The skill reads installed OpenClaw skill folders and maintains a local search index. <br>
Mitigation: Install it only in environments where local skill metadata may be indexed, and review the generated index if the skill set includes sensitive metadata. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Plain text search results or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include relevance scores, confidence labels, triggers, locations, and matched skill metadata.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
