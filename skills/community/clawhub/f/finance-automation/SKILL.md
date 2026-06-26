# Finance Automation

Automate payments, invoices, expenses, and financial reports.

## Features
- **Payments**: Real-time payment recording via Stripe/Lemon Squeezy webhooks
- **Invoices**: CRUD with auto-numbering, tax calculation, send/paid status management
- **Expenses**: Submit, approve, reject expenses with category analytics
- **Reports**: Daily/monthly revenue, MRR, profit reports
- **Notifications**: Real-time Telegram alerts

## Quick Start
```bash
cd finance-automation
cp .env.example .env
# Edit .env with your API keys
npm install
npm run db:init
npm run dev
```

## API Endpoints
```
POST   /api/invoices              Create invoice
GET    /api/invoices              List invoices
POST   /api/invoices/:id/send     Send invoice
POST   /api/invoices/:id/mark-paid Mark as paid

POST   /api/expenses              Add expense
POST   /api/expenses/:id/approve  Approve expense
POST   /api/expenses/:id/reject   Reject expense

GET    /api/reports/daily          Daily revenue + expenses
GET    /api/reports/monthly        Monthly report
GET    /api/reports/summary        Period summary
GET    /api/reports/mrr            Monthly Recurring Revenue
GET    /api/reports/profit         Profit report
```

## Requirements
- Node.js >= 18
- SQLite3 (default) or PostgreSQL
- Stripe account (for payment webhooks)

## Tags
finance, payment, invoice, expense, report, stripe, automation
