## Description:

eKYC Suite enables AI agents to run consent-based identity checks on user-provided images and videos, including face comparison, liveness checks, document OCR, and media risk review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carochen112233-commits](https://clawhub.ai/user/carochen112233-commits)

### License/Terms of Use:

MIT-0

## Use Case:

AI agent builders, fintech onboarding teams, and KYC workflow developers use the skill to add consent-based identity verification and document or media checks to human-reviewed onboarding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided identity images or videos may contain sensitive personal data and are sent to the configured external service; returned OCR and verification results can also contain sensitive fields.

Mitigation: Confirm user authorization, review the configured HTTPS destination and retention policy, restrict access to results, and use human review for consequential decisions.

Risk: The security evidence reports a benign verdict with medium confidence, identity-verification network activity, a missing declared tool scope, and a Skillspector exit error that limits scan reliability.

Mitigation: Review the destination and declared permissions before use, and treat verification outputs as advisory signals subject to operator controls and human review.

## Reference(s):

- [eKYC Suite ClawHub page](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite)
- [Related eKYC Suite npm package](https://www.npmjs.com/package/@wefi-ai/ekyc-suite-mcp)
- [Related repository listed in skill metadata](https://github.com/wefi-ai/ekyc-suite-mcp)
- [Tencent Cloud FaceID Verification Skill reference](https://skillhub.cn/skills/tencent-adm/tencentcloud-faceid-verification)

## Skill Output:

**Output Type(s):** [Structured data, Analysis]

**Output Format:** [Structured JSON results containing face comparison, liveness, document OCR, or media risk signals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory signals for human review; results may contain sensitive identity information.]

## Skill Version(s):

1.1.30 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
