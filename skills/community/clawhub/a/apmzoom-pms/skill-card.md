## Description:

APM 플랫폼의 메시지 푸시 서비스 API 모음으로, 헬스 체크, 관리자/사용자 푸시 메시지 목록·상세·읽음 상태 업데이트, 커스텀 정보 업로드 등 8개 엔드포인트를 다룹니다.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apmzoom](https://clawhub.ai/user/apmzoom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to understand and call APM push-message service endpoints, including message listing, message detail retrieval, read-status updates, custom information upload, and service health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated write-capable endpoints can mark messages as read or upload custom information.

Mitigation: Require explicit user approval before performing write actions and use a narrowly scoped APM_USER_TOKEN.

Risk: APM_USER_TOKEN values and generated request signatures are sensitive.

Mitigation: Avoid logging tokens or signatures and treat all authenticated request material as secret.

Risk: The documented signing scheme uses reusable salts with MD5.

Mitigation: Review the skill before installation and prefer a stronger signing scheme if maintaining the API documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apmzoom/skills/apmzoom-pms)
- [APM skills source homepage](https://github.com/apmzoom-ai/apm-skills)
- [APM push message service endpoint](https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with API endpoint details and example request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an APM_USER_TOKEN environment variable for authenticated endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
