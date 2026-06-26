## Description: <br>
Kayak for agents - search across ClawHub, SkillsMP, LobeHub, and more to find the right skill for your task, compare results across registries, get recommendations for your problem, and discover agents with specific capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Agentfinder to locate, compare, and recommend agent skills across supported registries from a local FastAPI search service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registry results may be stale or sample-like because the package uses bundled registry data. <br>
Mitigation: Verify any recommended skill on its actual registry page before installing or relying on it. <br>
Risk: Search and recommendation prompts could contain sensitive task details. <br>
Mitigation: Do not include secrets, private data, or confidential project context in prompts sent to the local API. <br>


## Reference(s): <br>
- [Agentfinder on ClawHub](https://clawhub.ai/mirni/gh-agentfinder) <br>
- [Publisher profile](https://clawhub.ai/user/mirni) <br>
- [ClawHub registry](https://clawhub.ai) <br>
- [SkillsMP registry](https://skillsmp.com) <br>
- [LobeHub skills](https://lobehub.com/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search, comparison, recommendation, and registry-listing responses are produced by local REST endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
