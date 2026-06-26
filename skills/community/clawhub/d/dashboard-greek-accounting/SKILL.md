---
name: dashboard-greek-accounting
description: Business intelligence dashboard for Greek accounting firms. Compliance status, alerts, deadline tracking, and financial metrics at a glance.
version: 1.0.0
author: openclaw-greek-accounting
homepage: https://github.com/satoshistackalotto/openclaw-greek-accounting
tags: ["greek", "accounting", "dashboard", "reporting", "compliance-scoring"]
metadata: {"openclaw": {"requires": {"bins": ["jq"], "env": ["OPENCLAW_DATA_DIR"]}, "optional_env": {"SLACK_WEBHOOK_URL": "Webhook URL for dashboard alert delivery to Slack", "SMTP_HOST": "Email server for alert notifications", "SMTP_USER": "Email account for sending alerts", "SMTP_PASSWORD": "Email account password", "SMS_GATEWAY_URL": "SMS gateway for urgent dashboard alerts (optional)", "GOOGLE_CALENDAR_ID": "Google Calendar ID for deadline calendar view (optional)"}, "notes": "Dashboard generation works locally with no credentials. Alert delivery channels (Slack, email) are optional — configure their env vars to enable. Unconfigured channels produce local file-based alerts only."}}
---

# Dashboard Greek Accounting

This skill transforms OpenClaw into a comprehensive accounting dashboard, providing English-language business intelligence for assistants managing Greek business clients. It aggregates data from all 10 existing skills into actionable views, alerts, and reports.


## Setup

```bash
export OPENCLAW_DATA_DIR="/data"
which jq || sudo apt install jq
```

No external credentials required. Generates text-based dashboard reports by reading data from local files in OPENCLAW_DATA_DIR.


## Core Philosophy

- **English Interface, Greek Data**: Dashboard in English, processing Greek business documents and regulations
- **Assistant-First Design**: Built for accountants assistants, not senior partners or IT staff
- **Real-Time Awareness**: Instant visibility into compliance status, deadlines, and client health
- **File-Based Processing**: Dashboard state managed through OpenClaw file system, no database required
- **Skill Integration Hub**: Pulls data from all existing skills into unified views
- **Production Ready**: Error handling, fallback displays, and graceful degradation

## OpenClaw Commands

### Dashboard Initialization & Configuration
```bash
# Initialize dashboard for accounting firm
openclaw dashboard init --firm-name "FIRM NAME" --language en --data-language el
openclaw dashboard configure --clients-dir /data/clients/ --reports-dir /data/reports/
openclaw dashboard set-preferences --timezone "Europe/Athens" --currency EUR --date-format DD/MM/YYYY

# User setup for assistants
openclaw dashboard add-user --name "Assistant Name" --role assistant --clients "CLIENT1,CLIENT2"
openclaw dashboard set-alerts --user "Assistant Name" --email  --urgency-threshold medium
openclaw dashboard set-working-hours --start 08:00 --end 18:00 --timezone "Europe/Athens"
```

### Daily Operations Dashboard
```bash
# Morning startup - comprehensive daily briefing
openclaw dashboard morning-briefing --date today --include-alerts --include-deadlines
openclaw dashboard daily-status --all-clients --highlight-urgent
openclaw dashboard task-queue --show-pending --show-overdue --prioritize

# Real-time monitoring
openclaw dashboard live-status --refresh 15min --alerts-only
openclaw dashboard compliance-check --all-clients --flag-issues
openclaw dashboard document-queue --unprocessed --awaiting-review --count

# End of day summary
openclaw dashboard eod-summary --completed-tasks --remaining-issues --tomorrow-preview
```

### Client Portfolio Dashboard
```bash
# Client overview and management
openclaw dashboard client-overview --client "CLIENT AE" --period current-month
openclaw dashboard client-health --all-clients --score --rank
openclaw dashboard client-alerts --client "CLIENT AE" --unresolved --history 30d

# Client financial snapshot
openclaw dashboard client-financials --client "CLIENT AE" --vat-status --payroll-status
openclaw dashboard client-documents --client "CLIENT AE" --pending --processed --missing
openclaw dashboard client-timeline --client "CLIENT AE" --upcoming-deadlines --past-filings

# Multi-client comparison
openclaw dashboard portfolio-summary --all-clients --compliance-score --risk-level
openclaw dashboard workload-analysis --by-client --by-task-type --estimated-hours
```

