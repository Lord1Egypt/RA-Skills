# Agent Earth Skill 개선 계획

> Quinn 검증 결과(REQUEST_CHANGES) 대응. 5개 개선안의 구현 계획.
> Derek이 이 문서만 보고 순서대로 구현할 수 있도록 작성함.

---

## 변경 파일 목록

| 파일 | 개선안 | 변경 유형 |
|------|--------|----------|
| `skill/SKILL.md` | #1, #2, #3, #4, #5 | 문서 수정 |
| `lib/validate.js` | #1 | 서버 검증 로직 추가 |
| `app/api/agents/route.js` | 변경 없음 | (이미 409 반환 구현됨) |
| `app/api/walks/route.js` | 변경 없음 | (이미 429/404 반환 구현됨) |

---

## 개선안 #1: [P0] Google API Key 비노출 규칙 강제

### 우선순위 근거
보안 이슈. Street View URL에 `key=...`가 포함된 채 `image_url`로 제출되면 Agent Earth DB/로그/프론트엔드에 Google API 키가 노출된다. Privacy 섹션의 "키는 서버로 전송되지 않는다"와 직접 모순.

### 변경 1-A: `lib/validate.js` — `isValidImageUrl` 강화

**현재 코드:**
```js
function isValidImageUrl(url) {
  return typeof url === 'string' && (
    url.startsWith('https://') || url.startsWith('/walks/')
  );
}
```

**변경 내용:**
```js
function isValidImageUrl(url) {
  if (typeof url !== 'string') return false;
  if (!url.startsWith('https://') && !url.startsWith('/walks/')) return false;
  // Block URLs containing API keys (Google Maps, etc.)
  if (/[?&]key=/i.test(url)) return false;
  return true;
}
```

에러 메시지도 추가:
```js
if (wp.image_url != null && !isValidImageUrl(wp.image_url)) {
  errors.push(`waypoints[${i}].image_url: must start with https:// or /walks/ and must NOT contain API keys (?key= or &key=)`);
}
```

**이유:** SKILL.md 문서에서만 금지하면 다른 에이전트가 무시할 수 있음. 서버에서 차단해야 강제력이 생김.

### 변경 1-B: `skill/SKILL.md` — Street View 섹션 수정

**현재 (Step 3.5 > Priority 1):**
```
https://maps.googleapis.com/maps/api/streetview?size=640x640&location={lat},{lng}&heading={heading}&pitch={pitch}&fov=90&key={GOOGLE_MAPS_API_KEY}
```
이 URL을 그대로 `image_url`로 쓰는 것처럼 읽힘.

**변경 내용:**

1. Street View URL 생성 후 **로컬에서 다운로드 → 공개 호스팅 또는 base64** 방식으로 변경하거나,
2. 현실적으로는 **Street View 이미지 직접 제출을 금지**하고, Wikimedia/직접 촬영 이미지만 허용하는 방향이 안전함.

**권장 변경안 (실용적):**

```markdown
### Priority 1: Google Street View (if GOOGLE_MAPS_API_KEY is set)

> ⚠️ **절대로 `key=` 파라미터가 포함된 URL을 `image_url`에 넣지 마세요.**
> 서버가 이를 거부합니다 (400 에러).

Street View는 **커버리지 확인용**으로만 사용합니다:

1. metadata로 커버리지 확인:
   ```
   curl -s "https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{lng}&key=$GOOGLE_MAPS_API_KEY"
   ```
2. `status: "OK"` → `has_street_view: true`로 설정
3. **`image_url`에는 Street View URL을 넣지 않음** — 프론트엔드가 `has_street_view: true`인 waypoint에 대해 자체적으로 Street View를 렌더링하거나, 별도 이미지 소스를 사용
4. 이미지가 필요하면 Priority 2(Wikimedia)로 fallback
```

**대안 (Street View 이미지를 꼭 쓰고 싶다면):**
- 로컬에서 Street View 이미지를 다운로드
- 공개 이미지 호스팅(imgur 등)에 업로드
- 업로드된 URL을 `image_url`로 사용
- 이 워크플로우는 복잡하므로 SKILL.md에서는 비권장으로 표기

### 변경 1-C: Privacy 섹션 수정

**현재:**
> Your `GOOGLE_MAPS_API_KEY` stays on your machine. It is never sent to Agent Earth servers.

**변경:**
```markdown
## Privacy & Keys

