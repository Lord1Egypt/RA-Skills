## Description:

Ban LLM em-dashes and en-dashes before delivery, rewrite via embedded LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnpetros](https://clawhub.ai/user/shawnpetros)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use deaiify to rewrite assistant replies before delivery when Unicode en dash or em dash characters appear outside code. It is intended for OpenClaw sessions where preserving the meaning and tone of the assistant response is more important than simple character replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assistant output containing sensitive text may be resent through an embedded model run for rewriting.

Mitigation: Install only in sessions where this automatic rewrite behavior is acceptable, and avoid contexts where assistant output should not be submitted to the active model provider again.

Risk: A rewrite can alter meaning, omit detail, or fail to remove all target dash characters.

Mitigation: The skill verifies word-count drift, length expansion, and remaining banned dash characters, then fails open by delivering the original response when verification fails.

Risk: The dev dependency lockfile needs a publisher refresh according to the security guidance.

Mitigation: Prefer an updated release once the publisher refreshes the dev dependency lockfile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawnpetros/skills/deaiify)
- [Publisher profile](https://clawhub.ai/user/shawnpetros)
- [Project homepage](https://github.com/shawnpetros/deaiify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Rewritten assistant reply text, preserving Markdown and code blocks where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the active session model for rewrites, applies a configurable timeout, and fails open by delivering the original reply if rewriting or verification fails.]

## Skill Version(s):

3.4.1 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
