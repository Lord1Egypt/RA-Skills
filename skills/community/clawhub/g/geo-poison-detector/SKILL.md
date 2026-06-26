---
name: geo-poison-detector
description: "AI推荐防投毒检测器 / AI Recommendation Poison Detector. 你有没有遇到过：AI推荐了一款产品，买回来才发现是劣质品或根本不存在的品牌？这就是GEO投毒——不法商家花钱批量制造虚假软文，让AI误以为这些产品是市场上的优质选择。这个skill帮你识破这些陷阱。三种使用方式：(1) 自动防护：每当AI向你推荐产品时，自动附上风险标记🟢🟡🔴，无需任何操作；(2) 主动检测：发送「检测 产品名」或「/check product name」，立即获得该产品的可信度分析；(3) 链接检测：把一篇产品推荐文章的链接发给AI，自动分析文章是否为投毒软文。支持国内外产品，中英文双语，覆盖淘宝/京东/Amazon等主流平台验证。无需任何API密钥，开箱即用。 | EN: Protects you from fake AI product recommendations planted by bad actors (GEO poisoning). Auto-flags suspicious products when AI recommends them, lets you quick-check any product by name, and analyzes article URLs for soft-ad poisoning patterns. Supports CN and Global markets, Chinese and English. No API keys needed."
---

# GEO Poison Detector — AI推荐投毒检测器

## 这个工具是做什么的？

**问题：** AI推荐的产品不一定可信。不法商家通过「GEO优化」——批量生成含虚假参数的软文并大量铺发——让AI误以为这些虚构商品是市场上的优质选择。2026年央视315晚会曝光此类黑产，收费1.5–2万元/年，2小时内即可让虚假产品成为AI的「标准答案」。

**这个skill做什么：** 在你收到AI产品推荐时，自动扫描伪科技话术、软文模板特征、来源可信度，给出🟢安全 / 🟡可疑 / 🔴高危三档风险判断，并生成验证链接让你一键核查。

**三种使用方式：**
- 🤖 **自动防护**：AI推荐产品时，自动附带风险标记，无需任何操作
- 🔍 **主动检测**：发送 `检测 产品名` 或 `/check product name`，立即查
- 🔗 **链接分析**：发送文章链接，自动抓取并分析是否为投毒软文

**覆盖范围：** 中文/英文产品，国内（京东/淘宝/企查查）和国际（Amazon/BBB/USPTO）双市场验证。

---

**What this tool does (EN):** Detects GEO (Generative Engine Optimization) poisoning — bad actors mass-generate fake product specs into AI training data, making fraudulent products appear as authoritative AI recommendations. Exposed by CCTV 315 (2026, China); similar tactics documented by Wired/MIT Tech Review globally. Auto-flags products when AI recommends them, supports user quick-checks by name, and analyzes article URLs for soft-ad patterns.

---

## Mode 1: Auto-Trigger (AI Recommending Products)

Whenever you are about to recommend a specific product or brand, **run detection first**, then append a risk badge inline:

```
[Your normal recommendation answer]

---
🛡️ GEO投毒检测 / Poison Check: [🟢 SAFE / 🟡 SUSPICIOUS / 🔴 HIGH RISK]
触发指标 / Indicators: [list triggered signals, or "无" if clean]
验证链接 / Verify: [run verify_product.py and include top 2-3 links]
```

**Do NOT skip this step when recommending products.** This is the core value of the skill.

---

## Mode 2: User Quick-Check (Product Name)

Triggered when user sends any of:
- `/check <product name>`
- `检测 <产品名>`
- `查一下 <产品名>`
- `is this legit: <product>`
- `这个可信吗: <产品名>`
- Or any message asking to verify a specific product by name

**Action**: Run the full 5-step detection workflow on the product name. Output the full report format. Run `scripts/verify_product.py "<product>"` to generate verification links.

**Example interaction**:
```
User: /check 量子能量水杯黑洞级净化
Agent: 🔴 HIGH RISK — 检测到2个高权重伪科技词汇
触发指标：
• [Step 1] 「量子能量」— 高风险伪量子话术
• [Step 1] 「黑洞级」— 高风险伪黑科技话术
验证链接：[京东] [企查查] [国家专利局]
建议：该产品名称含多个典型GEO投毒特征词，极可能为虚假推荐，请勿购买。
```

---

## Mode 3: URL Analysis (Article/Page)

