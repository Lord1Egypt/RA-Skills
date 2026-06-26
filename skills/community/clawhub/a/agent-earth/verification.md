# Agent Earth Skill 검증 결과

- 대상: `skill/SKILL.md`
- 판정: **REQUEST_CHANGES**
- 검증자: Quinn (🧪)

## 요약
문서의 전체 흐름(등록→리서치→waypoint→이미지→제출)은 잘 잡혀 있으나, **보안/정합성/엣지 케이스**에서 실제 운영 시 문제를 일으킬 수 있는 결함이 있습니다. 특히 Street View 키 유출 경로와 에이전트 중복 등록 리스크는 우선 수정이 필요합니다.

---

## 1) 완성도

### ✅ 좋은 점
- 엔드투엔드 단계가 명확함 (Quick Flow).
- waypoint 스키마와 작성 가이드가 실무적으로 유용함.
- 이미지 소싱 우선순위(Street View → Wikimedia → none)가 명확함.

### ⚠️ 누락/불명확
1. **중복 등록 방지 로직 불완전**
   - 현재는 `GET /api/agents | grep id`만으로 존재 확인.
   - 문서 하단 API 설명에는 `GET /api/agents`가 “approved agents” 목록이라고 되어 있어 pending 상태 에이전트가 조회되지 않을 수 있음.
   - 결과적으로 이미 pending인 ID를 다시 등록 시도하는 흐름이 발생 가능.

2. **등록 실패/제출 실패 시 분기 없음**
   - `POST /api/agents`, `POST /api/walks` 실패 코드(409/400/429/500 등) 대응 가이드 없음.

3. **필수 필드 기준 불명확**
   - waypoint 예시에서 `has_street_view: true`가 기본처럼 보이지만 실제로는 이미지 출처에 따라 false/omit 되어야 함.
   - "Not all fields required"와 JSON 샘플 간 엄밀성이 충돌.

---

## 2) 보안

### 🔴 HIGH-1: Google API Key 유출 가능성
- 문서상 Street View `image_url` 예시는 `...&key={GOOGLE_MAPS_API_KEY}` 포함 URL.
- 이 URL을 그대로 `image_url`로 API 제출하면:
  1) Agent Earth 서버에 키가 전송됨
  2) 저장/로그/클라이언트 노출 가능
- Privacy 섹션의 “키는 서버로 전송되지 않는다”와 **직접 모순**.

### 개선 방향
- `image_url`로 Google key 포함 URL을 저장/전송하지 않도록 구조 변경 필요.
  - 예: 서버 측 프록시/서명 URL/키 제거 가능한 내부 처리 규칙.
- 최소한 SKILL에 “Google URL(키 포함)은 절대 제출하지 말 것”을 명시해야 함.

---

## 3) Wikimedia API (2단계 쿼리 / URL 인코딩)

### 🟡 MEDIUM-1: URL 인코딩 누락
- Step A의 `srsearch={place_name}+{city}`는 비ASCII(예: 도쿄, 서울), 특수문자, 공백에서 깨질 수 있음.
- Step B의 `titles={title_from_step_A}`도 `File:...`에 공백/쉼표/괄호/유니코드가 포함될 수 있어 반드시 URL 인코딩 필요.

### 🟡 MEDIUM-2: 0건 결과 처리 불충분
- Step A에서 검색 결과가 0건일 때 Step B로 넘어가지 않도록 분기 명시 필요.
- 또한 `list=search` 상위 1건(`srlimit=1`)만 사용하는 것은 오탐 가능성이 큼.

---

## 4) Street View API 흐름

### ✅ 기본 흐름 자체는 타당
- metadata endpoint에서 `status=OK` 확인 후 이미지 URL 생성하는 순서는 맞음.

### ⚠️ 보완 필요
1. metadata 호출과 실제 이미지 파라미터 불일치 가능(heading/pitch/fov 차이) → metadata OK여도 기대 이미지가 아닐 수 있음.
2. `ERROR`/`ZERO_RESULTS`/`OVER_QUERY_LIMIT` 등 상태별 fallback 규칙을 표 형태로 명시하면 안정성 상승.
3. 키 노출 이슈 때문에 현재 제시 방식은 운영상 위험.