### Compliance & Deadline Dashboard
```bash
# Deadline monitoring integration
openclaw dashboard deadlines --upcoming 30d --by-client --by-type
openclaw dashboard deadline-calendar --month current --export-ical
openclaw dashboard deadline-risk --overdue --due-within 7d --missing-documents

# AADE compliance status
openclaw dashboard aade-status --vat-filings --mydata-submissions --system-health
openclaw dashboard aade-changes --recent --impact-assessment --action-required

# EFKA compliance status
openclaw dashboard efka-status --contributions --declarations --upcoming-deadlines
openclaw dashboard efka-employees --by-client --status-check --contribution-amounts

# Municipal & other compliance
openclaw dashboard municipal-status --property-taxes --local-fees --permit-renewals
openclaw dashboard compliance-scorecard --all-categories --trend --recommendations
```

### Financial Reporting Dashboard
```bash
# Revenue and billing reports
openclaw dashboard revenue-report --period monthly --by-client --by-service
openclaw dashboard billing-status --outstanding --overdue --payment-history
openclaw dashboard fee-tracking --billable-hours --fixed-fees --expenses

# VAT reporting
openclaw dashboard vat-summary --all-clients --current-period --comparison-previous
openclaw dashboard vat-reconciliation --client "CLIENT AE" --flag-discrepancies
openclaw dashboard vat-forecast --next-quarter --estimated-amounts

# Payroll overview
openclaw dashboard payroll-status --all-clients --current-month --cost-breakdown
openclaw dashboard payroll-calendar --upcoming-runs --contribution-deadlines
openclaw dashboard payroll-comparison --month-over-month --flag-anomalies

# Banking integration status
openclaw dashboard bank-feeds --all-clients --last-sync --unreconciled-count
openclaw dashboard bank-reconciliation --client "CLIENT AE" --status --discrepancies
openclaw dashboard cash-flow-overview --all-clients --current-month --trend
```

### Alert Management Dashboard
```bash
# Alert configuration
openclaw dashboard alert-rules --list --add --modify --delete
openclaw dashboard alert-channels --configure email,slack,sms --test  # Unconfigured channels skipped
openclaw dashboard alert-escalation --set-levels --timeout-minutes 60

# Alert monitoring
openclaw dashboard alerts --active --unacknowledged --critical-only
openclaw dashboard alert-history --last 7d --by-type --by-client
openclaw dashboard alert-acknowledge --alert-id {id} --note "Action taken"
openclaw dashboard alert-snooze --alert-id {id} --until "2026-03-01"

# Alert types and priorities
openclaw dashboard alert-types:
  # Priority: CRITICAL (immediate action required)
  - aade-deadline-missed          # Filing deadline has passed
  - aade-system-outage-critical   # Government system down near deadline
  - compliance-violation-detected  # Active compliance issue
  - bank-feed-authentication-failed # Banking connection lost
  
  # Priority: HIGH (action needed within 24 hours)
  - deadline-approaching-48h       # Deadline within 48 hours
  - document-missing-for-filing    # Required document not received
  - vat-discrepancy-detected       # VAT calculation mismatch
  - payroll-run-overdue            # Payroll not processed on time
  
  # Priority: MEDIUM (action needed within 1 week)
  - deadline-approaching-7d        # Deadline within 7 days
  - client-documents-pending       # Documents awaiting processing
  - bank-reconciliation-overdue    # Reconciliation not completed
  - efka-contribution-reminder     # Social security payment upcoming
  
  # Priority: LOW (informational)
  - aade-announcement-new          # New government announcement
  - document-processed-successfully # Successful processing confirmation
  - monthly-report-ready           # Automated report generated
  - system-maintenance-scheduled   # Planned maintenance window
```

### Report Generation Dashboard
```bash
# Automated report generation
openclaw dashboard generate-report --type daily-summary --format html --output /data/reports/
openclaw dashboard generate-report --type client-status --client "CLIENT AE" --format pdf
openclaw dashboard generate-report --type compliance-overview --all-clients --format xlsx
openclaw dashboard generate-report --type deadline-forecast --period 90d --format html

# Report scheduling
openclaw dashboard schedule-report --type daily-summary --time 08:00 --recipients "team@firm.gr"
openclaw dashboard schedule-report --type weekly-digest --day monday --time 09:00
openclaw dashboard schedule-report --type monthly-review --day 1 --time 10:00

# Report templates
openclaw dashboard report-templates --list
openclaw dashboard report-templates --create --name "Client Quarterly Review" --sections "financials,compliance,deadlines,recommendations"
openclaw dashboard report-templates --customize --template "Client Quarterly Review" --add-logo --add-footer
```

