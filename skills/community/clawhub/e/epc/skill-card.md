## Description: <br>
按品牌/车型/VIN 查 EPC 结构树、分解图与零件信息。当用户说：查一下这款大众的 EPC 爆炸图、这个零件在图里编号多少？或类似配件 EPC 问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and automotive parts workflows use this skill to query JisuAPI EPC data by brand, model, vehicle ID, or VIN, then retrieve vehicle details, EPC group trees, exploded-diagram groups, and part lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VINs and other vehicle identifiers are sent to the external JisuAPI EPC service. <br>
Mitigation: Use the skill only when an external EPC lookup is intended, and avoid real private or fleet VINs unless the user understands that the identifier leaves the local environment. <br>
Risk: EPC results depend on JisuAPI account access, quotas, and API availability. <br>
Mitigation: Configure a valid JISU_API_KEY and check returned API error codes before relying on results in parts workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/epc) <br>
- [Publisher profile](https://clawhub.ai/user/jisuapi) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI EPC documentation](https://www.jisuapi.com/api/epc/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [JSON API responses with Markdown and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends requested EPC lookup parameters to the JisuAPI EPC service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
