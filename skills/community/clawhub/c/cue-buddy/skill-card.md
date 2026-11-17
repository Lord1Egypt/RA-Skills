## Description:

Cue Buddy helps business users author, validate, test, tune, and pin reusable Cue research buddy templates through natural conversation, public-data workflows, and the Cue production API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and domain experts in finance, banking credit, asset management, private-fund diligence, compliance research, and strategy use this skill to turn recurring public-data research scenarios into reusable Cue buddy templates. The skill supports drafting, validating, creating, testing, tuning, and pinning templates in the user's Cue account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, pin, or unpin templates in the user's Cue account.

Mitigation: Confirm each account-changing action and review the template content or diff before allowing create, update, frequent, or unfrequent operations.

Risk: The skill uses a Cue API key and makes network calls to cuecue.cn.

Mitigation: Use only the intended CUE_API_KEY and CUE_API_BASE values, avoid exposing keys in conversation or logs, and install only if cuecue.cn API access is acceptable.

Risk: The skill may inspect selected local reference materials while drafting templates.

Mitigation: Treat local materials as source context, extract reusable structure instead of verbatim sensitive content, and do not upload private originals to Cue.

Risk: The skill includes GitHub-based self-maintenance behavior through update checks and upgrades.

Mitigation: Avoid +upgrade and session-start silent update checks unless GitHub-based self-maintenance is acceptable, and inspect changes before applying an upgrade.

## Reference(s):

- [Cue platform](https://cuecue.cn)
- [Cue API base endpoint](https://cuecue.cn/api)
- [Cue API key setup](https://cuecue.cn/hub/api-key)
- [Template fields specification](references/template-fields-spec.md)
- [Hard rules](references/hard-rules.md)
- [Materials intake rules](references/materials-intake.md)
- [Corporate credit example](references/examples/corporate-credit.md)
- [Earnings review example](references/examples/earnings-review.md)
- [Gemini CLI verification report](docs/verification-reports/2026-05-20-gemini-cli.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, optional JSON template files, and API-backed status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local template artifacts and may perform Cue account mutations only after user confirmation.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
