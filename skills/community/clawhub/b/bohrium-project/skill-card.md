## Description: <br>
Manage Bohrium projects through the bohr CLI and Bohrium project APIs, including project creation, membership, roles, budgets, and deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Bohrium project administrators use this skill to list, create, rename, delete, and budget projects, and to manage project members and admin roles. It is not intended for Bohrium job submission, node management, or image management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access-key authority to make persistent project, budget, membership, and admin-role changes. <br>
Mitigation: Use the least-privileged Bohrium access key available and require explicit human confirmation before deleting projects, changing members, changing admin roles, changing budgets, recovering members, or renaming projects. <br>
Risk: The required Bohrium access key is sensitive credential material. <br>
Mitigation: Keep the key out of prompts, logs, repositories, and shared transcripts; provide it only through the intended environment variable or protected configuration. <br>
Risk: The skill documentation installs the bohr CLI by running remote shell scripts. <br>
Mitigation: Inspect or verify the remote installer before running it in any trusted environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sorrymaker0624/bohrium-project) <br>
- [Publisher profile](https://clawhub.ai/user/sorrymaker0624) <br>
- [Bohrium project OpenAPI endpoint](https://open.bohrium.com/openapi/v1/project) <br>
- [Bohrium project API endpoint used by helper script](https://openapi.dp.tech/openapi/v1/project) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with bash and Python examples, plus command-line text output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bohrium ACCESS_KEY and may call external Bohrium APIs or the bohr CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
