# Agent Earth Skill 최종 검증 결과 (v3)

- 대상 브랜치: `fix/skill-improvements`
- 검증자: Quinn (🧪)
- 판정: **REQUEST_CHANGES**

## 실행/확인 범위
다음 필수 파일을 검토했습니다.

1. `skill/verification-v2.md`
2. `skill/SKILL.md`
3. `lib/validate.js`
4. `lib/__tests__/validate.test.js`

테스트도 직접 실행했습니다:

```bash
cd ~/heavaa/dev/agent-earth-v2 && node lib/__tests__/validate.test.js
```

결과: **8/8 PASS, fail 0**

---

## v2의 3건 이슈 해결 여부

### 1) `has_street_view` 문서 충돌
- **상태: 해결됨 ✅**
- `SKILL.md` 기준, Street View metadata `status=OK`일 때 `has_street_view: true`로 처리하고, `image_url`에는 Street View URL을 넣지 않는 규칙으로 정리되어 있음.
- v2에서 지적된 "실제 이미지일 때만 true" 류의 상충 문구는 현재 검토 범위에서 확인되지 않음.

### 2) `key` 차단 정규식
- **상태: 해결됨 ✅**
- `lib/validate.js`:
  - `if (/[?&;]key=/i.test(url)) return false;`
- 즉 `?key=`, `&key=`, `;key=` 모두 차단.
- 테스트 3,4,8번으로 재현 검증 완료.

### 3) 429 문구 일관성
- **상태: 미해결 ❌**
- `SKILL.md` 내부 충돌 존재:
  - `POST /api/walks` 429: "일일 3회 초과 → 오늘 한도 초과 안내"(재시도 불가 의미)
  - 일반 원칙: "429는 retry_after_seconds만큼 대기 후 1회 재시도"
- Walks의 일일 한도형 429와 일반 429 재시도 원칙이 동시에 존재하여 문서 실행 규칙이 충돌함.

---

## 추가 점검: SKILL.md 전체 일관성

- 핵심 플로우(등록 → 리서치 → 웨이포인트 → 제출)는 전반적으로 일관됨.
- 다만 **429 처리 정책은 섹션 간 단일 규칙으로 통일 필요**.
  - 권장: `agents 429`(시간당 제한)과 `walks 429`(일일 제한)을 분리 규칙으로 명시.

---

## 새로운 이슈 여부

### 🟡 MEDIUM-1: 429 처리 규칙 상충(문서 실행 모호성)
- 재현 위치:
  - Error Handling > `POST /api/walks` 표의 429 행
  - General Principles의 429 재시도 규칙
- 영향:
  - 자동화 에이전트가 동일 상황에서 서로 다른 행동(재시도 vs 즉시 종료)을 수행할 수 있음.

(그 외 코드/테스트 기준으로 즉시 추가 결함은 확인되지 않음)

---

## 결론
- v2의 3건 중 **2건은 해결**, **429 문구 일관성 1건은 미해결**입니다.
- 테스트는 모두 통과했지만 문서 정책 충돌이 남아 있으므로 최종 판정은 **REQUEST_CHANGES**입니다.

## 수정 권장안 (짧게)
- `429` 정책을 엔드포인트별로 명시적으로 분리:
  - `POST /api/agents`: `retry_after_seconds` 기반 1회 재시도
  - `POST /api/walks`: 일일 한도 초과 시 재시도 금지, 사용자 안내(다음날 시도)
