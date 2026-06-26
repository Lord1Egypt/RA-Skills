---
name: daily-sales-digest
description: 고객사용 일일 매출 요약 스킬. 네이버 스마트스토어, 쿠팡, 배민셀러, POS 연동하여 매출 데이터를 수집하고, 일일/주간/월간 요약 리포트를 자동 생성. Discord/카톡/이메일로 배달.
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires": { "bins": ["node"] },
      },
  }
---

# daily-sales-digest

고객사용 일일 매출 요약 및 분석 스킬입니다.

## 기능

1. **매출 데이터 수집** — 네이버 스마트스토어 API, 쿠팡 Wing API, 배민셀러 API, POS 시스템 연동
2. **일일 요약** — 매일 아침 8시 전일 매출 한 줄 요약 (총매출, 주문수, 객단가)
3. **비교 분석** — 전일 대비, 전주 동요일 대비, 전월 대비 변화율 자동 계산
4. **이상 탐지** — 매출 급증/급감 시 즉시 알림 (임계값: ±30%)
5. **주간/월간 리포트** — 자동 생성 및 트렌드 분석
6. **채널 배달** — Discord/카톡/이메일로 요약 전송

## 빠른 시작

### 1. 설정 파일 생성

```bash
cp {baseDir}/config.template.json ~/.openclaw/workspace/config/daily-sales-digest.json
```

`~/.openclaw/workspace/config/daily-sales-digest.json` 파일을 편집하여 API 키와 채널 설정:

```json
{
  "sources": {
    "naver": {
      "enabled": true,
      "clientId": "YOUR_CLIENT_ID",
      "clientSecret": "YOUR_CLIENT_SECRET"
    },
    "coupang": {
      "enabled": false,
      "accessKey": "YOUR_ACCESS_KEY",
      "secretKey": "YOUR_SECRET_KEY"
    },
    "baemin": {
      "enabled": false,
      "apiKey": "YOUR_API_KEY"
    },
    "pos": {
      "enabled": false,
      "type": "custom",
      "endpoint": "http://localhost:3000/api/sales"
    }
  },
  "alerts": {
    "threshold": 0.3,
    "channels": ["discord"]
  },
  "delivery": {
    "discord": {
      "channelId": "1234567890"
    },
    "email": {
      "to": "admin@example.com"
    }
  },
  "schedule": {
    "daily": "0 8 * * *",
    "weekly": "0 9 * * 1",
    "monthly": "0 9 1 * *"
  }
}
```

### 2. 수동 실행

#### 어제 매출 요약

```bash
node {baseDir}/scripts/digest.js --date yesterday --format text
```

#### 특정 날짜 매출

```bash
node {baseDir}/scripts/digest.js --date 2026-02-17 --format json
```

#### 주간 리포트

```bash
node {baseDir}/scripts/digest.js --period week --format text
```

#### 월간 리포트

```bash
node {baseDir}/scripts/digest.js --period month --format markdown
```

### 3. 자동 스케줄링 (OpenClaw cron)

매일 아침 8시 전일 매출 요약을 Discord로 자동 전송:

```bash
openclaw cron add \
  --name "daily-sales-digest:daily" \
  --schedule "0 8 * * *" \
  --command "node /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest/scripts/digest.js --date yesterday --deliver discord"
```

주간 리포트 (매주 월요일 오전 9시):

```bash
openclaw cron add \
  --name "daily-sales-digest:weekly" \
  --schedule "0 9 * * 1" \
  --command "node /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest/scripts/digest.js --period week --deliver discord"
```

월간 리포트 (매월 1일 오전 9시):

```bash
openclaw cron add \
  --name "daily-sales-digest:monthly" \
  --schedule "0 9 1 * *" \
  --command "node /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest/scripts/digest.js --period month --deliver email,discord"
```

### 4. 이상 탐지 알림

매출 급증/급감 감지 시 즉시 Discord 알림:

```bash
node {baseDir}/scripts/alert.js --threshold 0.3 --deliver discord
```

## 데이터 수집

데이터는 `~/.openclaw/workspace/data/sales/` 디렉토리에 JSON 형식으로 저장:

```
~/.openclaw/workspace/data/sales/
  ├── 2026-02-17.json
  ├── 2026-02-18.json
  └── ...
```

각 파일 형식:

```json
{
  "date": "2026-02-17",
  "sources": {
    "naver": {
      "revenue": 1250000,
      "orders": 45,
      "avgOrderValue": 27777
    },
    "coupang": {
      "revenue": 850000,
      "orders": 32,
      "avgOrderValue": 26562
    }
  },
  "total": {
    "revenue": 2100000,
    "orders": 77,
    "avgOrderValue": 27272
  }
}
```