## Dashboard Data Architecture

### File-Based State Management
```yaml
Dashboard_File_Structure:
  config:
    - /data/dashboard/config/firm-settings.yaml
    - /data/dashboard/config/user-preferences.yaml
    - /data/dashboard/config/alert-rules.yaml
    - /data/dashboard/config/report-templates.yaml
    
  state:
    - /data/dashboard/state/current-alerts.json
    - /data/dashboard/state/client-status.json
    - /data/dashboard/state/deadline-tracker.json
    - /data/dashboard/state/task-queue.json
    - /data/dashboard/state/system-health.json
    
  cache:
    - /data/dashboard/cache/aade-latest.json
    - /data/dashboard/cache/efka-latest.json
    - /data/dashboard/cache/bank-feeds-latest.json
    - /data/dashboard/cache/ocr-queue-status.json
    
  reports:
    - /data/dashboard/reports/daily/
    - /data/dashboard/reports/weekly/
    - /data/dashboard/reports/monthly/
    - /data/dashboard/reports/client-specific/
    
  history:
    - /data/dashboard/history/alerts/
    - /data/dashboard/history/compliance-scores/
    - /data/dashboard/history/performance-metrics/
```

### Client Status Data Model
```yaml
Client_Status_Schema:
  client_id: "unique_identifier"
  legal_name_gr: "ΕΤΑΙΡΕΙΑ ΑΕ"
  legal_name_en: "COMPANY SA"
  afm: "123456789"
  doy: "Α' ΑθηνϽν"
  entity_type: "AE|EPE|OE|EE|IKE|sole_proprietor"
  
  compliance:
    overall_score: 95  # 0-100
    vat_status: "current|overdue|pending"
    income_tax_status: "current|overdue|pending"
    efka_status: "current|overdue|pending"
    mydata_status: "current|overdue|pending"
    enfia_status: "current|overdue|pending"
    
  deadlines:
    next_deadline: "2026-03-20"
    next_deadline_type: "VAT Return"
    overdue_count: 0
    upcoming_7d_count: 2
    upcoming_30d_count: 5
    
  documents:
    pending_processing: 3
    awaiting_review: 1
    missing_required: 0
    processed_this_month: 47
    
  financials:
    monthly_revenue: 125000.00
    monthly_vat_liability: 30000.00
    payroll_cost: 45000.00
    outstanding_receivables: 15000.00
    
  banking:
    last_sync: "2026-02-17T08:00:00"
    unreconciled_transactions: 5
    bank_connections_active: 2
    bank_connections_failed: 0
    
  risk_level: "low|medium|high|critical"
  last_updated: "2026-02-17T10:30:00"
  assigned_assistant: "Assistant Name"
```

### Alert Data Model
```yaml
Alert_Schema:
  alert_id: "ALT-2026-02-001"
  type: "deadline-approaching-48h"
  priority: "HIGH"
  client_id: "CLIENT_001"
  client_name_en: "COMPANY SA"
  
  message_en: "VAT return for COMPANY SA due in 48 hours"
  message_gr: "Υποβολή ΦΠΑ για ΕΤΑΙΡΕΙΑ ΑΕ σε 48 Ͻρεπš"
  
  details:
    deadline_date: "2026-02-19"
    filing_type: "F2 VAT Return"
    period: "January 2026"
    amount_due: 12500.00
    documents_ready: true
    submission_system: "myDATA"
    
  status: "active|acknowledged|snoozed|resolved"
  created_at: "2026-02-17T08:00:00"
  acknowledged_by: null
  resolved_at: null
  
  actions:
    - "Review VAT calculation"
    - "Verify supporting documents"
    - "Submit via myDATA portal"
    - "Confirm submission receipt"
```

## Skill Integration Architecture

