# Agent Earth Skill 재검증 결과 (v2)

- 대상 브랜치: `fix/skill-improvements`
- 검증자: Quinn (🧪)
- 판정: **REQUEST_CHANGES**

## 실행/확인 범위
필수 파일 5개를 모두 검토했습니다.

1. `skill/verification.md` (이전 이슈)
2. `skill/plan.md` (개선 계획)
3. `skill/SKILL.md` (수정본)
4. `lib/validate.js` (key 차단 로직)
5. `lib/__tests__/validate.test.js` (테스트)

테스트도 직접 실행했습니다:

```bash
cd ~/heavaa/dev/agent-earth-v2 && node lib/__tests__/validate.test.js
```

결과: **7/7 PASS**

---

## 1) 이전 5개 개선안 반영 여부

### ✅ 반영 완료
- #1 P0 키 노출 방지: `validate.js`에 `[?&]key=` 차단 추가됨
- #2 P0 중복 등록 흐름 개선: SKILL.md에서 `POST /api/agents` 직접 시도 + 409 정상 처리 안내
- #3 P1 Wikimedia 인코딩/0건 분기: URL 인코딩 + fallback 명시
- #4 P1 실패 코드 분기표: agents/walks/streetview status별 처리 추가
- #5 P2 좌표 검증 규칙: 도시 경계/거리 sanity/country 일치/정밀도 규칙 추가

즉, **plan.md의 5개 항목은 문서/코드 기준으로 모두 구현됨**.

---

## 2) `validate.js` key= 차단 정확성 (오탐/미탐)

현재 로직:
```js
if (/[?&]key=/i.test(url)) return false;
```

### ✅ 잘 잡는 케이스
- `...?key=...` 차단
- `...?a=1&key=...` 차단
- 대소문자 혼합 `?KEY=`도 차단(i 플래그)
- 경로에 `keyboard.jpg`처럼 `key` 문자열만 있는 경우는 허용 (오탐 방지)

### ⚠️ 한계(미탐 가능)
- 쿼리 파라미터 구분자를 `;`로 쓰는 비표준/레거시 형태(`;key=`)는 미탐
- 퍼센트 인코딩으로 파라미터명을 우회한 비정상 입력은 미탐 가능

실사용 관점에서는 이번 패치가 **핵심 누출 경로(Street View 기본 URL 형태)는 효과적으로 차단**합니다. 다만 완전 방어를 원하면 URL 파싱 기반 검증으로 보강 권장.

---

## 3) SKILL.md 일관성/실행 가능성

전체 플로우는 실행 가능합니다(등록→리서치→waypoints→제출→리포트). 다만 아래 **문서 충돌**이 존재합니다.

### 🔴 HIGH-1: `has_street_view` 규칙이 문서 내에서 상충
- Step 3.5 Priority 1에는 metadata `status=OK`면 `has_street_view: true`로 설정하라고 되어 있음
- 같은 문서 하단에는 **"actual Street View image를 쓸 때만 true"**라고 되어 있음

이 충돌은 에이전트 구현을 분기시키고 데이터 품질(필드 의미)을 깨뜨립니다. 하나로 통일 필요.

---

## 4) 새 변경이 기존 기능을 깨뜨리는지

### 영향 요약
- `image_url` 검증 강화로 `?key=` / `&key=` 포함 URL은 이제 400 대상
- 의도된 보안 강화이나, 기존에 key 파라미터를 쓰던 외부 이미지 URL이 있었다면 동작 변경 발생 가능

### 발견 이슈
- 🟡 MEDIUM-1: 현재 차단 규칙이 정규식 기반이라 우회형 입력에 대한 완전성 부족(위 미탐 항목)
- 🟡 MEDIUM-2: 에러 핸들링 표에서 429는 "절대 자동 재시도하지 않음"이라면서 agents 429 항목에는 `retry_after_seconds` 후 재시도 지시가 있어 정책 문구가 다소 모순적
- 🟢 LOW-1: SKILL.md가 한국어/영어 혼합이며 일부 문장은 운영 룰 해석 여지가 있음(자동화 에이전트 간 일관성 저하 가능)

---

## 결론

5개 개선안은 구현됐고, 테스트도 통과했습니다. 하지만 **문서 내부 규칙 충돌(특히 `has_street_view`)**이 남아 있어 현재 상태로는 에이전트가 일관되게 수행하기 어렵습니다.

따라서 최종 판정은 **REQUEST_CHANGES**입니다.

---

## 수정 권장사항 (짧게)
1. `has_street_view` 정의를 한 줄로 고정 (metadata 기반인지, 실제 이미지 기반인지 단일 규칙)
2. key 차단을 URL 파싱 기반으로 보강(정규식 보완)
3. 429 재시도 정책 문구를 섹션 간 동일하게 정리
