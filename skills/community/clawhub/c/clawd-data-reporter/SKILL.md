---
name: data-reporter
description: "Automated data reporting and dashboard generation. Connect to databases, APIs, spreadsheets. Generate PDF/PPT/Excel reports with charts. Schedule daily/weekly/monthly reports. Send via email, Slack, Teams. Perfect for business intelligence, KPI tracking, financial reporting. Save 20+ hours per month on manual reporting."
homepage: https://clawhub.com/skills/data-reporter
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["openclaw", "curl", "jq"]
    tags: ["data", "reports", "bi", "automation", "dashboards"]
---

# Data Reporter Skill

**Automate all your reports. Never manually copy-paste again.**

## When to Use

✅ **USE this skill when:**

- "Generate daily sales report and email it to execs"
- "Create weekly KPI dashboard for my team"
- "Pull data from 5 sources and combine into single Excel"
- "Send monthly financials to board with charts"
- "Update Google Data Studio / Looker Studio daily"
- "Create PowerPoint deck for client meetings"
- "Track metrics and alert on anomalies"

## When NOT to Use

❌ **DON'T use this skill when:**

- One-time ad-hoc analysis (use Excel manually)
- Deep statistical modeling (needs specialized tools)
- Real-time streaming dashboards (different architecture)

## 💰 ROI: The Report Time Killer

**Manual reporting pain**:
- Daily sales report: 2 hours/day = 40 hours/month → **$2,400**
- Weekly KPI deck: 4 hours/week = 16 hours/month → **$960**
- Monthly financials: 8 hours/month → **$480**
- **Total: 64 hours/month = $3,840** wasted on copy-paste

**Our cost**: $20-60/month
**Payback**: 2 days

## Data Sources

### Databases
| Database | Status | Notes |
|----------|--------|-------|
| PostgreSQL | ✅ | Native connection |
| MySQL / MariaDB | ✅ | Native |
| SQLite | ✅ | Native |
| MongoDB | ✅ | Via connection string |
| BigQuery | ✅ | Google service account |
| Snowflake | ✅ | Key pair auth |
| Redshift | ✅ | PostgreSQL compatible |
| Microsoft SQL Server | ✅ | |
| Oracle | ✅ | |
| ClickHouse | ✅ | |
| Supabase | ✅ | Postgres wrapper |

### APIs & SaaS
| Service | What you can pull | Status |
|---------|-------------------|--------|
| Google Analytics | Traffic, conversions | ✅ |
| Google Search Console | SEO data | ✅ |
| HubSpot | CRM, deals, contacts | ✅ |
| Salesforce | Opportunities, forecasts | ✅ |
| Stripe | Payments, subscriptions | ✅ |
| Shopify | Orders, customers, products | ✅ |
| WooCommerce | Sales, inventory | ✅ |
| Amazon SP-API | Sales, inventory, ads | ✅ |
| Meta Ads | Campaign performance | ✅ |
| Google Ads | Campaign metrics | ✅ |
| LinkedIn Ads | Campaign stats | ✅ |
| TikTok Ads | Performance data | ✅ |
| Mailchimp | Campaigns, subscribers | ✅ |
| SendGrid | Email stats | ✅ |
| Intercom | Conversations, users | ✅ |
| Zendesk | Tickets, satisfaction | ✅ |
| Airtable | Table data | ✅ |
| Notion | Database exports | ✅ |
| Google Sheets | Direct read/write | ✅ |
| Microsoft Excel (Office 365) | Direct access | ✅ |
| Generic REST API | Any JSON/CSV | ✅ |
| GraphQL | Any schema | ✅ |

### Files & Storage
| Source | Format | Status |
|--------|--------|--------|
| Local files | CSV, Excel, JSON, XML | ✅ |
| SFTP / FTP | Pull remote files | ✅ |
| Google Drive | Sheets, Docs, CSV | ✅ |
| Dropbox | Files, folders | ✅ |
| OneDrive | Office files | ✅ |
| S3 buckets | Any object storage | ✅ |
| Azure Blob | Blob storage | ✅ |
| GCS buckets | Cloud storage | ✅ |

---

## Quick Start: Daily Sales Report

### 1. Define Your Report

Create `sales-report.yaml`:

