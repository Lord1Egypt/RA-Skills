# AI Search Rank Tracker

**Preview asset:** `assets/marketplace-preview.svg`

**Track whether ChatGPT, Claude, Gemini, and Perplexity recommend your startup.**

AI search is becoming the new SEO.  
This tool helps you monitor if your brand appears in AI answers.

**Best for:** AI SEO, GEO optimization, AI visibility, and brand monitoring.

---

# Why teams use it

- Track whether your brand is mentioned in AI answers
- Measure ranking position across multiple AI engines
- Detect competitors mentioned alongside your startup
- Estimate sentiment and overall visibility score
- Turn prompt-by-prompt answers into a simple report

---

# Marketplace Cover Demo

Example Brand: **clawlite.ai**

Prompt:
`best openclaw alternative`

ChatGPT:
1. LazyClaw
2. clawlite.ai
3. ZeroClaw

Claude:
Not mentioned

Gemini:
1. LazyClaw
2. ZeroClaw
3. OpenClaw forks
4. clawlite.ai

Perplexity:
1. clawlite.ai
2. LazyClaw
3. ZeroClaw

---

# Sample Report Snapshot

```text
Brand: clawlite.ai
Mention rate: 75%
Average rank: 2.3
Visibility score: 66/100
Best engine result: Perplexity #1
Weakest engine result: Claude not mentioned
Top competitors: LazyClaw, ZeroClaw, OpenClaw forks
```

See also:

```text
output/sample-marketplace-report.md
```

---

# Example

Brand: **clawlite.ai**

Prompt: `best openclaw alternative`

Results:

ChatGPT  
#2 clawlite.ai

Claude  
Not mentioned

Gemini  
#4 clawlite.ai

Perplexity  
#1 clawlite.ai

---

# What it tracks

• Whether your brand is mentioned  
• Ranking position in AI answers  
• Competitors mentioned alongside your brand  
• Sentiment (positive / neutral / negative)  
• Visibility score

---

# Why this matters

Millions of users now search directly in AI assistants.

If your product is not recommended in AI answers,  
you are invisible to those users.

AI Search Rank Tracker helps you understand:

• Where your startup appears  
• Which prompts trigger recommendations  
• Which competitors replace you

---

# Example Prompts

- `best openclaw alternative`
- `easiest openclaw installer`
- `openclaw for beginners`
- `secure openclaw alternative`
- `openclaw web ui`

---

# Prompt Database

This repo now includes a structured AI SEO / GEO prompt database in:

```text
prompt-db/
```

It currently covers 5 high-value categories:

- SaaS
- AI tools
- Developer tools
- OpenClaw ecosystem
- Local AI tools

You can also run built-in prompt packs directly, such as:

- `openclaw-ecosystem`

Each prompt record includes metadata like:
- category
- subcategory
- intent
- journey stage
- commercial value
- difficulty
- competitor fit

Use it to:
- run larger benchmark sets
- build prompt packs
- monitor specific intent clusters
- identify GEO opportunities where competitors appear but your brand does not

---

# Install

Clone repo

```bash
git clone https://github.com/yourrepo/ai-search-rank-tracker
```

Install dependencies

```bash
npm install
```

One-click local install

```bash
bash scripts/install.sh
```

Run tracker

```bash
node src/index.js prompts/starter.json
```

Run a built-in prompt pack

```bash
node src/index.js prompts/openclaw-pack.json
```

---

# Output

The tool generates:

```text
output/report.json
output/report.md
output/report.csv
```

Example summary:

```text
Mention rate: 75%
Average rank: 2.3
Visibility score: 66/100
Top GEO opportunities:
- secure openclaw alternative
- openclaw without terminal
- best openclaw ui
```

---

# Engines Supported

• ChatGPT  
• Claude  
• Gemini  
• Perplexity

---

# Use Cases

Startup founders  
AI SEO / GEO agencies  
Product marketing teams  
Indie hackers

---

# Marketplace Keywords

- AI SEO
- LLM SEO
- ChatGPT SEO
- AI search ranking
- AI visibility
- GEO optimization
- AI brand monitoring

---

# GitHub Topics

- `ai-seo`
- `llm-seo`
- `ai-search`
- `chatgpt-seo`
- `brand-monitoring`
- `ai-marketing`

---

# Roadmap

Upcoming features:

• Google AI Overview tracking  
• Competitor monitoring  
• Prompt discovery engine  
• AI SEO recommendations

---

# License

MIT
