## Description:

Feature-complete companion for the actual CLI, an ADR-powered CLAUDE.md/AGENTS.md generator that helps agents run, configure, and troubleshoot ADR synchronization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[actual-software-inc](https://clawhub.ai/user/actual-software-inc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to operate the actual CLI, select and configure AI runners, sync ADR guidance into agent instruction files, and troubleshoot setup or runtime failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostic workflow may expose authentication, configuration, or repository details in its output.

Mitigation: Review diagnostic output before sharing it, avoid running diagnostics in sensitive environments until redaction is confirmed, and prefer secure secret stores or environment variables over command-line API key examples.

Risk: Running ADR synchronization can modify agent instruction files such as CLAUDE.md, AGENTS.md, or Cursor rules.

Mitigation: Use dry-run first, review proposed changes, and approve file writes explicitly before executing sync.

Risk: External CLI behavior can change across versions.

Mitigation: Pin or verify installed external CLI versions before use in production workflows.

## Reference(s):

- [Actual CLI homepage](https://cli.actual.ai)
- [ClawHub skill page](https://clawhub.ai/actual-software-inc/skills/actual)
- [Config Reference](references/config-reference.md)
- [Error Catalog Reference](references/error-catalog.md)
- [Output Formats Reference](references/output-formats.md)
- [Runner Guide](references/runner-guide.md)
- [Sync Workflow Reference](references/sync-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local CLI state, environment variables, configuration files, and generated CLAUDE.md, AGENTS.md, or Cursor rules outputs.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
