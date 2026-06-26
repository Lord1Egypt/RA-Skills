## Description: <br>
素材库管理技能 - 提供素材的存储、检索、版本管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JEyeshield](https://clawhub.ai/user/JEyeshield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ad production teams use this skill to store, retrieve, tag, search, version, and archive generated advertising materials and their metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage ad material prompts, metadata, and archive or version actions in its library context. <br>
Mitigation: Use it only with campaign material that is intended to be stored in the agent context, and review archive or version actions before treating them as final. <br>
Risk: Confidential campaign details may be included in prompts or metadata if supplied by the user. <br>
Mitigation: Avoid storing confidential campaign details unless that retention is intentional and permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JEyeshield/ad-production-material-library) <br>
- [Publisher profile](https://clawhub.ai/user/JEyeshield) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Text] <br>
**Output Format:** [JSON command responses with material records, status messages, and file tokens] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores material metadata in the skill library context and returns IDs, search results, statistics, version IDs, or archive confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
