## Description:

Diagnoses Alibaba Cloud OSS upload and download failures by mapping reported error codes to root-cause guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to map Alibaba Cloud OSS transfer error codes to likely root causes and troubleshooting guidance, while identifying ambiguous cases that need more information or human support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online lookup and bucket-name disclosure behavior conflicts with the skill's offline, credential-free assurances.

Mitigation: Prefer a corrected version that removes bucket-disclosure instructions, makes online lookup optional, and validates redirects; keep cloud credentials unavailable and personally review and perform any recommended resource changes.

## Reference(s):

- [OSS Error Code Catalog](references/error-code-catalog.md)
- [OSS Troubleshooting Playbook](references/troubleshooting-playbook.md)
- [Alibaba Cloud OSS Common Errors](https://help.aliyun.com/en/oss/user-guide/common-errors)
- [Alibaba Cloud OSS Error Response Parsing](https://help.aliyun.com/zh/oss/user-guide/overview-14)
- [Alibaba Cloud OSS HTTP 403 Error Codes](https://help.aliyun.com/zh/oss/user-guide/http-403-error-code)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Structured JSON diagnosis summarized as concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status, root-cause direction, troubleshooting steps, and next action; ambiguous or incomplete inputs remain inconclusive.]

## Skill Version(s):

0.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
