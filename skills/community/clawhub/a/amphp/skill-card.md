## Description: <br>
This skill helps agents write non-blocking async PHP code using AMPHP v3, the Revolt event loop, amphp/amp, and the broader AMPHP ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rekryt](https://clawhub.ai/user/rekryt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to generate, review, and migrate PHP code that relies on AMPHP v3 for asynchronous I/O, HTTP servers and clients, WebSockets, databases, file operations, pipelines, workers, and event-loop behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated server examples may expose listeners or services more broadly than intended. <br>
Mitigation: Bind demo servers to localhost by default and require an explicit deployment decision before exposing public interfaces. <br>
Risk: Database, Redis, and credential examples may be copied into production with placeholder or unsafe settings. <br>
Mitigation: Treat credentials as placeholders, use local or disposable services for examples, and review connection strings before deployment. <br>
Risk: Upload-handling examples can be unsafe if filenames and paths are used directly. <br>
Mitigation: Sanitize upload filenames, constrain destination paths, and review generated file handling before running it against real user input. <br>
Risk: Async PHP guidance can still produce operational issues if blocking calls remain inside the event loop. <br>
Mitigation: Review generated code for blocking PHP APIs and replace them with the AMPHP async equivalents documented by the skill. <br>


## Reference(s): <br>
- [ClawHub amphp release page](https://clawhub.ai/rekryt/amphp) <br>
- [AMPHP v3 package reference](artifact/docs/packages.md) <br>
- [AMPHP v3 common mistakes and gotchas](artifact/docs/common-mistakes.md) <br>
- [AMPHP v2 to v3 migration guide](artifact/docs/v2-v3.md) <br>
- [Blocking PHP vs AMPHP async equivalents](artifact/resources/blocking-vs-async.md) <br>
- [AMPHP advanced patterns and gotchas](artifact/references/advanced-patterns.md) <br>
- [AMPHP class examples](artifact/references/class-examples.md) <br>
- [Full HTTP server workflow](artifact/workflows/http-server-full.md) <br>
- [Parallel fan-out workflow](artifact/workflows/parallel-fan-out.md) <br>
- [TCP server workflow](artifact/workflows/tcp-server.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline PHP, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PHP files, Composer dependency commands, test commands, and review guidance for AMPHP v3 projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
