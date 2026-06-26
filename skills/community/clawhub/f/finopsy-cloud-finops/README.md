# Finopsy — Cloud FinOps Analyzer — OpenClaw Skill ☁️💵

Analyze and optimize AWS, Azure, and GCP cloud costs via your OpenClaw agent.

## Quick Install

```bash
clawhub install finopsy-cloud-finops
```

## Configuration

```json
{
  "skills": {
    "entries": {
      "finopsy-cloud-finops": {
        "enabled": true,
        "env": {
          "TOOLWEB_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## Supported Providers

AWS, Azure, GCP — using read-only credentials for secure analysis.

## What You Get

- Cost breakdown by service
- Monthly spending trends
- Rightsizing recommendations
- Unused resource detection
- Reserved instance opportunities
- Total savings estimate

## Example

```
You: Analyze our AWS cloud costs for the last 3 months.

Agent: ☁️ Finopsy Cloud Cost Analysis
       Provider: AWS | Period: 3 months
       💵 Total: $45,230
       📈 Trend: +12% month-over-month
       💡 Savings: Rightsize 8 EC2 instances — save $3,200/mo
       💡 Savings: Delete 12 unused EBS volumes — save $480/mo
       💰 Total Potential: $3,680/month savings
```

## Pricing

| Plan | Price/month | API Calls |
|------|------------|-----------|
| Free Trial | $0 | 10/day, 50/month |
| Developer | $39 | 20/day, 500/month |
| Professional | $99 | 200/day, 5000/month |
| Enterprise | $299 | 100K/day, 1M/month |

## License

MIT-0

---

*Built by a CISSP & CISM certified professional at [ToolWeb.in](https://toolweb.in)*
