## Description: <br>
Audits cron and timer configurations for frequency, idempotency, retry, logging, and concurrency risks without triggering live jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations engineers use this skill to review cron files, timer configurations, script directories, or task descriptions before making scheduling or automation changes. It produces static, auditable findings and verification steps rather than controlling production jobs or replacing monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pointing the skill at broad directories may expose unrelated secrets, local paths, or sensitive snippets in generated reports. <br>
Mitigation: Use it only on intended cron files, timer configs, or script directories, and review or sanitize reports before sharing. <br>
Risk: The skill is a static audit helper and is not designed for production job control or real-time monitoring. <br>
Mitigation: Treat findings as review material, use dry-run or read-only workflows, and rely on dedicated systems for live scheduling, alerting, and monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/cron-job-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/resources/spec.json](artifact/resources/spec.json) <br>
- [artifact/resources/template.md](artifact/resources/template.md) <br>
- [artifact/tests/smoke-test.md](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown reports or JSON payloads, with optional local python3 command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only static analysis by default; report writing only when an explicit output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
