---
name: fibek-collections
description: Interact with the Fibek B2B collections platform API — manage invoices, clients, payment agreements, campaigns, and financial metrics
---

# Fibek Collections Skill

Interact with the Fibek B2B collections platform API. Authenticate users, query invoices, manage clients, create payment agreements, and monitor financial metrics.

Environment variable required: `FIBEK_BASE_URL`

## Authentication

**Each user logs in with their own account. No pre-configured credentials.**

1. On first message, if no token stored, respond: "¡Hola! Para comenzar necesito que inicies sesión o te registres. ¿Ya tienes cuenta en Fibek o quieres registrarte?" Do NOT process other requests until authenticated.
2. If token exists, verify with `GET /user/me` and greet by name.

**Login**: Ask email + password → `POST /auth/login` body `{"email":"...", "password":"..."}` → response: `{success, token, expiresAt, user: {id, email, names, lastnames, companyId, roles[]}, error?, message?}`. On success, store token and greet by `user.names`. Do NOT mention `companyId` or say the company name is missing — just greet naturally by name. On failure, show `message` and ask to retry. Error codes: `INVALID_CREDENTIALS`, `USER_NOT_FOUND`, `NO_COMPANY`, `USER_DISABLED`.

**Registro**: Guide step by step in this exact order:
1. Ask: empresa, nombre, apellido
2. Ask: email y celular
3. Verify email: call `POST /auth/send/verification-code` body `{"email":"..."}` → tell user a code was sent to their email → ask for the 6-digit code → call `POST /auth/check/verification-code` body `{"email":"...", "code":"..."}` → if false, ask to retry
4. Ask: contraseña (min 6 characters)
5. Register: `POST /auth/user/by/phone` body `{"companyName":"...", "email":"...", "password":"...", "phone":"...", "names":"...", "lastnames":"..."}` → response: `{success}`. Then auto-login with `POST /auth/login`.

Do NOT call registration without verifying the email code first.

**Logout**: Discard token, ask new credentials. **Re-auth**: On 401, ask credentials again.

**Important**: Never expose internal API details to the user. If the API response is missing a field (like company name), do NOT mention it — just continue naturally with what you have. The user should never know about missing fields or internal IDs.

Token header: `Authorization: Bearer ${TOKEN}` (JWT, 5-year validity)

## Endpoints

### Invoices
- `GET /invoices?companyRelationshipId={id}&status=open` — list invoices
- `GET /invoices/summary` — invoice summary
- `POST /invoices/sendPaymentReminder` — body: `{invoiceIds[], relationshipId, communicationChannels[]}` (channels: EMAIL, WHATSAPP; optional: contactId)
- `POST /invoices/sendAccountStatement` — body: `{clientId, communicationChannels[]}` (channels: EMAIL, WHATSAPP; optional: contactId)
- `GET /invoices/{invoiceId}/system-actions` — invoice history

### Clients
- `GET /companies/clients-with-contacts?searchValue={query}` — search by name/NIT
- `GET /companies/relationships/{relationshipId}` — client details
- `GET /companies/relationships/unique-classifications` — classifications

### Monitoring
- `GET /monitoring/clients-summary` — filters: `search`, `limit`, `offset`, `invoiceStatusFilter` (all/open/open_with_due/due_soon), `dueSoonDays`, `minDaysPastDue`, `actionFilter`, `actionPeriodDays`, `onlyOpenInvoices`
- `GET /monitoring/summary` — monitoring summary
- `GET /monitoring/{clientId}/actions` — client actions

### Aging Analysis
- `GET /companies/relationships/metrics/clients-with-due-categories` — clients with aging buckets (onTime, days1_15, days16_30, days31_60, days61_90, days90Plus). Each has `totalPendingAmount`, `earliestDueDate`, `dueCategories[]`. Sort: `sortBy` (buyerName/totalPendingAmount/days1_15/etc), `sortOrder` (ASC/DESC). Filter: `limit`, `name`, `nit`, `status`, `relationshipIds[]`
- `GET /companies/relationships/metrics/strategy-kpi-quarter` — per-client quarterly KPIs (sales, collections, DSO, delinquency). Sort: `sortBy` (quarterSales/quarterCollections/quarterDso/delinquencyRate/etc), `sortOrder`. Filter: `relationshipIds[]`, `name`, `nit`
- `GET /companies/relationships/metrics/strategy-kpi-month` — same, monthly
- `GET /companies/relationships/metrics/strategy-kpi-week` — same, weekly

### Financial Metrics
- `GET /financial-metrics` — required: `level` (general/client/segment), `metrics[]`, `startDate`, `endDate`. Metrics: `portfolio_days_dso`, `credit_sales`, `collection_amount`, `collection_effectiveness`, `delinquency_indicator`, `average_portfolio`, `weighted_due_days`, `portfolio_ageing`, `credit_limit_utilization`, `term_dso_ratio`, `dso_term_difference`. Optional: `relationshipIds[]`, `sortBy`, `sortOrder`, `limit`
- `GET /financial-metrics/comparison` — required: `level`, `metric` (single), `startDates[]`, `endDates[]`, `labels[]`. Returns period comparison with deltas.
- `GET /financial-metrics/historical` — required: `level`, `metric`, `granularity` (daily/weekly/monthly/quarterly/yearly), `periodsBack`
- `GET /financial-metrics/metadata` — available metrics info

### Payments
- `GET /account-receivables/payments` — filter: `accountReceivableId`, `page`, `limit`. Returns: receiptDate, paymentMethod, totalAmount, currency
- `GET /account-receivables/payments/{id}` — payment detail

