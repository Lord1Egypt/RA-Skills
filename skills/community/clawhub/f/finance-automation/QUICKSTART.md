# 🚀 Quick Start Guide

## 5분 만에 시작하기

### 1. 프로젝트 설정 (1분)

```bash
cd ~/ubik-collective/systems/ubik-pm/skills/finance-automation

# 의존성 설치
npm install

# 데이터베이스 초기화
npm run db:init
```

### 2. 환경 변수 설정 (2분)

```bash
# .env 파일 생성
cp .env.example .env

# 에디터로 열기
code .env  # 또는 nano .env
```

**최소 필수 설정:**

```env
# Stripe (테스트 키)
STRIPE_SECRET_KEY=sk_test_51...
STRIPE_WEBHOOK_SECRET=whsec_...

# Telegram (알림용)
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=123456789
```

> 💡 **Tip**: 처음에는 Stripe 테스트 키만 설정하고 시작하세요!

### 3. 서버 실행 (30초)

```bash
npm run dev
```

서버가 `http://localhost:3000`에서 실행됩니다! ✨

### 4. Webhook 터널 설정 (1분 30초)

**새 터미널에서:**

```bash
# Stripe CLI 설치 (Mac)
brew install stripe/stripe-cli/stripe

# 로그인
stripe login

# Webhook 포워딩 시작
stripe listen --forward-to localhost:3000/webhook/stripe
```

또는 **ngrok 사용:**

```bash
ngrok http 3000
# https://xxxx.ngrok.io 주소를 Stripe Dashboard에 등록
```

### 5. 테스트 (1분)

```bash
# Health check
curl http://localhost:3000/health

# API info
curl http://localhost:3000/api
```

## 🎯 첫 번째 결제 테스트

### Stripe 테스트 결제 생성

```bash
stripe payment_intents create \
  --amount=5000 \
  --currency=krw \
  --description="테스트 결제" \
  --payment-method=pm_card_visa \
  --confirm=true
```

Telegram으로 알림이 와야 합니다! 💰

## 📚 다음 단계

### 1. Lemon Squeezy 연동

```env
LEMON_SQUEEZY_API_KEY=your_key
LEMON_SQUEEZY_STORE_ID=your_store_id
```

### 2. 인보이스 기능 구현

```bash
# 서비스 파일 생성
touch src/services/invoice.js
touch src/services/payment.js
```

### 3. PDF 생성 테스트

```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

const doc = new PDFDocument();
doc.pipe(fs.createWriteStream('test-invoice.pdf'));
doc.fontSize(25).text('테스트 인보이스', 100, 100);
doc.end();
```

### 4. 경비 추가 API 구현

```javascript
// src/api/expenses.js
router.post('/', async (req, res) => {
  const expense = await expenseService.create(req.body);
  res.json(expense);
});
```

## 🔧 개발 팁

### 디버그 모드

```bash
DEBUG=* npm run dev
```

### 데이터베이스 확인

```bash
sqlite3 db/finance.db
sqlite> SELECT * FROM payments;
sqlite> .quit
```

### 로그 확인

```bash
tail -f logs/combined.log
```

## 🐛 문제 해결

### Stripe Webhook이 안 와요

```bash
# Webhook secret 확인
stripe listen --print-secret

# .env에 추가
STRIPE_WEBHOOK_SECRET=whsec_새로운시크릿
```

### Telegram 알림이 안 와요

```bash
# Bot token 테스트
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"

# Chat ID 확인
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
```

### 포트 충돌

```env
# .env에서 포트 변경
PORT=3001
```

## 📖 추가 자료

- [README.md](./README.md) - 전체 문서
- [ARCHITECTURE.md](./ARCHITECTURE.md) - 아키텍처 설명
- [Stripe Docs](https://stripe.com/docs/api)
- [Lemon Squeezy Docs](https://docs.lemonsqueezy.com/)

## 💬 도움이 필요하면

- Discord: https://discord.gg/openclaw
- Email: support@ubik.systems
- GitHub Issues: (곧 공개)

---

**Happy coding! 🚀**