### Data Flow from Existing Skills
```yaml
Skill_Integration_Map:
  accounting-workflows:
    provides:
      - document_processing_status
      - ocr_queue_metrics
      - data_entry_completion_rates
    dashboard_view: "Document Processing Queue"
    
  greek-compliance-aade:
    provides:
      - vat_calculation_status
      - payroll_processing_status
      - compliance_scores_per_client
    dashboard_view: "Compliance Overview"
    
  cli-deadline-monitor:
    provides:
      - upcoming_deadlines_by_client
      - overdue_items
      - deadline_tracker_data
    dashboard_view: "Deadline Tracker & Alerts"
    
  greek-email-processor:
    provides:
      - unprocessed_email_count
      - document_extraction_queue
      - client_communication_status
    dashboard_view: "Email & Communications"
    
  greek-individual-taxes:
    provides:
      - individual_tax_return_status
      - e1_form_progress
      - tax_calculation_summaries
    dashboard_view: "Individual Tax Returns"
    
  openclaw-greek-accounting-meta:
    provides:
      - orchestration_status
      - workflow_completion_rates
      - system_health_metrics
    dashboard_view: "System Overview"
    
  aade-api-monitor:
    provides:
      - government_system_status
      - regulatory_change_alerts
      - deadline_change_notifications
    dashboard_view: "Government Systems Status"
    
  greek-banking-integration:
    provides:
      - bank_feed_status_per_client
      - reconciliation_progress
      - transaction_import_metrics
    dashboard_view: "Banking & Reconciliation"
    
  greek-document-ocr:
    provides:
      - ocr_processing_queue
      - accuracy_metrics
      - greek_text_extraction_status
    dashboard_view: "OCR Processing Status"
    
  efka-api-integration:
    provides:
      - social_security_status
      - employee_contribution_tracking
      - declaration_submission_status
    dashboard_view: "EFKA Social Security"
```

### Dashboard Refresh Cycle
```yaml
Refresh_Schedule:
  real_time:  # Updated on every dashboard access
    - active_alerts
    - critical_deadlines
    - system_health
    
  frequent:   # Every 15 minutes
    - document_processing_queue
    - email_inbox_status
    - bank_feed_status
    
  periodic:   # Every hour
    - compliance_scores
    - client_status_overview
    - workload_metrics
    
  scheduled:  # Daily at configured times
    - daily_reports
    - deadline_tracker_update
    - performance_analytics
    
  on_demand:  # Triggered by user action
    - client_deep_dive
    - custom_reports
    - historical_analysis
```

## Dashboard Views (English Interface)

### 1. Morning Briefing View
```markdown
┌─────────────────────────────────────────────────────────â”
─š 🌅 MORNING BRIEFING - February 17, 2026               ─š
─š Good morning, [Assistant Name]                          ─š
├─────────────────────────────────────────────────────────┤
─š                                                         ─š
─š 🚨 CRITICAL ALERTS (2)                                 ─š
─š ├─ VAT Return overdue: ALPHA TRADING AE (was due 15/02)─š
─š └─ Bank feed disconnected: Eurobank - BETA SERVICES EPE─š
─š                                                         ─š
─š ⚠ï¸  TODAY'S DEADLINES (3)                              ─š
─š ├─ Submit payroll declaration: GAMMA TECH IKE           ─š
─š ├─ EFKA contribution payment: DELTA LOGISTICS OE       ─š
─š └─ myDATA monthly submission: EPSILON RETAIL AE        ─š
─š                                                         ─š
─š 📀¹ TASK QUEUE (12 items)                               ─š
─š ├─ 5 documents awaiting processing                     ─š
─š ├─ 3 bank reconciliations pending                      ─š
─š ├─ 2 client emails requiring response                  ─š
─š └─ 2 VAT calculations ready for review                 ─š
─š                                                         ─š
─š 📊 YESTERDAY'S SUMMARY                                 ─š
─š ├─ 23 documents processed (98% accuracy)               ─š
─š ├─ 4 filings submitted successfully                    ─š
─š ├─ 15 bank transactions reconciled                     ─š
─š └─ 0 deadlines missed ✅                               ─š
─š                                                         ─š
─š ðŸÂ¦ GOVERNMENT SYSTEMS STATUS                           ─š
─š ├─ TAXIS: ✅ Online                                    ─š
─š ├─ myDATA: ✅ Online                                   ─š
─š ├─ EFKA: ⚠ï¸ Slow (response >5s)                       ─š
─š └─ ENFIA: ✅ Online                                    ─š
└─────────────────────────────────────────────────────────┘
```

