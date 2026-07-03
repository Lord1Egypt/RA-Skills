# Output Template — Hunter Report Format

> This template defines the structured output format for all Airdrop Hunter reports.
> The AI agent receives JSON from MCP tools and renders it as savage Markdown.

---

## 1. Scan/Daily Report Output

### JSON Structure (from MCP tool)
```json
{
  "summary": "扫描完毕：2个金矿，3个值得关注，1个已空投（别碰）",
  "projects": [
    {
      "name": "Project Name",
      "grade": "S",
      "metrics": {
        "tvl": "$500M",
        "funding": "$80M (Paradigm +1)",
        "cost_estimate": "$20-$50 Gas",
        "roi_index": "9/10"
      },
      "savage_comment": "这就是Web3的亲儿子，顶级机构喂饭。",
      "action_required": "完成主网跨链并至少保留0.1 ETH余额"
    }
  ],
  "hunter_advice": "先处理S级，Gas低于15 gwei时再动B级。",
  "next_step_options": ["Deep Dive S/A Project", "Check Scam Risks", "Show Zero Cost"]
}
```

### Rendered Markdown Template
```markdown
## Radar Sweep — [Date]

[summary]

| # | Project | Grade | TVL | Funding | Cost | ROI | Action |
|---|---------|-------|-----|---------|------|-----|--------|
| 1 | **Project Name** | **S** | $500M | $80M (Paradigm) | $20-50 | 9/10 | Cross-chain + hold 0.1 ETH |

**Hunter Says:** savage_comment

---

**Hunter Advice:** hunter_advice

**What's Next?**
1. Deep Dive S/A Project
2. Check Scam Risks
3. Show Zero Cost
```

---

## 2. Check Project Output

### JSON Structure (from MCP tool)
```json
{
  "project_identity": {
    "name": "Monad",
    "status": "active",
    "grade": "S"
  },
  "analysis": {
    "vc_quality": "顶级VC站台（Paradigm、Electric Capital），这饼至少有人负责烤。",
    "tokenomics": "暂无代币，这是好信号——说明空投还没发，你现在交互还来得及。",
    "scam_probability": "低 - 项目数据完整且有正规背书。"
  },
  "the_harsh_truth": "Monad是当前最值得花时间的项目。不做？那你来币圈是来旅游的吗？",
  "verdict": "MUST DO - 顶级机会，不交互后悔",
  "next_step_options": ["Verify Official URL", "Show Zero Cost for This Chain", "Add to Watchlist"]
}
```

### Rendered Markdown Template
```markdown
## Deep Dive: **[Project Name]** — Grade [X]

| Dimension | Assessment |
|-----------|-----------|
| VC Quality | vc_quality |
| Tokenomics | tokenomics |
| Scam Probability | scam_probability |

**The Harsh Truth:** the_harsh_truth

**Verdict:** verdict

---

**What's Next?**
1. Verify Official URL
2. Show Zero Cost for This Chain
3. Add to Watchlist
```

---

## 3. Zero-Cost Output

### JSON Structure (from MCP tool)
```json
{
  "opportunity_type": "Zero-Cost Testnet & Free Mainnet",
  "items": [
    {
      "name": "Monad",
      "time_investment": "15 mins daily",
      "probability": "40-60%",
      "sybil_resistance": "Medium (需要链上活跃记录)",
      "savage_comment": "不需要你掏钱，只需要你出卖劳动力。"
    }
  ],
  "survival_tips": "一定要隔离IP和钱包，别让项目方觉得你是一台莫得感情的刷分机器。",
  "next_step_options": ["Verify First Project URL", "Set Daily Reminder", "Check Multi-Account Strategy"]
}
```

### Rendered Markdown Template
```markdown
## Broke-to-Rich Path — $0 Cost Opportunities

| # | Project | Time | Probability | Sybil Resistance |
|---|---------|------|-------------|-----------------|
| 1 | **Monad** | 15 min/day | 40-60% | Medium |

**Hunter Says:** savage_comment

**Survival Tips:** survival_tips

---

**What's Next?**
1. Verify First Project URL
2. Set Daily Reminder
3. Check Multi-Account Strategy
```

---

## 4. Scam Check Output

### JSON Structure (from MCP tool)
```json
{
  "security_verdict": "DANGER / HIGH RISK",
  "threat_level": "CRITICAL",
  "detection_report": {
    "url_analyzed": "https://scroll-airdrop-claim.xyz",
    "project_analyzed": "Scroll",
    "warnings_found": 2,
    "warning_details": [
      {
        "type": "fake_claim_website",
        "description": "Hyphenated knockoff: scroll-airdrop pattern detected",
        "severity": "critical"
      }
    ],
    "safe_alternatives": ["scroll.io"]
  },
  "savage_comment": "如果你想清空钱包，请务必点击这个链接。",
  "safe_action": "已为你找到官方验证的安全链接：scroll.io",
  "next_step_options": ["Find Legit Official Site", "Scan Safe Airdrops", "Report This Scam"]
}
```

### Rendered Markdown Template — CRITICAL/HIGH Risk
```markdown
## **DANGER** — Threat Level: CRITICAL

**DO NOT CLICK. DO NOT CONNECT YOUR WALLET.**

| Detection | Detail |
|-----------|--------|
| URL Analyzed | scroll-airdrop-claim.xyz |
| Warnings | 2 found |
| Type | fake_claim_website |

**Warning Details:**
- [CRITICAL] Hyphenated knockoff: scroll-airdrop pattern detected

**Hunter Says:** savage_comment

**Safe Alternative:** scroll.io

---

**What's Next?**
1. Find Legit Official Site
2. Scan Safe Airdrops
3. Report This Scam
```

### Rendered Markdown Template — Safe/Low Risk
```markdown
## All Clear — Threat Level: LOW

| Detection | Detail |
|-----------|--------|
| URL Analyzed | monad.xyz |
| Warnings | 0 found |

**Safe Action:** safe_action

---

**What's Next?**
1. Show Zero Cost for This Project
2. Daily Report
3. Scan All Airdrops
```

---

## 5. Prohibited Projects in Output

When a scan/check returns a **prohibited project**, it MUST be displayed differently:

```markdown
| # | Project | Grade | Status | Note |
|---|---------|-------|--------|------|
| - | ~~Arbitrum~~ | ~~C~~ | **Airdrop Done** | $ARB distributed. Skip. |
```

**Never show prohibited projects as active opportunities.** Always strikethrough and mark "Airdrop Done."
