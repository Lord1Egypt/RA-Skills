## Description:

This skill helps ecommerce merchants, ad teams, legal reviewers, and content operators precheck Chinese ecommerce ads and marketing assets for high-risk claims, evidence gaps, platform material risks, suggested replacements, and human review items, with optional AI-HIVE media generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, advertising, legal-review, and content-operations users use this skill to turn ad copy, images, video, product facts, target platform, region, and current rules into a pre-publication risk review and remediation plan. Developers and operators can also use its scripts to create project briefs, run AI-HIVE image or video generation, and perform deterministic video checks when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be broader than a narrow compliance checker because it also supports potentially billable AI-HIVE image and video generation.

Mitigation: Review the workflow before installation and require confirmation of generation parameters, routing mode, and budget before running image or video commands.

Risk: API keys can be stored in a local plaintext config file by the init workflow.

Mitigation: Prefer short-lived API keys supplied through the AI_HIVE_API_KEY environment variable and avoid committing config files, logs, or screenshots that expose credentials.

Risk: A custom AI_HIVE_BASE_URL can redirect requests to an endpoint outside the default AI-HIVE service.

Mitigation: Use the default service URL unless the alternate endpoint is fully trusted and approved for the data being uploaded.

Risk: Uploaded ad materials, reference images, or videos may contain content the user is not authorized to process.

Mitigation: Use only materials the user is authorized to upload and keep human review for legal, platform-rule, copyright, trademark, privacy, medical, financial, or child-related issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-ad-compliance-precheck-ai-hive)
- [AI-HIVE chat entry point](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured review sections, inline shell commands, JSON task records, and script-generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk levels, evidence locations or timestamps, replacement suggestions, model routing choices, price snapshots, task IDs, status, and downloaded file locations.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
