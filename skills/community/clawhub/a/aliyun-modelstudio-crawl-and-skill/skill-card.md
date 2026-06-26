## Description: <br>
Refreshes the Alibaba Cloud Model Studio model crawl and regenerates derived summaries, coverage reports, and related `skills/ai/**` skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to refresh Alibaba Cloud Model Studio model data, rebuild local model summaries, and check skill coverage before updating generated AI skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow executes a public webpage crawl through the `@just-every/crawl` npm package. <br>
Mitigation: Run it only when refreshing Alibaba Cloud Model Studio model data, and review or pin the npm package before execution. <br>
Risk: The scripts can create or update generated summaries, coverage reports, and `skills/ai/**` files. <br>
Mitigation: Run from a clean, version-controlled worktree and review all generated changes before keeping or committing them. <br>
Risk: Generated model identifiers or links could become stale if the source documentation changes. <br>
Mitigation: Use only links found in the crawled Model Studio page and validate generated outputs before publishing downstream skills. <br>


## Reference(s): <br>
- [Alibaba Cloud Model Studio models documentation](https://help.aliyun.com/zh/model-studio/models) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-modelstudio-crawl-and-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands plus generated Markdown, JSON, and skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces crawl output, cleaned summaries, structured model lists, coverage reports, and updates under `skills/ai/**`.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
