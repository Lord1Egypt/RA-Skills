## Description:

Dolphindb Skills helps an agent work with DolphinDB databases, including environment setup, Docker deployment, database CRUD operations, quantitative finance workflows, streaming computation, and Python SDK usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and quantitative engineering teams use this skill to prepare a DolphinDB Python environment, connect to DolphinDB, create and manage databases and tables, deploy local Docker instances, and draft DolphinDB/Python examples for finance and streaming workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can automatically install packages and make persistent environment changes.

Mitigation: Review setup scripts before installation, use a dedicated virtual environment, disable or avoid automatic installation, and pin the dolphindb package and Docker image.

Risk: Wrapper scripts evaluate generated shell export output, which creates command-execution risk if the generated output is unsafe.

Mitigation: Avoid sourcing wrappers that eval generated output until reviewed or fixed, and inspect generated export statements before applying them.

Risk: Examples use default DolphinDB credentials and include database delete/drop operations.

Mitigation: Replace admin/123456 with least-privileged credentials and require explicit confirmation before delete/drop operations, Docker deployment, or package installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/dolphindb-skills)
- [DolphinDB website](https://www.dolphindb.cn/)
- [DolphinDB documentation center](https://docs.dolphindb.cn/zh/)
- [DolphinDB Docker deployment documentation](https://docs.dolphindb.cn/zh/deploy/docker/docker_deployment.html)
- [DolphinDB database and table creation documentation](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/create_db_tb.html)
- [DolphinDB query documentation](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/queries.html)
- [DolphinDB quantitative finance examples](https://docs.dolphindb.cn/zh/tutorials/quant_finance_examples.html)
- [DolphinDB streaming tutorial](https://docs.dolphindb.cn/zh/stream/str_intro.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python, DolphinDB, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment setup steps, wrapper commands, database scripts, Docker commands, and operational cautions.]

## Skill Version(s):

1.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
