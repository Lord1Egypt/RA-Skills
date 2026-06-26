## Description: <br>
Ekyc Suite helps agents run eKYC identity workflows by invoking Tencent Cloud APIs for face comparison, liveness checks, document OCR, and media labeling on user-provided images or videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carochen112233-commits](https://clawhub.ai/user/carochen112233-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to support KYC onboarding, identity verification, fraud review, and document OCR workflows that require analysis of uploaded images or videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends biometric images, identity documents, bank-card images, videos, and OCR results to Tencent Cloud APIs. <br>
Mitigation: Install only if the publisher and Tencent Cloud are trusted for this data, process only media the user is authorized to submit, and mask full identifiers or card numbers unless strictly needed. <br>
Risk: Production Tencent Cloud credentials can incur charges and may expand the impact of misconfiguration or misuse. <br>
Mitigation: Use test or tightly scoped credentials first and avoid production credentials until billing, access control, and compliance requirements are approved. <br>
Risk: API verification outputs may be unsuitable as the sole basis for high-stakes identity decisions. <br>
Mitigation: Use results as decision support and require appropriate business logic and human review for legal, financial, or similarly significant outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carochen112233-commits/ekyc-suite) <br>
- [Tencent Cloud Face Verification Console](https://console.cloud.tencent.com/faceid/access) <br>
- [KYC API endpoint](https://kyc1.qcloud.com) <br>
- [Tencent Cloud mini program KYC endpoint](https://miniprogram-kyc.tencentcloudapi.com) <br>
- [Media labeling API endpoint](https://kyc2.qcloud.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials through KYC_APPID, KYC_SECRET, LABEL_APPID, and LABEL_SECRET; processes user-provided image and video files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
