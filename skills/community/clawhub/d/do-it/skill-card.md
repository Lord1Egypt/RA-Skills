## Description:

帮助地球人做人生选择的 AI 判断技能 - 你只管 do it，判断交给滚滚

This skill is ready for commercial/non-commercial use.

## Publisher:

[alsoforever](https://clawhub.ai/user/alsoforever)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to structure life decisions such as career, relationship, investment, and housing choices. The skill returns a recommendation with supporting rationale, action steps, and risk warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send or store sensitive personal decision data.

Mitigation: Review before use with real personal information and avoid entering sensitive data into packaged test pages or untrusted deployments.

Risk: The packaged API server or HTTP endpoint could expose user data on an untrusted network.

Mitigation: Run only in a trusted local environment, do not expose the API server publicly, and replace hardcoded HTTP endpoints with HTTPS or same-origin APIs before deployment.

Risk: Browser history or localStorage may retain decision data after testing.

Mitigation: Clear browser history/localStorage after testing and add consent and retention controls before collecting user data.

Risk: Career, relationship, investment, and life-choice recommendations can be high-impact and may be wrong or incomplete.

Mitigation: Present outputs as advisory, preserve the user's final decision authority, and strengthen warnings before high-stakes use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alsoforever/skills/do-it)
- [do-it decision database schema](references/database-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown decision analysis with recommendation, rationale, action plan, and risk warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured sections and checklist-style action items.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
