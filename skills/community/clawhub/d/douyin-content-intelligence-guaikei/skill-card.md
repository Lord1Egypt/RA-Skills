## Description:

Provides Douyin public-data intelligence for keyword search, account post extraction, comment analysis, and real-time hot-topic tracking for content operations, competitive research, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search public Douyin content, collect public account posts, retrieve comments, and monitor hot topics for content planning, competitor analysis, sentiment research, and marketing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill sends Douyin keywords, account or video URLs, and an API token to guaikei.com.

Mitigation: Use the skill only when that third-party data flow is acceptable; avoid submitting sensitive or non-public data and use a scoped token where available.

Risk: The security review says result data is saved under the skill's logs directory.

Mitigation: Review, protect, and delete generated logs according to the user's data retention requirements.

Risk: The security review says the skill needs review because auth-error behavior and API token handling are not yet low-risk.

Mitigation: Confirm runtime auth failures stay neutral and require token handling improvements, including moving the token out of URL query strings, before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/douyin-content-intelligence-guaikei)
- [Usage documentation](artifact/readme.md)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Guaikei token service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON data, Files]

**Output Format:** [Markdown guidance with bash command examples; CLI stdout is JSON and result logs are written as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and Node.js >=16.14.0; command results may be saved under the skill logs directory.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