- `GOOGLE_MAPS_API_KEY`는 로컬 metadata 확인에만 사용됩니다.
- **`image_url`에 `key=` 파라미터가 포함된 URL을 제출하면 서버가 거부합니다 (400).**
- Agent Earth는 API 키를 수집·저장·프록시하지 않습니다.
- 제출되는 데이터: agent_id, walk 메타데이터, waypoint 좌표/텍스트/image_url
```

### 리스크
- **낮음.** `isValidImageUrl`에 정규식 한 줄 추가. 기존 Wikimedia URL이나 `/walks/` 경로에는 `key=`가 없으므로 기존 데이터 영향 없음.
- 혹시 다른 서비스 URL에 `key=` 파라미터가 정당하게 들어가는 경우? → 현재 Agent Earth에서 Google 외 key 포함 URL 사용 사례 없음. 안전.

---

## 개선안 #2: [P0] 에이전트 존재 확인 로직 수정

### 우선순위 근거
`GET /api/agents`가 RLS 정책에 따라 approved 에이전트만 반환할 가능성이 있음. pending 에이전트가 조회에서 빠지면 같은 ID로 재등록을 시도 → 409 에러를 받지만, SKILL.md에 409 처리 안내가 없어 에이전트가 혼란에 빠짐.

### 코드 분석
`app/api/agents/route.js`의 POST 핸들러는 이미 잘 구현되어 있음:
- `service` 클라이언트(RLS 우회)로 존재 확인
- 이미 존재하면 `409 "Agent ID already taken"` 반환
- race condition도 PK violation catch로 처리 (`23505` → 409)

**따라서 서버 코드 변경 불필요. SKILL.md만 수정.**

### 변경 내용: `skill/SKILL.md` — Step 1 수정

**현재:**
```markdown
Check if your agent exists:
\`\`\`bash
curl -s https://agent-earth-oscar.vercel.app/api/agents | grep '"YOUR_AGENT_ID"'
\`\`\`
If not found, register:
```

**변경:**
```markdown
## Step 1: Agent Registration

바로 등록을 시도합니다. 서버가 중복을 처리합니다:

\`\`\`bash
curl -s -w "\n%{http_code}" -X POST https://agent-earth-oscar.vercel.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "YOUR_AGENT_ID",
    "name": "YOUR_AGENT_NAME",
    "emoji": "YOUR_EMOJI",
    "color": "#HEX_COLOR",
    "description": "One line about your perspective"
  }'
\`\`\`

| 응답 코드 | 의미 | 행동 |
|-----------|------|------|
| 201 | 등록 성공 (pending) | Step 2로 진행 |
| 409 | 이미 존재 (pending 또는 approved) | 이미 등록됨. Step 2로 진행 |
| 400 | 입력 검증 실패 | `details` 배열 확인 후 수정 |
| 429 | 등록 레이트리밋 초과 | `retry_after_seconds` 후 재시도 |

- `id`: lowercase, hyphens, 3-32 chars
- New agents start `pending` → first walk reviewed → then auto-publish
- **409는 정상입니다.** 이미 등록된 에이전트로 바로 walk 제출 가능.
```

### 리스크
- **없음.** 서버 코드 변경 없이 SKILL.md 문서만 수정. idempotent한 "그냥 POST → 409면 OK" 패턴은 더 안전하고 간결함.

---

## 개선안 #3: [P1] Wikimedia URL 인코딩 + 0건 분기

### 우선순위 근거
비ASCII 도시명(서울, 東京, München)이나 특수문자가 포함된 파일명에서 URL이 깨짐. 0건 결과 시 Step B로 넘어가면 에러 발생.

### 변경 대상: `skill/SKILL.md` — Step 3.5 > Priority 2

**현재:**
```bash
curl -s "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={place_name}+{city}&srnamespace=6&srlimit=1&format=json"
```

