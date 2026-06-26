## Description: <br>
Coordinates GEO optimization workflows by helping users configure and verify a Longxia key, view task lists, and route single rewrite requests while directing daily automation and mass-publish checks to companion skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators of the GEO optimization SaaS use this coordinator to set up local credentials, confirm access, inspect optimization tasks, and trigger a compatible one-time rewrite workflow when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a GEO API key for ai.gaobobo.cn. <br>
Mitigation: Treat the GEO key like a password, keep the local key file private, and rotate or revoke it if exposed. <br>
Risk: Users may unintentionally enable scheduled automation or publishing-related workflows through companion skills. <br>
Mitigation: Review geo-cycle-autopilot and geo-mass-publish-check before enabling scheduled automation or mass-publish checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chameleon-nexus/geo-opt-coordinator) <br>
- [Publisher profile](https://clawhub.ai/user/chameleon-nexus) <br>
- [GEO optimization service](https://ai.gaobobo.cn) <br>
- [GEO optimization task API](https://ai.gaobobo.cn/api/geo/optimization/tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and task status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or request a local GEO API key and may call the GEO optimization service when the user is configuring or viewing tasks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
