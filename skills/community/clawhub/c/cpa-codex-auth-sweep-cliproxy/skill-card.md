## Description:

Scans Codex authentication files through a CLI Proxy management API, reports invalid or quota-exhausted credentials, and can delete 401 entries only after explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bddiudiu](https://clawhub.ai/user/bddiudiu)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to audit Codex credentials managed by CLI Proxy, identify invalid or weekly-quota-exhausted entries, and optionally remove confirmed 401 credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles CLI Proxy management credentials and can cause real Codex tokens to be forwarded to the configured probe host.

Mitigation: Use only trusted CLI Proxy servers and operator environments, keep the default chatgpt.com probe target, and avoid overriding the allowed host list.

Risk: Unsafe probe hosts or disabled TLS verification can broaden credential exposure.

Mitigation: Do not use --allow-unsafe-probe-host or --insecure unless the operator has explicitly reviewed and accepted the endpoint and TLS risk.

Risk: The scanner can delete 401 authentication files in bulk.

Mitigation: Use --delete-401 --yes only after reviewing generated deletion targets and confirming the environment can recover deleted auth files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports progress, aggregate status counts, reason buckets, deletion status, and per-auth scan results when JSON output is enabled.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
