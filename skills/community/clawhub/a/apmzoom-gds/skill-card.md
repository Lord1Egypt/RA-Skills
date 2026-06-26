## Description: <br>
APM 플랫폼의 상품 관리 API 모음. 관리자용 상품 추가/삭제/수정/가격·재고·할인 관리 17개 + 사용자용 상품 조회/검색/카테고리/추천/유사 상품/이미지 검색 16개, 총 33개 엔드포인트. 모든 엔드포인트는 먼저 ids_*_login으로 access_token 획득 후 authcode 헤더(HH + token)로 호출. last_update_time 커서 페이지네이션 사용. 중국어/한국어 키워드 검색 지원. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apmzoom](https://clawhub.ai/user/apmzoom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through APM product catalog API calls for merchant and user workflows, including product creation, updates, deletion, price, stock, discounts, category lookup, search, recommendations, and image search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can make live catalog changes, including deletion, price, stock, discount, and listing-status updates. <br>
Mitigation: Use least-privilege APM tokens and require explicit confirmation before delete, price, stock, discount, or listing-status changes. <br>
Risk: Authentication tokens and auth headers may be exposed through logs or prompts. <br>
Mitigation: Keep auth headers out of logs and prompts and store credentials in APM_USER_TOKEN or another controlled secret store. <br>
Risk: Image-search or product-image workflows may upload sensitive or unintended visual content. <br>
Mitigation: Review or redact screenshots and images before upload. <br>
Risk: The security evidence notes insufficient safety guidance for live product-management APIs. <br>
Mitigation: Review the skill before deployment and add local approval policies for high-impact write actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/apmzoom/apmzoom-gds) <br>
- [APM skills homepage](https://github.com/apmzoom-ai/apm-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with API request details, headers, endpoint paths, and parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APM_USER_TOKEN and access-token handling before authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
