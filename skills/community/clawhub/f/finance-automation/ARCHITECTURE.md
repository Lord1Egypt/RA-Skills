# Finance Automation Skill - Architecture

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                     External Services                        │
├─────────────────────────────────────────────────────────────┤
│  Stripe API  │  Lemon Squeezy  │  Email SMTP  │  Telegram  │
└────────┬─────────────┬──────────────┬──────────────┬────────┘
         │             │              │              │
         │ Webhooks    │ Webhooks     │              │
         │             │              │              │
         v             v              v              v
┌─────────────────────────────────────────────────────────────┐
│                    Express.js Server                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Webhooks   │  │     API      │  │    Cron      │      │
│  │   Handler    │  │   Endpoints  │  │    Jobs      │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         v                  v                  v              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Service Layer                           │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │ Payment │ Invoice │ Expense │ Report │ Notification │    │
│  └────┬────────┬────────┬────────┬────────┬────────────┘    │
│       │        │        │        │        │                  │
│       v        v        v        v        v                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Data Layer                              │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │  Payment Model │ Invoice Model │ Expense Model      │    │
│  └────┬──────────────────┬──────────────────┬──────────┘    │
│       │                  │                  │                │
│       v                  v                  v                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           SQLite / PostgreSQL Database              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## 데이터베이스 스키마

### payments 테이블

```sql
CREATE TABLE payments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  external_id VARCHAR(255) UNIQUE NOT NULL,  -- Stripe/LS ID
  provider VARCHAR(50) NOT NULL,             -- 'stripe' | 'lemon_squeezy'
  customer_email VARCHAR(255),
  customer_name VARCHAR(255),
  amount INTEGER NOT NULL,                   -- cents
  currency VARCHAR(3) DEFAULT 'KRW',
  status VARCHAR(50) NOT NULL,               -- 'succeeded' | 'failed' | 'pending'
  description TEXT,
  metadata JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_provider ON payments(provider);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_created ON payments(created_at);
```

### invoices 테이블

```sql
CREATE TABLE invoices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  invoice_number VARCHAR(50) UNIQUE NOT NULL,
  customer_name VARCHAR(255) NOT NULL,
  customer_email VARCHAR(255) NOT NULL,
  customer_business_number VARCHAR(50),
  customer_address TEXT,
  
  subtotal INTEGER NOT NULL,                 -- cents
  tax_rate DECIMAL(5,2) DEFAULT 10.0,        -- VAT %
  tax_amount INTEGER NOT NULL,               -- cents
  total INTEGER NOT NULL,                    -- cents
  currency VARCHAR(3) DEFAULT 'KRW',
  
  status VARCHAR(50) DEFAULT 'draft',        -- 'draft' | 'sent' | 'paid' | 'overdue'
  issue_date DATE NOT NULL,
  due_date DATE NOT NULL,
  paid_date DATE,
  
  pdf_path VARCHAR(255),
  sent_at DATETIME,
  
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoice_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  invoice_id INTEGER NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  quantity INTEGER DEFAULT 1,
  unit_price INTEGER NOT NULL,              -- cents
  total INTEGER NOT NULL,                   -- cents
  FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
);

CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_customer ON invoices(customer_email);
CREATE INDEX idx_invoices_due_date ON invoices(due_date);
```

### expenses 테이블

```sql
CREATE TABLE expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amount INTEGER NOT NULL,                   -- cents
  currency VARCHAR(3) DEFAULT 'KRW',
  category VARCHAR(50) NOT NULL,             -- 'office' | 'travel' | 'software' | etc.
  subcategory VARCHAR(50),
  description TEXT NOT NULL,
  vendor VARCHAR(255),
  
  expense_date DATE NOT NULL,
  receipt_path VARCHAR(255),
  receipt_ocr_text TEXT,
  
  status VARCHAR(50) DEFAULT 'pending',      -- 'pending' | 'approved' | 'rejected'
  approved_by VARCHAR(255),
  approved_at DATETIME,
  
  tags JSON,
  metadata JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_expenses_category ON expenses(category);
CREATE INDEX idx_expenses_date ON expenses(expense_date);
CREATE INDEX idx_expenses_status ON expenses(status);
```

### subscriptions 테이블

```sql
CREATE TABLE subscriptions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  external_id VARCHAR(255) UNIQUE NOT NULL,
  provider VARCHAR(50) NOT NULL,
  customer_email VARCHAR(255) NOT NULL,
  customer_name VARCHAR(255),
  
  plan_name VARCHAR(255) NOT NULL,
  amount INTEGER NOT NULL,                   -- cents
  currency VARCHAR(3) DEFAULT 'KRW',
  interval VARCHAR(20) NOT NULL,             -- 'month' | 'year'
  
  status VARCHAR(50) NOT NULL,               -- 'active' | 'cancelled' | 'past_due'
  current_period_start DATE,
  current_period_end DATE,
  cancel_at DATE,
  cancelled_at DATE,
  
  metadata JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_customer ON subscriptions(customer_email);
```

## API 엔드포인트

### Webhook Endpoints

```
POST /webhook/stripe
POST /webhook/lemon-squeezy
```

### REST API