### 2. Client Portfolio View
```markdown
┌─────────────────────────────────────────────────────────────────────â”
─š 📊 CLIENT PORTFOLIO - All Clients                                  ─š
├──────────────────┬──────────┬───────────┬──────────┬───────────────┤
─š Client           ─š Health   ─š Deadlines ─š Docs     ─š Risk Level    ─š
├──────────────────┼──────────┼───────────┼──────────┼───────────────┤
─š ALPHA TRADING AE ─š 72/100   ─š 1 overdue ─š 3 pending─š 🔴 HIGH      ─š
─š BETA SERVICES EPE─š 85/100   ─š 2 in 7d   ─š 0 pending─š 🟡 MEDIUM   ─š
─š GAMMA TECH IKE   ─š 95/100   ─š 1 today   ─š 1 pending─š 🟢 LOW      ─š
─š DELTA LOGISTICS  ─š 91/100   ─š 1 today   ─š 0 pending─š 🟢 LOW      ─š
─š EPSILON RETAIL AE─š 88/100   ─š 1 today   ─š 2 pending─š 🟡 MEDIUM   ─š
─š ZETA CONSULTING  ─š 98/100   ─š 0 urgent  ─š 0 pending─š 🟢 LOW      ─š
├──────────────────┴──────────┴───────────┴──────────┴───────────────┤
─š Portfolio Health: 88/100 | Active Clients: 6 | Total Staff: 47    ─š
└─────────────────────────────────────────────────────────────────────┘
```

### 3. Compliance Scorecard View
```markdown
┌─────────────────────────────────────────────────────────────────────â”
─š ✅ COMPLIANCE SCORECARD - February 2026                            ─š
├──────────────────┬──────┬──────┬──────┬──────┬──────┬──────────────┤
─š Client           ─š VAT  ─š Tax  ─š EFKA ─š DATA ─š ENFIA─š Overall      ─š
├──────────────────┼──────┼──────┼──────┼──────┼──────┼──────────────┤
─š ALPHA TRADING AE ─š  âÂŒ  ─š  ✅  ─š  ✅  ─š  ⚠ï¸  ─š  ✅  ─š  72%        ─š
─š BETA SERVICES EPE─š  ✅  ─š  ✅  ─š  ⚠ï¸  ─š  ✅  ─š  ✅  ─š  85%        ─š
─š GAMMA TECH IKE   ─š  ✅  ─š  ✅  ─š  ✅  ─š  ✅  ─š  ✅  ─š  95%        ─š
─š DELTA LOGISTICS  ─š  ✅  ─š  ✅  ─š  ✅  ─š  ✅  ─š  ⚠ï¸  ─š  91%        ─š
─š EPSILON RETAIL AE─š  ✅  ─š  ✅  ─š  ✅  ─š  ⚠ï¸  ─š  ✅  ─š  88%        ─š
─š ZETA CONSULTING  ─š  ✅  ─š  ✅  ─š  ✅  ─š  ✅  ─š  ✅  ─š  98%        ─š
├──────────────────┴──────┴──────┴──────┴──────┴──────┴──────────────┤
─š ✅ = Current  ⚠ï¸ = Pending/Due Soon  âÂŒ = Overdue/Issue           ─š
─š Firm Average: 88% | National Average: 76% | Trend: †‘ improving    ─š
└─────────────────────────────────────────────────────────────────────┘
```

### 4. Deadline Tracker View
```markdown
┌─────────────────────────────────────────────────────────────────────â”
─š 📅 DEADLINE CALENDAR - February 2026                               ─š
├─────────┬───────────────────────────────────────────────────────────┤
─š Feb 17  ─š 🔴 Submit payroll: GAMMA TECH IKE                       ─š
─š (Today) ─š 🔴 EFKA payment: DELTA LOGISTICS OE                     ─š
─š         ─š 🔴 myDATA submit: EPSILON RETAIL AE                     ─š
├─────────┼───────────────────────────────────────────────────────────┤
─š Feb 20  ─š 🟡 VAT Return F2: BETA SERVICES EPE                    ─š
─š         ─š 🟡 VAT Return F2: GAMMA TECH IKE                       ─š
├─────────┼───────────────────────────────────────────────────────────┤
─š Feb 26  ─š 🟡 Monthly e-books submission: ALL CLIENTS              ─š
├─────────┼───────────────────────────────────────────────────────────┤
─š Feb 28  ─š ⚪ EFKA monthly declaration: ALL CLIENTS                ─š
─š         ─š ⚪ Withholding tax filing: ALPHA TRADING AE             ─š
├─────────┼───────────────────────────────────────────────────────────┤
─š Mar 05  ─š ⚪ Stamp duty quarterly: ZETA CONSULTING                ─š
├─────────┼───────────────────────────────────────────────────────────┤
─š Mar 15  ─š ⚪ Income tax advance: BETA SERVICES EPE                ─š
─š         ─š ⚪ Income tax advance: EPSILON RETAIL AE                ─š
├─────────┴───────────────────────────────────────────────────────────┤
─š 🔴 Due Today (3) | 🟡 Due This Week (2) | ⚪ Upcoming (5)        ─š
└─────────────────────────────────────────────────────────────────────┘
```