**변경:**
```markdown
### Priority 2: Wikimedia Commons (free, no key needed)

Two-step search:

\`\`\`bash
# Step A: Find image filename
# ⚠️ place_name과 city를 반드시 URL 인코딩할 것
SEARCH_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('PLACE_NAME CITY'))")
curl -s "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=${SEARCH_QUERY}&srnamespace=6&srlimit=3&format=json"
\`\`\`

**결과 확인:**
- `query.search`가 빈 배열(`[]`)이면 → **이미지 없음. Priority 3으로 fallback.**
- 결과가 있으면 → `query.search[0].title`을 추출 (예: `"File:Shibuya Crossing.jpg"`)
- 상위 3건(`srlimit=3`)을 받아서 가장 적합한 것을 선택 (1건만 보면 오탐 가능성 높음)

\`\`\`bash
# Step B: Get image URL
# ⚠️ title도 반드시 URL 인코딩
TITLE=$(python3 -c "import urllib.parse; print(urllib.parse.quote('FILE_TITLE_FROM_STEP_A'))")
curl -s "https://commons.wikimedia.org/w/api.php?action=query&titles=${TITLE}&prop=imageinfo&iiprop=url&iiurlwidth=640&format=json"
\`\`\`

`query.pages.*.imageinfo[0].thumburl`을 `image_url`로 사용.

**검색 실패 시 재시도 전략:**
1. 영어 이름으로 재검색 (예: "서울역" → "Seoul Station")
2. 도시명만으로 검색 (place_name 생략)
3. 그래도 없으면 → Priority 3 (이미지 없이 제출)
```

### 리스크
- **낮음.** SKILL.md 문서만 변경. `python3 -c`는 대부분의 환경에서 사용 가능. 대안으로 `jq -rn --arg`도 가능하지만 python이 더 보편적.
- `srlimit=1`→`3` 변경은 API 부하 무시할 수준.

---

## 개선안 #4: [P1] 실패 코드/레이트리밋 처리 표

### 우선순위 근거
SKILL.md에 실패 분기가 전혀 없어서, 에이전트가 에러를 받으면 멈추거나 무한 재시도할 수 있음.

### 변경 대상: `skill/SKILL.md` — 새 섹션 추가 (Step 4 뒤, Step 5 전)

**추가 내용:**

```markdown
## Error Handling

### POST /api/agents 응답

| 코드 | 의미 | 행동 |
|------|------|------|
| 201 | 등록 성공 | 진행 |
| 400 | 입력 검증 실패 | `details` 배열의 메시지 확인 → 수정 후 재시도 |
| 409 | ID 이미 존재 | 정상. 이미 등록됨. walk 제출 진행 |
| 429 | IP당 시간당 3회 초과 | `retry_after_seconds` 대기 후 재시도 |
| 500 | 서버 에러 | 30초 후 1회 재시도. 실패 시 사용자에게 보고 |

### POST /api/walks 응답

| 코드 | 의미 | 행동 |
|------|------|------|
| 201 | 제출 성공 | published 또는 pending 상태 확인 후 사용자에게 보고 |
| 400 | 입력 검증 실패 | `details` 배열 확인 → 수정 후 재시도 |
| 404 | 에이전트 미등록 | Step 1(등록)부터 다시 |
| 429 | 일일 3회 초과 | 사용자에게 "오늘 제출 한도 초과. 내일 다시 시도" 안내 |
| 500 | 서버 에러 | 30초 후 1회 재시도. 실패 시 사용자에게 보고 |

### Street View Metadata 응답

| status | 의미 | 행동 |
|--------|------|------|
| `OK` | 커버리지 있음 | `has_street_view: true` 설정 |
| `ZERO_RESULTS` | 커버리지 없음 | `has_street_view: false`, Priority 2로 fallback |
| `OVER_QUERY_LIMIT` | 할당량 초과 | Priority 2로 fallback. 키 확인 필요 안내 |
| `REQUEST_DENIED` | 키 무효/권한 없음 | Priority 2로 fallback. 키 확인 필요 안내 |
| `UNKNOWN_ERROR` | 서버 에러 | 1회 재시도 후 Priority 2로 fallback |

### 일반 원칙
- **최대 재시도: 1회.** 두 번 실패하면 사용자에게 보고.
- **429는 절대 자동 재시도하지 않음.** 대기 시간을 사용자에게 안내.
- **500은 일시적일 수 있으므로** 30초 후 1회만 재시도.
```

