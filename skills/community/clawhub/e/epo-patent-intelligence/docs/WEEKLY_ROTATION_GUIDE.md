# Weekly Rotation Guide

## Current Week: KW17 (Week 17, 2026)

## Directory Structure
```
reports/
├── index.html                    # Main index with all reports
├── modern_report_template.html   # Template for all weeks
├── Patent_report_kw14/           # Week 14 (current live)
│   └── index.html
└── Patent_report_kw17/        # Week 17 (prepared)
    └── index.html
```

## Rotation Process

### 1. Prepare New Week
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
./scripts/rotate_weekly.sh 16   # For KW16
```

### 2. Deploy New Week
```bash
./scripts/restart_tunnel_kw16.sh
```

### 3. Archive Old Week
```bash
# Move old week to archive
mv reports/Patent_report_kw14/ archive/kw14_2026/
```

## URL Structure
- Week 14: https://hermes.sqncr.ai/Patent_report_kw14
- Week 17: https://hermes.sqncr.ai/Patent_report_kw17
- Week 16: https://hermes.sqncr.ai/Patent_report_kw16

## Automation Notes
- The HTTP server always runs on port 8080
- Cloudflare tunnel routes based on subdomain path
- Each week gets its own log files
- Restart scripts are week-specific for easy management