```
# Payments
GET    /api/payments              # 결제 목록
GET    /api/payments/:id          # 결제 상세
GET    /api/payments/stats        # 통계

# Invoices
GET    /api/invoices              # 인보이스 목록
POST   /api/invoices              # 인보이스 생성
GET    /api/invoices/:id          # 인보이스 상세
PUT    /api/invoices/:id          # 인보이스 수정
DELETE /api/invoices/:id          # 인보이스 삭제
POST   /api/invoices/:id/send     # 인보이스 발송
GET    /api/invoices/:id/pdf      # PDF 다운로드

# Expenses
GET    /api/expenses              # 경비 목록
POST   /api/expenses              # 경비 추가
GET    /api/expenses/:id          # 경비 상세
PUT    /api/expenses/:id          # 경비 수정
DELETE /api/expenses/:id          # 경비 삭제
POST   /api/expenses/:id/approve  # 경비 승인

# Reports
GET    /api/reports/daily         # 일일 리포트
GET    /api/reports/weekly        # 주간 리포트
GET    /api/reports/monthly       # 월간 리포트
GET    /api/reports/mrr           # MRR
GET    /api/reports/churn         # Churn Rate
```

## 이벤트 흐름

### 결제 성공 시

```
1. Stripe/LS Webhook → Express Server
2. Webhook Handler → Payment Service
3. Payment Service → Database (저장)
4. Payment Service → Notification Service
5. Notification Service → Telegram (알림)
6. (선택) Invoice Service → 인보이스 자동 생성
```

### 인보이스 생성 시

```
1. API Request → Invoice Service
2. Invoice Service → Database (저장)
3. Invoice Service → PDF Service
4. PDF Service → PDF 파일 생성
5. Invoice Service → Email Service
6. Email Service → 고객에게 이메일 발송
7. Notification Service → Telegram (알림)
```

### 경비 추가 시

```
1. API Request → Expense Service
2. (선택) OCR Service → 영수증 텍스트 추출
3. Expense Service → AI 카테고리 분류
4. Expense Service → Database (저장)
5. Notification Service → Telegram (알림)
```

## 보안

### Webhook 검증

**Stripe:**
```javascript
const sig = req.headers['stripe-signature'];
const event = stripe.webhooks.constructEvent(
  req.body,
  sig,
  process.env.STRIPE_WEBHOOK_SECRET
);
```

**Lemon Squeezy:**
```javascript
const signature = req.headers['x-signature'];
const payload = JSON.stringify(req.body);
const hash = crypto
  .createHmac('sha256', process.env.LEMON_SQUEEZY_WEBHOOK_SECRET)
  .update(payload)
  .digest('hex');

if (signature !== hash) {
  throw new Error('Invalid signature');
}
```

### API 인증

```javascript
// JWT 기반 인증
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
  const token = req.headers['authorization']?.split(' ')[1];
  if (!token) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

// 사용
app.get('/api/payments', authenticateToken, getPayments);
```

## 성능 최적화

### 데이터베이스 인덱스

```sql
-- 자주 조회되는 필드에 인덱스
CREATE INDEX idx_payments_created ON payments(created_at);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_expenses_date ON expenses(expense_date);
```

### 캐싱

```javascript
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 }); // 10분

async function getMonthlyReport(month) {
  const cacheKey = `report:${month}`;
  
  // 캐시 체크
  const cached = cache.get(cacheKey);
  if (cached) return cached;
  
  // 계산
  const report = await calculateReport(month);
  
  // 캐시 저장
  cache.set(cacheKey, report);
  
  return report;
}
```

### Webhook 비동기 처리

```javascript
// Queue를 사용해서 Webhook 처리
const Queue = require('bull');
const webhookQueue = new Queue('webhooks');

// Webhook 수신
app.post('/webhook/stripe', async (req, res) => {
  // 빠르게 응답
  res.sendStatus(200);
  
  // 큐에 추가 (비동기 처리)
  await webhookQueue.add({
    provider: 'stripe',
    event: req.body
  });
});

// Worker에서 처리
webhookQueue.process(async (job) => {
  await processWebhook(job.data);
});
```

## 에러 처리

```javascript
class PaymentError extends Error {
  constructor(message, code, details) {
    super(message);
    this.name = 'PaymentError';
    this.code = code;
    this.details = details;
  }
}

// 사용
try {
  await processPayment(paymentData);
} catch (error) {
  if (error instanceof PaymentError) {
    // 알려진 에러
    logger.warn('Payment failed', { code: error.code, details: error.details });
    await notifyAdmin('Payment failed', error);
  } else {
    // 예상치 못한 에러
    logger.error('Unexpected error', error);
    await notifyAdmin('Critical error', error);
  }
}
```

## 모니터링

### Logging

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// 사용
logger.info('Payment processed', { paymentId: payment.id, amount: payment.amount });
```

### Metrics

```javascript
// Prometheus metrics
const promClient = require('prom-client');

const paymentsTotal = new promClient.Counter({
  name: 'payments_total',
  help: 'Total number of payments',
  labelNames: ['status', 'provider']
});

// 사용
paymentsTotal.inc({ status: 'succeeded', provider: 'stripe' });
```

## 배포 아키텍처

### 프로덕션 환경

```
┌──────────────┐
│   Cloudflare │  ← HTTPS, DDoS Protection
└──────┬───────┘
       │
       v
┌──────────────┐
│   Load       │  ← Nginx / Caddy
│   Balancer   │
└──────┬───────┘
       │
       ├─────────┐
       v         v
┌──────────┐ ┌──────────┐
│  Node.js │ │  Node.js │  ← Express Servers
│  Server  │ │  Server  │
└────┬─────┘ └────┬─────┘
     │            │
     └────┬───────┘
          v
    ┌──────────┐
    │PostgreSQL│  ← Primary Database
    └──────────┘
```

## 스케일링 전략

1. **Horizontal Scaling**: 여러 Node.js 인스턴스 실행
2. **Database Replication**: Read Replica 추가
3. **Caching**: Redis 추가
4. **Queue**: Bull Queue로 백그라운드 작업 처리
5. **CDN**: 정적 파일 (PDF) CDN 사용