---

## 5) Edge cases

### 🔴 HIGH-2: 에이전트 중복 등록/상태 불일치
- approved-only 조회로 존재 확인 시 pending agent를 놓칠 수 있어 중복 시도 유발.

### 🟡 MEDIUM-3: 잘못된 좌표 검증 미흡
- "검색으로 확인"만 있고, 최소 검증 규칙(도시 bounding box 체크, 국가 일치 여부, waypoint 간 거리 sanity check)이 없음.

### 🟡 MEDIUM-4: Wikimedia 0건/오탐 처리 미흡
- 0건 시 분기 및 대체 전략(검색어 변형, 언어 바꿔 재시도) 부재.

### 🟢 LOW-1: Rate limit 대응 UX 부족
- 3 walks/day 제한 언급은 있으나 429 대응 안내(재시도 시점 계산/사용자 안내 문구) 없음.

---

## 6) UX (다른 에이전트 오퍼레이터 관점)

### ✅ 장점
- 빠르게 이해 가능한 단계형 문서.
- 글쓰기 톤 가이드(see/know/never)가 제품 철학 전달에 좋음.

### 개선 포인트
- 실제 실행 가능한 "최소 예제 1개"(도시 입력→완성 payload)가 있으면 온보딩 속도 개선.
- 실패 케이스별 사용자 보고 템플릿(예: "이미지 없음으로 제출", "등록 pending") 제공 권장.

---

## 7) Privacy 섹션

### 판단: **불충분**
- 현재 문구는 안전하다고 단정하지만, 본문 절차상 key 포함 URL 제출 가능성이 있어 사실과 어긋남.
- "무엇이 전송되고, 어디에 저장되며, 로그에 남는지"를 항목별로 분리해 명시해야 함.

---

## 8) ClawHub publish 준비 (frontmatter/description)

### ✅ 적절한 점
- frontmatter 필수 키 `name`, `description` 존재.
- description이 트리거 상황(탐험/산책/여행 요청)을 꽤 잘 포괄.

### ⚠️ 개선 제안
- description에 "API 키 보안 조건"(예: 키 포함 URL 제출 금지)을 짧게 추가하면 오용 방지에 도움.
- body 길이는 관리 가능한 편이나, 실패 분기/상태코드 표를 추가하면 재현성 상승.

---

## 개선 제안 (최소 3개, 우선순위 포함)

1. **[P0] Google key 비노출 규칙 강제**
   - SKILL에 "`image_url`에 key 포함 URL 금지"를 명시.
   - 가능하면 서버/프록시 기반으로 공개 가능한 URL만 저장하도록 변경.

2. **[P0] 에이전트 존재 확인 로직 수정**
   - approved 목록만 보는 방식 제거.
   - `GET /api/agents/{id}` 또는 등록 시 idempotent upsert/409 처리 규칙 문서화.

3. **[P1] Wikimedia URL 인코딩 + 0건 분기 추가**
   - Step A/B 모두 URL encode 필수 명시.
   - 검색 0건 시 재시도 전략(키워드 변형, 영어/현지어 전환, `geosearch` 보조) 추가.

4. **[P1] 실패 코드/레이트리밋 처리 표 추가**
   - 400/409/429/5xx별 행동 지침(재시도, 사용자 안내, graceful fallback).

5. **[P2] 좌표 검증 규칙 명시**
   - 도시/국가 일치, 비정상 점프 거리 차단, waypoint route 연속성 검증 규칙 추가.

---

## 최종 판정 근거
- **REQUEST_CHANGES**
- 사유: 최소 2건의 고위험 이슈(🔴) 존재
  - Street View key 유출 가능성
  - 에이전트 중복 등록/상태 불일치 리스크
- 위 이슈가 해결되기 전에는 운영 배포/공개 공유(ClawHub publish) 비권장.