```yaml
report:
  name: "Daily Sales Dashboard"
  schedule: "0 7 * * *"  # 7 AM daily

  data_sources:
    - name: "Shopify Orders"
      type: "shopify"
      config:
        api_key: "..."
        store: "your-store.myshopify.com"
      query: |
        date >= yesterday()
        status: "fulfilled"

    - name: "Stripe Payments"
      type: "stripe"
      config:
        api_key: "..."
      query: |
        created >= 24h ago
        status: "succeeded"

    - name: "Google Analytics"
      type: "google_analytics"
      config:
        view_id: "123456"
        credentials: "ga-credentials.json"
      metrics:
        - sessions
        - revenue
        - conversion_rate

  transformations:
    - join:
        on: "date, product_sku"
        sources: ["shopify", "stripe", "ga"]
        output: "combined_metrics"

    - calculate:
        formulas:
          gross_revenue: "stripe.amount + shopify.total"
          avg_order_value: "gross_revenue / shopify.order_count"
          margin: "gross_revenue - shopify.cost_of_goods"

  outputs:
    - format: "pdf"
      template: "templates/daily-sales.html"
      email:
        to: ["exec@company.com", "sales@company.com"]
        subject: "Daily Sales Report {{date}}"
        body: "Attached is yesterday's sales performance..."

    - format: "excel"
      file: "reports/daily-sales-{{date}}.xlsx"
      sheets:
        - "Summary" (aggregated metrics)
        - "Orders" (raw data)
        - "Trends" (7-day chart)

    - format: "slack"
      channel: "#sales-reports"
      blocks:
        - header: "📊 Daily Sales {{date}}"
        - metric: "Revenue: ${{gross_revenue}}"
        - metric: "Orders: {{order_count}}"
        - metric: "AOV: ${{avg_order_value}}"
        - chart: "7-day revenue trend"

  alerts:
    - if: "gross_revenue < 10000"
      action: "send_alert"
      to: ["vpsales@company.com"]
      message: "🚨 Sales below threshold: ${{gross_revenue}}"
    - if: "order_count < 50"
      action: "send_alert"
      to: ["ops@company.com"]
      message: "⚠️ Low order volume: {{order_count}}"
```

### 2. Run It

```bash
# Test with sample data
clawhub workflow test sales-report --date 2026-03-16

# Run now
clawhub workflow run sales-report

# Schedule it
clawhub workflow schedule sales-report

# Check last run
clawhub workflow runs sales-report --limit 1
```

### 3. View Output

Check email, Slack channel, or `reports/` folder for generated files.

---

## Report Types

### Type 1: Executive Dashboards

**For C-suite / board meetings**:
```yaml
exec_dashboard:
  frequency: "weekly (Mon 8 AM)"
  data: ["revenue", "growth_rate", "cash_balance", "headcount", "churn"]
  format: ["pdf", "powerpoint"]
  style: "corporate_template.pptx"
  distribution: ["board@company.com", "investors@company.com"]
```

### Type 2: Operational Reports

**For daily team syncs**:
```yaml
ops_report:
  frequency: "daily (7 AM)"
  data: ["orders", "fulfillment_rate", "support_tickets", "inventory"]
  format: ["slack", "email", "google_sheets"]
  distribution: ["team@company.com", "#ops"]
```

### Type 3: Marketing Performance

**Campaign tracking**:
```yaml
marketing_report:
  frequency: "weekly (Tue 9 AM)"
  data_sources:
    - google_ads
    - meta_ads
    - linkedin_ads
    - google_analytics
  metrics:
    - spend, impressions, clicks, conversions, cpc, cpa, roas
  visualizations:
    - "Spend vs. conversions (campaign breakdown)"
    - "ROAS by channel"
    - "Conversion funnel"
  format: ["google_slides", "email"]
```

### Type 4: Financial Statements

**Monthly close**:
```yaml
financials:
  frequency: "monthly (3rd business day)"
  data_sources:
    - quickbooks
    - stripe
    - bank_accounts
  outputs:
    - income_statement
    - balance_sheet
    - cash_flow
    - kpi_dashboard
  format: "excel (book with formulas)"
  security: "encrypt with password"
```

---

## Advanced Features

### Dynamic Date Ranges

```yaml
date_range:
  relative: "last_7_days"  # last_week, month_to_date, quarter_to_date
  or:
    start: "2025-01-01"
    end: "2025-03-31"

  auto_adjust:
    weekdays_only: true  # Skip weekends for B2B
    business_days: true
```

### Multi-Tenant Reports

**White-label for agencies**:

