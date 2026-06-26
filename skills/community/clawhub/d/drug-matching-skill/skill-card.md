## Description: <br>
药撮合品种综合查询技能可根据剂型、产品名称、适应症、治疗领域和医保属性等需求筛选药品转让品种，并查询医保、基药、产量、一致性评价、医院用药排名、国际认证和药品说明书信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maa018809-eng](https://clawhub.ai/user/maa018809-eng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and drug-industry users use this skill to match drug approval-transfer opportunities and look up structured Chinese drug-market reference data. It is also used to route medication-label questions to a configured MCP service instead of answering from model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes MCP queries and advertised package downloads through an unencrypted raw-IP HTTP endpoint. <br>
Mitigation: Use only after trusting the server operator; prefer the listed Gitee repository or an HTTPS, version-pinned distribution path when available. <br>
Risk: Drug and medication-label queries can include confidential business, patient, or medication details. <br>
Mitigation: Avoid entering sensitive details unless the user accepts sending them to the listed HTTP MCP service. <br>
Risk: Medication-label and safety answers could be harmful if generated without source data. <br>
Mitigation: Follow the artifact guidance to call the MCP instructions query and refuse to invent dosage, adverse-reaction, contraindication, or interaction details when the service is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/maa018809-eng/drug-matching-skill) <br>
- [Gitee repository listed by artifact](https://gitee.com/drug-matching/tool-library-for-drug-matching) <br>
- [Embedded drug instructions reference](references/sino-drug-instructions-search/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown-style agent responses with MCP query results and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MCP query posture is declared in artifact tool annotations; transfer-query output is capped by the skill guidance to avoid overloading users.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
