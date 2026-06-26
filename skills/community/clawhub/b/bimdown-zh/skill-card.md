## Description: <br>
AI与建筑信息的桥梁。像写代码一样读写BIM数据！让智能体自动完成建筑建模、按图建模、工程量统计或模型审查，甚至只是为你建一栋专属的数据化房屋！ <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novashang](https://clawhub.ai/user/novashang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Architects, BIM modelers, developers, and external agents use this skill to create, modify, validate, render, review, and optionally publish BimDown building information models from design briefs, drawings, or structured building data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the required bimdown-cli package globally through npm can execute package scripts and modify the global npm environment. <br>
Mitigation: Review the npm package before installation and obtain explicit user permission before running npm install -g bimdown-cli. <br>
Risk: Publishing uploads the project directory, including CSV, SVG, GLB assets, file names, geometry, room names, materials, and notes, and the returned share link allows access during its lifetime. <br>
Mitigation: Explain what will be uploaded, ask for explicit authorization before the first publish for each project, avoid publishing confidential projects, or use a trusted self-hosted BIMCLAW_API endpoint. <br>
Risk: Generated or modified BIM data can contain geometric, schema, or connectivity errors that affect downstream interpretation. <br>
Mitigation: Run bimdown build and bimdown render after changes, visually inspect rendered floors, and resolve reported validation issues before delivery. <br>


## Reference(s): <br>
- [BimDown 中文 on ClawHub](https://clawhub.ai/novashang/bimdown-zh) <br>
- [BIM Modeling SOP](references/bim-modeling.md) <br>
- [Building Design SOP](references/building-design.md) <br>
- [BimClaw publish endpoint](https://bim-claw.com/api/shares/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CSV, SVG, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify BimDown project files and may return a public BimClaw sharing URL only after user authorization.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
