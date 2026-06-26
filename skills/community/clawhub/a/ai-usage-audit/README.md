# 🔍 AI Usage Audit — Monthly Retrospective & Insights

> Sprint Retro for your AI collaboration. Turn your conversation history into a mirror.

## What is this?

A [ClawHub Skill](https://github.com/jjliu6) that analyzes your past month of AI conversations and generates a polished HTML report with actionable insights.

**Think of it as a personal coach reviewing your AI usage patterns** — what you're spending time on, where you're inefficient, where collaboration breaks down, and what to improve next month.

## The Problem

You use AI every day. But do you use it *well*?

Most people have no idea:
- How much time goes to **real output** vs. **passive info consumption**
- Which conversations are **repeated** (same question, different day)
- Where the **human-AI friction** is (unclear prompts → endless revisions)
- Whether their AI usage **aligns with their actual priorities**

This skill turns your chat history into data-driven self-awareness.

## What It Analyzes

| Dimension | What It Looks For |
|-----------|-------------------|
| **Theme Clustering** | What topics dominate? Does your AI usage match your goals? |
| **Pattern Detection** | Repeated questions, abandoned threads, info-consumption loops |
| **Value Output** | Which conversations produced real deliverables vs. just browsing? |
| **Collaboration Friction** | Where does the human-AI loop break down? Root cause analysis |
| **Highlights** | Your best AI collaboration moments — what made them work? |

## Output

A polished HTML report including:

- 📊 Data overview with topic distribution
- 🔍 Inefficiency patterns with evidence
- 📈 Value output assessment
- 🔧 Friction point analysis with root causes
- ✅ **Next month's improvement checklist** (actionable, measurable)
- 💬 One-paragraph coaching summary

## Language Support

The report **auto-detects your language** from your message. You can also explicitly request any language:

- `Run a usage audit` → English report
- `帮我做一次 AI 使用回顾` → Chinese report
- `Fais un audit de mon utilisation` → French report

## How to Use

### Option 1: Install as ClawHub Skill

Download `ai-usage-audit.skill` and install it in your Claude environment.

Then simply say:
```
Run a monthly AI usage audit
```

### Option 2: Use the Prompt Directly

Copy the prompt below into any AI product that has **chat history / memory** features:

<details>
<summary>📋 Click to expand the full prompt</summary>

```
Please run an "AI Usage Retrospective & Insights" analysis:

1. Pull my recent conversations (as many as possible from the past month, paginate through multiple pages)

2. Analyze across these dimensions:
   * Theme clustering: What have I mainly been doing? How is my time distributed?
   * Pattern detection: Any recurring workflows, repeated questions, or abandoned conversations?
   * Value assessment: Which conversations produced high-value results (files, decisions, code)? Which were low-efficiency info consumption?
   * Friction points: Where did my collaboration with AI break down? (e.g. excessive revisions, unclear requirements, wrong tool choices)
   * Recommendations: Based on the above, give me 3-5 specific, actionable improvements (what to do + why + how to measure)

3. Output format: concise prose (not bullet lists), highlight key insights with color, end with a one-paragraph summary.
```

</details>

### Requirements

⚠️ **This only works with AI products that have chat history / memory features.** Examples:
- Claude Pro / Team / Enterprise (with memory enabled)
- Any AI product with conversation history APIs

## Why Monthly?

Like any retrospective, the value compounds over time. Monthly cadence is ideal because:
- **Weekly** is too noisy — not enough data to spot patterns
- **Quarterly** is too late — bad habits have already calcified
- **Monthly** hits the sweet spot — enough data, fast enough feedback loop

## License

MIT — use it, fork it, improve it.

## Author

Built by [Junjie Eric Liu](https://linkedin.com/in/junjieliu/) as part of the [ClawHub](https://github.com/jjliu6) skill collection.

---

*If you find this useful, consider giving it a ⭐ — it helps others discover it.*