## Implementation Guidelines

### Dashboard Initialization Workflow
```yaml
Initialization_Steps:
  1_firm_setup:
    - Create dashboard directory structure
    - Configure firm-level settings (name, timezone, currency)
    - Set data source paths for existing skills
    - Verify all 10 skills are accessible
    
  2_client_import:
    - Scan existing client data from other skills
    - Build initial client status records
    - Calculate baseline compliance scores
    - Generate initial risk assessments
    
  3_user_configuration:
    - Create assistant user accounts
    - Assign clients to assistants
    - Configure alert preferences
    - Set working hours and notification schedules
    
  4_integration_verification:
    - Test data flow from each skill
    - Verify alert generation
    - Confirm report generation
    - Run end-to-end dashboard test
```

### Error Handling & Graceful Degradation
```yaml
Error_Handling:
  skill_unavailable:
    behavior: "Show cached data with 'last updated' timestamp"
    alert: "Dashboard data may be stale - [Skill Name] connection issue"
    fallback: "Display last known good state with warning indicator"
    
  data_inconsistency:
    behavior: "Flag inconsistent data with visual indicator"
    alert: "Data mismatch detected for [Client] - manual review needed"
    fallback: "Show both values with comparison indicator"
    
  government_system_down:
    behavior: "Show system status indicator, disable affected submissions"
    alert: "AADE/EFKA system unavailable - monitoring for recovery"
    fallback: "Queue submissions, show estimated retry time"
    
  file_system_error:
    behavior: "Attempt recovery from backup state files"
    alert: "Dashboard state recovery in progress"
    fallback: "Fresh rebuild from skill data sources"

  stale_data_thresholds:
    alerts: 5_minutes
    client_status: 1_hour
    compliance_scores: 4_hours
    financial_data: 24_hours
```

### Performance Optimization
```yaml
Performance_Strategy:
  caching:
    - Cache computed compliance scores (recalculate hourly)
    - Cache client health scores (recalculate on data change)
    - Cache deadline tracker (rebuild daily + on deadline changes)
    - Cache report templates (rebuild on template change)
    
  lazy_loading:
    - Load client details only when client selected
    - Load historical data only when requested
    - Load bank transaction details on drill-down
    - Generate reports only when requested or scheduled
    
  incremental_updates:
    - Update only changed client records
    - Append new alerts without rebuilding alert list
    - Update deadline tracker incrementally
    - Process document queue changes only
```

## Report Templates

### Daily Summary Report (HTML)
```yaml
Daily_Summary_Report:
  header:
    firm_name: "ACCOUNTING FIRM NAME"
    report_date: "February 17, 2026"
    generated_at: "08:00 Athens time"
    prepared_by: "OpenClaw Dashboard"
    
  sections:
    - critical_alerts:
        title: "Critical & High Priority Alerts"
        content: "List of unresolved critical/high alerts with action items"
        
    - deadline_overview:
        title: "Today's Deadlines & Upcoming 7 Days"
        content: "Calendar view of immediate deadlines by client"
        
    - client_status:
        title: "Client Portfolio Health"
        content: "Compliance scores, risk levels, key metrics per client"
        
    - document_processing:
        title: "Document Processing Summary"
        content: "Processed, pending, flagged documents from last 24 hours"
        
    - government_systems:
        title: "Government System Status"
        content: "AADE, EFKA, myDATA system availability and announcements"
        
    - action_items:
        title: "Today's Action Items"
        content: "Prioritized task list for assistants"
        
  footer:
    disclaimer: "Automated report - verify critical items manually"
    support: "Contact: support@firm.gr"
```

### Client Quarterly Review Report
```yaml
Client_Quarterly_Report:
  header:
    client_name: "CLIENT NAME AE"
    afm: "123456789"
    period: "Q1 2026 (January - March)"
    
  sections:
    - compliance_summary:
        title: "Compliance Performance"
        content: "Quarter compliance score trend, filings completed, issues resolved"
        
    - financial_overview:
        title: "Financial Summary"
        content: "Revenue, VAT, payroll costs, banking reconciliation status"
        
    - filing_history:
        title: "Filing & Submission History"
        content: "All filings made during quarter with dates and confirmation numbers"
        
    - deadline_performance:
        title: "Deadline Adherence"
        content: "On-time vs late filings, average days before deadline"
        
    - recommendations:
        title: "Recommendations"
        content: "Process improvements, compliance risks, upcoming changes"
```