```yaml
client_report:
  client: "Acme Corp"
  branding:
    logo: "clients/acme/logo.png"
    colors: ["#003366", "#FF6600"]
    footer: "Confidential - Acme Corp"

  data_sources:
    - type: "google_analytics"
      view: "Acme Website"
    - type: "shopify"
      store: "acme.myshopify.com"

  delivery:
    email:
      to: "marketing@acme.com"
      from: "reports@youragency.com"
    cc: "account-manager@youragency.com"
```

### Real-Time Dashboards

**Live metrics** (refreshes hourly):

```yaml
live_dashboard:
  refresh_interval: "1h"
  visualizations:
    - metric_cards: ["revenue_today", "orders_today", "visitors_now"]
    - line_chart: "revenue_last_24h (15-min intervals)"
    - bar_chart: "top_products_today"
  publish_to:
    - google_sheets: "Live Dashboard"
    - public_url: "https://yourdomain.com/dashboard/abc123"
```

### Alerting on Anomalies

```yaml
anomaly_detection:
  metrics: ["daily_revenue", "new_users", "conversion_rate"]
  algorithm: "statistical (3-sigma)"  # or "ML", "moving_average"
  lookback_period: "30 days"
  sensitivity: "medium"

  when_anomaly:
    - slack_alert: "#data-alerts"
    - email: "data-team@company.com"
    - create_ticket: "jira"  # Auto-create investigation task

  include:
    - current_value
    - expected_range
    - historical_context
    - suggested_investigation_steps
```

---

## Template Library

### Monthly Revenue Report

`templates/monthly-revenue.yaml`:
- P&L by product line
- CAC/LTV calculations
- Cohort analysis
- Full Excel export with formulas

### Weekly Marketing Report

`templates/weekly-marketing.yaml`:
- Channel performance table
- Funnel visualization
- Creative performance
- Budget vs. actual

### Daily Operations

`templates/daily-ops.yaml`:
- Production metrics
- Quality control
- Inventory levels
- Staffing needs

---

## Integrations

### BI Tools

Export to any dashboard tool:
```yaml
export:
  google_data_studio:
    dataset: "company_metrics"
    refresh: "every 6 hours"

  tableau:
    extract: "hyper file"
    publish_to: "tableau_server/site"
```

### Notification Channels

| Channel | Use Case | Setup |
|---------|----------|-------|
| Email | Exec reports | SMTP or Gmail |
| Slack | Team alerts | Webhook |
| Microsoft Teams | Enterprise | Incoming webhook |
| Discord | Community | Webhook |
| Telegram | Mobile alerts | Bot token |
| SMS / Twilio | Urgent alerts | Account SID |
| PagerDuty | Critical issues | REST API |
| Webhook | Custom systems | POST JSON |

---

## Pricing Strategy

### Tiers

**Free** (lead gen):
- 3 reports max
- 1 data source per report
- Email delivery only
- Community support

**Pro** ($29/mo):
- 50 reports
- 10 data sources/report
- All output formats
- 14-day data retention
- Email support
→ **Target: small businesses, startups**

**Business** ($99/mo):
- Unlimited reports
- Unlimited sources
- Real-time dashboards
- White-label PDFs
- Alerting
- Priority support
→ **Target: mid-market, agencies**

**Enterprise** ($499+/mo):
- Custom connectors
- Audit logs / SOC2
- SSO / SAML
- Dedicated engineer
- SLA guarantees
→ **Target: Fortune 1000**

---

## Competitive Edge

| Competitor | Price | Limits | Our Advantage |
|------------|-------|--------|---------------|
| Google Data Studio | Free | None, but manual | **Automation** |
| Tableau | $70+/user/mo | Complex | **Simple**, cheaper |
| Power BI | $10+/user/mo | Manual refresh | **Fully automated** |
| Stitch + Looker | $500+/mo | Pipe + viz separate | **All-in-one** |
| Custom dev agency | $10k+ project | One-off | **Recurring, self-serve** |

---

## Next Steps

1. ✅ Build skill skeleton
2. [ ] Add more data connectors (user requests)
3. [ ] Create template gallery (gallery/)
4. [ ] Build landing page with ROI calculator
5. [ ] Offer 30-day trial (credit card not required)
6. [ ] Beta program (10 companies free for 3 months)
7. [ ] Launch on ClawHub
8. [ ] Collect case studies → social proof

---

_Data reporting, automated. Spend time on insights, not formatting._ 📈
