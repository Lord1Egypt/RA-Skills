## Description: <br>
面向 AI 从业者的开源项目研究技能，帮助从候选项目补齐 GitHub、模型、论文等资源并形成技术选型建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiqizhixin](https://clawhub.ai/user/jiqizhixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and product teams use this skill to discover and compare AI open-source projects, verify project resources, and turn candidate sets into actionable technical selection guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project search terms and detail requests are sent to the Jiqizhixin-backed API service. <br>
Mitigation: Use the skill only for queries acceptable under that provider's terms and avoid confidential internal project names unless disclosure is approved. <br>
Risk: The skill requires a JQZX_API_TOKEN for API-backed project search and detail lookup. <br>
Mitigation: Use a scoped, rotatable token stored in the environment, keep BASE_URL pointed at the intended service, and avoid exposing the token in logs or shared outputs. <br>
Risk: Project recommendations can be incomplete when candidate results are sparse or links remain unverified. <br>
Mitigation: Broaden keywords, paginate when needed, fetch project details before comparison, and clearly separate verified links from items that still need confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiqizhixin/ai-project-radar) <br>
- [Jiqizhixin data service](https://www.jiqizhixin.com/data-service) <br>
- [/api/v1 projects reference](references/api-v1-projects.md) <br>
- [Default API service endpoint](https://mcp.applications.jiqizhixin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with project comparison tables, resource link lists, technical fit guidance, and optional bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JQZX_API_TOKEN for API-backed project search and detail lookup.] <br>

## Skill Version(s): <br>
0.1.3 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
