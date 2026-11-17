## Description:

Generates Xiaohongshu-style multi-page graphic layout output from JSON input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit JSON content for Xiaohongshu-style multi-page text and image layout generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted JSON content and a bearer token are sent to a configurable, unvalidated network endpoint.

Mitigation: Use a narrowly scoped TS_TOKEN, provision AIZNT_PROXY_URLS only from a trusted source, and confirm xhs_generate points to an approved HTTPS service.

Risk: Sensitive drafts or real credentials could be exposed to the configured upstream service.

Mitigation: Review the skill before installing, avoid sensitive drafts unless the endpoint is approved, and rotate credentials if endpoint trust changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshengli0421/skills/aiznt-xhs)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON returned by a command-line Node.js wrapper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TS_TOKEN and AIZNT_PROXY_URLS with an xhs_generate endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
