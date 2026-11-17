## Description:

AI diabetes rehabilitation management assistant for blood glucose logging, risk classification, personalized diet and exercise guidance, and reference insulin calculations based on ADA 2025 guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-feng123](https://clawhub.ai/user/chen-feng123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can run a local diabetes-coaching API to record blood glucose data, generate diet and exercise suggestions, calculate reference insulin doses, and produce short-term risk summaries. Medical outputs should be reviewed by a qualified clinician before use in care decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health data and returns insulin-dose guidance that could be unsafe if treated as medical advice.

Mitigation: Use outputs only as reference guidance and require review by a qualified clinician before applying them to care decisions.

Risk: The packaged service is not suitable for direct internet exposure or production multi-user health-service use.

Mitigation: Install only for local, single-user testing unless authentication, request size limits, rate limits, record limits, user isolation, and deployment hardening are added.

Risk: Dependency and authentication documentation issues may cause insecure or inconsistent deployments.

Mitigation: Remove the npm Flask dependency entry, pin Python dependencies, resolve the authentication documentation conflict, and verify the API key requirement before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen-feng123/skills/ai-diabetes-coach)
- [README.md](README.md)
- [API_SPEC.md](API_SPEC.md)
- [USE_GUIDE.md](USE_GUIDE.md)
- [DEPLOY.md](DEPLOY.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Configuration]

**Output Format:** [JSON API responses and Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes medical disclaimers, local API configuration guidance, and in-memory records that are lost on restart.]

## Skill Version(s):

1.0.5 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