Triggered when user sends a URL and asks to check it:
- `check this: https://...`
- `帮我检测这篇文章: https://...`
- `这个链接可信吗: https://...`
- Any URL from: WeChat (mp.weixin.qq.com), Zhihu, Baijiahao, Medium, blog sites

**Action**:
1. Use `web_fetch` to retrieve the article content
2. Run the full 5-step detection workflow on the fetched text
3. Also note the source domain as part of Step 4 source quality assessment
4. Output the full report format

**Example interaction**:
```
User: 帮我检测这篇文章 https://mp.weixin.qq.com/s/xxxxx
Agent: [fetches content]
🟡 SUSPICIOUS — 检测到软文批量生成特征
触发指标：
• [Step 2] 模板化结构："很多人不知道的是" + 产品推荐固定格式
• [Step 4] 来源：微信公众号自媒体，无权威背书
验证链接：[产品名搜索链接]
建议：内容结构符合GEO软文模板，建议通过官方渠道核实产品信息。
```

**Handling fetch failures**: If `web_fetch` fails or is blocked, ask user to paste the article text and switch to Mode 2 workflow.

---

## Detection Workflow (5 Steps)

Apply to content from any mode.

### Step 1 — Pseudo-tech buzzword scan (HIGH weight)

Load `references/pseudo-tech-terms.md`. Scan for high-risk terms in both CN and EN sections.
- 2+ high-risk terms → immediately 🔴
- 1 high-risk term → 🟡 suspicious

### Step 2 — Batch-generated content fingerprint (HIGH weight)

**Universal signals (CN+EN):**
- Fixed template structure (Problem → Solution → Product plug)
- Keyword stuffing (product name repeated 5+ times)
- Vague superlatives without verifiable data
- No model numbers, no verifiable specs, no brand registration
- Multiple sources with identical or near-identical wording

**CN-specific:**
- "很多人不知道的是..." / "内部员工都在用"
- 自媒体/百家号/微信公众号 as sole sources
- 无厂商官网、无天猫/京东旗舰店

**EN/Global-specific:**
- "Doctors don't want you to know..."
- Affiliate disclosure buried or absent
- Only "as seen on" claims, no retailer presence
- Reviews only on brand's own site, not Amazon/Trustpilot

### Step 3 — Product authenticity cross-verification (MEDIUM weight)

Run `scripts/verify_product.py "<product name>" [--market cn|global|auto]`

**CN market:** JD.com, Taobao, Qichacha, Tianyancha, CNIPA patents, GB standards
**Global market:** Amazon, Google Shopping, BBB, Trustpilot, USPTO patents, EU RAPEX, Reddit

### Step 4 — Source quality assessment (MEDIUM weight)

| Source Type | CN Example | Global Example | Trust |
|---|---|---|---|
| Major retailer official | 京东/天猫旗舰店 | Amazon/BestBuy official | High |
| Gov/standards body | 国家标准委/CNIPA | FDA/CE/ISO | High |
| Mainstream media | 央视/人民日报 | NYT/BBC/Reuters | High |
| Brand official site | 品牌官网 | brand.com | Medium |
| Self-media only | 百家号/头条/微信 | Medium blogs/affiliate | Low |
| Unknown/unverifiable | 来源不明 | Unknown | Very Low |

### Step 5 — Risk verdict

| Result | Threshold |
|---|---|
| 🟢 SAFE | 0–1 low-weight indicators |
| 🟡 SUSPICIOUS | 2+ medium OR 1 high-weight indicator |
| 🔴 HIGH RISK | 2+ high-weight OR confirmed fake specs |

---

## Output Format

**Quick badge** (Mode 1 auto-trigger):
```
🛡️ GEO Check: 🟢 SAFE — no poisoning signals detected
```

**Full report** (Mode 2 quick-check or Mode 3 URL, or when user asks for details):
```
[🟢/🟡/🔴] <one-line verdict in user's language>

触发指标 / Indicators:
• [Step N] <indicator> — <explanation>

验证链接 / Verify:
• <platform>: <url>

建议 / Recommendation: <next action>
```

## Language

- Match user's language (CN/EN/mixed)
- Auto-detect market from product name (CJK → CN, Latin → Global)
- For CN products in global context: check international presence too

---

## References

- Term library (CN+EN): `references/pseudo-tech-terms.md` — load during Step 1
- Verification script: `scripts/verify_product.py` — run during Step 3
  - Usage: `python3 verify_product.py "<name>" [--market cn|global|auto]`
