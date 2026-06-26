# Finance Automation Skill

OpenClaw용 금융/결제 자동화 스킬

## 개요

Stripe/Lemon Squeezy 연동, 인보이스 자동화, 경비 처리, 재무 리포트 생성을 자동화하는 OpenClaw 스킬입니다.

## 핵심 가치 제안

- **경리 직원 1명 월급 절감** (월 300-420만원 → 49,000원)
- **ROI: 600-800%**
- **시간 70% 절감** (인보이스 작성)
- **실수 90% 감소** (경비 분류)

## 주요 기능

### Phase 1: MVP (Week 1-2)
- ✅ Stripe/Lemon Squeezy 결제 모니터링
- ✅ 실시간 알림 (Telegram)
- ✅ 일일/주간/월간 매출 요약
- ✅ 기본 인보이스 생성

### Phase 2: 인보이스 자동화 (Week 3)
- ✅ 인보이스 템플릿 (한국 세금계산서 포함)
- ✅ PDF 생성
- ✅ 자동 발송 (이메일)
- ✅ 결제 리마인더

### Phase 3: 경비 처리 (Week 4)
- ✅ 경비 입력 및 분류
- ✅ 영수증 OCR (선택)
- ✅ 카테고리 자동 분류
- ✅ 월별 경비 리포트

### Phase 4: 고급 분석 (Week 5-6)
- ✅ MRR (Monthly Recurring Revenue)
- ✅ Churn Rate
- ✅ LTV (Customer Lifetime Value)
- ✅ 트렌드 분석 및 예측

## 기술 스택

- **Backend**: Node.js 18+
- **Framework**: Express.js
- **Database**: SQLite (로컬) / PostgreSQL (프로덕션)
- **PDF**: PDFKit
- **OCR**: Tesseract.js (선택)
- **APIs**:
  - Stripe API
  - Lemon Squeezy API
  - OpenClaw Message API

## 프로젝트 구조

```
finance-automation/
├── README.md                 # 이 파일
├── ARCHITECTURE.md          # 아키텍처 문서
├── SKILL.md                 # OpenClaw 스킬 정의
├── package.json
├── .env.example
├── .gitignore
├── src/
│   ├── index.js            # 메인 진입점
│   ├── config/
│   │   └── config.js       # 환경 변수 관리
│   ├── api/
│   │   ├── stripe.js       # Stripe API 클라이언트
│   │   └── lemonSqueezy.js # Lemon Squeezy API 클라이언트
│   ├── webhooks/
│   │   ├── stripe.js       # Stripe Webhook 핸들러
│   │   └── lemonSqueezy.js # Lemon Squeezy Webhook 핸들러
│   ├── services/
│   │   ├── payment.js      # 결제 처리 로직
│   │   ├── invoice.js      # 인보이스 생성
│   │   ├── expense.js      # 경비 처리
│   │   ├── report.js       # 리포트 생성
│   │   └── notification.js # 알림 발송
│   ├── models/
│   │   ├── payment.js      # 결제 모델
│   │   ├── invoice.js      # 인보이스 모델
│   │   └── expense.js      # 경비 모델
│   ├── utils/
│   │   ├── pdf.js          # PDF 생성 유틸
│   │   ├── ocr.js          # OCR 처리
│   │   └── analytics.js    # 분석 함수
│   └── templates/
│       ├── invoice-kr.html # 한국 세금계산서 템플릿
│       └── invoice-en.html # 영문 인보이스 템플릿
├── db/
│   ├── schema.sql          # DB 스키마
│   └── migrations/         # DB 마이그레이션
├── tests/
│   ├── unit/
│   └── integration/
└── docs/
    ├── API.md              # API 문서
    ├── DEPLOYMENT.md       # 배포 가이드
    └── PRICING.md          # 과금 모델
```

## 빠른 시작

### 1. 설치

```bash
mkdir -p ~/ubik-collective/systems/ubik-pm/skills/finance-automation
cd ~/ubik-collective/systems/ubik-pm/skills/finance-automation
npm init -y
npm install express stripe @lemonsqueezy/lemonsqueezy.js dotenv sqlite3 pdfkit nodemailer axios
npm install --save-dev jest nodemon
```

### 2. 환경 변수 설정

`.env` 파일 생성:

```bash
cp .env.example .env
```

필수 환경 변수:

```env
# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Lemon Squeezy
LEMON_SQUEEZY_API_KEY=...
LEMON_SQUEEZY_STORE_ID=...
LEMON_SQUEEZY_WEBHOOK_SECRET=...

# Database
DATABASE_URL=sqlite:./db/finance.db

# Server
PORT=3000
NODE_ENV=development

# OpenClaw (선택)
OPENCLAW_API_URL=http://localhost:7777
OPENCLAW_TOKEN=...

# Telegram (알림용)
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...

# Email (인보이스 발송용)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASS=...
```

