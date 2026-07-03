## Description: <br>
Cloudbase guides agents through CloudBase application development, deployment, debugging, migration, and troubleshooting across Web, WeChat Mini Program, native/mobile, database, cloud function, CloudRun, storage, AI model, and agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route CloudBase tasks to the right reference guidance, prepare backend resources through MCP or mcporter, and produce implementation, deployment, and troubleshooting steps for CloudBase projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward high-impact CloudBase resource operations such as create, modify, renew, deploy, or public-access actions. <br>
Mitigation: Require human review of every MCP or CLI command before execution and confirm the intended CloudBase environment and operation. <br>
Risk: The security evidence flags under-scoped deployment guidance and hidden agent-directed steps that could cause unsafe automatic actions. <br>
Mitigation: Treat deployment and cleanup steps as proposals; confirm target paths, affected resources, and data-loss impact before running them. <br>
Risk: Auth, logging, geolocation, public endpoint, and third-party AI examples may not be production-ready for a specific application. <br>
Mitigation: Perform production security and privacy review before adopting those examples in deployed systems. <br>


## Reference(s): <br>
- [CloudBase main entry](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/SKILL.md) <br>
- [CloudBase MCP setup reference](references/mcp-setup.md) <br>
- [CloudBase activation map](references/activation-map.yaml) <br>
- [CloudBase Web SDK CDN](https://static.cloudbase.net/cloudbase-js-sdk/latest/cloudbase.full.js) <br>
- [CloudBase pricing](https://cloud.tencent.com/document/product/876/75213) <br>
- [CloudBase skill page](https://clawhub.ai/binggg/skills/cloudbase) <br>
- [Publisher profile](https://clawhub.ai/user/binggg) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose MCP or mcporter actions for CloudBase resource management; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.92.11 (source: server release metadata; artifact frontmatter reports 2.23.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
