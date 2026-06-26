# MVP Spec

`frontend-backend-flow-test`의 최소 실행 가능 범위는 **프론트엔드-백엔드 계약 감사(audit)** 다. 
이 MVP는 임의 API용 CRUD 테스트 생성기가 아니라, 프론트엔드 요청 흐름과 백엔드 계약 정의의 불일치를 빠르게 찾는 분석 도구를 목표로 한다.

## 1. Scope

MVP에서 반드시 지원할 것:
- 프론트엔드 코드에서 API 호출 지점 탐색
- 요청 메서드, 경로, 인증 사용, 쿼리/바디 형태의 추출
- 백엔드 코드에서 엔드포인트, DTO, 인증/권한 힌트, 응답 구조 힌트 추출
- 프론트엔드 기대값과 백엔드 계약의 차이점 비교
- 사람이 바로 읽을 수 있는 감사 리포트 생성

MVP에서 제외할 것:
- 범용 CRUD 테스트 코드 자동 생성 완성
- 프로덕션 쓰기 검증
- 완전한 브라우저/앱 UI 자동화
- 진짜 트랜잭션 롤백 보장
- 모든 프레임워크/언어 조합의 자동 지원

## 2. Modes

### Audit mode (MVP 기본값)
- 정적 분석 중심
- 실제 네트워크 write 요청 없음
- 반드시 구현 우선순위 1순위

### Live read-only mode (MVP 이후 초기 확장)
- 선택된 안전한 GET/조회 시나리오만 실환경 검증
- MVP 문서상 허용하지만 구현은 2단계

### Live write mode (MVP 이후 확장)
- dev/staging에서 제한된 쓰기 검증
- best-effort cleanup만 허용
- MVP 핵심 성공 조건에는 포함하지 않음

## 3. Inputs

감사 실행에 필요한 최소 입력:
- `frontend_paths`: 분석할 프론트엔드 루트 경로 목록
- `backend_paths`: 분석할 백엔드 루트 경로 목록
- `surfaces`: `web`, `mobile`, `admin` 중 대상 표면
- `analysis_targets`: 특정 기능, 도메인, 혹은 엔드포인트 범위
- `conventions` (선택): 베이스 URL, 공통 헤더, 인증 토큰 패턴, DTO 네이밍 규칙

권장 추가 입력:
- 샘플 API 클라이언트 파일 경로
- 샘플 컨트롤러/DTO 파일 경로
- 제외 디렉터리 (`build`, `dist`, generated code 등)

## 4. Analysis Targets

감사 시 최소 비교 단위:

### Frontend side
- HTTP method
- path / path template
- base URL 결합 방식
- auth header 또는 cookie 사용
- query params
- request body shape
- response field usage
- status/error handling 분기

### Backend side
- controller route mapping
- allowed HTTP methods
- request DTO / validator shape
- auth / role requirement hints
- response DTO / serializer shape
- nullable / required field hints
- path param / query param expectations

### Comparison outputs
- method mismatch
- path mismatch
- missing/extra request fields
- auth mismatch
- response field mismatch
- naming drift / casing drift
- likely runtime breakpoints

## 5. Output Report Schema

감사 결과는 아래 구조를 따르는 Markdown 또는 JSON 리포트로 정리한다.

```yaml
summary:
  audited_surfaces: [web, admin]
  endpoints_checked: 12
  mismatches_found: 5
  risk_level: medium

findings:
  - id: FB-001
    surface: admin
    feature: faq
    endpoint:
      method: POST
      path: /admin/faqs
    frontend_source:
      file: src/api/faq.ts
      symbol: createFaq
    backend_source:
      file: admin/controller/FaqAdminController.java
      symbol: create
    category: request-body-mismatch
    severity: high
    summary: frontend sends `displayOrder` as string but backend expects integer
    evidence:
      frontend: "displayOrder: String(order)"
      backend: "private Integer displayOrder;"
    recommendation: normalize payload type before request

unknowns:
  - dynamic request assembly prevented exact body inference

next_actions:
  - fix payload typing in admin FAQ client
  - re-run audit for faq feature
```

필수 필드:
- `summary`
- `findings[]`
- finding별 `category`, `severity`, `summary`, `evidence`, `recommendation`
- `unknowns`
- `next_actions`

## 6. Immediate Implementation Phases

### Phase 1 — Identity correction
- 스킬 설명, README, 참조 문서에서 핵심 목적을 **audit-first** 로 고정
- “CRUD generator” 인상을 주는 표현은 보조/후순위로 내림
- 이 문서를 단일 MVP 기준점으로 사용

### Phase 2 — Static extraction MVP
- 프론트엔드 요청 추출 규칙 1~2개 추가
  - 예: Axios 스타일, Dart/Flutter API service 스타일
- 백엔드 계약 추출 규칙 1~2개 추가
  - 예: Spring controller + DTO
- 기능 단위 비교기와 mismatch 분류기 구현

### Phase 3 — Report generation MVP
- 표준 감사 리포트 Markdown 생성
- 심각도 규칙 (`high`, `medium`, `low`) 정의
- 증거(evidence)와 수정 권고(recommendation) 자동 채움

### Phase 4 — Controlled live extension
- read-only live verification 추가
- write mode는 안전장치와 환경 경고가 준비된 뒤에만 확장

## 7. MVP Success Criteria

다음 조건을 만족하면 MVP로 간주한다:
- 최소 1개 프론트엔드 표면과 1개 백엔드 코드베이스를 함께 분석 가능
- 최소 3종 이상의 mismatch를 안정적으로 검출
- 리포트만 읽어도 개발자가 수정 작업을 시작할 수 있음
- live mode 없이도 독립적인 가치가 있음