### 3. 데이터베이스 초기화

```bash
npm run db:init
```

### 4. 개발 서버 실행

```bash
npm run dev
```

서버가 `http://localhost:3000`에서 실행됩니다.

### 5. Webhook 터널 설정

로컬 개발 시 Stripe Webhook을 받으려면:

```bash
# Stripe CLI 설치
brew install stripe/stripe-cli/stripe

# 로그인
stripe login

# Webhook 포워딩
stripe listen --forward-to localhost:3000/webhook/stripe
```

또는 ngrok 사용:

```bash
ngrok http 3000
# https://xxxx.ngrok.io/webhook/stripe를 Stripe Dashboard에 등록
```

## API 키 발급

### Stripe

1. https://dashboard.stripe.com 접속
2. 개발자 > API 키
3. Secret Key, Publishable Key 복사
4. Webhook 엔드포인트 추가:
   - URL: `https://your-domain.com/webhook/stripe`
   - 이벤트:
     - `payment_intent.succeeded`
     - `payment_intent.payment_failed`
     - `invoice.payment_succeeded`
     - `customer.subscription.created`
     - `customer.subscription.deleted`

### Lemon Squeezy

1. https://app.lemonsqueezy.com 접속
2. Settings > API
3. Create new API key
4. Webhooks 설정:
   - URL: `https://your-domain.com/webhook/lemon-squeezy`
   - 이벤트:
     - `order_created`
     - `subscription_created`
     - `subscription_cancelled`

## 사용 예제

### 결제 모니터링

```javascript
// Stripe 결제 성공 시 자동 알림
// Webhook이 자동으로 처리
```

### 인보이스 생성

```javascript
const { generateInvoice } = require('./src/services/invoice');

const invoice = await generateInvoice({
  customer: {
    name: '홍길동',
    email: 'customer@example.com',
    businessNumber: '123-45-67890',
    address: '서울시 강남구...'
  },
  items: [
    { name: 'Multi-Agent Dev Team Pro', quantity: 1, price: 49000 }
  ],
  dueDate: '2026-03-31'
});

// PDF 자동 생성 및 이메일 발송
```

### 경비 추가

```javascript
const { addExpense } = require('./src/services/expense');

await addExpense({
  amount: 50000,
  category: 'office',
  description: '사무용품',
  date: '2026-03-04',
  receipt: './receipts/2026-03-04.jpg' // 선택
});
```

### 월간 리포트 생성

```javascript
const { generateMonthlyReport } = require('./src/services/report');

const report = await generateMonthlyReport('2026-03');

console.log(`
총 매출: ${report.revenue}원
총 경비: ${report.expenses}원
순이익: ${report.profit}원
MRR: ${report.mrr}원
`);
```

## OpenClaw 통합

### 자동 알림

`.openclaw/config.yaml`:

```yaml
skills:
  finance-automation:
    enabled: true
    notifications:
      channel: telegram
      events:
        - payment_success
        - payment_failed
        - invoice_overdue
        - budget_exceeded
```

### Cron 작업

일일 매출 요약 (매일 아침 9시):

```bash
openclaw cron add \
  --name "Daily Revenue Report" \
  --cron "0 9 * * *" \
  --agent "ubik-pm" \
  --message "오늘의 재무 요약을 생성해주세요."
```

## 테스트

```bash
# 단위 테스트
npm test

# 통합 테스트
npm run test:integration

# Stripe 테스트 모드
# .env에서 STRIPE_SECRET_KEY를 sk_test_로 시작하는 키로 설정
```

### Stripe 테스트 카드

```
성공: 4242 4242 4242 4242
실패 (잔액 부족): 4000 0000 0000 9995
실패 (카드 거부): 4000 0000 0000 0002
```

## 배포

### Heroku

```bash
heroku create finance-automation
heroku config:set STRIPE_SECRET_KEY=sk_live_...
git push heroku main
```

### Railway

```bash
railway init
railway add
railway up
```

### Docker

```bash
docker build -t finance-automation .
docker run -p 3000:3000 --env-file .env finance-automation
```

## 보안 체크리스트

- [ ] API 키를 절대 Git에 커밋하지 않음
- [ ] `.env` 파일을 `.gitignore`에 추가
- [ ] Webhook 서명 검증 활성화
- [ ] HTTPS 사용 (프로덕션)
- [ ] 민감한 데이터 암호화
- [ ] Rate Limiting 설정
- [ ] CORS 설정
- [ ] SQL Injection 방지

## 라이선스

MIT

## 기여

Pull Request 환영합니다!

## 지원

- Discord: https://discord.gg/openclaw
- Email: support@ubik.systems
- 문서: https://docs.openclaw.ai
