## Description:

Checks draft post content against bundled Chinese and English sensitive-word, advertising-law, and platform-compliance wordlists before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kong-zi-chg](https://clawhub.ai/user/kong-zi-chg)

### License/Terms of Use:

MIT

## Use Case:

External users and content operators use this skill to check draft posts before publication and identify terms that may violate platform, advertising, or sensitive-word policies. It returns pass/fail status, source-grouped hits, compliance tips, and an optional Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft text may be sent to DeepSeek when local DeepSeek credentials are discovered.

Mitigation: Require explicit opt-in for remote suggestions, disable implicit credential discovery, and avoid using private drafts with AI suggestions enabled.

Risk: The included HTTP API can expose draft-checking behavior beyond localhost if deployed without controls.

Mitigation: Bind the API to localhost or place it behind authentication, rate limits, and network access controls.

Risk: Chinese/CN-platform-style moderation lists may overblock or reflect rules that do not match every publishing context.

Mitigation: Review bundled and synchronized wordlists against the target platform, jurisdiction, and content policy before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kong-zi-chg/skills/compliance-check)
- [README](README.md)
- [Bundled wordlist source manifest](config/wordlist_sources.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON result or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks up to the first 5,000 characters and can include optional AI rewrite suggestions when enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
