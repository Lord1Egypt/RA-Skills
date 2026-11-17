## Description:

CNB 云原生构建平台的 Git 操作技能。使用 git 和 CNB Open API 进行代码克隆、提交、推送、分支管理、Merge Request 管理、流水线触发、流水线结果读取等操作。首次使用需收集用户的 Git 用户名和邮箱信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[twksos](https://clawhub.ai/user/twksos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to operate CNB repositories with Git and CNB Open API, including cloning, committing, pushing, branch management, merge request work, and pipeline actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CNB Git and API tokens may grant write, merge, or pipeline permissions and can be exposed if embedded in clone URLs or logs.

Mitigation: Use least-privilege, expiring tokens, inject them as secrets, avoid token-bearing clone URLs when possible, inspect remotes after use, and rotate any token previously used in a URL.

Risk: The skill provides commands for merge request and pipeline actions that can change repository state.

Mitigation: Review generated commands before execution and restrict token permissions to the specific repository actions required.

## Reference(s):

- [CNB API service endpoint](https://api.cnb.cool)
- [ClawHub skill page](https://clawhub.ai/twksos/skills/cnb-cool-git)
- [Publisher profile](https://clawhub.ai/user/twksos)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference required CNB Git and API token secrets plus non-sensitive Git user environment variables.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
