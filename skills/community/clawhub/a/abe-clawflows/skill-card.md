## Description: <br>
Search, install, and run multi-skill automations from clawflows.com. Combine multiple skills into powerful workflows with logic, conditions, and data flow between steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to discover, install, inspect, run, schedule, and publish portable multi-skill workflows that compose abstract capabilities such as database access, chart generation, email, calendar, weather, and AI services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded automations can execute workflows that use credentials, external APIs, email, calendars, databases, or scheduled runs. <br>
Mitigation: Inspect downloaded YAML, run the check command, use dry-run first, and provide only least-privilege credentials before execution. <br>
Risk: The skill depends on the third-party clawflows npm package and registry. <br>
Mitigation: Install only if the npm package and registry are trusted, and review the installed automation before enabling scheduled or state-changing behavior. <br>


## Reference(s): <br>
- [ClawFlows registry](https://clawflows.com) <br>
- [clawflows npm package](https://www.npmjs.com/package/clawflows) <br>
- [ClawFlows registry GitHub repository](https://github.com/Cluka-399/clawflows-registry) <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-clawflows) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawflows CLI and SKILLBOSS_API_KEY for automations that call SkillBoss API Hub AI services.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