### 수동 데이터 수집

```bash
node {baseDir}/scripts/collect.js --date yesterday
node {baseDir}/scripts/collect.js --date 2026-02-17
node {baseDir}/scripts/collect.js --date today --source naver
```

## 출력 형식

### 텍스트 (기본)

```
📊 2026-02-17 매출 요약

💰 총 매출: ₩2,100,000 (↑ 15.2% vs 전일)
🛒 주문 수: 77건 (↑ 8.5% vs 전일)
💳 객단가: ₩27,272 (↑ 6.2% vs 전일)

📈 비교 분석:
  • 전일 대비: +15.2% (₩278,000)
  • 전주 동요일: +8.7% (₩168,000)
  • 전월 동일: +3.2% (₩65,000)

🏪 채널별:
  • 네이버: ₩1,250,000 (45건)
  • 쿠팡: ₩850,000 (32건)
```

### JSON

```json
{
  "date": "2026-02-17",
  "summary": {
    "revenue": 2100000,
    "orders": 77,
    "avgOrderValue": 27272
  },
  "comparison": {
    "vsYesterday": {
      "revenue": 0.152,
      "orders": 0.085,
      "avgOrderValue": 0.062
    },
    "vsLastWeek": {
      "revenue": 0.087,
      "orders": 0.045,
      "avgOrderValue": 0.039
    },
    "vsLastMonth": {
      "revenue": 0.032,
      "orders": 0.018,
      "avgOrderValue": 0.014
    }
  },
  "sources": {
    "naver": {
      "revenue": 1250000,
      "orders": 45
    },
    "coupang": {
      "revenue": 850000,
      "orders": 32
    }
  }
}
```

### Markdown (리포트용)

```markdown
# 주간 매출 리포트 (2026-02-10 ~ 2026-02-16)

## 요약

- **총 매출**: ₩14,500,000
- **평균 일매출**: ₩2,071,428
- **총 주문**: 523건
- **평균 객단가**: ₩27,725

## 일별 추이

| 날짜 | 매출 | 주문 | 객단가 |
|------|------|------|--------|
| 02-10 | ₩1,890,000 | 68건 | ₩27,794 |
| 02-11 | ₩2,150,000 | 78건 | ₩27,564 |
| ... | ... | ... | ... |

## 주요 인사이트

- 화요일 매출이 가장 높음 (₩2,350,000)
- 주말 주문수 감소 (-18%)
- 객단가는 안정적 유지 (±5% 이내)
```

## 이상 탐지 알림

임계값(기본 ±30%)을 초과하는 매출 변화 감지 시 즉시 알림:

```
🚨 매출 이상 감지!

2026-02-17 매출이 전일 대비 45.3% 급증했습니다.

💰 오늘: ₩3,050,000
💰 어제: ₩2,100,000
📈 증가: +₩950,000 (+45.3%)

원인 분석이 필요합니다.
```

## 보안 및 데이터 관리

- API 키는 반드시 `~/.openclaw/workspace/config/daily-sales-digest.json`에 저장
- 데이터 파일은 `.gitignore`에 추가 권장
- 민감한 정보는 절대 로그에 기록하지 않음
- 주기적으로 오래된 데이터 아카이빙 권장 (90일 이상)

## 의존성

- Node.js 18+
- OpenClaw gateway
- (선택) Discord webhook 또는 message 스킬
- (선택) 이메일 발송 스킬 (himalaya 등)

## 트러블슈팅

### API 연결 실패

```bash
# 설정 파일 확인
cat ~/.openclaw/workspace/config/daily-sales-digest.json

# 네이버 API 테스트
curl -H "X-Naver-Client-Id: YOUR_ID" -H "X-Naver-Client-Secret: YOUR_SECRET" \
  "https://api.commerce.naver.com/external/v1/pay-order/seller-product-order/list"
```

### 데이터 누락

수동으로 누락된 날짜 데이터 수집:

```bash
node {baseDir}/scripts/collect.js --date 2026-02-15 --force
```

### 스케줄 확인

```bash
openclaw cron list | grep daily-sales
openclaw cron runs daily-sales-digest:daily
```

## 향후 개선 계획

- [ ] 카카오톡 알림 연동
- [ ] 대시보드 웹 UI (Canvas 활용)
- [ ] 상품별 매출 분석
- [ ] 시간대별 매출 패턴 분석
- [ ] AI 기반 매출 예측
- [ ] Slack 연동
- [ ] Google Sheets 자동 업데이트

## 참고

- 네이버 커머스 API 문서: https://developer.naver.com/docs/commerce/commerce-api/commerce-api.md
- 쿠팡 Wing API: https://wing-developers.coupang.com/
- 배민셀러 API: (별도 제공)
