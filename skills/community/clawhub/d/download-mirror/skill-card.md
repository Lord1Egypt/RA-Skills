## Description:

Helps agents diagnose failed or slow Hugging Face and GitHub downloads, then use available mirrors such as hf-mirror, ModelScope, GitCode, or ghfast.top to retrieve models, datasets, and repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yazuibi](https://clawhub.ai/user/yazuibi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when model, dataset, or repository downloads fail, time out, or are too slow, especially for Hugging Face and GitHub resources. It provides connectivity checks, mirrored download commands, diagnostic scripts, and model ID mapping guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloads may be routed through third-party mirror services.

Mitigation: Use mirrors only for public resources or trusted environments, and avoid sending Hugging Face tokens or other credentials to untrusted mirrors.

Risk: Downloaded repositories, archives, or model files may not match the intended upstream artifact.

Mitigation: Verify downloads with pinned revisions, commit hashes, signatures, checksums, or other trusted integrity data before building, importing, or running them.

Risk: Helper scripts can install Python packages into the active environment.

Mitigation: Prefer a pinned and preinstalled dependency environment before running the helper scripts.

Risk: Disabling certificate checks can weaken transport security.

Mitigation: Do not disable certificate validation; update certificates or fix network configuration instead.

## Reference(s):

- [ModelScope ID Map](references/modelscope_id_map.md)
- [ModelScope Models](https://modelscope.cn/models)
- [ClawHub Skill Release](https://clawhub.ai/yazuibi/skills/download-mirror)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local helper scripts that check network connectivity, install Python packages, set download endpoints, and clone or download files from selected mirrors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
