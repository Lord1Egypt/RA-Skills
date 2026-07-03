## Description: <br>
基于明日DMP开放平台API，提供人群洞察分析功能，支持明略洞察（人口属性/兴趣爱好/媒体分析）和合作伙伴洞察（基础标签/地域分布/兴趣偏好/应用偏好/手机偏好/场景偏好/品类偏好），帮助深度理解目标人群特征，优化营销策略。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingri26](https://clawhub.ai/user/mingri26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers and operators use this skill to create, query, and retrieve Mingri DMP audience-insight tasks for authorized audience IDs. It helps compare demographic, interest, media, regional, app, mobile, scene, and category dimensions before marketing analysis or campaign planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Mingri DMP API credentials. <br>
Mitigation: Use narrowly scoped credentials, avoid sharing secrets in untrusted contexts, and rotate credentials if they are pasted into chat or exposed. <br>
Risk: The skill dynamically finds and runs a companion local authentication skill. <br>
Mitigation: Install companion skills only from trusted publisher sources and review the resolved auth helper before running API operations. <br>
Risk: The skill can persist business task history and result files locally. <br>
Mitigation: Check output and history file locations, restrict workspace access, and remove or protect generated files that contain audience insight data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mingri26/dmp-insight) <br>
- [Mingri DMP auth companion skill](https://clawhub.ai/mingri26/mingdata-dmp-auth) <br>
- [DMP task logger companion skill](https://clawhub.ai/mingri26/dmp-skill-logger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, and generated JSON/XLSX result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result retrieval can write raw JSON and Excel files for an insight task in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
