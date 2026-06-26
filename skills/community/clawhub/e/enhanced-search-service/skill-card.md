## Description: <br>
Enhances memory search by combining co-occurrence graph analysis and semantic vector similarity for contextual relevance ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system integrators use this skill to improve memory search by re-ranking raw results and surfacing related memories with semantic and co-occurrence signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Query snippets and result relationships may be recorded by local memory infrastructure, creating privacy exposure for secrets or highly sensitive personal data. <br>
Mitigation: Avoid using the skill with secrets or highly sensitive personal data unless the deployment accepts that local recording behavior. <br>
Risk: Search quality depends on trusted co-occurrence and semantic-vector adapters. <br>
Mitigation: Install only with trusted adapters and verify dependency health before relying on ranking output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whoisme007/enhanced-search-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python API responses as dictionaries plus Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Enhanced results include base, co-occurrence, semantic, and combined relevance scores when adapters are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
