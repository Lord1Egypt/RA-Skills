# CORE Prism (CORE 四维战略透镜)

> **Strategic analysis framework** that cuts through noise and finds essence, opportunities, risks, and actions.

[![ClawHub](https://img.shields.io/badge/ClawHub-Published-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

---

## 🎯 What It Does

CORE is a **four-dimensional analysis framework** that forces you (or your AI) to think deeply about ANY strategic problem:

- **[C] Core Logic** — Strip away packaging, find first principles
- **[O] Opportunity** — Track value flows, find leverage points
- **[R] Risk** — Contrarian thinking, spot black swans
- **[E] Execution** — Map insights to YOUR context, answer "So What?"

**Not for**: Casual reading summaries  
**Perfect for**: News analysis, product decisions, investment research, strategic planning

---

## ⚡ Quick Start

### Install

```bash
# From ClawHub (recommended)
clawhub install core-prism

# Or manually
cp -r core-prism ~/.openclaw/workspace/skills/
```

### Use It

**Analyze anything:**
```
Ask your AI: "Use CORE framework to analyze [news article / product idea / business strategy]"
```

**Example input:**
> "Analyze this: OpenAI just released GPT-5 with PhD-level reasoning."

**Example output:**
```markdown
[C] Core Logic:
First AI to pass reasoning benchmarks that previously required human PhDs. 
Essence: Reasoning is becoming a commodity, just like text generation did with GPT-3.

[O] Opportunity:
- Winners: Companies that layer proprietary data/workflows on top of GPT-5
- Losers: "AI wrapper" startups with no defensible moat
- You: If building AI products, shift from "we use AI" to "we have unique data"

[R] Risk (Contrarian):
- Crowd is euphoric about "reasoning breakthrough"
- Reality: Regulators may freeze capabilities at GPT-4 level (EU AI Act)
- Hidden assumption: OpenAI can legally train on academic papers (lawsuit pending)

[E] Execution (For You):
TODAY: Audit your AI product's defensibility
- Does it depend on GPT-4 being SOTA? (danger)
- Does it have proprietary data/workflows? (safe)
ACTION: If no moat → pivot to data acquisition or workflow lock-in
```

---

## 📊 Use Cases

### 1. Daily News Analysis (Most Popular)
- **Who**: Investors, product managers, strategists
- **How**: Pair with `insight-radar` skill for automated daily briefings
- **Value**: See what others miss (contrarian insights, second-order effects)

### 2. Product Decision Making
- **Who**: Founders, PMs
- **Example**: "Should we build feature X?"
  - **[C]** What user problem does this solve at its core?
  - **[O]** Who captures value if we do this? (us, competitors, users?)
  - **[R]** What's the contrarian take? (maybe users don't actually want this)
  - **[E]** Should we build it? Ship an MVP first? Kill it?

### 3. Investment Research
- **Who**: Investors, analysts
- **Example**: "Analyze Tesla's FSD rollout"
  - **[C]** Core tech: Vision-only vs. LiDAR tradeoff
  - **[O]** Value flow: Data moat > hardware sales
  - **[R]** Regulatory black swan: One fatal accident = nationwide ban
  - **[E]** Buy, sell, or wait?

### 4. Strategic Planning
- **Who**: Executives, consultants
- **Example**: "Analyze our competitor's pivot"
  - **[C]** Why are they doing this? (running out of cash? new insight?)
  - **[O]** Where will profit pools shift?
  - **[R]** What if they're wrong? (contrarian scenario)
  - **[E]** Should we copy them, do the opposite, or ignore?

---

## 🧠 Why CORE Works

### 1. MECE Principle
**Mutually Exclusive, Collectively Exhaustive** — No overlap, no gaps.

Traditional analysis often mixes levels:
- "This is innovative" (vague)
- "Market size is $10B" (opportunity)
- "Competitors are weak" (risk assessment)

CORE forces clean separation:
- **[C]** What IS this? (essence)
- **[O]** Where's the money? (value capture)
- **[R]** What can go wrong? (risk)
- **[E]** What should I do? (action)

### 2. Forced Compression
You can't be vague. CORE demands:
- ONE sentence for Core Logic
- Specific value flows in Opportunity
- Named risks in Risk
- Concrete actions in Execution

**Before CORE**:
> "AI is transforming industries and creating new opportunities."

**After CORE**:
> [C] AI commoditizes cognitive labor → [O] Value shifts to data moats → [R] Regulatory freeze risk → [E] Build data acquisition NOW.

### 3. Context Adaptation
The **[E] Execution** dimension adapts to YOUR situation:
- If you're a founder → "Should you pivot?"
- If you're an investor → "Buy or sell?"
- If you're irrelevant to the topic → "Cognitive reserve only"

**How it works**: The skill reads your `USER.md` to understand your context.

---

## 🛠️ Advanced Usage

### Custom Analysis Depth

**Quick version** (1 sentence per dimension):
```
Ask your AI: "CORE analysis of [topic] — quick version"
```

**Deep dive** (3-5 sentences per dimension):
```
Ask your AI: "Deep CORE analysis of [topic] with examples"
```

### Batch Analysis

Analyze multiple items at once:
```
Ask your AI: "Use CORE to compare: Option A vs Option B vs Option C"
```

Output:
```
| Dimension | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| [C] Core  | ...      | ...      | ...      |
| [O] Opp.  | ...      | ...      | ...      |
| [R] Risk  | ...      | ...      | ...      |
| [E] Exec. | ...      | ...      | ...      |

**Verdict**: Choose B (highest upside, manageable risk)
```

### Integration with Other Skills

**Pair with `insight-radar`**:
- `insight-radar` fetches news → `core-prism` analyzes each item
- Output: Daily strategic briefings with CORE analysis

**Pair with `mental-model-forge`**:
- Extract mental models from books → Analyze with CORE
- Output: Reusable strategic patterns

---

## 📂 File Structure

```
core-prism/
├── SKILL.md    # Framework definition
└── README.md   # This file
```

Super lightweight. No dependencies.

---

## 🚀 Examples

### Example 1: News Analysis

**Input**: "Analyze: Grab acquires Foodpanda Taiwan for $600M"

**Output**:
```
[C] Core Logic:
Southeast Asia's largest delivery platform expanding beyond home turf.
Essence: Regional monopolies hit growth ceiling → forced international expansion.

[O] Opportunity:
- Grab: Tests Chinese market viability (Taiwan = stepping stone)
- Foodpanda parent (Delivery Hero): Exit underperforming asset
- Competitors (Meituan/饿了么): Face new threat in Greater China

[R] Risk (Contrarian):
Crowd thinks: "Grab expansion = bullish"
Reality: This signals Southeast Asia growth has PEAKED.
Black swan: Taiwan delivery market already saturated → Grab burns $600M.

[E] Execution:
If you're in food delivery: Design for cross-region scalability from Day 1.
If you're an investor: Grab's growth story is ending; look elsewhere.
```

---

### Example 2: Product Decision

**Input**: "Should we add AI chatbot to our SaaS product?"

**Output**:
```
[C] Core Logic:
Every SaaS is adding AI chat. Question: Does it solve a real user pain or just FOMO?

[O] Opportunity:
- If you do it: Small differentiation (everyone has it soon)
- If you DON'T: Users may churn to "AI-powered" competitors
Value capture: Near zero (commodity feature)

[R] Risk (Contrarian):
Crowd: "AI is the future, must add it"
Contrarian: Users don't actually use chatbots (see: every website's ignored chat widget)
Real risk: Waste 3 months building something no one uses

[E] Execution:
TODAY: Talk to 10 users. Ask: "Would you use an AI chat in our product?"
If <50% say yes → DON'T build it. Focus on core value prop instead.
If >80% say yes → Build minimal MVP, ship in 1 week, measure usage.
```

---

## 💡 Pro Tips

### 1. Always Start with [C]
If you can't articulate the Core Logic in ONE sentence, you don't understand the problem yet.

### 2. Be Brutally Contrarian in [R]
Everyone can see obvious risks. Your job: Find the BLACK SWAN no one is talking about.

### 3. Make [E] Concrete
Bad: "Consider investing in this space"  
Good: "Open a $10K position this week, set stop-loss at -15%"

### 4. Read USER.md First
The skill auto-reads it, but you should too. Context is everything.

---

## 🛠️ Troubleshooting

**"Analysis is too shallow"**:
- Ask for "deep CORE analysis" instead of quick version
- Provide more context in your input

**"Execution section is generic"**:
- Update your `USER.md` with more specific info (current projects, skills, resources)
- Ask: "Tailor [E] to my exact situation"

**"I don't understand the contrarian take"**:
- That's the point! Contrarian = uncomfortable but valuable
- Ask: "Explain the Risk dimension in simpler terms"

---

## 📜 License

MIT-0 (No Attribution Required)

Use it, fork it, teach it — no strings attached.

---

## 🙌 Credits

Created by **汤圆 (Tangyuan)** for 雯姐's strategic decision-making workflow.

**Inspired by**:
- First-principles thinking (Elon Musk, Naval Ravikant)
- Contrarian investing (Howard Marks, Ray Dalio)
- MECE frameworks (McKinsey, BCG)

---

## 📣 Feedback

Found a bug? Want a feature? Open an issue or ping `@KeDOuPi` on ClawHub.

**Star this skill** if it changed how you think! ⭐
