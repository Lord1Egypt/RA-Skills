## Description: <br>
Run Claude Code tasks in headless mode with `claude -p` through the local `cc-task-runner.sh` wrapper, including model switching, JSON output capture, structured schema checks, multi-file artifact validation, and glob matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zwd0313](https://clawhub.ai/user/zwd0313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run non-interactive Claude Code jobs for coding, review, analysis, report generation, and file-producing tasks with structured output and artifact validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes unattended Claude Code automation with permission bypasses and depends on an unbundled local runner script. <br>
Mitigation: Install only when that automation is intended, review or trust the local runner script, use a temporary dedicated work directory, avoid bypassPermissions for untrusted prompts or repositories, keep secrets out of prompts, inspect generated artifacts, and clean stored task state after sensitive runs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zwd0313/claude-task-runner) <br>
- [Runner Usage Reference](references/runner-usage.md) <br>
- [Task Schema Example](references/task-schema-example.json) <br>
- [BigModel Anthropic-compatible API](https://open.bigmodel.cn/api/anthropic) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Markdown, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or validate files through the external local runner when the invoking agent follows the skill instructions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
