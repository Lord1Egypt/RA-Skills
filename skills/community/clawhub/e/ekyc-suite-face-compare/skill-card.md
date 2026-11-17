## Description:

Compares two consented face images for KYC onboarding and returns a structured similarity score for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carochen112233-commits](https://clawhub.ai/user/carochen112233-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, fintech onboarding teams, compliance engineers, and identity verification builders use this skill to compare two consented face images for KYC selfie checks and route the similarity result for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected face images and an environment value are sent to an external service, and the benign verdict has medium confidence rather than guaranteeing zero risk.

Mitigation: Use only authorized images with a trusted configured HTTPS endpoint; confirm retention and access controls and apply an appropriate human-review process.

Risk: The security guidance notes that the skill's tool scope is not declared.

Mitigation: Review the skill and configured endpoint before use.

## Reference(s):

- [eKYC Suite Face Compare on ClawHub](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite-face-compare)
- [eKYC Suite Face Compare MCP package](https://www.npmjs.com/package/@wefi-ai/ekyc-suite-face-compare-mcp)
- [Tencent Cloud FaceID Verification Skill on SkillHub](https://skillhub.cn/skills/tencent-adm/tencentcloud-faceid-verification)
- [eKYC Suite parent skill on ClawHub](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON containing a similarity score and available response metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The score ranges from 0 to 100 and is one verification signal; use deployment-appropriate thresholds and human review.]

## Skill Version(s):

1.0.22 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