## Greek Business Specifics

### Entity Type Dashboard Variations
```yaml
Entity_Type_Views:
  AE_SA:  # ΑνϽνυμη Επžαιρεία
    additional_fields:
      - board_meeting_deadlines
      - annual_general_assembly_date
      - GEMI_filing_status
      - auditor_appointment_status
    compliance_extras:
      - published_financial_statements
      - dividend_tax_calculations
      
  EPE_LLC:  # Επžαιρεία Περιορισμένηπš Ευθύνηπš
    additional_fields:
      - partner_meeting_deadlines
      - GEMI_filing_status
    compliance_extras:
      - profit_distribution_tracking
      
  IKE_PC:  # Ιδιπ°πžική Ρεπ αλαιουπ¡ική Επžαιρεία
    additional_fields:
      - annual_report_deadline
      - GEMI_filing_status
    compliance_extras:
      - simplified_compliance_view
      
  OE_EE_Partnership:  # θμςρρυθμη / Επžερςρρυθμη
    additional_fields:
      - partner_tax_obligations
      - partnership_agreement_renewal
    compliance_extras:
      - partner_individual_tax_integration
      
  Sole_Proprietor:  # Απžομική Επιπ¡είρηση
    additional_fields:
      - personal_tax_integration
      - simplified_books_status
    compliance_extras:
      - integrated_personal_business_view
```

### Greek Deadline Integration
```yaml
Greek_Calendar_Awareness:
  public_holidays:
    - "2026-01-01: Πρπ°πžοπ¡ρονιά (New Year's Day)"
    - "2026-01-06: Μεοπ άνεια (Epiphany)"
    - "2026-03-02: Ραθαρά Δευπžέρα (Clean Monday)"
    - "2026-03-25: Εθνική Εορπžή (Independence Day)"
    - "2026-04-17: Μεγάλη Παρασκευή (Good Friday - Orthodox)"
    - "2026-04-20: Πάσπ¡α (Easter Monday - Orthodox)"
    - "2026-05-01: Εργαπžική Πρπ°πžομαγιά (Labour Day)"
    - "2026-06-08: Αγίου Πνεύμαπžοπš (Whit Monday)"
    - "2026-08-15: Ροίμηση Μεοπžςκου (Assumption)"
    - "2026-10-28: Εθνική Εορπžή (Ohi Day)"
    - "2026-12-25: Χρισπžούγεννα (Christmas)"
    - "2026-12-26: Σύναξη Μεοπžςκου (Boxing Day)"
    
  impact_on_deadlines:
    - "Adjust filing deadlines that fall on holidays"
    - "Account for AADE/EFKA office closures"
    - "Display holiday warnings on deadline tracker"
    - "Factor in reduced working days for workload planning"
    
  local_holidays:
    - "Variable by municipality - patron saint days"
    - "Athens: Nov 15 (Patron Saint)"
    - "Thessaloniki: Oct 26 (Liberation Day)"
    - "Configure per-client based on registered location"
```

## OpenClaw Integration Requirements

### Required Skills Dependencies
```yaml
Required_Skills:
  core_dependencies:
    - accounting-workflows          # Document processing data
    - greek-compliance-aade         # VAT/payroll compliance data
    - cli-deadline-monitor          # Deadline tracking data
    - greek-email-processor         # Email processing status
    - greek-individual-taxes        # Individual tax data
    - openclaw-greek-accounting-meta # System orchestration
    
  advanced_dependencies:
    - aade-api-monitor              # Government system status
    - greek-banking-integration     # Bank feed data
    - greek-document-ocr            # OCR processing metrics
    - efka-api-integration          # Social security data
    
  openclaw_core:
    - file-processor                # File system operations
    - deepread                      # Document reading
    - doc-converter                 # Report format conversion

Installation_Command:
  setup: "npx openclaw skills add dashboard-greek-accounting --install-deps"
  verification: "openclaw dashboard health-check --verify-all-integrations"
```

## Performance Metrics