### Payment Agreements
- `GET /payment-agreements` — filter: `status` (ACTIVE/COMPLETED/CANCELLED), `upcoming=true&daysAhead=7`, `companyRelationshipId`, `searchTerm`, `page`, `limit`
- `GET /payment-agreements/by-client` — filter: `period` (week/month), `status`, `clientId`
- `GET /payment-agreements/summary`
- `GET /payment-agreements/preview-association?totalAmount={n}&companyRelationshipId={id}`
- `GET /payment-agreements/overdue-schedules`
- `GET /payment-agreements/{id}/schedules`
- `GET /payment-agreements/{id}/payments`
- `POST /payment-agreements/{id}/send-reminder`
- `POST /payment-agreements` — required: `companyRelationshipId`, `description`, `totalAmount`, `currency`, `schedules[]` (each: `scheduledDate` required, `amount` or `percentage`, optional `notes`). Optional: `invoiceIds[]`, `invoices[]` ({invoiceId, amountIncluded?}), `autoRemindersEnabled`, `reminderDays`

### Dashboard Widgets
- `GET /widgets/delinquency-indicator`, `GET /widgets/collection-rate`, `GET /widgets/receivables-turnover`, `GET /widgets/weighted-due-days`
- `GET /agent-metrics/kpis`, `GET /agent-metrics/funnel`
- `GET /payment-agreement-metrics/active`, `GET /payment-agreement-metrics/adherence`
- `GET /collections-projection/summary`

### Campaigns
- `GET /campaigns`, `POST /campaigns`, `POST /campaign-execution/validate`, `POST /campaign-execution/{id}/execute`, `GET /campaign-analytics/runs/{runId}`, `GET /campaign-analytics/weekly-metrics`

## Flows

**US-01 Auth**: Ask login or register → authenticate → greet by name

**US-02 Cartera próxima**: "¿Qué vence esta semana?" → `GET /monitoring/clients-summary?invoiceStatusFilter=due_soon&dueSoonDays=7` + `GET .../metrics/clients-with-due-categories?sortBy=totalPendingAmount&sortOrder=DESC` → table: Cliente | Monto | Fecha

**US-03 Mayor deuda**: "¿Quién me debe más?" → `GET .../metrics/clients-with-due-categories?sortBy=totalPendingAmount&sortOrder=DESC&limit=10` → table with aging distribution. Follow-up "último pago": `GET .../strategy-kpi-quarter?relationshipIds[]={id}`

**US-04 Historial pagos**: "¿Último pago de [X]?" → search client → `GET .../strategy-kpi-quarter?relationshipIds[]={id}` + `GET /account-receivables/payments?accountReceivableId={id}`. Handle name ambiguity.

**US-05 DSO drill-down**: "¿Por qué está alto el DSO?" → `GET /financial-metrics?level=general&metrics[]=portfolio_days_dso` → `GET /financial-metrics/comparison?level=client&metric=portfolio_days_dso&sortOrder=desc&limit=5` (top 5 worst) → `GET /financial-metrics?metrics[]=credit_sales&metrics[]=collection_amount` → interpret in natural language. NEVER recalculate, only interpret API data.

**US-06 Comparación períodos**: "¿Ventas vs mes pasado?" → `GET /financial-metrics/comparison?level=general&metric=credit_sales` + `metric=collection_amount` → for client drop: `level=client&sortOrder=asc&limit=5` → present deltas absolute + %

**US-07 Crear promesa de pago**: Guided multi-step: 1) ¿Cliente? (search) 2) ¿Descripción? 3) ¿Monto y moneda? 4) ¿Facturas específicas o libre? 5) ¿Cuotas y fechas? 6) ¿Recordatorios? 7) Mostrar resumen, pedir confirmación 8) `POST /payment-agreements` 9) Ofrecer enviar recordatorio

**US-08 Estado de cuenta**: "Avísale a [X]" → search client → ask channel → `POST /invoices/sendAccountStatement` body `{clientId, communicationChannels}`

**US-09 Promesas activas**: "¿Acuerdos esta semana?" → `GET /payment-agreements?upcoming=true&daysAhead=7&status=ACTIVE` or `GET /payment-agreements/by-client?period=week` → table: Cliente | Monto | Fecha | Estado

**Dashboard**: Fetch delinquency, collection rate, monitoring summary, overdue schedules, projection in parallel.

## Swagger Discovery

For unlisted endpoints: `curl -s "${FIBEK_BASE_URL}/swagger/json" | jq '.paths | keys'`

## Response Format

Never show raw JSON. Never use markdown tables — they break on mobile. Instead, format lists as numbered blocks:

```
📋 **Título**

**1. Nombre del cliente**
• Monto: $2.450.000 COP
• Vence: 16 de mayo de 2026
• Facturas: 3 pendientes

**2. Otro cliente**
• Monto: $1.800.000 COP
• Vence: 18 de mayo de 2026
• Facturas: 2 pendientes
```

Additional formatting rules:
- Monetary: thousand separators + currency ($1.250.000 COP)
- Dates: human-readable (15 de mayo de 2026)
- Status: translate to Spanish (ACTIVE→Activo, OVERDUE→Vencido, PAID→Pagado)
- DSO/metrics: include units (52.3 días)

## Error Handling

- 401: Re-authenticate. 403: No permission. 404: Not found. 400: Bad params, check Swagger.
- Connection errors (ECONNREFUSED, timeout, network errors): Tell the user "Estamos teniendo problemas técnicos en este momento. Por favor intentá de nuevo en unos minutos." NEVER mention internal details like URLs, server names, Docker, localhost, ports, or infrastructure. The user is a client, not a developer.
