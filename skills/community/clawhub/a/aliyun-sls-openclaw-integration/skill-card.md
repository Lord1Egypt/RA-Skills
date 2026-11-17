## Description:

Use when the user needs to integrate OpenClaw with Alibaba Cloud SLS/Observability, including collector setup, machine groups, indexes, dashboards, collection configs, or Logtail bindings on Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to provision Alibaba Cloud SLS observability for OpenClaw on Linux, including the CLI, LoongCollector, machine groups, indexes, dashboards, collection configs, and bindings. It is intended for hosts where the target project, logstore, credentials, and sudo access are already available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or start system logging software on the host.

Mitigation: Run it only on an approved Linux host, preferably a dedicated single-user or test machine, and review the installation steps before execution.

Risk: The collector configuration can upload OpenClaw session transcripts from local user home directories.

Mitigation: Collect only with approval from affected users and restrict the collector path to the intended user or workspace before binding the config.

Risk: Alibaba Cloud AK/SK credentials may be exposed if long-lived keys are kept in shared shells.

Mitigation: Use least-privilege SLS permissions, avoid long-lived credentials in shared environments, and rotate or unset credentials after setup.

Risk: The LoongCollector installer is downloaded during setup.

Mitigation: Pin and verify the installer source before running it in production environments.

Risk: Collected logs may retain sensitive session data longer than intended.

Mitigation: Set short SLS retention and maintain a documented uninstall and cleanup procedure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-sls-openclaw-integration)
- [Command flow](references/cli-commands.md)
- [Index definition](references/index.json)
- [Dashboard template: OpenClaw Audit](references/dashboard-audit.json)
- [Dashboard template: OpenClaw Gateway](references/dashboard-gateway.json)
- [Collection config template](references/collector-config.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux, sudo, aliyun CLI access, Alibaba Cloud AK/SK environment variables, ALIYUN_UID, PROJECT, and LOGSTORE.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
