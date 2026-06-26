## Description: <br>
Cue is an AI-powered research assistant for financial, business, and industry analysis with multi-agent research, task tracking, and monitoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huhoo](https://clawhub.ai/user/huhoo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and finance, business, or industry research users use Cue to launch deep research jobs, review task status, and receive monitoring notifications. It is intended for agent-assisted research workflows that send research topics to external services and keep local task, monitor, and log state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports a suspicious combination of background monitoring, API-key handling, and unsafe shell command construction. <br>
Mitigation: Review the code or wait for a patched version before installing, and verify notification handling before enabling monitoring features. <br>
Risk: Research topics and optional search queries may be sent to external services. <br>
Mitigation: Avoid submitting sensitive research topics and use dedicated, low-privilege API keys. <br>
Risk: The skill can create persistent local state and run monitoring behavior. <br>
Mitigation: Install on a non-shared machine, inspect ~/.cuecue data, and disable or avoid monitoring unless it is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huhoo/cue) <br>
- [CueCue Service](https://cuecue.cn) <br>
- [Security & Privacy Guide](SECURITY.md) <br>
- [Skill Description](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-oriented agent responses with task IDs, progress links, summaries, notifications, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local state under ~/.cuecue, call external research/search APIs, and run monitoring checks when enabled] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, artifact manifest.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
