## Description:

APM 플랫폼의 관리자 및 사용자 상품 관리 API 33개 엔드포인트를 정리해 상품 추가, 삭제, 수정, 가격, 재고, 할인, 조회, 검색, 카테고리, 추천, 유사 상품, 이미지 검색 작업을 지원합니다.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apmzoom](https://clawhub.ai/user/apmzoom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare authenticated APM product-management API calls for catalog administration and product discovery workflows. It is intended for agents that need endpoint-specific parameters, signing notes, pagination behavior, and token-handling requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support add, edit, delete, price, stock, and discount operations against live catalog data.

Mitigation: Use a limited APM token where possible and require explicit confirmation before write or destructive API calls.

Risk: APM_USER_TOKEN may grant seller or administrator access.

Mitigation: Keep APM_USER_TOKEN out of prompts and logs, and rotate or revoke it if exposure is suspected.

Risk: Deletion behavior requires review before operational use.

Mitigation: Verify the correct delete method with the API owner before enabling deletion workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apmzoom/skills/apmzoom-gds)
- [OpenClaw homepage metadata](https://github.com/apmzoom-ai/apm-skills)
- [APM API base URL](https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown API reference and API-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint paths, HTTP methods, headers, authentication requirements, signing notes, pagination fields, and request parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
