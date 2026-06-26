## Description: <br>
Scans Codex authentication files through the CLI Proxy Management API, reports invalid or quota-exhausted credentials, and deletes 401 entries only after explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bddiudiu](https://clawhub.ai/user/bddiudiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators managing CLI Proxy Codex authentication files use this skill to audit credential health, identify 401 or weekly-quota-zero accounts, and optionally remove confirmed invalid entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The management key can enumerate and modify Codex authentication files. <br>
Mitigation: Use the skill only with a CLI Proxy instance you control, keep the management key secret, and start with scan-only output before enabling deletion. <br>
Risk: The probe flow can forward real tokens to the configured probe host. <br>
Mitigation: Keep the default chatgpt.com probe host unless a trusted alternative has been explicitly approved, and avoid unsafe probe-host overrides. <br>
Risk: Bulk deletion can remove authentication files that are still needed. <br>
Mitigation: Use deletion only after reviewing the JSON results and confirming that the listed 401 entries are safe to remove. <br>
Risk: Disabling TLS verification can expose management traffic or probe traffic to interception. <br>
Mitigation: Avoid insecure TLS flags except for explicitly authorized internal troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bddiudiu/cpa-codex-auth-sweep-cliproxy) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLI Proxy base URL and management key; scan-only mode is the default, while deletion requires explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
