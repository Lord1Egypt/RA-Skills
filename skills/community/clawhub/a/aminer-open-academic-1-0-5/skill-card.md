## Description: <br>
Uses AMiner Open Platform APIs to query and analyze academic data for scholars, papers, institutions, venues, patents, and academic question answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrhenghu](https://clawhub.ai/user/mrhenghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to query AMiner academic data and run workflows for scholar profiles, paper deep dives, institution analysis, journal monitoring, academic QA, and patent analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic search queries and API requests are sent to AMiner. <br>
Mitigation: Avoid sending sensitive or proprietary research queries unless the user is comfortable sharing them with AMiner. <br>
Risk: The skill uses an AMiner token that may authorize paid API calls. <br>
Mitigation: Use a revocable token, review AMiner API pricing before multi-step workflows, and avoid pasting real tokens into shared transcripts or logs. <br>


## Reference(s): <br>
- [AMiner API catalog](references/api-catalog.md) <br>
- [AMiner Open Platform documentation](https://open.aminer.cn/open/doc) <br>
- [AMiner Open Platform console](https://open.aminer.cn/open/board?tab=control) <br>
- [ClawHub skill page](https://clawhub.ai/mrhenghu/aminer-open-academic-1-0-5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AMiner API token supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
