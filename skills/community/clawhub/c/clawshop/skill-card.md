## Description: <br>
Operate the ClawShop Web API for Taobao/Goofish product posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qsgy](https://clawhub.ai/user/qsgy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to manage their own ClawShop product posts, including token registration or rotation, create, update, delete, filtered search, and API metadata discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The saved ./.clawshop_token can authorize write access if it is exposed. <br>
Mitigation: Store the token like a password, keep file permissions strict, do not commit or share it, and rotate it if exposed. <br>
Risk: Create, update, delete, and token-rotation requests can modify product posts or access state. <br>
Mitigation: Review and approve write, delete, and token-rotation actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qsgy/clawshop) <br>
- [ClawShop OpenAPI specification](https://82.156.31.238:19133/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save and reuse a local ./.clawshop_token bearer token for write endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
