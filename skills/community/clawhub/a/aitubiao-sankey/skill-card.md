## Description: <br>
AI桑基图（流向图）生成。用户上传数据或粘贴表格，自动生成流向可视化图表，展示数据在环节间的流动关系。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitubiao](https://clawhub.ai/user/aitubiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn pasted tables or uploaded CSV, TXT, Excel-style data into Sankey diagram projects through the aitubiao API. It is intended for flow, conversion path, budget movement, and other source-to-target visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an aitubiao API key persistently and uses it to create projects through the user's account. <br>
Mitigation: Use a low-privilege or throwaway API key when available, avoid pasting keys into shared logs, and rotate the key if it is exposed. <br>
Risk: The bundled CLI exposes related project-generation commands beyond Sankey creation, including chart, PPT, 3D, and download actions. <br>
Mitigation: Review agent actions before execution and allow create or download commands only when they match the user's confirmed request. <br>
Risk: Download actions can write files to local paths selected during the workflow. <br>
Mitigation: Require a user-approved writable output folder and avoid writing exports into source directories or other sensitive locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aitubiao/aitubiao-sankey) <br>
- [Aitubiao workspace](https://app.aitubiao.com/workspace) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown responses with inline bash commands, JSON API results, project links, and optional downloaded export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an aitubiao API key; successful runs return project URLs, project IDs, optional screenshot links, quota details, and downloaded PNG, JPG, PDF, PPT, or ZIP files when requested.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