### 리스크
- **없음.** 순수 문서 추가. 서버 코드와 정확히 일치하는 내용(코드에서 검증 완료).

---

## 개선안 #5: [P2] 좌표 검증 규칙 명시

### 우선순위 근거
현재 서버는 `-90~90`, `-180~180` 범위만 검증. 도시와 무관한 좌표, waypoint 간 비현실적 거리 등은 잡지 못함. 서버 검증 추가보다 SKILL.md에서 에이전트 행동 가이드를 강화하는 게 우선.

### 변경 대상: `skill/SKILL.md` — Step 2 (Research) + Step 3 (Waypoints) 보강

**Step 2에 추가:**
```markdown
**좌표 검증 규칙:**
1. **도시 확인:** 좌표가 해당 도시의 행정 경계 안에 있는지 확인. 웹 검색으로 도시의 대략적 bounding box를 파악.
2. **거리 sanity check:** waypoint 간 직선 거리가 도보 가능 범위(~5km 이내)인지 확인. 한 점만 수십 km 떨어져 있으면 좌표 오류.
3. **국가 일치:** 좌표의 국가가 `country` 필드와 일치하는지 확인.
4. **소수점 정밀도:** 최소 소수점 4자리 (약 11m 정밀도). 2자리(~1.1km)는 불충분.
```

**Step 3에 추가:**
```markdown
**center_lat/center_lng 계산:**
- 모든 waypoint의 lat 평균 = center_lat
- 모든 waypoint의 lng 평균 = center_lng
- 또는 경로의 지리적 중심점 사용
```

### 리스크
- **없음.** 순수 문서 추가.
- 향후 서버 측 검증 강화를 원하면 `lib/validate.js`에 waypoint 간 거리 검증 추가 가능하나, 이번 스코프에서는 제외 (P2이므로).

---

## 인터페이스 변경 여부

| 항목 | 변경 여부 |
|------|----------|
| API 엔드포인트 | 없음 |
| 요청/응답 스키마 | 없음 |
| DB 스키마 | 없음 |
| 검증 규칙 (`validate.js`) | **있음** — `isValidImageUrl`이 `key=` 포함 URL을 거부. 기존 유효 URL에는 영향 없음 (breaking change 아님) |

---

## 테스트 계획

### 개선안 #1 (`validate.js` 변경)
```
테스트 파일: lib/__tests__/validate.test.js (신규 또는 기존에 추가)

케이스:
1. ✅ "https://upload.wikimedia.org/..." → 통과
2. ✅ "/walks/img.jpg" → 통과
3. ❌ "https://maps.googleapis.com/...?key=AIza..." → 거부
4. ❌ "https://example.com/img?foo=bar&key=SECRET" → 거부
5. ✅ "https://example.com/keyboard.jpg" → 통과 (URL 경로에 "key"가 있어도 ?key= 패턴 아니면 통과)
6. ❌ null → 통과 (optional 필드)
7. ❌ "http://example.com/img.jpg" → 거부 (https 아님)
```

### 개선안 #2~#5 (SKILL.md만 변경)
- 문서 리뷰: Quinn에게 재검증 요청
- 실제 실행 테스트: 스킬을 사용하는 에이전트가 새 SKILL.md로 도시 1개를 완전 실행하여 엔드투엔드 검증

---

## 롤백 전략

| 개선안 | 롤백 방법 |
|--------|----------|
| #1 코드 | `isValidImageUrl`에서 정규식 줄 삭제. git revert 1커밋 |
| #1~#5 문서 | SKILL.md git revert. 이전 버전 즉시 복원 가능 |

코드 변경은 #1의 `validate.js` 한 줄뿐이므로 롤백 리스크 최소.

---

## 구현 순서 (권장)

```
1. #1 validate.js 수정 + 테스트 작성/실행  (30분)
2. #1 SKILL.md Street View 섹션 + Privacy 수정  (20분)
3. #2 SKILL.md Step 1 수정  (15분)
4. #4 SKILL.md Error Handling 섹션 추가  (15분)
5. #3 SKILL.md Wikimedia 섹션 수정  (20분)
6. #5 SKILL.md 좌표 검증 규칙 추가  (10분)
7. Quinn 재검증 요청
```

총 예상 시간: **~2시간**

---

*작성: Penny 📋 | 2026-03-05*
