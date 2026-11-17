## Description:

Governed Apache HTTP Server config, virtual-host, module and HTTP diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Apache operators and developers use this skill to inspect local Apache HTTP Server configuration, virtual hosts, modules, health probes, and logs, and to perform a guarded graceful reload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A graceful reload can leave existing workers using the old configuration, so the final state may remain uncertain.

Mitigation: Use the dry-run and config test first, then check server status and traffic before retrying a reload.

Risk: Reading selected Apache configuration and log files can expose sensitive operational details.

Mitigation: Use operator-selected files with restricted permissions and grant the process account only the access it needs.

## Reference(s):

- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Capabilities](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup guide](artifact/references/setup-guide.md)
- [Project homepage](https://github.com/AIops-tools/Apache-AIops)
- [ClawHub skill page](https://clawhub.ai/zw008/skills/apache-aiops)

## Skill Output:

**Output Type(s):** [Analysis, Configuration guidance, Shell commands]

**Output Format:** [Structured diagnostic results with concise text guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Access-log summaries report status codes without raw URLs, IP addresses, or headers.]

## Skill Version(s):

0.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
