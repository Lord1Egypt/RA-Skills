## Description: <br>
Manage Codeline through CLI commands for tools, products, orders, users, and coupons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to manage Codeline account resources through the Codeline CLI, including products, orders, users, tools, and coupon creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through authenticated Codeline operations involving business data and account actions. <br>
Mitigation: Use a least-privileged token, confirm the target account and command before execution, and avoid exposing production tokens in shared terminals or logs. <br>
Risk: Setup guidance includes installing or bundling CLI tooling from remote sources. <br>
Mitigation: Prefer a pinned or verified installation path and review the source before running remote installer commands. <br>


## Reference(s): <br>
- [Codeline Cli on ClawHub](https://clawhub.ai/Melvynx/codeline-cli) <br>
- [Bun installer](https://bun.sh/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use --json for programmatic execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
