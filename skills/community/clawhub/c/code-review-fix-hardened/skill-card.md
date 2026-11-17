## Description:

Automated code review with fix suggestions and in-place code repairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review source files for bugs, security risks, performance issues, and style problems, then receive fix suggestions or in-place repairs when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes monetized billing behavior that contacts skillpay.me, stores local usage state, and may send a username-derived identifier externally.

Mitigation: Review or remove the billing integration and hardcoded billing key, require explicit charge confirmation, and disclose any external billing calls before use.

Risk: The skill can write in-place code repairs when fix mode is used.

Mitigation: Require explicit approval in the current conversation, show proposed changes before writing, and confine reviewed and modified paths to the project root.

Risk: The artifact includes examples and guardrails related to transmitting code or review findings to external services.

Mitigation: Keep review output local unless the user has approved an internal sharing channel, and avoid uploading sensitive source code to external LLMs or paste services.

Risk: Reviewed files may contain secrets that could persist in logs or terminal history if echoed.

Mitigation: Report secret presence and location without printing secret values, and recommend rotation when exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/code-review-fix-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/code-review-fix)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown or terminal text with issue lists, fix suggestions, and optional in-place file edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write code changes when fix mode is used; review proposed changes and billing behavior before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
