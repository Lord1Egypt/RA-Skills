---
name: ai-cost-estimator
description: Estimate infrastructure and API costs for running AI agents in production. Covers compute, API tokens, storage, and monitoring costs. Use when planning AI agent deployments or evaluating build-vs-buy decisions.
---

# AI Cost Estimator Skill

## Purpose
Help teams estimate the true cost of running AI agents in production — not just API fees, but compute, storage, monitoring, maintenance, and engineering time.

## When to Use
- Planning an AI agent deployment
- Comparing build-in-house vs managed service
- Budgeting for AI infrastructure
- Evaluating vendor proposals

## Cost Categories

### 1. Compute (Server/VPS)

| Provider | Spec | Monthly Cost |
|----------|------|-------------|
| Hetzner CX31 | 2 vCPU, 8GB RAM, 80GB | $8/mo |
| Hetzner CX41 | 4 vCPU, 16GB RAM, 160GB | $15/mo |
| AWS t3.medium | 2 vCPU, 4GB RAM | ~$30/mo |
| AWS t3.large | 2 vCPU, 8GB RAM | ~$60/mo |
| DigitalOcean | 2 vCPU, 4GB RAM | $24/mo |
| Railway | Usage-based | $5-50/mo |

**Recommendation:** Hetzner for cost efficiency. AWS/GCP if client requires specific cloud.

### 2. LLM API Costs

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|----------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| Claude Sonnet 4 | $3.00 | $15.00 |
| Claude Haiku | $0.25 | $1.25 |
| Llama 3.1 70B (self-hosted) | ~$0 (compute only) | ~$0 |

**Typical agent usage:** 500K-2M tokens/day depending on complexity.

**Monthly API cost estimate:**
- Light agent (email triage, scheduling): $15-50/mo
- Medium agent (research, content, CRM): $50-200/mo
- Heavy agent (coding, analysis, multi-step): $200-800/mo

### 3. Storage & Database

| Service | Free Tier | Paid |
|---------|-----------|------|
| Supabase | 500MB, 2 projects | $25/mo (8GB) |
| PlanetScale | 5GB | $39/mo |
| SQLite (on VPS) | $0 | $0 |
| S3/R2 (file storage) | 10GB free | $0.015/GB |

### 4. Monitoring & Ops

| Service | Free Tier | Paid |
|---------|-----------|------|
| UptimeRobot | 50 monitors | $7/mo (1-min intervals) |
| Better Stack | 10 monitors | $24/mo |
| Sentry (errors) | 5K events | $26/mo |
| Datadog | Limited | $15/host/mo |

### 5. Hidden Costs (Often Forgotten)

| Item | Estimated Cost |
|------|---------------|
| Engineer setup time (40-80 hrs) | $4,000-16,000 one-time |
| Ongoing maintenance (5-10 hrs/mo) | $500-2,000/mo |
| Security patches & updates | 2-4 hrs/mo |
| Prompt engineering & tuning | 5-20 hrs initial |
| Testing & QA | 10-20 hrs initial |
| Documentation | 5-10 hrs |
| On-call / incident response | $500-2,000/mo |

## Total Cost Calculator

### DIY Single Agent
```
Compute (Hetzner):     $8/mo
API costs (medium):    $100/mo
Database (SQLite):     $0/mo
Monitoring:            $0/mo (free tier)
Engineering (10h/mo):  $1,000/mo
─────────────────────────────
TOTAL:                 ~$1,108/mo
+ Setup:               ~$8,000 one-time
```

### DIY Multi-Agent Swarm (5 agents)
```
Compute:               $30/mo
API costs:             $400/mo
Database (Supabase):   $25/mo
Monitoring:            $25/mo
Engineering (20h/mo):  $2,000/mo
─────────────────────────────
TOTAL:                 ~$2,480/mo
+ Setup:               ~$20,000 one-time
```

### Managed Service (AfrexAI)
```
Single agent:          $1,500/mo (all-inclusive)
Full swarm:            $5,000/mo (all-inclusive)
Setup:                 $0 (included)
Maintenance:           $0 (included)
Monitoring:            $0 (included)
Engineering:           $0 (included)
```

## Build vs Buy Decision Matrix

| Factor | Build In-House | Managed (AfrexAI) |
|--------|---------------|-------------------|
| Time to deploy | 2-8 weeks | 1 week |
| Monthly cost (single) | $1,100+ | $1,500 |
| Monthly cost (swarm) | $2,500+ | $5,000 |
| Engineering dependency | High | None |
| Customization | Full | High |
| Support/SLA | Self-managed | Included |
| Scaling | You handle it | We handle it |
| Risk | On you | Shared |

**Key insight:** Build-in-house looks cheaper on paper, but engineering time is the real cost. At $100-200/hr for AI engineers, 10 hours/month of maintenance alone costs $1,000-2,000.

## ROI Framework

```
Monthly savings from automation:
- Hours saved × hourly cost of employee
- Error reduction × cost per error
- Speed improvement × revenue per hour

Example (legal firm):
- Paralegal: 20 hrs/week saved × $35/hr = $2,800/mo
- Error reduction: 5 fewer mistakes × $500/mistake = $2,500/mo
- Speed: 30% faster case processing = $3,000/mo additional capacity
- TOTAL VALUE: $8,300/mo
- COST: $1,500/mo (managed agent)
- ROI: 453%
```

## Get Started

Want accurate cost estimates for your specific use case?
→ Free consultation: https://calendly.com/cbeckford-afrexai/30min
→ AI-as-a-Service from $1,500/mo: https://afrexai-cto.github.io/aaas/landing.html
→ ROI Calculator: https://afrexai-cto.github.io/ai-revenue-calculator/
