---
name: card-news-gen
description: 인스타그램/SNS용 카드뉴스를 자동 생성하는 스킬. 주제를 입력하면 → HTML 디자인 → Playwright 스크린샷 → 업로드용 이미지 생성. 다크 에디토리얼 스타일(사진 커버 + 다크 텍스트 카드) 기본 제공. "카드뉴스", "인스타 콘텐츠", "캐러셀", "card news", "carousel" 키워드에 반응.
---

# Card News Generator

주제만 주면 인스타그램 캐러셀 카드뉴스를 자동 생성합니다.

## 디자인 시스템

### 기본 스타일: Dark Editorial (검증 완료)

커버: **사진 배경 + 다크 그라데이션 + 큰 텍스트**
내부 카드: **#0A0A0A 다크 배경 + 텍스트 중심 + 블루 포인트**

레퍼런스: highoutputclub, oneononenote 스타일

### 디자인 토큰

```
배경: #0A0A0A (거의 블랙)
텍스트 메인: #FFFFFF
텍스트 서브: rgba(255,255,255,0.5)
포인트 블루: #60A5FA
포인트 옐로: #FBBF24
포인트 그린: #34D399
폰트: Pretendard (웹폰트)
카드 사이즈: 1080x1350px (4:5 인스타 세로형)
커버 제목: 96-104px, 900 weight
내부 제목: 44px, 900 weight
본문: 27px, 400 weight
프롬프트 블록: 24px
```

### 카드 구조

```
커버 (1장)
├── 배경 사진 (Unsplash 무료, opacity 0.45)
├── 다크 그라데이션 오버레이
├── 핸들 @lio_universe_00
├── 대형 제목 (96-104px, 핵심 키워드 블루 강조)
├── 서브타이틀 (34px, 반투명)
└── 페이지 인디케이터 dots

내부 카드 (N장)
├── 상단: 라벨 + 페이지 번호
├── 배경 번호 (140px, 3% opacity)
├── 제목 (44px, 키워드 블루/옐로 강조)
├── 구분선 (48px)
├── 본문 (27px, 강조는 strong/blue)
├── 프롬프트 블록 또는 예시 (어두운 박스)
├── 결과/팁 블록 (블루 좌측 보더)
└── 핸들 워터마크

CTA (1장)
├── 이모지
├── 제목 + 서브
├── 3개 아이템 리스트
├── 팔로우 버튼
└── 핸들
```

## 워크플로우

### 1단계: 콘텐츠 기획

주제를 받으면:
- 커버 후킹 카피 작성 (호기심 유발)
- 5-7장 내부 카드 구성
- CTA 카드
- 캡션 작성 (카드 내용을 상세히 풀어쓴 글 + 해시태그 3-5개)

**콘텐츠 품질 기준:**
- "이거 다 아는 내용 아니야?" → NO. 논문/데이터/구체적 수치 필수
- 바로 복붙/실행 가능한 실용성
- 저장하고 싶은 정보 밀도

### 2단계: HTML 생성

템플릿 기반 HTML을 생성합니다.

```bash
# 작업 디렉토리 생성
mkdir -p /Users/gyeuun/.openclaw/workspace/rio-interactive/card-news/{프로젝트명}/output
```

**CSS 임포트 (필수):**
```css
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
```

**배경 사진 (커버용):**
- Unsplash에서 무료 다운로드
- 저장: `photos/` 폴더
- 또는 기존 사진 활용: `../insta-first/photos-v5/` (ai-code.jpg, laptop-desk.jpg, ai-robot.jpg, ai-abstract.jpg)

**잘림/겹침 방지 체크리스트:**
- [ ] 내부 카드 padding: 상 110px, 좌우 80px, 하 90px
- [ ] 본문 텍스트가 프롬프트 블록과 겹치지 않는지
- [ ] 결과 블록이 카드 하단을 넘지 않는지
- [ ] 핸들 워터마크가 잘리지 않는지

### 3단계: 스크린샷 생성

```javascript
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 2
  });
  await page.goto('file://' + path.resolve('cards.html'), { waitUntil: 'networkidle' });
  const cards = await page.locator('.card').all();
  for (let i = 0; i < cards.length; i++) {
    await cards[i].screenshot({ path: `output/card_${i}.png` });
  }
  await browser.close();
})();
```

### 4단계: JPEG 변환 (업로드용)

PNG가 너무 크면 (>1MB) JPEG 변환:
```bash
cd output
for f in *.png; do
  sips -s format jpeg -s formatOptions 90 "$f" --out "${f%.png}.jpg"
done
```

### 5단계: 업로드

**API 업로드 (instagram-content-studio 스킬):**
```bash
cd /Users/gyeuun/.openclaw/workspace/skills/instagram-content-studio
node scripts/post-image.js \
  --env .env \
  --caption '캡션 텍스트' \
  ./output/cover.jpg ./output/card_1.jpg ...
```

**API 레이트 리밋 걸릴 경우:**
- 텔레그램으로 이미지 + 캡션 전송 → 대표님 수동 업로드
- 1시간 후 재시도
- 하루 1개 캐러셀 권장

## 캡션 작성 가이드

```
[후킹 1줄 - 질문 또는 충격적 사실]

[핵심 요약 2-3줄]

—

[카드별 상세 내용 - 각 번호별로 풀어서]

—

[CTA - 저장/팔로우 유도]

#해시태그1 #해시태그2 #해시태그3 #해시태그4 #해시태그5
```

- 해시태그: 3-5개만 (많으면 스팸 판정)
- 캡션 자체가 가치 있는 글이어야 함 (카드 요약 X, 추가 정보 O)
- 캡션에 키워드 SEO 중요 (2026 알고리즘)

## 인스타 운영 정책

- **게시 시간:** 평일 오전 7-9시 / 점심 12-13시 / 저녁 19-21시
- **주 3회:** 월/수/금 권장
- **저장(Save)이 최고 지표** — 저장하고 싶은 콘텐츠 = 알고리즘 노출 ↑
- **캐러셀 최대 20장** (2024년부터)
- **음악:** API 불가, 앱에서 수동 추가
- **핸들:** @lio_universe_00

## 대체 스타일

### Toss Clean (밝은 배경)
- 템플릿: `card-news/templates/toss-clean-v5.html`
- 화이트 배경, #3182F6 블루 포인트, 깔끔한 카드

### Toss Frosted (반투명 배경)
- 템플릿: `card-news/templates/toss-frosted-v5b.html`
- 사진 위 frosted glass 오버레이

사용자가 밝은 스타일 요청 시 위 템플릿 참고.
기본은 Dark Editorial.
