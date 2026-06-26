## Description: <br>
Run Gemini CLI as a headless worker agent for long-running or parallelizable tasks, parallel analysis, validation, deep research, code analysis, and fallback execution when Anthropic API access is overloaded or unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cl0ckt0wer](https://clawhub.ai/user/cl0ckt0wer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate self-contained file, code, review, analysis, and batch tasks to Gemini CLI in headless mode. It is best suited for parallel worker jobs, long-context analysis, CI-style runs, and fallback execution when the primary agent service is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Headless --yolo runs can auto-approve Gemini CLI tool calls that read, write, or execute shell actions. <br>
Mitigation: Run the skill in a low-privilege account or container, grant only narrow task-specific directories with --include-directories, and review generated file changes before using them. <br>
Risk: Cached Gemini OAuth credentials can be reused by unattended runs. <br>
Mitigation: Protect ~/.gemini/oauth_creds.json, avoid shared privileged accounts, and re-authenticate only in trusted environments. <br>
Risk: Untrusted prompt content or fetched pages can steer an autonomous worker during --yolo execution. <br>
Mitigation: Treat external content as data, keep prompts explicit about allowed actions, pre-fetch web content into files when needed, and avoid giving untrusted tasks broad directory access. <br>
Risk: Large or long-running tasks can hang, exceed quotas, or produce truncated stdout. <br>
Mitigation: Use timeouts, reduce parallel workers when quota errors occur, and ask Gemini to write complete results to files with only short summaries on stdout. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cl0ckt0wer/gemini-worker) <br>
- [ACP vs Headless Reference](references/acp-vs-headless.md) <br>
- [Prompt Patterns Reference](references/prompt-patterns.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>
- [Gemini Run Wrapper Script](scripts/gemini-run.sh) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Agent Communication Protocol](https://agentcommunicationprotocol.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional generated files from Gemini CLI runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be printed to stdout or written to task-specific files; the wrapper can capture output and apply a timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and CHANGELOG, released 2026-03-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
