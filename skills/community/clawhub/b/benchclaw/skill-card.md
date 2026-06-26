## Description: <br>
BenchClaw runs automated OpenClaw agent benchmarks that fetch tasks, execute them, score performance across capability, configuration, security, hardware, and permission dimensions, and generate reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antutuadmin](https://clawhub.ai/user/antutuadmin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to run repeatable agent benchmarks, compare score and throughput, inspect category-level performance, and generate local result reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark data uploads are enabled by default and may include OpenClaw session metadata plus truncated stdout and stderr snippets. <br>
Mitigation: Review the upload disclosure before running; use local-only mode by setting upload_to_server=false when leaderboard submission is not desired. <br>
Risk: The benchmark exercises the OpenClaw agent and mutates shared OpenClaw session state during evaluation. <br>
Mitigation: Run it in an isolated session or workspace that does not contain sensitive data or active production work. <br>
Risk: Local reports, cache files, and temp logs may contain benchmark routing metadata and execution output. <br>
Mitigation: Treat data/ and temp/ artifacts as sensitive, review them before sharing, and remove them when no longer needed. <br>
Risk: Question fetching still uses the network even when result upload is disabled. <br>
Mitigation: Run only in environments where outbound HTTPS access to the benchmark service is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antutuadmin/benchclaw) <br>
- [BenchClaw homepage](https://benchclaw.antutu.com) <br>
- [BenchClaw repository](https://github.com/BenchClaw/benchclaw) <br>
- [Upload disclosure](UPLOAD_DISCLOSURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal progress text, local JSON result data, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes benchmark data and logs under data/ and temp/; leaderboard upload is enabled by default unless local-only mode is selected.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
