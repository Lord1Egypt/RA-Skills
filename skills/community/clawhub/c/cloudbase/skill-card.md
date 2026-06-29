## Description: <br>
Use this skill when developing, designing, building, deploying, debugging, migrating, or troubleshooting CloudBase projects across web apps, WeChat mini programs, native/mobile HTTP API integrations, authentication, databases, serverless functions, CloudRun, cloud storage, AI model use, operations, and specification workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route CloudBase tasks to the appropriate guidance for app development, authentication, data access, deployment, AI features, troubleshooting, and code review. It is intended for agents assisting with CloudBase project implementation and operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward high-impact CloudBase changes such as MCP or CLI operations, deployments, permission changes, billing changes, and public-access changes. <br>
Mitigation: Require explicit user confirmation before those actions and review proposed changes before execution. <br>
Risk: Some examples may use public access patterns or wildcard CORS that are too broad for production use. <br>
Mitigation: Harden generated configurations with authenticated endpoints, specific allowed origins, and least-privilege data sharing. <br>
Risk: Deletion commands and identity or JWT logging examples can cause data loss or expose sensitive identifiers if copied directly. <br>
Mitigation: Avoid destructive commands without confirmation and backups, and redact sensitive identifiers from logs and examples. <br>
Risk: The skill distinguishes CloudBase PostgreSQL paths from legacy API paths, and using the wrong path can create incorrect or unsafe implementations. <br>
Mitigation: Confirm the target data platform before implementation and use the CloudBase PG guidance for PostgreSQL workflows. <br>


## Reference(s): <br>
- [Cloudbase skill page](https://clawhub.ai/binggg/skills/cloudbase) <br>
- [CloudBase MCP setup reference](artifact/references/mcp-setup.md) <br>
- [CloudBase activation map](artifact/references/activation-map.yaml) <br>
- [CloudBase main entry](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/SKILL.md) <br>
- [CloudBase pricing](https://cloud.tencent.com/document/product/876/75213) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and implementation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to inspect referenced skill files and CloudBase MCP schemas before acting.] <br>

## Skill Version(s): <br>
1.92.9 (source: server release metadata; artifact frontmatter reports 2.23.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
