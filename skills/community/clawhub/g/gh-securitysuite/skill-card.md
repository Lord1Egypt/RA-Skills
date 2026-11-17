## Description:

Comprehensive agent security platform with 7 endpoints. Scan text for injection, audit SKILL.md files for malware and scope issues, generate detailed security reports with severity ratings and recommendations, browse the pattern catalog, or batch-audit multiple skills at once.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to run a local API for prompt-injection scans, SKILL.md security audits, scope checks, detailed security reports, pattern catalog review, and batch audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing the local API on an untrusted network could allow unauthenticated users to submit skill or prompt text for scanning.

Mitigation: Keep Uvicorn bound to localhost; add authentication and request-size limits before any network exposure.

Risk: Submitted prompts or SKILL.md content may contain secrets or proprietary instructions.

Mitigation: Avoid submitting secrets or confidential prompts, and sanitize or redact inputs before scanning.

Risk: Unpinned Python dependencies can make installs less repeatable.

Mitigation: Pin and review fastapi, uvicorn, pydantic, and pyyaml versions for production use.

Risk: Large batch requests can create resource pressure on the local API.

Mitigation: Limit batch size and request body size for shared or automated deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/gh-securitysuite)
- [Publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown usage examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local FastAPI service responses include scan scores, findings, verdicts, risk levels, recommendations, pattern catalog entries, and batch summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
