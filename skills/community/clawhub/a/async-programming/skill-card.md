## Description: <br>
Handles programming requests asynchronously by delegating coding work to background sub-agents, confirming receipt immediately, and reporting progress or completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[broommonk](https://clawhub.ai/user/broommonk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding assistants use this skill to keep a conversation responsive while programming tasks are delegated to background sub-agents. It is intended for coding, bug fixing, refactoring, scripting, project configuration, dependency installation, progress tracking, and completion reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad programming requests may start background coding agents without a clear per-task opt-in. <br>
Mitigation: Confirm scope and user intent before spawning sub-agents, and require review before applying or accepting generated code changes. <br>
Risk: Concurrent background agents may modify files or repositories beyond the user's intended scope. <br>
Mitigation: Constrain sub-agent filesystem and repository access, cap concurrency, monitor running tasks, and stop jobs that exceed the approved scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/broommonk/async-programming) <br>
- [Artifact repository reference](https://git.kingcms.cn/OpenClaw/Skills-Collection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with sub-agent invocation examples, task confirmation templates, progress summaries, and completion reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate up to 8 concurrent background coding sub-agents according to the artifact configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
