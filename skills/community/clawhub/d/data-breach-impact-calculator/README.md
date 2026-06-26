# Data Breach Impact Calculator — OpenClaw Skill 💰🔓

Calculate data breach costs with a single message to your OpenClaw agent.

## Quick Install

```bash
clawhub install data-breach-impact-calculator
```

## Configuration

```json
{
  "skills": {
    "entries": {
      "data-breach-impact-calculator": {
        "enabled": true,
        "env": {
          "TOOLWEB_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## Get Your API Key

Visit [portal.toolweb.in](https://portal.toolweb.in) — free trial includes 10 API calls.

## What It Calculates

- Total estimated breach cost
- Regulatory fines (GDPR, CCPA, HIPAA, PCI DSS)
- Legal and litigation expenses
- Notification costs
- Remediation and recovery costs
- Reputation and business loss
- Investigation and forensics costs
- Cost reduction recommendations

## Example

```
You: How much would it cost if 50,000 patient records were breached?
     We're a large hospital, HIPAA and GDPR regulated, moderate security.

Agent: 💰 Data Breach Impact Assessment
       Total Estimated Cost: $8.2M
       🏛️ Regulatory Fines: $3.1M
       ⚖️ Legal: $1.8M
       📧 Notification: $0.4M
       📉 Reputation Loss: $2.9M
       💡 An IR plan could reduce costs by ~$2.66M
```

## Pricing

| Plan | Price/month | API Calls |
|------|------------|-----------|
| Free Trial | $0 | 10 calls |
| Starter | ₹2,999 (~$36) | 500 |
| Professional | ₹9,999 (~$120) | 5,000 |
| Enterprise | ₹49,999 (~$600) | Unlimited |

International: Select PayPal at checkout for USD/EUR/GBP.

## License

MIT-0

---

*Built by a CISSP & CISM certified professional at [ToolWeb.in](https://toolweb.in)*
