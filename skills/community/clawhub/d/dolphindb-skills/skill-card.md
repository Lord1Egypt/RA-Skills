## Description: <br>
Dolphindb Skills helps agents work with DolphinDB databases, Docker deployment, CRUD workflows, quantitative finance analysis, and streaming-computation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and quantitative-finance practitioners use this skill to prepare DolphinDB environments, generate database operation examples, and plan analytics or streaming workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup workflows can install Python packages into local environments. <br>
Mitigation: Review setup scripts first and use --no-install, a dedicated virtual environment, or a container unless package changes are explicitly approved. <br>
Risk: Shell wrappers source scripts and evaluate generated export commands. <br>
Mitigation: Use the bundled wrappers only from trusted artifact files and avoid eval/source workflows with untrusted files. <br>
Risk: Generated DolphinDB examples may include default credentials or destructive database operations. <br>
Mitigation: Replace default credentials and require explicit confirmation before DELETE, DROP, bulk write, Docker install, or subskill-update actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ugpoor/dolphindb-skills) <br>
- [USAGE_GUIDE.md](artifact/USAGE_GUIDE.md) <br>
- [MIGRATION_GUIDE.md](artifact/MIGRATION_GUIDE.md) <br>
- [DolphinDB documentation center](https://docs.dolphindb.cn/zh/) <br>
- [DolphinDB Docker deployment](https://docs.dolphindb.cn/zh/deploy/docker/docker_deployment.html) <br>
- [DolphinDB distributed database operations](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/create_db_tb.html) <br>
- [DolphinDB quantitative finance examples](https://docs.dolphindb.cn/zh/tutorials/quant_finance_examples.html) <br>
- [DolphinDB streaming data tutorial](https://docs.dolphindb.cn/zh/stream/str_intro.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, and DolphinDB code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment setup steps, database commands, Docker commands, and workflow recommendations.] <br>

## Skill Version(s): <br>
1.4.1 (source: ClawHub release evidence and target metadata; artifact documentation references v1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
