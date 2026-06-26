# deep-researcher

**Domain Research Report Generator** — an AI agent skill that turns any research topic into a structured, decision-ready report in minutes.

## What it produces

For any domain, runs multi-angle deep research and outputs a structured `.md` report:

| Section | Description |
|---------|-------------|
| **Top 5 Consensus** | Core established facts, each tagged with evidence strength (HIGH / MEDIUM / LOW) |
| **Top 5 Divergences** | Contested questions with both sides' arguments side by side |
| **Key Numbers** | Critical metrics, every figure sourced, forecasts marked `[ESTIMATED]` |
| **Failed Paths** | Directions already proven unworkable, with reasons and recurrence conditions |
| **Core Tension** | The irreducible contradiction at the heart of the domain, in one sentence |
| **Decision Readiness** | What can be decided now vs. what needs more information, with confidence index 0–10 and next concrete action |
| **Landscape** *(optional)* | Competitive/ecosystem structure — key players, market structure, recent moves |
| **Implications** *(optional)* | What the findings mean for each stakeholder group |
| **Scenarios** *(optional)* | Base / upside / downside scenarios for high-uncertainty topics |

## What makes it different

**Anti-hallucination enforcement** — full-text fetch before any inference; vendor self-reported data is automatically downgraded to LOW evidence.

**Local-language research** — auto-detects the domain's region and searches primary sources in the official local language. No configuration needed:
- Greek labor law → searched in ελληνικά, hits the Ministry of Labour directly
- Panama maritime regulations → searched in Español, hits amp.gob.pa
- Vietnam e-commerce law → searched in Tiếng Việt, finds the 2025 National Assembly legislation that English search misses entirely

**Semantic intent routing** — infers research mode, subjects, region, language, and output path from meaning. No flags or options:
- `调研AWS、阿里云和华为云` → brief-multi (parallel research on 3 subjects)
- `AWS和阿里云哪个更适合出海` → compare (head-to-head)
- `更新我关于东南亚电商的研究` → update (read existing report, add new findings)

**Per-subject independence** — in multi-subject mode, each subject gets its own region detection and language. AWS searched in English, Alibaba Cloud searched in Chinese, no cross-contamination.

**Evidence scoring** — every claim rated HIGH / MEDIUM / LOW with source citations. LOW claims carry a mandatory warning. See [`references/evidence-scoring.md`](references/evidence-scoring.md).

## Installation

Install as a skill in any compatible AI agent environment. Copy the skill files into your agent's skills directory, or use the pre-packaged zip:

**Option A — ZIP install**

1. Download [`deep-researcher-skill.zip`](deep-researcher-skill.zip)
2. Import it through your agent platform's skill install UI

**Option B — Manual**

```bash
# Copy skill files into your agent's skills directory
# (adjust path to match your platform)
mkdir -p ~/.your-agent/skills/deep-researcher
cp -R SKILL.md references/ strategies/ templates/ ~/.your-agent/skills/deep-researcher/
```

## Usage

Just describe what you want — the skill is triggered automatically when the AI recognizes research intent:

> "帮我调研东南亚电商物流"
> "Research the current state of Germany's manufacturing digitalization"
> "AWS和阿里云哪个更适合出海业务"
> "Update my notes on Vietnam e-commerce with the latest developments"

The skill infers everything from your description: how many subjects, whether to compare or do parallel research, which region and language to use, and where to save the output.

You can also invoke it explicitly with `/deep-researcher`:

```
/deep-researcher Southeast Asia e-commerce logistics
/deep-researcher AWS and Alibaba Cloud — which fits better for overseas expansion?
/deep-researcher research AWS, Alibaba Cloud and Huawei Cloud
/deep-researcher update my research on Vietnam e-commerce
/deep-researcher save results to reports/japan-saas.md  Japan SaaS market
```

## Search provider setup

deep-researcher requires a web search tool. If your agent platform has a built-in web search tool, it works out of the box. Otherwise, configure one of the following search providers:

| Provider | Recommended for | Free tier | Get key |
|----------|----------------|-----------|---------|
| **Serper** ⭐ | General research — real Google results | 2,500/month | [serper.dev](https://serper.dev) → `SERPER_API_KEY` |
| **Tavily** | Deep research — AI-optimized results | 1,000/month | [tavily.com](https://tavily.com) → `TAVILY_API_KEY` |
| **Brave Search** | Privacy-first, no Google dependency | 2,000/month | [brave.com/search/api](https://brave.com/search/api/) → `BRAVE_API_KEY` |
| **Gemini** | No credit card needed | 500 req/day | [aistudio.google.com](https://aistudio.google.com/apikey) → `GEMINI_API_KEY` |
| **Kimi / Moonshot** | Paid, Alipay accepted | Paid | [platform.moonshot.cn](https://platform.moonshot.cn) → `KIMI_API_KEY` |

**Serper** is the recommended default — it returns real Google search results, which gives deep-researcher the best coverage for local-language searches across all regions.

Set the API key as an environment variable and restart your agent:

```bash
export SERPER_API_KEY=your_key_here
```

## File structure

```
deep-researcher/
├── SKILL.md                      # Main skill definition — all logic lives here
├── references/
│   └── evidence-scoring.md       # Evidence strength criteria (HIGH/MEDIUM/LOW)
├── strategies/
│   └── search-protocol.md        # Search angles, language rules, multi-subject protocol
├── templates/
│   ├── decision-brief.md         # Output template for brief / brief-multi modes
│   └── comparison.md             # Output template for compare / compare-multi modes
└── deep-researcher-skill.zip     # Pre-packaged install zip
```

## Output languages

The report is written in the same language as your query. Research is conducted in the domain's local language regardless of the output language — a Chinese-language query about Greek labor law will search in Greek but output in Chinese.

## License

Apache 2.0
