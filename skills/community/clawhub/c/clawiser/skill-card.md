## Description: <br>
ClaWiser is an agent memory and workflow enhancement suite with modules for memory setup, retrieval improvement, conversation noise reduction, hypothesis-driven debugging, scenario-driven planning, save/load handoffs, and project-skill pairing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MattWenJun](https://clawhub.ai/user/MattWenJun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ClaWiser to install and route a suite of OpenClaw and Claude Code skills that improve agent memory, retrieval, planning, debugging, and cross-session continuity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClaWiser can create persistent local memory that retains conversation history and personal context. <br>
Mitigation: Install only when persistent memory is intended; review indexed paths, memory rules, and whether real names or sensitive details should be written to memory. <br>
Risk: ClaWiser can alter future agent behavior by editing AGENTS.md, SOUL.md, HEARTBEAT.md, OpenClaw configuration, cron jobs, and scripts. <br>
Mitigation: Review and approve these edits before enabling the skill, and install only the modules needed for the target environment. <br>
Risk: The included auto-commit behavior can commit broad local file changes, including unrelated files or secrets if repository ignore rules are incomplete. <br>
Mitigation: Remove, disable, or narrow the auto-commit script; confirm .gitignore excludes secrets and review commits before sharing or pushing them. <br>
Risk: Conversation noise-reduction rules can accidentally remove useful memory content or preserve irrelevant content if patterns are poorly tuned. <br>
Mitigation: Run the provided diagnosis and validation workflow, inspect filtered and retained samples, and keep conservative rules with explicit reasons. <br>


## Reference(s): <br>
- [ClaWiser ClawHub release page](https://clawhub.ai/MattWenJun/clawiser) <br>
- [README](artifact/README.md) <br>
- [Memory rules](artifact/assets/memory-deposit/references/memory-rules.md) <br>
- [Noise categories](artifact/assets/noise-reduction/references/noise-categories.md) <br>
- [Noise reduction common failures](artifact/assets/noise-reduction/references/common-failures.md) <br>
- [Noise classifier example](artifact/assets/noise-reduction/references/example-classifier.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [DashScope compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON snippets, configuration edits, and generated or modified local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install nested skill directories, update agent routing and memory files, configure scheduled jobs, and run validation commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
