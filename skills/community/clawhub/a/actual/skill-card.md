## Description: <br>
Companion skill for the actual CLI, an ADR-powered CLAUDE.md and AGENTS.md generator that helps agents run and troubleshoot adr-bot, authentication, configuration, runners, models, output formats, and common errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[actual-software-inc](https://clawhub.ai/user/actual-software-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install, configure, run, and troubleshoot the actual CLI when syncing ADR context into CLAUDE.md, AGENTS.md, or Cursor rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic and troubleshooting workflows can reveal sensitive authentication, configuration, account, repository, or API-key details if their output is shared without review. <br>
Mitigation: Inspect diagnostic output before sharing it and redact auth, config, account, repository, and API-key details. <br>
Risk: Sync workflows can make persistent changes to CLAUDE.md, AGENTS.md, or Cursor rule files. <br>
Mitigation: Use dry runs first, review proposed diffs before writing, and avoid force mode except in trusted automation. <br>
Risk: Runner or model misconfiguration can cause failed runs or unexpected API spend. <br>
Mitigation: Run pre-flight checks for runners, auth, and config, and set a spending cap when using paid API runners. <br>


## Reference(s): <br>
- [Actual CLI Homepage](https://cli.actual.ai) <br>
- [Config Reference](references/config-reference.md) <br>
- [Error Catalog Reference](references/error-catalog.md) <br>
- [Output Formats Reference](references/output-formats.md) <br>
- [Runner Guide Reference](references/runner-guide.md) <br>
- [Sync Workflow Reference](references/sync-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes references for runner setup, configuration, error diagnosis, sync workflow, output formats, and read-only diagnostics.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
