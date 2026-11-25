## Description:

Optional helper skill for Boktoshi human /my endpoints that require Firebase ID token auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsmfc](https://clawhub.ai/user/rsmfc)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to work with Boktoshi human account endpoints such as profile, positions, and activity when a human session context and Firebase ID token are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firebase ID token exposure could reveal or enable access to Boktoshi human account data.

Mitigation: Keep FIREBASE_ID_TOKEN private and avoid including token values, account responses, or credentials in shared logs.

Risk: The skill is intended only for human /my account endpoints that require session context.

Mitigation: Use it only for authenticated Boktoshi human account calls and avoid applying it to unrelated public or service-account endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rsmfc/skills/boktoshi-human-helper)
- [Publisher profile](https://clawhub.ai/user/rsmfc)
- [Boktoshi API base URL](https://boktoshi.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown guidance with endpoint and authorization-header details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIREBASE_ID_TOKEN and network access to Boktoshi API endpoints.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
