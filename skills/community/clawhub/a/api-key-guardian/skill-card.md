## Description:

Scans code repositories for leaked API keys, passwords, tokens, private keys, database URLs, and generic secrets, with optional git history scanning and AI-assisted risk analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan source trees, selected files, and recent git history for exposed credentials before code is shared or released.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AI analysis sends finding metadata through a local OpenClaw-compatible HTTP endpoint using a hardcoded API key.

Mitigation: Use local scanning mode unless the proxy is trusted; remove and rotate the embedded key, document what metadata is sent, and require explicit consent before enabling AI analysis.

Risk: Scan output reports masked secret matches and file locations that may still reveal sensitive project information in logs.

Mitigation: Run scans in trusted terminals or CI jobs, restrict log sharing, and remediate or rotate exposed credentials before publishing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaohuaishu/skills/api-key-guardian)
- [Publisher profile](https://clawhub.ai/user/xiaohuaishu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text with masked findings and optional risk-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exit code 1 when findings are detected and exit code 0 when no findings are detected.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
