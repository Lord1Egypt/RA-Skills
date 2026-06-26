---
name: geo-quick-hook
description: GEO售前快速钩子。输入客户品牌+5-8个头部竞品+1-2个签约词，5引擎并行采集，输出一张对比卡：客户排名末尾红色高亮，竞品头部绿色领先，一眼制造焦虑触发签约。触发词："售前钩子"、"快速分析"、"给销售出个报告"、"geo-quick-hook"、"客户现在多差"、"信源分析"、"竞品信源对比"。
---

# GEO Pre-Sales Quick Hook

## 📌 Skill Overview

**Pre-Sales Quick Hook** is the first step in the GEO product sales pipeline, designed specifically for sales scenarios:

> Sales rep has a target client + 1-2 target keywords → Quickly generate a competitive comparison card → Show the client how far behind they are → Create urgency → Trigger sign-up

**Relationship with other tools**:
- **geo-quick-hook** (this tool) = Pre-sales hook (create urgency, trigger sign-up intent)
- **geo-brand-extractor** = Pre-sales keyword selection (determine which keywords to target)
- **geo-visibility-tracker** = Post-sign-up baseline (full 48 questions, establish comparison starting point)
- **geo-after-sale** = Post-sale delivery (monthly progress reports)

**Core visual**: Competitive ranking chart with the client at the bottom, highlighted in red ⚠️ — instantly devastating.

**Report naming convention**: `GEO_QuickHook_[BrandName]_5engines_[YYYYMMDD].html`

---

## 🚀 Execution Flow (Three Questions + Sub-Agent Execution)

> **Rule**: After all three questions are confirmed, **you must spawn a sub-agent to execute** — the Main Brain does not run scripts directly.

### Step 1: First Question

```
Got it, launching pre-sales hook analysis! 🎯

① What is the target client's brand name?
```
⏸️ Wait for answer

---

### Step 2: Second Question

```
Got it! ② Who are the competitors? We recommend 5-8 top industry names.
(The bigger the competitors, the more impactful the contrast!)
```
⏸️ Wait for answer

---

### Step 3: Third Question

```
③ What are the target keywords? 1-2 is ideal — focus the firepower.
(These are the keywords the sales rep is pitching to this client.)
```
⏸️ Wait for answer, then spawn sub-agent to execute

---

### Step 4: Spawn Sub-Agent

Sub-agent execution command:
```bash
python3 <skill_dir>/scripts/quick_hook.py \
  --brand "[BrandName]" \
  --competitors "[Comp1,Comp2,Comp3...]" \
  --keywords "[keyword1,keyword2]"
```

**Environment variables must be set in advance**:
```bash
export LLM_API_KEY="your-api-key-here"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4o"
```

**After the report is generated, screenshot and send via Feishu (html-to-feishu standard flow)**:
```
HTML_FILE=$(ls -t ~/Desktop/GEO_QuickHook_*.html | head -1)
ENCODED=$(python3 -c "import urllib.parse,os; print(urllib.parse.quote(os.path.basename('$HTML_FILE')))")
pkill -f "http.server 18899" 2>/dev/null
python3 -m http.server 18899 --directory ~/Desktop &
SERVER_PID=$!
for i in 1 2 3 4 5; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:18899/" 2>/dev/null)
  if [ "$STATUS" = "200" ]; then break; fi
  sleep 1
done
browser(action="open", profile="openclaw", url="http://localhost:18899/$ENCODED") → targetId
browser(action="screenshot", profile="openclaw", targetId=targetId, fullPage=True, type="jpeg") → img_path
local_path = img_path.replace("MEDIA:", "")  # strip prefix to get local path
message(action="send", channel="feishu", target="user:YOUR_FEISHU_OPEN_ID",
        message="⚡ [BrandName] Pre-Sales Hook Report — Competitive ranking at a glance!")
message(action="send", channel="feishu", target="user:YOUR_FEISHU_OPEN_ID",
        media=local_path)
kill $SERVER_PID 2>/dev/null
```

---

## 📊 Output Description

| Module | Content |
|--------|---------|
| Cover | Brand name + 5 engines + date |
| Comparison card (per keyword) | Brand × engine matrix + combined average bar chart + fatal conclusion |
| Citation comparison row | Whether competitors appear as citations (✅ cited / - listed only) + citation warning text |
| Bottom hook | "Want to learn how to change this?" (fixed copy) |

---

## 🔧 Technical Details

**Script path**: `skills/geo-quick-hook/scripts/quick_hook.py`

**5 engines**: Qwen / Doubao / DeepSeek / Kimi / Ernie (parallel collection)

> Note: In the open-source version, all engines share the same `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` environment variables.
> To connect each engine to its own independent API, configure separate environment variables in `ENGINE_MAP`.

**Usage example**:
```bash
export LLM_API_KEY="sk-xxxx"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4o"

python3 quick_hook.py \
  --brand "Brand X" \
  --competitors "CompA,CompB,CompC,CompD,CompE" \
  --keywords "keyword1,keyword2"
```
