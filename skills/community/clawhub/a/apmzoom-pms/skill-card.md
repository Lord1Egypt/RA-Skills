## Description: <br>
APM 플랫폼의 메시지 푸시 서비스 API 모음. 헬스 체크, 관리자/사용자 푸시 메시지 목록·상세·읽음 상태 업데이트, 커스텀 정보 업로드 등 8개 엔드포인트를 포함. authcode 헤더(HH + access_token)로 호출. 서비스명: ApmZoomPushMessageService. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apmzoom](https://clawhub.ai/user/apmzoom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to call APM platform push-message service endpoints for health checks, seller and user message lookup, read-status updates, and custom information upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents authenticated non-public API endpoints and includes static signing salts. <br>
Mitigation: Install only when the APM service owner is trusted, keep tokens private, and have the publisher remove or rotate exposed signing salts. <br>
Risk: Write-capable endpoints can update read status or upload custom information. <br>
Mitigation: Require manual approval before POST, read-status update, or upload actions, and use a least-privilege APM_USER_TOKEN. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/apmzoom/apmzoom-pms) <br>
- [Publisher profile](https://clawhub.ai/user/apmzoom) <br>
- [Project homepage](https://github.com/apmzoom-ai/apm-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown API reference with request headers, endpoints, and signing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an APM_USER_TOKEN environment variable for authenticated endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
