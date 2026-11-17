## Description:

eKYC Suite AI Guardian reviews consented face photos and short videos for KYC liveness, replay, and synthetic-media risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carochen112233-commits](https://clawhub.ai/user/carochen112233-commits)

### License/Terms of Use:

MIT-0

## Use Case:

KYC onboarding, identity operations, and fraud review teams use it to screen user-authorized selfie media in remote onboarding. Treat results as review signals, not identity proof, and route ambiguous or high-risk results to an authorized human reviewer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan reports that media and environment data are sent to an external service; its benign verdict is not a guarantee of zero risk.

Mitigation: Use only consented media, confirm the configured HTTPS service and the environment values it receives, and follow the service's retention policy. Route ambiguous or high-risk results to an authorized human reviewer.

## Reference(s):

- [eKYC Suite AI Guardian on ClawHub](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite-ai-guardian)
- [eKYC Suite AI Guardian MCP package](https://www.npmjs.com/package/@wefi-ai/ekyc-suite-ai-guardian-mcp)
- [Tencent Cloud FaceID Verification Skill on SkillHub](https://skillhub.cn/skills/tencent-adm/tencentcloud-faceid-verification)
- [eKYC Suite parent skill](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite)
- [eKYC Suite Face Compare](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite-face-compare)
- [eKYC Suite Media Labeling](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite-media-labeling)
- [eKYC Suite Document OCR](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite-document-ocr)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON results with risk levels and tags, with human-review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separate photo and video checks; results are screening signals, not identity proof.]

## Skill Version(s):

1.0.22 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