### Dashboard Performance Targets
```yaml
Performance_Targets:
  response_times:
    morning_briefing: "<5 seconds"
    client_overview: "<3 seconds"
    compliance_scorecard: "<3 seconds"
    deadline_tracker: "<2 seconds"
    alert_list: "<1 second"
    full_report_generation: "<30 seconds"
    
  accuracy:
    compliance_score_calculation: "99%+"
    deadline_tracking: "100% (zero missed)"
    alert_generation: "99%+ (no false negatives)"
    data_freshness: "Within configured thresholds"
    
  reliability:
    dashboard_availability: "99.5%+"
    graceful_degradation: "Always show something useful"
    data_recovery: "<5 minutes from backup"
    
  user_experience:
    time_to_first_insight: "<10 seconds from login"
    clicks_to_any_client: "‰¤2 clicks"
    alert_response_time: "<1 minute from generation to display"
    report_delivery: "Within 5 minutes of scheduled time"
```

## Security & Access Control

### Data Protection
```yaml
Security_Measures:
  data_access:
    - Assistants see only assigned clients
    - Sensitive fields (AFM, bank details) masked by default
    - Full data visible only on explicit request with audit log
    - Client data isolation between assistant views
    
  audit_trail:
    - All dashboard access logged with timestamp and user
    - Alert acknowledgments tracked with user and notes
    - Report generation and distribution logged
    - Data exports require confirmation and are logged
    
  gdpr_compliance:
    - Client consent tracking for data processing
    - Data retention policies enforced automatically
    - Right to erasure support for client data
    - Data processing records maintained per GDPR Art. 30
```

## Usage Examples

### Example 1: Morning Startup
```markdown
User Action: "openclaw dashboard morning-briefing"
System Response:
1. Aggregates overnight alerts from all 10 skills
2. Checks all government system statuses (AADE, EFKA, myDATA)
3. Compiles today's deadlines across all clients
4. Generates prioritized task queue
5. Produces formatted English briefing with Greek data references
6. Highlights 2 critical alerts requiring immediate attention
7. Shows 3 deadlines due today with preparation status
8. Lists 12 tasks in priority order with estimated time
```

### Example 2: Client Deep Dive
```markdown
User Action: "openclaw dashboard client-overview --client 'ALPHA TRADING AE'"
System Response:
1. Pulls latest compliance data from greek-compliance-aade skill
2. Gets deadline status from cli-deadline-monitor
3. Checks document processing queue from accounting-workflows
4. Retrieves bank feed status from greek-banking-integration
5. Shows EFKA employee status from efka-api-integration
6. Displays comprehensive English-language client overview
7. Highlights overdue VAT return with action steps
8. Shows compliance score trend (72/100, down from 85 last month)
```

### Example 3: End-of-Day Wrap-up
```markdown
User Action: "openclaw dashboard eod-summary"
System Response:
1. Summarizes all tasks completed today with timestamps
2. Lists remaining unresolved items with priority levels
3. Shows tomorrow's preview (4 deadlines, 2 scheduled reports)
4. Generates daily summary report and emails to team
5. Updates compliance scores based on today's activities
6. Queues overnight monitoring for government announcements
```

## Troubleshooting

### Common Issues
```yaml
Troubleshooting:
  stale_data:
    symptom: "Dashboard shows outdated information"
    check: "Verify skill integrations are active"
    fix: "openclaw dashboard refresh --force --rebuild-cache"
    
  missing_client:
    symptom: "Client not appearing in portfolio view"
    check: "Verify client data exists in source skills"
    fix: "openclaw dashboard sync-clients --rebuild"
    
  alerts_not_generating:
    symptom: "Expected alerts not appearing"
    check: "Review alert rules configuration"
    fix: "openclaw dashboard alert-rules --validate --test"
    
  slow_performance:
    symptom: "Dashboard takes >10 seconds to load"
    check: "Review cache status and data volumes"
    fix: "openclaw dashboard optimize --rebuild-cache --archive-old"
    
  report_generation_failure:
    symptom: "Scheduled reports not delivered"
    check: "Verify report template and delivery settings"
    fix: "openclaw dashboard schedule-report --test --verbose"
```

A successful dashboard deployment should achieve:
- ✅ Complete visibility across all Greek accounting clients
- ✅ English-language interface processing Greek business data seamlessly
- ✅ Real-time alerts with zero missed critical notifications
- ✅ Integration with all 10 existing OpenClaw Greek accounting skills
- ✅ Assistants productive within 15 minutes of first use
- ✅ 80% reduction in time spent checking compliance status manually
- ✅ Professional reports generated automatically on schedule
- ✅ Complete audit trail for all dashboard actions
